"""
AI Hiring Committee — LangGraph graph
Architecture: parallel blind evaluation + chair aggregation

Flow: bootstrap → [technical ‖ manager ‖ culture ‖ advocate] → chair → persist

All four evaluators run in parallel. None sees another's output.
Chair sees all four simultaneously.
"""
import json
import uuid

from langgraph.graph import END, START, StateGraph

from agents.technical_agent import run_technical
from agents.manager_agent   import run_manager
from agents.culture_agent   import run_culture
from agents.advocate_agent  import run_advocate
from agents.chair_agent     import run_chair
from mcp_server import (
    parse_cv_sync, extract_requirements_sync,
    save_session_sync, list_sessions_sync, load_session_sync,
)
from state import CommitteeState


# ── nodes ──────────────────────────────────────────────────────────────────────

def bootstrap_node(state: CommitteeState) -> dict:
    parsed    = parse_cv_sync(state["cv_text"])
    reqs      = extract_requirements_sync(state["job_spec"])
    return {
        "session_id":        state.get("session_id") or uuid.uuid4().hex[:10],
        "candidate_name":    parsed.get("candidate_name", "Candidate"),
        "parsed_skills":     parsed.get("skills", []),
        "parsed_exp":        parsed.get("experience", "Unknown"),
        "key_requirements":  reqs.get("requirements", []),
        "error":             None,
    }

def technical_node(state: CommitteeState) -> dict:
    return run_technical(state)

def manager_node(state: CommitteeState) -> dict:
    return run_manager(state)

def culture_node(state: CommitteeState) -> dict:
    return run_culture(state)

def advocate_node(state: CommitteeState) -> dict:
    return run_advocate(state)

def chair_node(state: CommitteeState) -> dict:
    return run_chair(state)

def persist_node(state: CommitteeState) -> dict:
    data = {k: state.get(k) for k in [
        "session_id", "candidate_name", "role_title",
        "cv_text", "job_spec", "parsed_skills", "parsed_exp", "key_requirements",
        "technical", "manager", "culture", "advocate",
        "overall_score", "decision", "chair_reasoning",
        "key_agreements", "key_disagreements", "top_interview_qs", "red_flags",
    ]}
    save_session_sync(state["session_id"], data)
    return {}


# ── graph ───────────────────────────────────────────────────────────────────────

def build_graph():
    g = StateGraph(CommitteeState)

    g.add_node("bootstrap",  bootstrap_node)
    g.add_node("node_technical", technical_node)
    g.add_node("node_manager",   manager_node)
    g.add_node("node_culture",   culture_node)
    g.add_node("node_advocate",  advocate_node)
    g.add_node("chair",      chair_node)
    g.add_node("persist",    persist_node)

    g.add_edge(START, "bootstrap")

    # Fan out — all four run in parallel from bootstrap
    for ev in ["node_technical", "node_manager", "node_culture", "node_advocate"]:
        g.add_edge("bootstrap", ev)
        g.add_edge(ev, "chair")

    g.add_edge("chair",   "persist")
    g.add_edge("persist", END)

    return g.compile()


# ── engine ──────────────────────────────────────────────────────────────────────

class HiringEngine:
    def __init__(self):
        self.graph = build_graph()

    def evaluate(self, cv_text: str, job_spec: str, role_title: str) -> CommitteeState:
        empty_eval = {
            "score": 0.0, "verdict": "", "strengths": [],
            "concerns": [], "interview_qs": [], "reasoning": "",
        }
        initial: CommitteeState = {
            "session_id":        "",
            "candidate_name":    "",
            "role_title":        role_title,
            "cv_text":           cv_text,
            "job_spec":          job_spec,
            "parsed_skills":     [],
            "parsed_exp":        "",
            "key_requirements":  [],
            "technical":         empty_eval,
            "manager":           empty_eval,
            "culture":           empty_eval,
            "advocate":          empty_eval,
            "overall_score":     0.0,
            "decision":          "",
            "chair_reasoning":   "",
            "key_agreements":    [],
            "key_disagreements": [],
            "top_interview_qs":  [],
            "red_flags":         [],
            "error":             None,
        }
        return self.graph.invoke(initial)

    def load_session(self, session_id: str) -> dict | None:
        return load_session_sync(session_id)

    def list_sessions(self) -> list[dict]:
        return list_sessions_sync()