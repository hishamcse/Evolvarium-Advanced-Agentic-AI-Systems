import json

from launchpad_strategist.config import OUTPUT_DIR


def write_outputs(session_id: str, response: str, session_json: str, sessions):
    (OUTPUT_DIR / "latest_launch_brief.md").write_text(response)
    (OUTPUT_DIR / "latest_launch_state.json").write_text(session_json)
    (OUTPUT_DIR / "session_index.json").write_text(json.dumps(sessions, indent=2))
    (OUTPUT_DIR / "latest_session.json").write_text(json.dumps({"session_id": session_id}, indent=2))
