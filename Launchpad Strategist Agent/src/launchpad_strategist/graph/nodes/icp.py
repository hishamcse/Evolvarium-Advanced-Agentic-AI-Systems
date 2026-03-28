from langchain_core.messages import HumanMessage, SystemMessage

from launchpad_strategist.prompts.system_prompts import ICP_SYSTEM_PROMPT


def make_icp_node(client, icp_llm):
    def icp(state):
        raw = client.call_tool(
            "build_icp",
            {"session_id": state["session_id"], "segment": "default", "request": state["user_request"]},
        )
        report = icp_llm.invoke(
            [
                SystemMessage(content=ICP_SYSTEM_PROMPT),
                HumanMessage(
                    content=(
                        f"User request:\n{state['user_request']}\n\n"
                        f"Raw ICP JSON:\n{raw}\n\n"
                        "Translate this into a sharp early-audience report."
                    )
                ),
            ]
        )
        step_outputs = dict(state.get("step_outputs", {}))
        step_outputs["icp"] = report.content
        return {
            "icp_report": report.content,
            "execution_cursor": int(state.get("execution_cursor", 0)) + 1,
            "step_outputs": step_outputs,
            "session_json": client.read_resource(f"launchpad://session/{state['session_id']}"),
        }

    return icp
