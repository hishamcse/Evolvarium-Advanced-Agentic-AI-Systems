"""
Medical Differential Engine — LangGraph state
Bayesian cascade: each agent receives and updates a shared probability distribution.
"""
from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


class DiagnosisCandidate(TypedDict):
    name: str
    icd_hint: str          # rough ICD category hint
    probability: float     # 0–100
    confidence: str        # EXCLUDED / UNLIKELY / POSSIBLE / PROBABLE / LIKELY / HIGHLY LIKELY
    supporting: List[str]  # symptoms/signs that support this
    against: List[str]     # findings that argue against this
    urgency: str           # EMERGENCY / URGENT / ROUTINE


class EngineState(TypedDict):
    # ── inputs ──────────────────────────────────────────────────────────────
    case_id:          str
    patient_age:      str
    patient_sex:      str
    chief_complaint:  str
    symptoms:         str         # raw symptom text
    vitals:           str         # BP, HR, Temp, RR, SpO2
    history:          str         # PMH, meds, allergies, social
    exam_findings:    str         # physical exam

    # ── cascade layers (each agent writes its own slot) ─────────────────────
    parsed_features:  Dict[str, Any]   # symptom parser structured output
    prior_candidates: List[DiagnosisCandidate]   # symptom scorer output
    refined_candidates: List[DiagnosisCandidate] # rare disease probe output
    comorbidity_flags:  List[str]                # comorbidity mapper flags
    weighted_candidates: List[DiagnosisCandidate] # evidence weigher output

    # ── final output ─────────────────────────────────────────────────────────
    differential:     List[DiagnosisCandidate]   # top ranked final list
    red_flags:        List[str]                  # emergency flags
    workup_plan:      List[str]                  # recommended tests
    disposition:      str                        # EMERGENCY / URGENT / ROUTINE
    clinical_summary: str                        # one-paragraph synthesis
    probability_narrative: str                   # how probabilities shifted

    error: Optional[str]