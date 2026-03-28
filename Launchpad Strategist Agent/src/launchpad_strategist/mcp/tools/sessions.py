import json
import uuid

from launchpad_strategist.mcp.data.templates import (
    build_context_profile,
    normalize_budget,
    normalize_goal,
    normalize_product_type,
    normalize_stage,
)
from launchpad_strategist.mcp.server_app import mcp
from launchpad_strategist.persistence.store import list_launch_states, now_utc, load_launch_state, save_launch_state


@mcp.tool()
def create_launch_session(
    startup_name: str,
    product_name: str,
    product_type: str = "ai_tool",
    stage: str = "beta",
    budget_band: str = "lean",
    launch_goal: str = "beta waitlist",
) -> str:
    """Create a persistent product launch session."""

    product_key = normalize_product_type(product_type)
    stage_key = normalize_stage(stage)
    budget_key = normalize_budget(budget_band)
    goal_key = normalize_goal(launch_goal)
    base_state = {
        "product_type": product_key,
        "stage": stage_key,
        "budget_band": budget_key,
        "launch_goal": goal_key,
    }
    profile = build_context_profile(base_state)
    template = profile["product"]
    session_id = uuid.uuid4().hex[:10]
    state = {
        "session_id": session_id,
        "startup_name": startup_name.strip() or "Northstar Labs",
        "product_name": product_name.strip() or "SignalForge",
        "product_type": product_key,
        "stage": stage_key,
        "budget_band": budget_key,
        "launch_goal": goal_key,
        "market_signal": template["market_signal"],
        "competitor_pressure": template["competitor_pressure"],
        "buyer_mindset": template["buyer_mindset"],
        "default_channels": template["channels"],
        "proof_assets": template["proof_assets"],
        "primary_segments": template["primary_segments"],
        "promise_shape": template["promise_shape"],
        "urgency_hooks": template["urgency_hooks"],
        "launch_motion": template["launch_motion"],
        "message_tone": template["message_tone"],
        "readiness_focus": profile["stage"]["readiness_focus"],
        "proof_requirement": profile["stage"]["proof_requirement"],
        "asset_priority": profile["stage"]["asset_priority"],
        "budget_profile": profile["budget"]["channel_bias"],
        "goal_cta": profile["goal"]["primary_cta"],
        "latest_reports": {},
        "latest_plan": {},
        "latest_board": {},
        "launch_log": [],
        "created_at": now_utc(),
        "updated_at": now_utc(),
    }
    save_launch_state(state)
    payload = {
        "session_id": session_id,
        "startup_name": state["startup_name"],
        "product_name": state["product_name"],
        "product_type": state["product_type"],
        "launch_goal": state["launch_goal"],
    }
    return json.dumps(payload, indent=2)


@mcp.tool()
def append_launch_log(session_id: str, actor: str, content: str) -> str:
    """Append a timeline item to the launch session log."""

    state = load_launch_state(session_id)
    state["launch_log"].append({"actor": actor, "content": content, "timestamp": now_utc()})
    save_launch_state(state)
    return json.dumps({"ok": True, "count": len(state["launch_log"])}, indent=2)


@mcp.tool()
def list_sessions() -> str:
    """List saved launch sessions for the UI."""

    return json.dumps(list_launch_states(), indent=2)
