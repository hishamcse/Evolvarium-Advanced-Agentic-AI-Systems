from langchain_core.messages import HumanMessage, SystemMessage

from launchpad_strategist.prompts.system_prompts import PRESENTER_SYSTEM_PROMPT


def make_presenter_node(presenter_llm):
    def presenter(state):
        feedback = f"\nReviewer feedback:\n{state['feedback']}\n" if state.get("feedback") else ""
        response = presenter_llm.invoke(
            [
                SystemMessage(content=PRESENTER_SYSTEM_PROMPT),
                HumanMessage(
                    content=(
                        f"User request:\n{state['user_request']}\n\n"
                        f"Launch session JSON:\n{state['session_json']}\n\n"
                        f"Planner output:\n{state['plan_json']}\n\n"
                        f"Market report:\n{state['market_report']}\n\n"
                        f"ICP report:\n{state['icp_report']}\n\n"
                        f"Messaging report:\n{state['messaging_report']}\n\n"
                        f"Timeline report:\n{state['timeline_report']}\n\n"
                        f"Final board JSON:\n{state['final_board_json']}\n"
                        f"{feedback}\n"
                        "Requirements:\n"
                        "- Start with one bold headline line.\n"
                        "- Include sections named `Market Window`, `Audience Lock`, `Message Stack`, `Launch Runway`, and `Operator Call`.\n"
                        "- Use only flat bullet points where bullets make sense.\n"
                        "- End with a short motivating final paragraph.\n"
                    )
                ),
            ]
        )
        return {"final_response": response.content}

    return presenter
