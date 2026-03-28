import json
from typing import Any, Dict, List, Optional

from langgraph.checkpoint.memory import MemorySaver

from launchpad_strategist.config import LAUNCHPAD_MAX_RETRIES, LAUNCHPAD_TEMPERATURE
from launchpad_strategist.graph.builder import build_graph
from launchpad_strategist.mcp.client import LaunchpadMCPClient
from launchpad_strategist.models.schemas import ExecutionPlan, LaunchBoard, LaunchReview
from launchpad_strategist.models.state import LaunchState
from launchpad_strategist.services.model_factory import make_llm
from launchpad_strategist.services.output_service import write_outputs


class LaunchpadStrategistEngine:
    def __init__(self) -> None:
        self.client = LaunchpadMCPClient()
        self.memory = MemorySaver()
        self.planner_llm = make_llm(0.3).with_structured_output(ExecutionPlan)
        self.market_llm = make_llm(0.35)
        self.icp_llm = make_llm(0.4)
        self.messaging_llm = make_llm(0.5)
        self.timeline_llm = make_llm(0.35)
        self.operator_llm = make_llm(LAUNCHPAD_TEMPERATURE).with_structured_output(LaunchBoard)
        self.presenter_llm = make_llm(0.45)
        self.critic_llm = make_llm(0.1).with_structured_output(LaunchReview)
        self.graph = build_graph(self)

    def run_turn(
        self,
        user_request: str,
        startup_name: str = "Northstar Labs",
        product_name: str = "SignalForge",
        product_type: str = "ai_tool",
        stage: str = "beta",
        budget_band: str = "lean",
        launch_goal: str = "beta waitlist",
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        cleaned_request = (user_request or "").strip() or "Plan a strong launch sequence for this product."
        state: LaunchState = {
            "session_id": session_id,
            "startup_name": startup_name.strip() or "Northstar Labs",
            "product_name": product_name.strip() or "SignalForge",
            "product_type": product_type.strip().lower() or "ai_tool",
            "stage": stage.strip().lower() or "beta",
            "budget_band": budget_band.strip().lower() or "lean",
            "launch_goal": launch_goal.strip() or "beta waitlist",
            "user_request": cleaned_request,
            "session_json": "",
            "plan_json": "",
            "step_order": [],
            "execution_cursor": 0,
            "market_report": "",
            "icp_report": "",
            "messaging_report": "",
            "timeline_report": "",
            "final_board_json": "",
            "final_response": "",
            "feedback": "",
            "retry_count": 0,
            "step_outputs": {},
            "max_retries": LAUNCHPAD_MAX_RETRIES,
        }
        config = {"configurable": {"thread_id": session_id or f"launch-{startup_name.lower().replace(' ', '-')}"}}
        result = self.graph.invoke(state, config=config)
        session_json = result["session_json"]
        sessions = self.list_sessions()
        write_outputs(result["session_id"], result["final_response"], session_json, sessions)
        return {
            "session_id": result["session_id"],
            "response": result["final_response"],
            "launch_state": json.loads(session_json),
            "sessions": sessions,
        }

    def list_sessions(self) -> List[Dict[str, Any]]:
        return json.loads(self.client.call_tool("list_sessions", {}))

    def load_launch_state(self, session_id: str) -> Dict[str, Any]:
        return json.loads(self.client.read_resource(f"launchpad://session/{session_id}"))
