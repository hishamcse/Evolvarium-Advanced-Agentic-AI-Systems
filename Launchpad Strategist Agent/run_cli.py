from pathlib import Path
import json
import sys

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from launchpad_strategist.services.engine import LaunchpadStrategistEngine


def cli() -> None:
    engine = LaunchpadStrategistEngine()
    startup_name = input("Startup name [Northstar Labs]: ").strip() or "Northstar Labs"
    product_name = input("Product name [SignalForge]: ").strip() or "SignalForge"
    product_type = input("Product type [ai_tool]: ").strip() or "ai_tool"
    stage = input("Stage [beta]: ").strip() or "beta"
    budget_band = input("Budget [lean]: ").strip() or "lean"
    launch_goal = input("Launch goal [beta waitlist]: ").strip() or "beta waitlist"

    result = engine.run_turn(
        "",
        startup_name=startup_name,
        product_name=product_name,
        product_type=product_type,
        stage=stage,
        budget_band=budget_band,
        launch_goal=launch_goal,
    )
    session_id = result["session_id"]
    print("\n" + result["response"] + "\n")
    print("Session state:")
    print(json.dumps(result["launch_state"], indent=2))
    print(f"\nSession ID: {session_id}\n")

    while True:
        prompt = input("Ask the strategist (`quit` to exit): ").strip()
        if prompt.lower() in {"quit", "exit"}:
            break
        turn = engine.run_turn(
            prompt,
            startup_name=startup_name,
            product_name=product_name,
            product_type=product_type,
            stage=stage,
            budget_band=budget_band,
            launch_goal=launch_goal,
            session_id=session_id,
        )
        print("\n" + turn["response"] + "\n")


if __name__ == "__main__":
    cli()
