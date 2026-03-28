from langchain_core.messages import HumanMessage, SystemMessage

from launchpad_strategist.prompts.system_prompts import CRITIC_SYSTEM_PROMPT


def make_critic_node(critic_llm):
    def critic(state):
        review = critic_llm.invoke(
            [
                SystemMessage(content=CRITIC_SYSTEM_PROMPT),
                HumanMessage(content=f"User request:\n{state['user_request']}\n\nBrief:\n{state['final_response']}"),
            ]
        )
        if review.approved:
            return {"feedback": ""}
        return {"feedback": review.feedback, "retry_count": int(state.get("retry_count", 0)) + 1}

    return critic
