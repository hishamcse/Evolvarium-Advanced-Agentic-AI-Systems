from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


class EvaluatorResult(TypedDict):
    score:          float        # 0-10
    verdict:        str          # hire / lean_hire / lean_no_hire / no_hire
    strengths:      List[str]
    concerns:       List[str]
    interview_qs:   List[str]    # questions this evaluator would ask
    reasoning:      str


class CommitteeState(TypedDict):
    # Input
    session_id:      str
    candidate_name:  str
    role_title:      str
    cv_text:         str
    job_spec:        str

    # Parsed fields (from bootstrap/MCP)
    parsed_skills:   List[str]
    parsed_exp:      str         # years + seniority
    key_requirements: List[str]  # extracted from job spec

    # Evaluator outputs — all blind to each other
    technical:       EvaluatorResult
    manager:         EvaluatorResult
    culture:         EvaluatorResult
    advocate:        EvaluatorResult   # devil's advocate

    # Chair synthesis
    overall_score:   float
    decision:        str         # STRONG HIRE / HIRE / NO HIRE / STRONG NO HIRE
    chair_reasoning: str
    key_agreements:  List[str]
    key_disagreements: List[str]
    top_interview_qs: List[str]
    red_flags:       List[str]

    error: Optional[str]