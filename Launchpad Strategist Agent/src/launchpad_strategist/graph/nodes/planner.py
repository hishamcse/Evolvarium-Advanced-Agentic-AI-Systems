import json

from langchain_core.messages import HumanMessage, SystemMessage

from launchpad_strategist.graph.routing import sanitize_steps
from launchpad_strategist.prompts.system_prompts import PLANNER_SYSTEM_PROMPT


def make_planner_node(client, planner_llm):
    def planner(state):
        objective = "proof" if "proof" in state["user_request"].lower() else "balanced"
        raw = client.call_tool(
            "plan_launch",
            {"session_id": state["session_id"], "objective": objective, "request": state["user_request"]},
        )
        plan = planner_llm.invoke(
            [
                SystemMessage(content=PLANNER_SYSTEM_PROMPT),
                HumanMessage(
                    content=(
                        f"User request:\n{state['user_request']}\n\n"
                        f"Launch session JSON:\n{state['session_json']}\n\n"
                        f"Raw planner JSON:\n{raw}\n\n"
                        "Return the execution plan."
                    )
                ),
            ]
        )
        payload = {
            "objective": plan.objective,
            "launch_angle": plan.launch_angle,
            "rationale": plan.rationale,
            "step_order": sanitize_steps(plan.step_order),
            "confidence": max(0.0, min(plan.confidence, 1.0)),
        }
        return {
            "plan_json": json.dumps(payload, indent=2),
            "step_order": payload["step_order"],
            "execution_cursor": 0,
            "session_json": client.read_resource(f"launchpad://session/{state['session_id']}"),
        }

    return planner
