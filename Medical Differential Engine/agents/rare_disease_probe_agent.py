"""
Rare Disease Probe Agent — Layer 2 of the Bayesian cascade.
Reads the prior distribution and actively probes for rare diagnoses
that could be masquerading as common presentations.
Updates the probability distribution by injecting rare candidates.
"""
import json
import re
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from config import OLLAMA_BASE_URL, OLLAMA_MODEL, TEMPERATURE

SYSTEM = """You are a specialist in rare and atypical disease presentations — a diagnostician
known for catching diagnoses others miss.

You receive the CURRENT probability distribution from a prior scoring agent.
Your job:
1. Identify any rare, atypical, or "zebra" diagnoses that the prior distribution may have MISSED
2. Check if any common diagnosis is actually a rare variant in disguise
3. Add or adjust candidates accordingly

You MUST:
- Keep all existing candidates (you may adjust their probabilities)
- Add 1–3 new rare/atypical candidates if clinically justified
- Flag any "diagnostic traps" — ways this case could fool a clinician
- Renormalise so probabilities still sum to ~100

Return ONLY valid JSON — the COMPLETE updated array:
[
  {
    "name": "<diagnosis name>",
    "icd_hint": "<ICD-10 hint>",
    "probability": <float 0-100>,
    "confidence": "<EXCLUDED|UNLIKELY|POSSIBLE|PROBABLE|LIKELY|HIGHLY LIKELY>",
    "supporting": ["<supporting feature>"],
    "against": ["<against feature>"],
    "urgency": "<EMERGENCY|URGENT|ROUTINE>",
    "rare_flag": <true if this is a rare/atypical addition, else false>
  }
]"""


def run_rare_probe(state: dict) -> dict:
    llm = ChatOpenAI(
        base_url=OLLAMA_BASE_URL, api_key="ollama",
        model=OLLAMA_MODEL, temperature=TEMPERATURE + 0.1,
    )

    prior = state.get("prior_candidates", [])
    features = state.get("parsed_features", {})

    prior_summary = "\n".join(
        f"  {i+1}. {c['name']}: {c['probability']:.0f}% ({c['confidence']}) [{c['urgency']}]"
        for i, c in enumerate(prior)
    )

    prompt = f"""Patient: {state.get('patient_age', '?')}, {state.get('patient_sex', '?')}
Chief complaint: {state.get('chief_complaint', '?')}

CURRENT PROBABILITY DISTRIBUTION:
{prior_summary}

KEY CLINICAL FEATURES:
- Red flags: {', '.join(features.get('red_flag_features', [])) or 'None'}
- Associated symptoms: {', '.join(features.get('associated_symptoms', [])) or 'None'}
- Risk factors: {', '.join(features.get('risk_factors', [])) or 'None'}
- Excluded features: {', '.join(features.get('excluded_features', [])) or 'None'}

HISTORY & EXAM:
{state.get('history', 'Not provided')}
{state.get('exam_findings', 'Not provided')}

Probe for rare/atypical diagnoses. Update the full distribution. Return JSON array only."""

    resp = llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=prompt)])
    candidates = _parse(resp.content, prior)
    return {"refined_candidates": candidates}


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
        "name":       d.get("name", "Unknown"),
        "icd_hint":   d.get("icd_hint", ""),
        "probability": float(d.get("probability", 5)),
        "confidence": d.get("confidence", "UNLIKELY"),
        "supporting": d.get("supporting", []),
        "against":    d.get("against", []),
        "urgency":    d.get("urgency", "ROUTINE"),
        "rare_flag":  bool(d.get("rare_flag", False)),
    }