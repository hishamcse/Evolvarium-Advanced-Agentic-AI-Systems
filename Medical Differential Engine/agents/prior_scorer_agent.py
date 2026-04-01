"""
Prior Scorer Agent — Layer 1 of the Bayesian cascade.
Generates the initial probability distribution over candidate diagnoses
based purely on epidemiology and classic presentation patterns.
Does NOT refine — sets the prior before evidence is applied.
"""
import json
import re
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from config import OLLAMA_BASE_URL, OLLAMA_MODEL, TEMPERATURE

SYSTEM = """You are an experienced emergency physician and clinical epidemiologist.
Your role is to generate an INITIAL probability distribution (priors) over likely diagnoses.

Base your priors on:
- Epidemiological base rates for this age/sex/presentation
- Classic symptom patterns (sensitivity/specificity of key features)
- Do NOT yet weight individual pieces of evidence heavily — this is the prior

You must generate 5–8 candidate diagnoses covering:
- The most common explanation (high prior probability)
- The most dangerous "must not miss" diagnoses (even if low probability)
- At least one rare but plausible alternative

Return ONLY valid JSON — an array:
[
  {
    "name": "<diagnosis name>",
    "icd_hint": "<ICD-10 category, e.g. I21 - AMI>",
    "probability": <float 0-100, prior probability>,
    "confidence": "<EXCLUDED|UNLIKELY|POSSIBLE|PROBABLE|LIKELY|HIGHLY LIKELY>",
    "supporting": ["<feature from presentation that supports this>"],
    "against": ["<feature that argues against this>"],
    "urgency": "<EMERGENCY|URGENT|ROUTINE>"
  }
]

IMPORTANT: Probabilities should sum to approximately 100 across the list.
Always include at least one EMERGENCY-level diagnosis even if probability is low."""


def run_prior_scorer(state: dict) -> dict:
    llm = ChatOpenAI(
        base_url=OLLAMA_BASE_URL, api_key="ollama",
        model=OLLAMA_MODEL, temperature=TEMPERATURE,
    )

    features = state.get("parsed_features", {})
    red_flags = features.get("red_flag_features", [])
    system_review = features.get("system_review", {})

    prompt = f"""Patient: {state.get('patient_age', '?')}, {state.get('patient_sex', '?')}
Chief complaint: {state.get('chief_complaint', '?')}

STRUCTURED FEATURES (from parser):
- Onset: {features.get('onset', 'unknown')}
- Location: {', '.join(features.get('location', []))}
- Character: {', '.join(features.get('character', []))}
- Severity: {features.get('severity', 'unknown')}
- Timing: {features.get('timing', 'unknown')}
- Associated symptoms: {', '.join(features.get('associated_symptoms', []))}
- Red flag features: {', '.join(red_flags) if red_flags else 'None identified'}
- Vital abnormalities: {', '.join(features.get('vital_abnormalities', []))}
- Risk factors: {', '.join(features.get('risk_factors', []))}
- Modifying: better with {', '.join(features.get('modifying_factors', {}).get('better', []))}; worse with {', '.join(features.get('modifying_factors', {}).get('worse', []))}

SYSTEMS POSITIVE: {', '.join(k for k, v in system_review.items() if v == 'pos')}
SYSTEMS NEGATIVE: {', '.join(k for k, v in system_review.items() if v == 'neg')}

Generate the initial probability distribution. Return JSON array only."""

    resp = llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=prompt)])
    candidates = _parse(resp.content)
    return {"prior_candidates": candidates}


def _parse(text: str) -> list:
    clean = re.sub(r"```(?:json)?", "", text).strip().strip("`")
    try:
        data = json.loads(clean)
        if isinstance(data, list):
            return [_normalize(d) for d in data]
        return []
    except Exception:
        return []


def _normalize(d: dict) -> dict:
    return {
        "name":       d.get("name", "Unknown"),
        "icd_hint":   d.get("icd_hint", ""),
        "probability": float(d.get("probability", 10)),
        "confidence": d.get("confidence", "POSSIBLE"),
        "supporting": d.get("supporting", []),
        "against":    d.get("against", []),
        "urgency":    d.get("urgency", "ROUTINE"),
    }