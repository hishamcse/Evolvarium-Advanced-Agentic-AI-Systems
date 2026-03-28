import json


def make_bootstrap_node(client):
    def bootstrap(state):
        session_id = state.get("session_id")
        if not session_id:
            payload = json.loads(
                client.call_tool(
                    "create_launch_session",
                    {
                        "startup_name": state["startup_name"],
                        "product_name": state["product_name"],
                        "product_type": state["product_type"],
                        "stage": state["stage"],
                        "budget_band": state["budget_band"],
                        "launch_goal": state["launch_goal"],
                    },
                )
            )
            session_id = payload["session_id"]
        session_json = client.read_resource(f"launchpad://session/{session_id}")
        return {"session_id": session_id, "session_json": session_json, "feedback": "", "retry_count": 0}

    return bootstrap
