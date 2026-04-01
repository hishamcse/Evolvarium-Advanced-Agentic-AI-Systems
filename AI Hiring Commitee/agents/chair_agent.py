"""Committee Chair — sees all four blind scores simultaneously and makes the call."""
import json, re
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from config import OLLAMA_BASE_URL, OLLAMA_MODEL, SCORE_WEIGHTS, DECISION_THRESHOLDS

SYSTEM = """You are the Committee Chair. You have just received four independent blind
evaluations of the same candidate. Your job is to:

1. Note where the committee AGREES (all leaning same direction)
2. Call out where they DISAGREE (e.g. tech lead loves them, culture screener has concerns)
3. Weight the devil's advocate's concerns seriously — their high score means real red flags
4. Make a final DECISION with clear reasoning

The devil's advocate score is INVERSE — high score = more red flags, so factor accordingly.

Return ONLY valid JSON:
{
  "overall_score": <float 0-10 — weighted final score>,
  "decision": "<STRONG HIRE|HIRE|NO HIRE|STRONG NO HIRE>",
  "chair_reasoning": "<3-4 sentences — your synthesis and rationale>",
  "key_agreements": ["<thing all/most evaluators agreed on>", "<agreement 2>"],
  "key_disagreements": ["<point of disagreement with context>", "<disagreement 2>"],
  "top_interview_qs": [
    "<the most important question this committee would ask>",
    "<second most important>",
    "<third most important>"
  ],
  "red_flags": ["<most serious red flag identified>", "<second red flag>"]
}"""


def run_chair(state: dict) -> dict:
    llm = ChatOpenAI(
        base_url=OLLAMA_BASE_URL, api_key="ollama",
        model=OLLAMA_MODEL, temperature=0.2,
    )

    tech  = state.get("technical", {})
    mgr   = state.get("manager",   {})
    cult  = state.get("culture",   {})
    adv   = state.get("advocate",  {})

    # Weighted score — advocate is inverted (high score = bad)
    adv_score_adj = 10.0 - float(adv.get("score", 5.0))
    weighted = (
        float(tech.get("score", 5.0)) * SCORE_WEIGHTS["technical"] +
        float(mgr.get("score",  5.0)) * SCORE_WEIGHTS["manager"]   +
        float(cult.get("score", 5.0)) * SCORE_WEIGHTS["culture"]   +
        adv_score_adj                 * SCORE_WEIGHTS["advocate"]
    )

    prompt = f"""CANDIDATE: {state.get('candidate_name')} — ROLE: {state.get('role_title')}

TECHNICAL LEAD (weight 35%):
Score: {tech.get('score')}/10  |  Verdict: {tech.get('verdict')}
Strengths: {tech.get('strengths')}
Concerns: {tech.get('concerns')}
Reasoning: {tech.get('reasoning')}

HIRING MANAGER (weight 25%):
Score: {mgr.get('score')}/10  |  Verdict: {mgr.get('verdict')}
Strengths: {mgr.get('strengths')}
Concerns: {mgr.get('concerns')}
Reasoning: {mgr.get('reasoning')}

CULTURE SCREENER (weight 20%):
Score: {cult.get('score')}/10  |  Verdict: {cult.get('verdict')}
Strengths: {cult.get('strengths')}
Concerns: {cult.get('concerns')}
Reasoning: {cult.get('reasoning')}

DEVIL'S ADVOCATE (weight 20% — INVERTED: high score = more red flags):
Red Flag Score: {adv.get('score')}/10  |  Verdict: {adv.get('verdict')}
Red Flags: {adv.get('concerns')}
Reasoning: {adv.get('reasoning')}

WEIGHTED SCORE CALCULATED: {weighted:.2f}/10

Synthesise these evaluations and return your JSON decision."""

    resp = llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=prompt)])
    data = _parse(resp.content, weighted)

    # Collect top interview questions from all evaluators
    all_qs = (
        tech.get("interview_qs", []) +
        mgr.get("interview_qs", [])  +
        cult.get("interview_qs", []) +
        adv.get("interview_qs", [])
    )

    return {
        "overall_score":     round(data.get("overall_score", weighted), 2),
        "decision":          data.get("decision", _threshold_decision(weighted)),
        "chair_reasoning":   data.get("chair_reasoning", ""),
        "key_agreements":    data.get("key_agreements", []),
        "key_disagreements": data.get("key_disagreements", []),
        "top_interview_qs":  data.get("top_interview_qs", all_qs[:3]),
        "red_flags":         data.get("red_flags", adv.get("concerns", [])[:2]),
    }


def _parse(text: str, fallback_score: float) -> dict:
    clean = re.sub(r"```(?:json)?", "", text).strip().strip("`")
    try:
        return json.loads(clean)
    except Exception:
        return {
            "overall_score":     fallback_score,
            "decision":          _threshold_decision(fallback_score),
            "chair_reasoning":   text[:300],
            "key_agreements":    [],
            "key_disagreements": [],
            "top_interview_qs":  [],
            "red_flags":         [],
        }


def _threshold_decision(score: float) -> str:
    if score >= DECISION_THRESHOLDS["strong_hire"]: return "STRONG HIRE"
    if score >= DECISION_THRESHOLDS["hire"]:        return "HIRE"
    if score >= DECISION_THRESHOLDS["no_hire"]:     return "NO HIRE"
    return "STRONG NO HIRE"