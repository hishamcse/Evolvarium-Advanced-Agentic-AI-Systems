import asyncio
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional

import mcp
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


load_dotenv(override=True)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_BASE_MODEL = os.getenv("OLLAMA_BASE_MODEL", "qwen3:8b")
ARENA_TEMPERATURE = float(os.getenv("ARENA_TEMPERATURE", "0.45"))
ARENA_MAX_RETRIES = int(os.getenv("ARENA_MAX_RETRIES", "2"))


class ArenaState(TypedDict):
    session_id: Optional[str]
    player_handle: str
    team_name: str
    title: str
    role: str
    rank_tier: str
    focus_mode: str
    user_request: str
    arena_state_json: str
    meta_brief: str
    scout_brief: str
    draft_brief: str
    training_brief: str
    mindset_brief: str
    coach_plan_json: str
    feedback: str
    final_response: str
    retry_count: int


class CoachPlan(BaseModel):
    headline: str = Field(description="Short, punchy match-prep headline.")
    win_condition: str = Field(description="What most likely wins this match.")
    danger_zone: str = Field(description="Biggest trap or failure mode to avoid.")
    tempo_call: str = Field(description="The main pacing instruction for the team.")
    confidence: float = Field(description="Confidence score between 0 and 1.")
    key_map: str = Field(description="Most important map, lane, or zone.")
    signature_pick: str = Field(description="Best comfort pick, comp, or system to lean on.")
    bench_note: str = Field(description="One optional adjustment if the first plan stalls.")


class ArenaReview(BaseModel):
    approved: bool = Field(description="Whether the final arena brief is clear and complete.")
    feedback: str = Field(description="Specific feedback if the final arena brief is weak.")


def _run_async(coro):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(lambda: asyncio.run(coro))
        return future.result()


