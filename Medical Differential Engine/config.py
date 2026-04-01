"""
Medical Differential Engine — configuration
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

BASE_DIR   = Path(__file__).resolve().parent
MEMORY_DIR = BASE_DIR / "memory"
MEMORY_DIR.mkdir(exist_ok=True)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL    = os.getenv("OLLAMA_BASE_MODEL",    "qwen3:8b")
TEMPERATURE     = float(os.getenv("MDE_TEMPERATURE", "0.3"))

# Confidence thresholds for probability display
CONFIDENCE_LEVELS = {
    (0,   20): ("EXCLUDED",       "#4a5568"),
    (20,  40): ("UNLIKELY",       "#718096"),
    (40,  60): ("POSSIBLE",       "#d69e2e"),
    (60,  75): ("PROBABLE",       "#dd6b20"),
    (75,  90): ("LIKELY",         "#e53e3e"),
    (90, 101): ("HIGHLY LIKELY",  "#c53030"),
}

def confidence_label(score: float) -> tuple[str, str]:
    for (lo, hi), (label, color) in CONFIDENCE_LEVELS.items():
        if lo <= score < hi:
            return label, color
    return "UNKNOWN", "#718096"