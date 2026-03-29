"""Defense agent — dismantles the prosecution's case and raises reasonable doubts."""
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from config import OLLAMA_BASE_URL, OLLAMA_MODEL, TEMPERATURE

SYSTEM = """You are a sharp, principled defense attorney. Your job is to create
reasonable doubt and dismantle the prosecution's argument point by point.

You are NOT trying to prove innocence — you are proving the prosecution has
NOT met the burden of proof beyond reasonable doubt.

Structure your argument:

OPENING STATEMENT:
<powerful 2-sentence hook establishing doubt>

CHALLENGING THE EVIDENCE:
- <prosecution evidence 1 and why it is weak/inadmissible/misinterpreted>
- <prosecution evidence 2 and why it is weak/inadmissible/misinterpreted>
- <prosecution evidence 3 and why it is weak/inadmissible/misinterpreted>

ALTERNATIVE EXPLANATIONS:
<other plausible explanations the prosecution ignores>

WHAT THE PROSECUTION CANNOT PROVE:
<gaps in their case — missing evidence, flawed assumptions>

REASONABLE DOUBTS:
- <doubt 1>
- <doubt 2>
- <doubt 3>

CLOSING ARGUMENT:
<why the jury must acquit — decisive and confident>

DEFENSE CONFIDENCE (in acquittal): <integer 0-100>"""


def run_defense(state: dict) -> dict:
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

PROSECUTION'S ARGUMENT TO CHALLENGE:
{state['prosecution_argument']}

Build the defense argument."""

    resp = llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=prompt)])
    return {"defense_argument": resp.content.strip()}