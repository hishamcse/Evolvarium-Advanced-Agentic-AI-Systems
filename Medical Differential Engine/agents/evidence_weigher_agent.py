"""
Evidence Weigher Agent — Layer 4 of the Bayesian cascade.
Applies the full weight of clinical examination, vital signs, and all collected
evidence to produce a posterior probability distribution.
This is the final refinement before the differential ranker.
"""
import json
import re
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from config import OLLAMA_BASE_URL, OLLAMA_MODEL, TEMPERATURE

SYSTEM = """You are a senior consultant applying Bayesian clinical reasoning.
You receive a probability distribution already updated for comorbidities and rare diseases.
Now apply the FULL WEIGHT of the clinical examination findings and vital signs
to produce the final POSTERIOR probability distribution.

For each candidate diagnosis, consider:
- Do the exam findings fit this diagnosis (positive likelihood ratios)?
- Do any exam findings argue strongly against this diagnosis?
- What is the combined posterior probability after all evidence?

Return the COMPLETE updated array as JSON:
[
  {
    "name": "<diagnosis name>",
    "icd_hint": "<ICD-10 hint>",
    "probability": <float 0-100, posterior probability>,
    "confidence": "<EXCLUDED|UNLIKELY|POSSIBLE|PROBABLE|LIKELY|HIGHLY LIKELY>",
    "supporting": ["<feature supporting>"],
    "against": ["<feature against>"],
    "urgency": "<EMERGENCY|URGENT|ROUTINE>",
    "rare_flag": <true/false>,
    "key_test": "<single most important test to confirm/exclude this diagnosis>",
    "likelihood_ratio_note": "<brief note on what drove the probability change>"
  }
]

confidence mapping:
- EXCLUDED: < 5%
- UNLIKELY: 5–25%
- POSSIBLE: 25–50%
- PROBABLE: 50–70%
- LIKELY: 70–85%
- HIGHLY LIKELY: > 85%

Renormalise so probabilities sum to ~100."""


def run_evidence_weigher(state: dict) -> dict:
    llm = ChatOpenAI(
        base_url=OLLAMA_BASE_URL, api_key="ollama",
        model=OLLAMA_MODEL, temperature=max(0.1, TEMPERATURE - 0.1),
    )

    candidates = state.get("refined_candidates", state.get("prior_candidates", []))
    features = state.get("parsed_features", {})
    flags = state.get("comorbidity_flags", [])

    current_dist = "\n".join(
        f"  {i+1}. {c['name']}: {c['probability']:.1f}% — {c['confidence']}"
        for i, c in enumerate(candidates)
    )

    prompt = f"""Patient: {state.get('patient_age', '?')}, {state.get('patient_sex', '?')}
Chief complaint: {state.get('chief_complaint', '?')}

CURRENT PROBABILITY DISTRIBUTION (after comorbidity update):
{current_dist}

COMORBIDITY FLAGS:
{chr(10).join('  - ' + f for f in flags) if flags else '  None'}

VITAL SIGNS:
{state.get('vitals', 'Not provided')}

PHYSICAL EXAMINATION:
{state.get('exam_findings', 'Not documented')}

EXCLUDED CLINICAL FEATURES:
{', '.join(features.get('excluded_features', [])) or 'None documented'}

Apply full evidence weight and return the final posterior distribution. JSON array only."""

    resp = llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=prompt)])
    candidates = _parse(resp.content, state.get("refined_candidates", []))
    return {"weighted_candidates": candidates}


def _parse(text: str, fallback: list) -> list:
    clean = re.sub(r"```(?:json)?", "", text).strip().strip("`")
    try:
        data = json.loads(clean)
        if isinstance(data, list) and data:
            return [_normalize(d) for d in data]
    except Exception:
        pass
    return fallback


def _normalize(d: dict) -> dict:
    return {
        "name":        d.get("name", "Unknown"),
        "icd_hint":    d.get("icd_hint", ""),
        "probability": float(d.get("probability", 5)),
        "confidence":  d.get("confidence", "POSSIBLE"),
        "supporting":  d.get("supporting", []),
        "against":     d.get("against", []),
        "urgency":     d.get("urgency", "ROUTINE"),
        "rare_flag":   bool(d.get("rare_flag", False)),
        "key_test":    d.get("key_test", ""),
        "likelihood_ratio_note": d.get("likelihood_ratio_note", ""),
    }