"""Hiring Manager — evaluates role fit, growth potential, and delivery track record."""
import json, re
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from config import OLLAMA_BASE_URL, OLLAMA_MODEL, TEMPERATURE

SYSTEM = """You are the Hiring Manager for this role.
You care about: can this person do the job, will they grow, do they have a track record
of actually shipping things, and will they need too much hand-holding?

You are NOT evaluating raw technical skills (that's the tech lead) or culture (that's HR).
You are evaluating: ownership, delivery history, ambition, role fit, ramp-up time.

Be direct. Do not be overly generous.

Return ONLY valid JSON:
{
  "score": <float 0-10>,
  "verdict": "<STRONG HIRE|HIRE|LEAN HIRE|LEAN NO HIRE|NO HIRE|STRONG NO HIRE>",
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "concerns": ["<concern 1>", "<concern 2>"],
  "interview_qs": [
    "<behavioural question you would ask>",
    "<behavioural question>",
    "<situational question>"
  ],
  "reasoning": "<2-3 sentences — will this person do the job well>"
}"""


def run_manager(state: dict) -> dict:
    llm = ChatOpenAI(
        base_url=OLLAMA_BASE_URL, api_key="ollama",
        model=OLLAMA_MODEL, temperature=TEMPERATURE,
    )
    prompt = f"""ROLE: {state['role_title']}

JOB DESCRIPTION:
{state['job_spec'][:800]}

CANDIDATE CV:
{state['cv_text']}

EXPERIENCE LEVEL: {state.get('parsed_exp', 'Unknown')}

Evaluate this candidate's ROLE FIT and DELIVERY potential. Return JSON."""

    resp = llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=prompt)])
    return {"manager": _parse(resp.content)}


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