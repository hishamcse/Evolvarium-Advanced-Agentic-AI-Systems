from graph.state import MutationState


def controller_node(state: MutationState) -> dict:
    """
    Node function — must return a dict (even if empty).
    LangGraph calls this as a graph node; it just passes state through.
    The actual routing decision is made by route_controller below.
    """
    return {}


def route_controller(state: MutationState) -> str:
    """
    Routing function for add_conditional_edges.
    Returns 'continue' to loop back to mutate, or 'end' to terminate.
    """
    generation = state.get("generation", 0)
    max_generations = state.get("max_generations", 3)

    if generation >= max_generations:
        return "end"
    return "continue"