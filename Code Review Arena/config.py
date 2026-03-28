import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

BASE_DIR = Path(__file__).resolve().parent
MEMORY_DIR = BASE_DIR / "memory"
MEMORY_DIR.mkdir(exist_ok=True)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_BASE_MODEL", "qwen3:8b")
TEMPERATURE = float(os.getenv("REVIEW_TEMPERATURE", "0.3"))

REVIEWER_ROLES = ["security", "performance", "logic", "style"]

SCORE_WEIGHTS = {
    "security": 0.35,
    "performance": 0.25,
    "logic": 0.25,
    "style": 0.15,
}