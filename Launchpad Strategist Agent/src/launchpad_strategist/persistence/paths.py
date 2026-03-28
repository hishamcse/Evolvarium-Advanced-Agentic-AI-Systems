from launchpad_strategist.config import LAUNCH_DIR


def launch_path(session_id: str):
    return LAUNCH_DIR / f"{session_id}.json"
