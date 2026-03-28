import json
from datetime import datetime, timezone
from typing import Any, Dict, List

from launchpad_strategist.persistence.paths import launch_path


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def load_launch_state(session_id: str) -> Dict[str, Any]:
    path = launch_path(session_id)
    if not path.exists():
        raise FileNotFoundError(f"Unknown session_id: {session_id}")
    return json.loads(path.read_text())


def save_launch_state(state: Dict[str, Any]) -> None:
    state["updated_at"] = now_utc()
    launch_path(state["session_id"]).write_text(json.dumps(state, indent=2))


def list_launch_states() -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for path in sorted(launch_path("").parent.glob("*.json")):
        payload = json.loads(path.read_text())
        items.append(
            {
                "session_id": payload["session_id"],
                "startup_name": payload["startup_name"],
                "product_name": payload["product_name"],
                "product_type": payload["product_type"],
                "stage": payload["stage"],
                "launch_goal": payload["launch_goal"],
                "updated_at": payload.get("updated_at", ""),
            }
        )
    return sorted(items, key=lambda item: item.get("updated_at", ""), reverse=True)
