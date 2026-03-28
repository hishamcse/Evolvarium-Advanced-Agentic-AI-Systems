from typing import Dict, List, Tuple

from launchpad_strategist.mcp.data.templates import build_context_profile
from launchpad_strategist.persistence.store import load_launch_state


def context_for(session_id: str) -> Tuple[Dict, Dict]:
    state = load_launch_state(session_id)
    return state, build_context_profile(state)


def request_signals(text: str) -> Dict[str, bool]:
    lowered = (text or "").lower()
    return {
        "proof": any(word in lowered for word in ["proof", "trust", "case study", "testimonial", "roi"]),
        "fast": any(word in lowered for word in ["fast", "quick", "urgent", "soon", "immediate"]),
        "technical": any(word in lowered for word in ["technical", "developer", "engineer", "builder", "founder"]),
        "community": any(word in lowered for word in ["community", "audience", "creator", "viral", "social"]),
        "revenue": any(word in lowered for word in ["revenue", "sales", "pipeline", "buy", "conversion"]),
        "lean": any(word in lowered for word in ["lean", "budget", "low-budget", "cheap", "bootstrap"]),
    }


def step_order_for(state: Dict, signals: Dict[str, bool]) -> List[str]:
    if signals["revenue"] or state["launch_goal"] in {"early revenue", "pilot signups"}:
        return ["icp", "market", "messaging", "timeline"]
    if signals["community"] or state["launch_goal"] == "community growth":
        return ["market", "messaging", "icp", "timeline"]
    if state["stage"] == "idea":
        return ["market", "icp", "messaging", "timeline"]
    return ["market", "icp", "messaging", "timeline"]
