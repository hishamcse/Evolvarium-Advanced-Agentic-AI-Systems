import html
import json
from typing import Any, Dict


def escape_html(value: Any) -> str:
    return html.escape(str(value or ""))


def parse_state_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    try:
        return json.loads(str(payload or "{}"))
    except json.JSONDecodeError:
        return {}
