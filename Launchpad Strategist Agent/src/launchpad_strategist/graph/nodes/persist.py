def make_persist_node(client):
    def persist(state):
        client.call_tool(
            "append_launch_log",
            {"session_id": state["session_id"], "actor": state["startup_name"], "content": state["user_request"]},
        )
        client.call_tool(
            "append_launch_log",
            {"session_id": state["session_id"], "actor": "Launch Operator", "content": state["final_response"]},
        )
        return {"session_json": client.read_resource(f"launchpad://session/{state['session_id']}")}

    return persist
