from typing import List


VALID_STEPS = {"market", "icp", "messaging", "timeline"}


def sanitize_steps(steps: List[str]) -> List[str]:
    cleaned = [step for step in steps if step in VALID_STEPS]
    return cleaned or ["market", "icp", "messaging", "timeline"]


def next_step(state) -> str:
    steps = sanitize_steps(list(state.get("step_order", [])))
    cursor = int(state.get("execution_cursor", 0))
    return steps[cursor] if cursor < len(steps) else "finalizer"


def route_from_critic(state) -> str:
    if not state.get("feedback"):
        return "persist"
    return "persist" if int(state.get("retry_count", 0)) >= int(state.get("max_retries", 0)) else "presenter"
