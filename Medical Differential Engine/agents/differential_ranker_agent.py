"""
Differential Ranker Agent — Layer 5, final synthesis.
Ranks the posterior distribution, generates the clinical summary,
workup plan, red flags, and probability narrative.
"""
import json
import re
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from config import OLLAMA_BASE_URL, OLLAMA_MODEL

SYSTEM = """You are the attending physician delivering the final clinical assessment.
You receive the fully-updated posterior probability distribution from the evidence weigher.

Your job:
1. Rank diagnoses from most to least probable
2. Flag any EMERGENCY diagnoses regardless of probability (must-not-miss)
3. Generate a prioritised workup plan (tests in order of urgency and yield)
4. Write a concise probability narrative explaining how the distribution evolved
5. Write a clinical summary paragraph

Return ONLY valid JSON:
{
  "differential": [
    {
      "name": "<diagnosis>",
      "icd_hint": "<ICD-10>",
      "probability": <float>,
      "confidence": "<level>",
      "supporting": ["<feature>"],
      "against": ["<feature>"],
      "urgency": "<EMERGENCY|URGENT|ROUTINE>",
      "rare_flag": <bool>,
      "key_test": "<most important confirming test>",
      "likelihood_ratio_note": "<probability shift explanation>"
    }
  ],
  "red_flags": ["<emergency warning that requires immediate action>"],
  "workup_plan": [
    "<STAT: test — reason>",
    "<URGENT: test — reason>",
    "<ROUTINE: test — reason>"
  ],
  "disposition": "<EMERGENCY|URGENT|ROUTINE>",
  "clinical_summary": "<3-4 sentence clinical synthesis>",
  "probability_narrative": "<2-3 sentences describing how the probability distribution shifted through the cascade — what moved it most>"
}"""


def run_differential_ranker(state: dict) -> dict:
    llm = ChatOpenAI(
        base_url=OLLAMA_BASE_URL, api_key="ollama",
        model=OLLAMA_MODEL, temperature=0.2,
    )

    candidates = state.get("weighted_candidates",
                 state.get("refined_candidates",
                 state.get("prior_candidates", [])))

    # Sort by probability descending for the prompt
    sorted_cands = sorted(candidates, key=lambda x: x.get("probability", 0), reverse=True)
    cand_text = "\n".join(
        f"  {i+1}. {c['name']}: {c['probability']:.1f}% — {c['confidence']} — {c['urgency']}"
        f"\n     Supporting: {'; '.join(c.get('supporting', []))}"
        f"\n     Against: {'; '.join(c.get('against', []))}"
        for i, c in enumerate(sorted_cands)
    )

    prompt = f"""Patient: {state.get('patient_age', '?')}, {state.get('patient_sex', '?')}
Chief complaint: {state.get('chief_complaint', '?')}

FINAL POSTERIOR DISTRIBUTION:
{cand_text}

COMORBIDITY FLAGS:
{chr(10).join('  - ' + f for f in state.get('comorbidity_flags', [])) or '  None'}

VITALS: {state.get('vitals', 'Not provided')}
EXAM: {state.get('exam_findings', 'Not provided')}

Generate the final ranked differential, workup plan, and clinical synthesis. JSON only."""

    resp = llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=prompt)])
    result = _parse(resp.content, sorted_cands)
    return result


def _parse(text: str, fallback_cands: list) -> dict:
    clean = re.sub(r"```(?:json)?", "", text).strip().strip("`")
    try:
        data = json.loads(clean)
        return {
            "differential":          data.get("differential", fallback_cands),
            "red_flags":             data.get("red_flags", []),
            "workup_plan":           data.get("workup_plan", []),
            "disposition":           data.get("disposition", "ROUTINE"),
            "clinical_summary":      data.get("clinical_summary", ""),
            "probability_narrative": data.get("probability_narrative", ""),
        }
    except Exception:
        return {
            "differential":          fallback_cands,
            "red_flags":             [],
            "workup_plan":           [],
            "disposition":           "ROUTINE",
            "clinical_summary":      text[:300],
            "probability_narrative": "",
        }