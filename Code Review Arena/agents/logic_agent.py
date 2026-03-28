"""Logic reviewer — bugs, edge cases, correctness issues."""
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from config import OLLAMA_BASE_URL, OLLAMA_MODEL, TEMPERATURE
from state import ReviewState

SYSTEM_PROMPT = """You are a principal software engineer focused on code correctness.
Review the provided code exclusively for LOGIC and CORRECTNESS issues.

Focus on:
- Off-by-one errors, wrong comparisons, incorrect boolean logic
- Unhandled edge cases (empty input, None/null, zero, negative values)
- Incorrect error handling or swallowed exceptions
- Race conditions or concurrency bugs
- Incorrect assumptions about data types or state
- Missing return values or unreachable code paths

Output format (strict):
SCORE: <integer 0-10 where 10 = logically correct>
ISSUES:
- [CRITICAL/HIGH/MEDIUM/LOW] <concise issue description> (line ~N if known)
RECOMMENDATION:
<1-2 sentence fix summary>

If no issues found, write ISSUES: None"""


def build_prompt(state: ReviewState) -> str:
    return f"""Language: {state['language']}
Lint: {state.get('lint_output', 'N/A')}

Code:
```
{state['code']}
```"""


def run_logic_review(state: ReviewState) -> dict:
    llm = ChatOpenAI(
        base_url=OLLAMA_BASE_URL,
        api_key="ollama",
        model=OLLAMA_MODEL,
        temperature=TEMPERATURE,
    )
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=build_prompt(state)),
    ]
    response = llm.invoke(messages)
    text = response.content

    score = _extract_score(text)
    return {
        "logic_review": text,
        "logic_score": score,
    }


def _extract_score(text: str) -> float:
    for line in text.splitlines():
        if line.upper().startswith("SCORE:"):
            try:
                return float(line.split(":", 1)[1].strip().split()[0])
            except (ValueError, IndexError):
                pass
    return 5.0
