import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

BASE_DIR   = Path(__file__).resolve().parent
MEMORY_DIR = BASE_DIR / "memory"
MEMORY_DIR.mkdir(exist_ok=True)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL    = os.getenv("OLLAMA_MODEL",    "qwen3:8b")
TEMPERATURE     = float(os.getenv("CSI_TEMPERATURE", "0.5"))

VERDICT_LABELS = {
    (0,  30):  ("INSUFFICIENT EVIDENCE", "var(--muted)"),
    (30, 55):  ("CASE DISMISSED",        "var(--cyan)"),
    (55, 75):  ("PROBABLE CAUSE",        "var(--gold)"),
    (75, 90):  ("GUILTY — BEYOND REASONABLE DOUBT", "var(--orange)"),
    (90, 101): ("GUILTY — OVERWHELMING EVIDENCE",   "var(--red)"),
}

def verdict_label(confidence: float) -> tuple[str, str]:
    for (lo, hi), (label, color) in VERDICT_LABELS.items():
        if lo <= confidence < hi:
            return label, color
    return "UNKNOWN", "var(--muted)"