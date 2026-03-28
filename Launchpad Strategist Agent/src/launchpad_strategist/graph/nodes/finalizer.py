import json

from langchain_core.messages import HumanMessage, SystemMessage

from launchpad_strategist.prompts.system_prompts import OPERATOR_SYSTEM_PROMPT


def make_finalizer_node(client, operator_llm):
    def finalizer(state):
        board = operator_llm.invoke(
            [
                SystemMessage(content=OPERATOR_SYSTEM_PROMPT),
                HumanMessage(
                    content=(
                        f"User request:\n{state['user_request']}\n\n"
                        f"Launch session JSON:\n{state['session_json']}\n\n"
                        f"Planner output:\n{state['plan_json']}\n\n"
                        f"Market report:\n{state['market_report']}\n\n"
                        f"ICP report:\n{state['icp_report']}\n\n"
                        f"Messaging report:\n{state['messaging_report']}\n\n"
                        f"Timeline report:\n{state['timeline_report']}\n\n"
                        "Return the final launch board fields."
                    )
                ),
            ]
        )
        payload = {
            "headline": board.headline,
            "launch_angle": board.launch_angle,
            "primary_audience": board.primary_audience,
            "hero_message": board.hero_message,
            "channel_focus": board.channel_focus,
            "launch_sequence": board.launch_sequence,
            "proof_stack": board.proof_stack,
            "risk_watch": board.risk_watch,
            "next_best_action": board.next_best_action,
        }
        persisted = client.call_tool("lock_launch_board", {"session_id": state["session_id"], **payload})
        return {
            "final_board_json": persisted,
            "session_json": client.read_resource(f"launchpad://session/{state['session_id']}"),
            "plan_json": json.dumps(json.loads(state["plan_json"]), indent=2),
        }

    return finalizer
