"""Devil's Advocate — actively hunts for red flags, gaps, and reasons NOT to hire."""
import json, re
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from config import OLLAMA_BASE_URL, OLLAMA_MODEL, TEMPERATURE

SYSTEM = """You are the Devil's Advocate on a hiring committee. Your ONLY job is to
find reasons NOT to hire this candidate. You are not being mean — you are the person
who protects the team from costly bad hires.

You actively look for:
- Gaps in employment history and what they might mean
- Skills claimed but never demonstrated with evidence
- Job titles that don't match described responsibilities
- Vague impact claims ("helped improve", "contributed to") with no numbers
- Missing skills that are critical for this role
- Signs of exaggeration or inconsistency
- Whether the candidate is overqualified and likely to leave quickly
- Whether the candidate is underqualified and will struggle

Your score is INVERSE — a high score (8-10) means you found MANY serious red flags.
A low score (1-3) means the candidate is clean and you couldn't find much to worry about.

Return ONLY valid JSON:
{
  "score": <float 0-10 — HIGH MEANS MORE RED FLAGS>,
  "verdict": "<STRONG HIRE|HIRE|LEAN HIRE|LEAN NO HIRE|NO HIRE|STRONG NO HIRE>",
  "strengths": ["<one thing even you admit is good>"],
  "concerns": [
    "<specific red flag 1 — be precise>",
    "<specific red flag 2>",
    "<specific red flag 3>",
    "<specific red flag 4>"
  ],
  "interview_qs": [
    "<hard probing question to expose a weakness>",
    "<question to verify a suspicious claim>",
    "<question about a gap or concern>"
  ],
  "reasoning": "<2-3 sentences — your case against hiring>"
}"""


def run_advocate(state: dict) -> dict:
    llm = ChatOpenAI(
        base_url=OLLAMA_BASE_URL, api_key="ollama",
        model=OLLAMA_MODEL, temperature=min(0.6, TEMPERATURE + 0.1),
    )
    prompt = f"""ROLE: {state['role_title']}

REQUIREMENTS:
{chr(10).join(f"- {r}" for r in state.get('key_requirements', []))}

CANDIDATE CV:
{state['cv_text']}

Find every reason NOT to hire this candidate. Be forensic. Return JSON."""

    resp = llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=prompt)])
    return {"advocate": _parse(resp.content)}


def _parse(text: str) -> dict:
    clean = re.sub(r"```(?:json)?", "", text).strip().strip("`")
    try:
        d = json.loads(clean)
        return {
            "score":        float(d.get("score", 5.0)),
            "verdict":      d.get("verdict", "LEAN NO HIRE"),
            "strengths":    d.get("strengths", []),
            "concerns":     d.get("concerns", []),
            "interview_qs": d.get("interview_qs", []),
            "reasoning":    d.get("reasoning", ""),
        }
    except Exception:
        return {"score": 5.0, "verdict": "LEAN NO HIRE",
                "strengths": [], "concerns": ["Parse error"],
                "interview_qs": [], "reasoning": text[:200]}