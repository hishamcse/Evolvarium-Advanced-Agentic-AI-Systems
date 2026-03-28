from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


class ReviewState(TypedDict):
    session_id: str
    code: str
    language: str
    filename: Optional[str]
    lint_output: str
    ast_summary: str
    # Reviewer outputs (filled in parallel)
    security_review: str
    performance_review: str
    logic_review: str
    style_review: str
    # Scores per reviewer (0-10)
    scores: Dict[str, float]
    # Aggregated output
    overall_score: float
    summary: str
    top_issues: List[Dict[str, Any]]
    final_report: str
    error: Optional[str]
    security_score: Optional[float]
    performance_score: Optional[float]
    logic_score: Optional[float]
    style_score: Optional[float]
