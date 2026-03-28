from typing import TypedDict, List, Dict, Any


class Variant(TypedDict):
    code: str
    score: float
    feedback: str
    strategy: str
    breakdown: dict


class GenerationRecord(TypedDict):
    generation: int
    variants: List[Variant]
    selected: Variant


class MutationState(TypedDict):
    # Input
    original_code: str
    current_code: str

    # Loop control
    generation: int
    max_generations: int

    # Working memory
    variants: List[Variant]

    # History tracking
    history: List[GenerationRecord]