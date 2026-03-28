from langgraph.graph import END, START, StateGraph

from launchpad_strategist.graph.nodes.bootstrap import make_bootstrap_node
from launchpad_strategist.graph.nodes.critic import make_critic_node
from launchpad_strategist.graph.nodes.finalizer import make_finalizer_node
from launchpad_strategist.graph.nodes.icp import make_icp_node
from launchpad_strategist.graph.nodes.market import make_market_node
from launchpad_strategist.graph.nodes.messaging import make_messaging_node
from launchpad_strategist.graph.nodes.persist import make_persist_node
from launchpad_strategist.graph.nodes.planner import make_planner_node
from launchpad_strategist.graph.nodes.presenter import make_presenter_node
from launchpad_strategist.graph.nodes.timeline import make_timeline_node
from launchpad_strategist.graph.routing import next_step, route_from_critic
from launchpad_strategist.models.state import LaunchState


def build_graph(engine):
    graph = StateGraph(LaunchState)
    graph.add_node("bootstrap", make_bootstrap_node(engine.client))
    graph.add_node("planner", make_planner_node(engine.client, engine.planner_llm))
    graph.add_node("market", make_market_node(engine.client, engine.market_llm))
    graph.add_node("icp", make_icp_node(engine.client, engine.icp_llm))
    graph.add_node("messaging", make_messaging_node(engine.client, engine.messaging_llm))
    graph.add_node("timeline", make_timeline_node(engine.client, engine.timeline_llm))
    graph.add_node("finalizer", make_finalizer_node(engine.client, engine.operator_llm))
    graph.add_node("presenter", make_presenter_node(engine.presenter_llm))
    graph.add_node("critic", make_critic_node(engine.critic_llm))
    graph.add_node("persist", make_persist_node(engine.client))

    graph.add_edge(START, "bootstrap")
    graph.add_edge("bootstrap", "planner")
    graph.add_conditional_edges(
        "planner",
        next_step,
        {"market": "market", "icp": "icp", "messaging": "messaging", "timeline": "timeline", "finalizer": "finalizer"},
    )
    for name in ("market", "icp", "messaging", "timeline"):
        graph.add_conditional_edges(
            name,
            next_step,
            {"market": "market", "icp": "icp", "messaging": "messaging", "timeline": "timeline", "finalizer": "finalizer"},
        )
    graph.add_edge("finalizer", "presenter")
    graph.add_edge("presenter", "critic")
    graph.add_conditional_edges("critic", route_from_critic, {"presenter": "presenter", "persist": "persist"})
    graph.add_edge("persist", END)
    return graph.compile(checkpointer=engine.memory)
