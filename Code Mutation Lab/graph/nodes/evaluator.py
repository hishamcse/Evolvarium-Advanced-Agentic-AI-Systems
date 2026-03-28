from operator import index, indexOf
from agents.evaluate_agent import EvaluateAgent
from graph.state import MutationState


evaluator = EvaluateAgent()


def evaluator_node(state: MutationState) -> MutationState:
    variants = state.get("variants", [])

    evaluated = []

    for v in variants:
        print(f"Evaluating variant")
        result = evaluator.evaluate(v["code"])
        print(f"Evaluation done variant")

        evaluated.append({
            "code": v["code"],
            "strategy": v.get("strategy", ""),
            "score": result["score"],
            "feedback": result["feedback"],
            "breakdown": result["breakdown"]
        })

    return {
        "variants": evaluated
    }
