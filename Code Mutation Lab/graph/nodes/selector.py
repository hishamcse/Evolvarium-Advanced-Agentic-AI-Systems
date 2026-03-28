from agents.select_agent import SelectAgent
from graph.state import MutationState


selector = SelectAgent()


def selector_node(state: MutationState) -> MutationState:
    variants = state.get("variants", [])
    generation = state.get("generation", 0)
    history = state.get("history", [])

    best = selector.select(variants)

    # Record this generation
    record = {
        "generation": generation,
        "variants": variants,
        "selected": best
    }

    updated_history = history + [record]

    return {
        "current_code": best.get("code", ""),
        "history": updated_history,
        "generation": generation + 1
    }
