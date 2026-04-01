"""Technical Lead — evaluates skills depth, technical fit, and engineering quality."""
import json, re
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from config import OLLAMA_BASE_URL, OLLAMA_MODEL, TEMPERATURE

SYSTEM = """You are a Senior Technical Lead on a hiring committee.
You evaluate candidates ONLY on technical merit — skills, depth, problem-solving, 
engineering quality, and relevance to the role's technical requirements.

You do NOT consider culture, personality, or soft skills — that's someone else's job.
Be rigorous. Do not inflate scores. A 10 means exceptional.

Return ONLY valid JSON:
{
  "score": <float 0-10>,
  "verdict": "<STRONG HIRE|HIRE|LEAN HIRE|LEAN NO HIRE|NO HIRE|STRONG NO HIRE>",
  "strengths": ["<technical strength 1>", "<technical strength 2>", "<technical strength 3>"],
  "concerns": ["<technical concern 1>", "<technical concern 2>"],
  "interview_qs": [
    "<specific technical question you would ask this candidate>",
    "<specific technical question>",
    "<specific technical question>"
  ],
  "reasoning": "<2-3 sentences of technical assessment>"
}"""


def run_technical(state: dict) -> dict:
    llm = ChatOpenAI(
        base_url=OLLAMA_BASE_URL, api_key="ollama",
        model=OLLAMA_MODEL, temperature=TEMPERATURE,
    )
    prompt = f"""ROLE: {state['role_title']}

TECHNICAL REQUIREMENTS:
{chr(10).join(f"- {r}" for r in state.get('key_requirements', []))}

CANDIDATE CV:
{state['cv_text']}

DETECTED SKILLS: {', '.join(state.get('parsed_skills', []))}
EXPERIENCE: {state.get('parsed_exp', 'Unknown')}

Evaluate this candidate's TECHNICAL fit only. Return JSON."""

    resp = llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=prompt)])
    return {"technical": _parse(resp.content)}


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