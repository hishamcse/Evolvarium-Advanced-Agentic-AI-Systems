from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from launchpad_strategist.ui.layout import build_demo


demo = build_demo()


if __name__ == "__main__":
    demo.launch()
