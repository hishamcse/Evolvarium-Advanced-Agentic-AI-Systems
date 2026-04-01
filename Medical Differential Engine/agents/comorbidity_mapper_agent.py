"""
Comorbidity Mapper Agent — Layer 3 of the Bayesian cascade.
Analyses past medical history, medications, and social factors
to generate likelihood ratio modifiers that update the probability distribution.
"""
import json
import re
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from config import OLLAMA_BASE_URL, OLLAMA_MODEL, TEMPERATURE

SYSTEM = """You are an internist specialising in complex multimorbidity and drug interactions.
You receive a probability distribution and a patient's past medical history.

Your job is to:
1. Identify how each comorbidity MODIFIES the probability of each candidate diagnosis
2. Flag drug interactions, iatrogenic causes, or medication side effects as possible diagnoses
3. Note how risk factors (smoking, diabetes, immunosuppression, etc.) shift probabilities
4. Identify drug-drug interactions that could explain symptoms

Return TWO things as valid JSON:
{
  "comorbidity_flags": [
    "<clinical flag — e.g. 'Metformin use: lactic acidosis possible if AKI'>",
    "<flag>",
    ...
  ],
  "probability_modifiers": [
    {
      "diagnosis": "<diagnosis name from current list>",
      "modifier": <float multiplier, e.g. 1.8 = 80% more likely, 0.3 = 70% less likely>,
      "reason": "<why this comorbidity modifies this diagnosis probability>"
    }
  ]
}

Be clinically precise. Only generate modifiers where the comorbidity has a MEANINGFUL effect."""


def run_comorbidity_mapper(state: dict) -> dict:
    llm = ChatOpenAI(
        base_url=OLLAMA_BASE_URL, api_key="ollama",
        model=OLLAMA_MODEL, temperature=max(0.1, TEMPERATURE - 0.1),
    )

    candidates = state.get("refined_candidates", state.get("prior_candidates", []))
    dx_list = "\n".join(
        f"  - {c['name']} ({c['probability']:.0f}%)"
        for c in candidates
    )

    prompt = f"""Patient: {state.get('patient_age', '?')}, {state.get('patient_sex', '?')}
Chief complaint: {state.get('chief_complaint', '?')}

CURRENT DIFFERENTIAL (probabilities):
{dx_list}

PAST MEDICAL HISTORY & MEDICATIONS:
{state.get('history', 'None documented')}

RISK FACTORS IDENTIFIED:
{', '.join(state.get('parsed_features', {}).get('risk_factors', [])) or 'None identified'}

How does this patient's comorbidity profile modify the probability distribution?
Return JSON only."""

    resp = llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=prompt)])
    result = _parse(resp.content)

    # Apply modifiers to the candidate list
    candidates_with_mods = _apply_modifiers(
        candidates,
        result.get("probability_modifiers", [])
    )

    return {
        "comorbidity_flags": result.get("comorbidity_flags", []),
        "refined_candidates": candidates_with_mods,
    }


def _parse(text: str) -> dict:
    clean = re.sub(r"```(?:json)?", "", text).strip().strip("`")
    try:
        return json.loads(clean)
    except Exception:
        return {"comorbidity_flags": [], "probability_modifiers": []}


def _apply_modifiers(candidates: list, modifiers: list) -> list:
    """Apply likelihood ratio modifiers to the candidate probabilities."""
    modifier_map = {}
    for mod in modifiers:
        name = mod.get("diagnosis", "").lower()
        modifier_map[name] = float(mod.get("modifier", 1.0))

    updated = []
    for c in candidates:
        c = dict(c)
        name_lower = c["name"].lower()
        if name_lower in modifier_map:
            c["probability"] = min(99, max(1, c["probability"] * modifier_map[name_lower]))
        updated.append(c)

    # Renormalise to ~100
    total = sum(c["probability"] for c in updated)
    if total > 0:
        scale = 100.0 / total
        for c in updated:
            c["probability"] = round(c["probability"] * scale, 1)

    return updated