from langchain_core.messages import HumanMessage, SystemMessage

from launchpad_strategist.prompts.system_prompts import TIMELINE_SYSTEM_PROMPT


def make_timeline_node(client, timeline_llm):
    def timeline(state):
        pace = "fast" if "fast" in state["user_request"].lower() or "quick" in state["user_request"].lower() else "steady"
        raw = client.call_tool(
            "build_launch_timeline",
            {"session_id": state["session_id"], "pace": pace, "request": state["user_request"]},
        )
        report = timeline_llm.invoke(
            [
                SystemMessage(content=TIMELINE_SYSTEM_PROMPT),
                HumanMessage(
                    content=(
                        f"User request:\n{state['user_request']}\n\n"
                        f"Raw timeline JSON:\n{raw}\n\n"
                        "Translate this into a launch runway brief."
                    )
                ),
            ]
        )
        step_outputs = dict(state.get("step_outputs", {}))
        step_outputs["timeline"] = report.content
        return {
            "timeline_report": report.content,
            "execution_cursor": int(state.get("execution_cursor", 0)) + 1,
            "step_outputs": step_outputs,
            "session_json": client.read_resource(f"launchpad://session/{state['session_id']}"),
        }

    return timeline
