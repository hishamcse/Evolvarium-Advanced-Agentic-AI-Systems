"""Judge agent — impartially weighs the debate and delivers a structured verdict."""
import json
import re
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from config import OLLAMA_BASE_URL, OLLAMA_MODEL

SYSTEM = """You are a senior judge presiding over a criminal case. You have heard
arguments from both prosecution and defense. You must now deliberate and rule.

You are NOT a prosecutor or defender. You weigh evidence impartially.

You must return ONLY valid JSON in this exact format:
{
  "verdict": "guilty" | "not guilty" | "insufficient evidence",
  "confidence": <integer 0-100 representing certainty in your verdict>,
  "reasoning": "<3-4 sentences explaining your legal reasoning>",
  "key_evidence": ["<most damning piece of evidence>", "<second>", "<third>"],
  "reasonable_doubts": ["<main doubt 1>", "<main doubt 2>"],
  "final_summary": "<one powerful sentence that is your closing statement>"
}

confidence guide:
- 0-30:  nowhere near proven — insufficient evidence
- 31-54: some suspicion but not proven — not guilty
- 55-74: probable cause — leaning guilty but doubt remains
- 75-89: guilty beyond reasonable doubt
- 90-100: overwhelming — guilty with near certainty"""


def run_judge(state: dict) -> dict:
    llm = ChatOpenAI(
        base_url=OLLAMA_BASE_URL, api_key="ollama",
        model=OLLAMA_MODEL, temperature=0.2,
    )
    prompt = f"""CASE: {state['case_title']}

FORENSICS REPORT:
{state['forensics_report']}

PROSECUTION ARGUMENT:
{state['prosecution_argument']}

DEFENSE ARGUMENT:
{state['defense_argument']}

Deliberate and return your verdict as JSON."""

    resp = llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=prompt)])
    data = _parse_verdict(resp.content)

    return {
        "verdict":           data.get("verdict",         "insufficient evidence"),
        "confidence":        float(data.get("confidence", 50)),
        "judge_reasoning":   data.get("reasoning",       ""),
        "key_evidence":      data.get("key_evidence",    []),
        "reasonable_doubts": data.get("reasonable_doubts", []),
        "final_summary":     data.get("final_summary",   ""),
    }


def _parse_verdict(text: str) -> dict:
    # strip markdown fences
    clean = re.sub(r"```(?:json)?", "", text).strip().strip("`")
    try:
        return json.loads(clean)
    except Exception:
        # fallback: extract confidence from text
        m = re.search(r'"confidence"\s*:\s*(\d+)', clean)
        conf = int(m.group(1)) if m else 50
        v = "guilty" if conf >= 55 else "not guilty"
        return {
            "verdict": v, "confidence": conf,
            "reasoning": clean[:300],
            "key_evidence": [], "reasonable_doubts": [],
            "final_summary": "Verdict determined by evidence weight.",
        }