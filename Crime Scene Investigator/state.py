from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


class CaseState(TypedDict):
    # Input
    case_id:        str
    case_title:     str
    case_brief:     str
    evidence_list:  str          # raw text, one item per line

    # Agent outputs
    forensics_report:   str
    prosecution_argument: str
    defense_argument:   str
    judge_reasoning:    str

    # Verdict
    verdict:            str      # guilty / not guilty / insufficient
    confidence:         float    # 0–100
    key_evidence:       List[str]
    reasonable_doubts:  List[str]
    final_summary:      str

    error: Optional[str]