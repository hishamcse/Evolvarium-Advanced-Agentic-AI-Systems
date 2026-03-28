import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(override=True)

BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE_DIR / "output"
MEMORY_DIR = BASE_DIR / "memory"
LAUNCH_DIR = MEMORY_DIR / "launches"

for directory in (OUTPUT_DIR, MEMORY_DIR, LAUNCH_DIR):
    directory.mkdir(parents=True, exist_ok=True)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_BASE_MODEL = os.getenv("OLLAMA_BASE_MODEL", "qwen3:8b")
LAUNCHPAD_TEMPERATURE = float(os.getenv("LAUNCHPAD_TEMPERATURE", "0.45"))
LAUNCHPAD_MAX_RETRIES = int(os.getenv("LAUNCHPAD_MAX_RETRIES", "2"))
