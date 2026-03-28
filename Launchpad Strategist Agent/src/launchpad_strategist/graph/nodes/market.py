from langchain_core.messages import HumanMessage, SystemMessage

from launchpad_strategist.prompts.system_prompts import MARKET_SYSTEM_PROMPT


def make_market_node(client, market_llm):
    def market(state):
        focus = "focused" if "niche" in state["user_request"].lower() else "balanced"
        raw = client.call_tool(
            "map_market",
            {"session_id": state["session_id"], "focus": focus, "request": state["user_request"]},
        )
        report = market_llm.invoke(
            [
                SystemMessage(content=MARKET_SYSTEM_PROMPT),
                HumanMessage(
                    content=(
                        f"User request:\n{state['user_request']}\n\n"
                        f"Raw market JSON:\n{raw}\n\n"
                        "Translate this into a launch market read."
                    )
                ),
            ]
        )
        step_outputs = dict(state.get("step_outputs", {}))
        step_outputs["market"] = report.content
        return {
            "market_report": report.content,
            "execution_cursor": int(state.get("execution_cursor", 0)) + 1,
            "step_outputs": step_outputs,
            "session_json": client.read_resource(f"launchpad://session/{state['session_id']}"),
        }

    return market
