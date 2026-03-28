import json

from launchpad_strategist.mcp.server_app import mcp
from launchpad_strategist.persistence.store import load_launch_state


@mcp.resource("launchpad://session/{session_id}")
def read_launch_state(session_id: str) -> str:
    return json.dumps(load_launch_state(session_id), indent=2)


@mcp.resource("launchpad://summary/{session_id}")
def read_launch_summary(session_id: str) -> str:
    state = load_launch_state(session_id)
    summary = {
        "session_id": state["session_id"],
        "startup_name": state["startup_name"],
        "product_name": state["product_name"],
        "product_type": state["product_type"],
        "launch_goal": state["launch_goal"],
        "launch_angle": state.get("latest_plan", {}).get("launch_angle", ""),
        "primary_audience": state.get("latest_board", {}).get("primary_audience", ""),
        "updated_at": state.get("updated_at", ""),
    }
    return json.dumps(summary, indent=2)
