from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_BASE_MODEL", "qwen3:8b")
TEMPERATURE = float(os.getenv("REVIEW_TEMPERATURE", "0.3"))


def get_llm():
    return ChatOpenAI(
        base_url=OLLAMA_BASE_URL,
        api_key="ollama",
        model=OLLAMA_MODEL,
        temperature=TEMPERATURE,
    )