class ArenaMCPClient:
    def __init__(self) -> None:
        server_path = str((BASE_DIR / "esports_server.py").resolve())
        self.params = StdioServerParameters(command=sys.executable, args=[server_path], env=os.environ.copy())

    @staticmethod
    def _tool_result_to_text(result: Any) -> str:
        if hasattr(result, "content") and result.content:
            chunk = result.content[0]
            if hasattr(chunk, "text"):
                return chunk.text
        return str(result)

    @staticmethod
    def _resource_result_to_text(result: Any) -> str:
        if hasattr(result, "contents") and result.contents:
            chunk = result.contents[0]
            if hasattr(chunk, "text"):
                return chunk.text
        return str(result)

    async def call_tool_async(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> str:
        async with stdio_client(self.params) as streams:
            async with mcp.ClientSession(*streams) as session:
                await session.initialize()
                result = await session.call_tool(name, arguments or {})
                return self._tool_result_to_text(result)

    async def read_resource_async(self, uri: str) -> str:
        async with stdio_client(self.params) as streams:
            async with mcp.ClientSession(*streams) as session:
                await session.initialize()
                result = await session.read_resource(uri)
                return self._resource_result_to_text(result)

    def call_tool(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> str:
        return _run_async(self.call_tool_async(name, arguments))

    def read_resource(self, uri: str) -> str:
        return _run_async(self.read_resource_async(uri))


class EsportsCoachArenaEngine:
    def __init__(self) -> None:
        self.client = ArenaMCPClient()
        self.memory = MemorySaver()
        self.meta_llm = self._make_llm(0.35)
        self.scout_llm = self._make_llm(0.4)
        self.draft_llm = self._make_llm(0.35)
        self.mechanics_llm = self._make_llm(0.45)
        self.mindset_llm = self._make_llm(0.55)
        self.head_coach_llm = self._make_llm(ARENA_TEMPERATURE).with_structured_output(CoachPlan)
        self.host_llm = self._make_llm(0.5)
        self.critic_llm = self._make_llm(0.1).with_structured_output(ArenaReview)
        self.graph = self._build_graph()

    @staticmethod
    def _make_llm(temperature: float) -> ChatOpenAI:
        return ChatOpenAI(
            model=OLLAMA_BASE_MODEL,
            base_url=OLLAMA_BASE_URL,
            api_key="ollama",
            temperature=temperature,
        )

    def _refresh_state(self, session_id: str) -> str:
        return self.client.read_resource(f"arena://session/{session_id}")

    def bootstrap(self, state: ArenaState) -> Dict[str, Any]:
        session_id = state.get("session_id")
        if not session_id:
            payload_text = self.client.call_tool(
                "create_arena_session",
                {
                    "player_handle": state["player_handle"],
                    "team_name": state["team_name"],
                    "title": state["title"],
                    "role": state["role"],
                    "rank_tier": state["rank_tier"],
                    "focus_mode": state["focus_mode"],
                },
            )
            payload = json.loads(payload_text)
            session_id = payload["session_id"]
        arena_state_json = self._refresh_state(session_id)
        return {"session_id": session_id, "arena_state_json": arena_state_json, "feedback": "", "retry_count": 0}

    def meta_agent(self, state: ArenaState) -> Dict[str, Any]:
        priority = "aggressive" if "aggressive" in state["user_request"].lower() else "balanced"
        raw = self.client.call_tool("analyze_meta", {"session_id": state["session_id"], "priority": priority})
        response = self.meta_llm.invoke(
            [
                SystemMessage(
                    content=(
                        "You are the Meta Analyst for an esports coaching staff. "
                        "Write a compact tactical read with a title line and exactly three flat bullet points."
                    )
                ),
                HumanMessage(
                    content=(
                        f"User request:\n{state['user_request']}\n\n"
                        f"Raw meta report JSON:\n{raw}\n\n"
                        "Focus on what the staff should exploit right now."
                    )
                ),
            ]
        )
        return {"meta_brief": response.content, "arena_state_json": self._refresh_state(state["session_id"])}

    def scout_agent(self, state: ArenaState) -> Dict[str, Any]:
        emphasis = "tempo" if "fast" in state["user_request"].lower() or "tempo" in state["user_request"].lower() else "default"
        raw = self.client.call_tool("scout_opponent", {"session_id": state["session_id"], "emphasis": emphasis})
        response = self.scout_llm.invoke(
            [
                SystemMessage(
                    content=(
                        "You are the Opponent Scout on an esports analyst desk. "
                        "Write a concise scouting note with a short heading and exactly three flat bullet points."
                    )
                ),
                HumanMessage(
                    content=(
                        f"User request:\n{state['user_request']}\n\n"
                        f"Raw scouting JSON:\n{raw}\n\n"
                        "Explain how to punish this opponent."
                    )
                ),
            ]
        )
        return {"scout_brief": response.content, "arena_state_json": self._refresh_state(state["session_id"])}

    def draft_agent(self, state: ArenaState) -> Dict[str, Any]:
        style = "safe" if "safe" in state["user_request"].lower() else "balanced"
        raw = self.client.call_tool("build_draft_plan", {"session_id": state["session_id"], "style": style})
        response = self.draft_llm.invoke(
            [
                SystemMessage(
                    content=(
                        "You are the Draft and Veto Coach. "
                        "Write a sharp prep note with a heading and exactly three flat bullet points."
                    )
                ),
                HumanMessage(
                    content=(
                        f"User request:\n{state['user_request']}\n\n"
                        f"Raw draft JSON:\n{raw}\n\n"
                        "Highlight pick-ban-veto edge and fallback logic."
                    )
                ),
            ]
        )
        return {"draft_brief": response.content, "arena_state_json": self._refresh_state(state["session_id"])}

    def mechanics_agent(self, state: ArenaState) -> Dict[str, Any]:
        intensity = "high" if any(word in state["user_request"].lower() for word in ["must-win", "high pressure", "playoffs"]) else "balanced"
        raw = self.client.call_tool("design_training_block", {"session_id": state["session_id"], "intensity": intensity})
        response = self.mechanics_llm.invoke(
            [
                SystemMessage(
                    content=(
                        "You are the Mechanics and Practice Coach. "
                        "Write a compact training brief with a heading and exactly three flat bullet points."
                    )
                ),
                HumanMessage(
                    content=(
                        f"User request:\n{state['user_request']}\n\n"
                        f"Raw training JSON:\n{raw}\n\n"
                        "Translate it into a practical warmup and scrim block."
                    )
                ),
            ]
        )
        return {"training_brief": response.content, "arena_state_json": self._refresh_state(state["session_id"])}

    def mindset_agent(self, state: ArenaState) -> Dict[str, Any]:
        pressure = "playoff" if any(word in state["user_request"].lower() for word in ["nervous", "pressure", "final"]) else "standard"
        raw = self.client.call_tool("issue_mindset_protocol", {"session_id": state["session_id"], "pressure": pressure})
        response = self.mindset_llm.invoke(
            [
                SystemMessage(
                    content=(
                        "You are the Mindset Coach on an esports staff. "
                        "Write a steadying locker-room note with a heading and exactly three flat bullet points."
                    )
                ),
                HumanMessage(
                    content=(
                        f"User request:\n{state['user_request']}\n\n"
                        f"Raw mindset JSON:\n{raw}\n\n"
                        "Keep it calm, strong, and actionable."
                    )
                ),
            ]
        )
        return {"mindset_brief": response.content, "arena_state_json": self._refresh_state(state["session_id"])}

    def head_coach(self, state: ArenaState) -> Dict[str, Any]:
        plan = self.head_coach_llm.invoke(
            [
                SystemMessage(
                    content=(
                        "You are the Head Coach supervising five esports specialists. "
                        "Synthesize one match plan that is decisive, realistic, and grounded in the staff reports."
                    )
                ),
                HumanMessage(
                    content=(
                        f"User request:\n{state['user_request']}\n\n"
                        f"Arena state JSON:\n{state['arena_state_json']}\n\n"
                        f"Meta brief:\n{state['meta_brief']}\n\n"
                        f"Scout brief:\n{state['scout_brief']}\n\n"
                        f"Draft brief:\n{state['draft_brief']}\n\n"
                        f"Training brief:\n{state['training_brief']}\n\n"
                        f"Mindset brief:\n{state['mindset_brief']}\n\n"
                        "Return the final coach plan fields."
                    )
                ),
            ]
        )
        plan_payload = {
            "headline": plan.headline,
            "win_condition": plan.win_condition,
            "danger_zone": plan.danger_zone,
            "tempo_call": plan.tempo_call,
            "confidence": max(0.0, min(plan.confidence, 1.0)),
            "key_map": plan.key_map,
            "signature_pick": plan.signature_pick,
            "bench_note": plan.bench_note,
        }
        persisted = self.client.call_tool("lock_match_plan", {"session_id": state["session_id"], **plan_payload})
        return {"coach_plan_json": persisted, "arena_state_json": self._refresh_state(state["session_id"])}

    def arena_host(self, state: ArenaState) -> Dict[str, Any]:
        feedback = f"\nReviewer feedback:\n{state['feedback']}\n" if state.get("feedback") else ""
        response = self.host_llm.invoke(
            [
                SystemMessage(
                    content=(
                        "You are the Arena Host presenting the coaching staff's final prep in a high-energy but practical way. "
                        "Do not mention hidden agents, tools, JSON, MCP, or orchestration."
                    )
                ),
                HumanMessage(
                    content=(
                        f"User request:\n{state['user_request']}\n\n"
                        f"Persisted arena state JSON:\n{state['arena_state_json']}\n\n"
                        f"Meta analyst:\n{state['meta_brief']}\n\n"
                        f"Opponent scout:\n{state['scout_brief']}\n\n"
                        f"Draft coach:\n{state['draft_brief']}\n\n"
                        f"Mechanics coach:\n{state['training_brief']}\n\n"
                        f"Mindset coach:\n{state['mindset_brief']}\n\n"
                        f"Head coach plan JSON:\n{state['coach_plan_json']}\n"
                        f"{feedback}\n"
                        "Requirements:\n"
                        "- Start with one bold headline line.\n"
                        "- Include sections named `Meta Pulse`, `Opponent Read`, `Draft Edge`, `Practice Circuit`, `Mental Reset`, and `Head Coach Call`.\n"
                        "- Use only flat bullet points where bullets make sense.\n"
                        "- End with a short motivating but grounded final paragraph.\n"
                    )
                ),
            ]
        )
        return {"final_response": response.content}

    def critic(self, state: ArenaState) -> Dict[str, Any]:
        review = self.critic_llm.invoke(
            [
                SystemMessage(
                    content=(
                        "Approve only if the arena brief clearly includes all required sections and gives actionable esports advice."
                    )
                ),
                HumanMessage(
                    content=(
                        f"User request:\n{state['user_request']}\n\n"
                        f"Brief:\n{state['final_response']}"
                    )
                ),
            ]
        )
        if review.approved:
            return {"feedback": ""}
        return {"feedback": review.feedback, "retry_count": int(state.get("retry_count", 0)) + 1}

    def route_from_critic(self, state: ArenaState) -> str:
        if not state.get("feedback"):
            return "persist"
        if int(state.get("retry_count", 0)) >= ARENA_MAX_RETRIES:
            return "persist"
        return "arena_host"

    def persist(self, state: ArenaState) -> Dict[str, Any]:
        self.client.call_tool(
            "append_coach_log",
            {"session_id": state["session_id"], "actor": state["player_handle"], "content": state["user_request"]},
        )
        self.client.call_tool(
            "append_coach_log",
            {"session_id": state["session_id"], "actor": "Arena Host", "content": state["final_response"]},
        )
        return {"arena_state_json": self._refresh_state(state["session_id"])}

    def _build_graph(self):
        graph = StateGraph(ArenaState)
        graph.add_node("bootstrap", self.bootstrap)
        graph.add_node("meta_agent", self.meta_agent)
        graph.add_node("scout_agent", self.scout_agent)
        graph.add_node("draft_agent", self.draft_agent)
        graph.add_node("mechanics_agent", self.mechanics_agent)
        graph.add_node("mindset_agent", self.mindset_agent)
        graph.add_node("head_coach", self.head_coach)
        graph.add_node("arena_host", self.arena_host)
        graph.add_node("critic", self.critic)
        graph.add_node("persist", self.persist)

        graph.add_edge(START, "bootstrap")
        graph.add_edge("bootstrap", "meta_agent")
        graph.add_edge("meta_agent", "scout_agent")
        graph.add_edge("scout_agent", "draft_agent")
        graph.add_edge("draft_agent", "mechanics_agent")
        graph.add_edge("mechanics_agent", "mindset_agent")
        graph.add_edge("mindset_agent", "head_coach")
        graph.add_edge("head_coach", "arena_host")
        graph.add_edge("arena_host", "critic")
        graph.add_conditional_edges("critic", self.route_from_critic, {"persist": "persist", "arena_host": "arena_host"})
        graph.add_edge("persist", END)
        return graph.compile(checkpointer=self.memory)

    def _write_outputs(self, session_id: str, final_response: str, arena_state_json: str) -> None:
        (OUTPUT_DIR / "latest_arena_brief.md").write_text(final_response)
        (OUTPUT_DIR / "latest_arena_state.json").write_text(arena_state_json)
        (OUTPUT_DIR / "session_index.json").write_text(json.dumps(self.list_sessions(), indent=2))
        (OUTPUT_DIR / "latest_session.json").write_text(json.dumps({"session_id": session_id}, indent=2))

    def run_turn(
        self,
        user_request: str,
        player_handle: str = "Hisham",
        team_name: str = "Neon Rift",
        title: str = "valorant",
        role: str = "igl",
        rank_tier: str = "ascendant",
        focus_mode: str = "tournament",
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        cleaned_request = (user_request or "").strip() or "Prepare my full match plan for the next series."
        state: ArenaState = {
            "session_id": session_id,
            "player_handle": player_handle.strip() or "Player One",
            "team_name": team_name.strip() or "Arena Squad",
            "title": title.strip().lower() or "valorant",
            "role": role.strip().lower() or "igl",
            "rank_tier": rank_tier.strip() or "ascendant",
            "focus_mode": focus_mode.strip().lower() or "tournament",
            "user_request": cleaned_request,
            "arena_state_json": "",
            "meta_brief": "",
            "scout_brief": "",
            "draft_brief": "",
            "training_brief": "",
            "mindset_brief": "",
            "coach_plan_json": "",
            "feedback": "",
            "final_response": "",
            "retry_count": 0,
        }
        config = {"configurable": {"thread_id": session_id or f"arena-{player_handle.lower()}"}}
        result = self.graph.invoke(state, config=config)
        arena_state_json = result["arena_state_json"]
        self._write_outputs(result["session_id"], result["final_response"], arena_state_json)
        return {
            "session_id": result["session_id"],
            "response": result["final_response"],
            "arena_state": json.loads(arena_state_json),
            "sessions": self.list_sessions(),
        }

    def list_sessions(self) -> List[Dict[str, Any]]:
        return json.loads(self.client.call_tool("list_sessions", {}))

    def load_arena_state(self, session_id: str) -> Dict[str, Any]:
        return json.loads(self.client.read_resource(f"arena://session/{session_id}"))


def cli() -> None:
    engine = EsportsCoachArenaEngine()
    player_handle = input("Player handle [Hisham]: ").strip() or "Hisham"
    team_name = input("Team name [Neon Rift]: ").strip() or "Neon Rift"
    title = input("Title [valorant]: ").strip() or "valorant"
    role = input("Role [igl]: ").strip() or "igl"
    rank_tier = input("Rank tier [ascendant]: ").strip() or "ascendant"
    focus_mode = input("Focus mode [tournament]: ").strip() or "tournament"

    result = engine.run_turn(
        "",
        player_handle=player_handle,
        team_name=team_name,
        title=title,
        role=role,
        rank_tier=rank_tier,
        focus_mode=focus_mode,
    )
    session_id = result["session_id"]
    print("\n" + result["response"] + "\n")
    print(f"Session ID: {session_id}\n")

    while True:
        prompt = input("Ask the coach (`quit` to exit): ").strip()
        if prompt.lower() in {"quit", "exit"}:
            break
        turn = engine.run_turn(
            prompt,
            player_handle=player_handle,
            team_name=team_name,
            title=title,
            role=role,
            rank_tier=rank_tier,
            focus_mode=focus_mode,
            session_id=session_id,
        )
        print("\n" + turn["response"] + "\n")


if __name__ == "__main__":
    cli()
