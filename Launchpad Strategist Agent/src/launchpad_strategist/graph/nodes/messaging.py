from langchain_core.messages import HumanMessage, SystemMessage

from launchpad_strategist.prompts.system_prompts import MESSAGING_SYSTEM_PROMPT


def make_messaging_node(client, messaging_llm):
    def messaging(state):
        tone = "bold" if "bold" in state["user_request"].lower() or "strong" in state["user_request"].lower() else "clear"
        raw = client.call_tool(
            "craft_message_stack",
            {"session_id": state["session_id"], "tone": tone, "request": state["user_request"]},
        )
        report = messaging_llm.invoke(
            [
                SystemMessage(content=MESSAGING_SYSTEM_PROMPT),
                HumanMessage(
                    content=(
                        f"User request:\n{state['user_request']}\n\n"
                        f"Raw messaging JSON:\n{raw}\n\n"
                        "Translate this into a launch messaging stack."
                    )
                ),
            ]
        )
        step_outputs = dict(state.get("step_outputs", {}))
        step_outputs["messaging"] = report.content
        return {
            "messaging_report": report.content,
            "execution_cursor": int(state.get("execution_cursor", 0)) + 1,
            "step_outputs": step_outputs,
            "session_json": client.read_resource(f"launchpad://session/{state['session_id']}"),
        }

    return messaging
