import json
from typing import Any, Dict, List, Optional

import gradio as gr

from launchpad_strategist.services.engine import LaunchpadStrategistEngine
from launchpad_strategist.ui.views.dashboard import dashboard_outputs, render_log


engine = LaunchpadStrategistEngine()

PRODUCT_TYPES = ["ai_tool", "saas", "devtool", "consumer_app"]
STAGES = ["idea", "alpha", "beta", "live"]
BUDGETS = ["lean", "moderate", "aggressive"]
GOALS = ["beta waitlist", "early revenue", "pilot signups", "community growth"]


def _log_to_messages(state: Dict[str, Any]) -> List[Dict[str, str]]:
    messages: List[Dict[str, str]] = []
    for entry in state.get("launch_log", []):
        role = "assistant" if entry.get("actor") == "Launch Operator" else "user"
        messages.append({"role": role, "content": entry.get("content", "")})
    return messages


def start_session(startup_name: str, product_name: str, product_type: str, stage: str, budget_band: str, launch_goal: str):
    result = engine.run_turn(
        "",
        startup_name=startup_name,
        product_name=product_name,
        product_type=product_type,
        stage=stage,
        budget_band=budget_band,
        launch_goal=launch_goal,
        session_id=None,
    )
    state = result["launch_state"]
    panels = dashboard_outputs(state)
    sessions = result["sessions"]
    return (
        [{"role": "assistant", "content": result["response"]}],
        "",
        result["response"],
        *panels,
        render_log(state),
        json.dumps(state, indent=2),
        result["session_id"],
        sessions,
        gr.update(choices=[item["session_id"] for item in sessions], value=result["session_id"]),
    )


def run_launch(
    request: str,
    chat_history: Optional[List[Dict[str, str]]],
    session_id: str,
    startup_name: str,
    product_name: str,
    product_type: str,
    stage: str,
    budget_band: str,
    launch_goal: str,
):
    if not session_id:
        raise gr.Error("Open a launch session first.")
    if not request.strip():
        raise gr.Error("Enter a launch request for mission control.")
    result = engine.run_turn(
        request,
        startup_name=startup_name,
        product_name=product_name,
        product_type=product_type,
        stage=stage,
        budget_band=budget_band,
        launch_goal=launch_goal,
        session_id=session_id,
    )
    state = result["launch_state"]
    history = list(chat_history or [])
    history.append({"role": "user", "content": request})
    history.append({"role": "assistant", "content": result["response"]})
    panels = dashboard_outputs(state)
    sessions = result["sessions"]
    return (
        history,
        "",
        result["response"],
        *panels,
        render_log(state),
        json.dumps(state, indent=2),
        session_id,
        sessions,
        gr.update(choices=[item["session_id"] for item in sessions], value=session_id),
    )


def load_session(session_id: str):
    if not session_id:
        raise gr.Error("Select a saved launch session.")
    state = engine.load_launch_state(session_id)
    sessions = engine.list_sessions()
    panels = dashboard_outputs(state)
    return (
        _log_to_messages(state),
        "",
        state.get("launch_log", [{}])[-1].get("content", ""),
        *panels,
        render_log(state),
        json.dumps(state, indent=2),
        state.get("session_id", session_id),
        sessions,
        gr.update(choices=[item["session_id"] for item in sessions], value=session_id),
        state.get("startup_name", "Northstar Labs"),
        state.get("product_name", "SignalForge"),
        state.get("product_type", "ai_tool"),
        state.get("stage", "beta"),
        state.get("budget_band", "lean"),
        state.get("launch_goal", "beta waitlist"),
    )
