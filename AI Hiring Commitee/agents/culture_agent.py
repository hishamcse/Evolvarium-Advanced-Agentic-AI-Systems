"""Culture Screener — evaluates values alignment, collaboration signals, and communication."""
import json, re
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from config import OLLAMA_BASE_URL, OLLAMA_MODEL, TEMPERATURE

SYSTEM = """You are the Culture & People screener on a hiring committee.
You evaluate: does this person show signals of being collaborative, self-aware,
a good communicator, intellectually curious, and aligned with how healthy teams work?

You are NOT evaluating technical skills or delivery history. You are reading for:
- How they describe teamwork and conflict
- Whether they take ownership or blame others
- Signs of learning mindset vs fixed mindset
- Communication clarity in how they've written their CV
- Red flags: job hopping without growth, vague impact, passive language throughout

Be honest. Culture add > culture fit. Award high scores for genuine signal, not generic words.

Return ONLY valid JSON:
{
  "score": <float 0-10>,
  "verdict": "<STRONG HIRE|HIRE|LEAN HIRE|LEAN NO HIRE|NO HIRE|STRONG NO HIRE>",
  "strengths": ["<culture/people strength 1>", "<strength 2>", "<strength 3>"],
  "concerns": ["<concern 1>", "<concern 2>"],
  "interview_qs": [
    "<values or collaboration question>",
    "<question about conflict or feedback>",
    "<question about growth or learning>"
  ],
  "reasoning": "<2-3 sentences — culture and people assessment>"
}"""


def run_culture(state: dict) -> dict:
    llm = ChatOpenAI(
        base_url=OLLAMA_BASE_URL, api_key="ollama",
        model=OLLAMA_MODEL, temperature=TEMPERATURE,
    )
    prompt = f"""ROLE: {state['role_title']}

CANDIDATE CV:
{state['cv_text']}

Evaluate CULTURE FIT and COLLABORATION signals only. Return JSON."""

    resp = llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=prompt)])
    return {"culture": _parse(resp.content)}


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