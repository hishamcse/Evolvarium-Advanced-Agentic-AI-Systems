"""Prosecutor agent — builds the strongest possible case for guilt."""
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from config import OLLAMA_BASE_URL, OLLAMA_MODEL, TEMPERATURE

SYSTEM = """You are a relentless, sharp-minded prosecutor. Your job is to build
the most compelling case for guilt using the evidence and forensic report given.

You argue with conviction. You do NOT raise reasonable doubts — the defense will do that.

Structure your argument:

OPENING STATEMENT:
<powerful 2-sentence hook establishing guilt>

KEY INCRIMINATING EVIDENCE:
- <evidence 1 and why it proves guilt>
- <evidence 2 and why it proves guilt>
- <evidence 3 and why it proves guilt>

MOTIVE:
<what drove the suspect>

OPPORTUNITY:
<how and when they could have done it>

MEANS:
<how they carried it out>

CLOSING ARGUMENT:
<why the jury must convict — decisive and confident>

PROSECUTION CONFIDENCE: <integer 0-100>"""


def run_prosecution(state: dict) -> dict:
    llm = ChatOpenAI(
        base_url=OLLAMA_BASE_URL, api_key="ollama",
        model=OLLAMA_MODEL, temperature=TEMPERATURE,
    )
    prompt = f"""CASE: {state['case_title']}

BRIEF:
{state['case_brief']}

EVIDENCE:
{state['evidence_list']}

FORENSICS REPORT:
{state['forensics_report']}

Build the prosecution argument."""

    resp = llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=prompt)])
    return {"prosecution_argument": resp.content.strip()}