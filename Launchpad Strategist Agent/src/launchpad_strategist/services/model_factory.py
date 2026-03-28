from langchain_openai import ChatOpenAI

from launchpad_strategist.config import OLLAMA_BASE_MODEL, OLLAMA_BASE_URL


def make_llm(temperature: float) -> ChatOpenAI:
    return ChatOpenAI(
        model=OLLAMA_BASE_MODEL,
        base_url=OLLAMA_BASE_URL,
        api_key="ollama",
        temperature=temperature,
    )
