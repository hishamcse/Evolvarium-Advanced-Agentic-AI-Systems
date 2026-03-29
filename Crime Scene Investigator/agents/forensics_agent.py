"""Forensics agent — cold, neutral analysis of physical and digital evidence."""
import re

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from config import OLLAMA_BASE_URL, OLLAMA_MODEL, TEMPERATURE

SYSTEM = """You are a senior forensic scientist. You analyse evidence with zero bias.
You neither try to convict nor acquit — you only state what the evidence shows.

Structure your report exactly as:

PHYSICAL EVIDENCE ANALYSIS:
<findings>

DIGITAL / WITNESS EVIDENCE:
<findings>

TIMELINE RECONSTRUCTION:
<chronology>

FORENSIC ASSESSMENT:
<what the evidence proves, what it cannot prove>

CRITICAL GAPS:
<what evidence is missing that would change the analysis>"""


def _tag_evidence(text: str) -> str:
    lines, tagged = [l.strip() for l in text.splitlines() if l.strip()], []
    for item in lines:
        lo = item.lower()
        if any(w in lo for w in ["witness","saw","heard","testimony","claims","confirms","testified"]):
            tag = "WITNESS"
        elif any(w in lo for w in ["fingerprint","dna","blood","glass","weapon","footprint","shoe","mud","fibre","hair"]):
            tag = "PHYSICAL"
        elif any(w in lo for w in ["cctv","phone","laptop","email","digital","log","record","camera"]):
            tag = "DIGITAL"
        else:
            tag = "CIRCUMSTANTIAL"
        tagged.append(f"[{tag}] {item}")
    return "\n".join(tagged) if tagged else "No evidence items."


def _extract_timeline(text: str) -> str:
    times = re.findall(
        r"(?:at\s+)?(\d{1,2}[:.]\d{2}\s*(?:am|pm)?|\d{1,2}\s*(?:am|pm)|"
        r"(?:morning|afternoon|evening|night|midnight|noon))[^.]*\.",
        text, re.IGNORECASE
    )
    if times:
        return "Timeline:\n" + "\n".join(f"- {t.strip()}" for t in times[:10])
    return "No explicit timestamps found in brief."


def run_forensics(state: dict) -> dict:
    llm = ChatOpenAI(
        base_url=OLLAMA_BASE_URL, api_key="ollama",
        model=OLLAMA_MODEL, temperature=max(0.1, TEMPERATURE - 0.2),
    )
    tagged   = _tag_evidence(state.get("evidence_list", ""))
    timeline = _extract_timeline(state.get("case_brief", ""))

    prompt = f"""CASE: {state['case_title']}

BRIEF:
{state['case_brief']}

TAGGED EVIDENCE:
{tagged}

EXTRACTED TIMELINE:
{timeline}

Produce your forensic report."""

    resp = llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=prompt)])
    return {"forensics_report": resp.content.strip()}