import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

BASE_DIR   = Path(__file__).resolve().parent
MEMORY_DIR = BASE_DIR / "memory"
MEMORY_DIR.mkdir(exist_ok=True)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL    = os.getenv("OLLAMA_BASE_MODEL",    "qwen3:8b")
TEMPERATURE     = float(os.getenv("COMMITTEE_TEMPERATURE", "0.4"))

# Weights for overall score — must sum to 1.0
SCORE_WEIGHTS = {
    "technical": 0.35,
    "manager":   0.25,
    "culture":   0.20,
    "advocate":  0.20,   # devil's advocate is inverted — high = more concerns
}

DECISION_THRESHOLDS = {
    "strong_hire":   8.0,
    "hire":          6.5,
    "no_hire":       5.0,
    # below 5.0 → strong no hire
}