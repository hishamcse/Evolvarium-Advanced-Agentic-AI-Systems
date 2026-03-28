from agents.mutate_agent import MutateAgent
from graph.state import MutationState


mutator = MutateAgent()


def mutator_node(state: MutationState) -> MutationState:
    code = state["current_code"]

    print("Running mutator...")

    variants_raw = mutator.mutate(code)

    print("mutator done...")

    variants = []
    for v in variants_raw:
        variants.append({
            "code": v.get("code", ""),
            "score": 0.0,
            "feedback": "",
            "strategy": v.get("strategy", "")
        })

    return {
        "variants": variants
    }
