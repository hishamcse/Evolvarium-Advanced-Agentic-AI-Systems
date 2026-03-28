from langgraph.graph import StateGraph, END

from graph.state import MutationState
from graph.nodes.mutator import mutator_node
from graph.nodes.evaluator import evaluator_node
from graph.nodes.selector import selector_node
from graph.nodes.controller import controller_node, route_controller


def build_graph():
    builder = StateGraph(MutationState)

    # Nodes
    builder.add_node("mutate",    mutator_node)
    builder.add_node("evaluate",  evaluator_node)
    builder.add_node("select",    selector_node)
    builder.add_node("control",   controller_node)   # node: returns dict

    # Linear flow
    builder.set_entry_point("mutate")
    builder.add_edge("mutate",   "evaluate")
    builder.add_edge("evaluate", "select")
    builder.add_edge("select",   "control")

    # Conditional loop — route_controller is the routing fn, not the node
    builder.add_conditional_edges(
        "control",
        route_controller,            # returns "continue" or "end"
        {
            "continue": "mutate",
            "end":      END,
        }
    )

    return builder.compile()