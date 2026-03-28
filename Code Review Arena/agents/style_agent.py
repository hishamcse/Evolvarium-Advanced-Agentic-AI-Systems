"""Style reviewer — naming, readability, code structure, documentation."""
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from config import OLLAMA_BASE_URL, OLLAMA_MODEL, TEMPERATURE
from state import ReviewState

SYSTEM_PROMPT = """You are a senior engineer focused on code quality and maintainability.
Review the provided code exclusively for STYLE and READABILITY issues.

Focus on:
- Naming clarity (variables, functions, classes)
- Function/method length and single responsibility
- Code duplication that should be extracted
- Missing or misleading comments/docstrings
- Inconsistent formatting or conventions
- Magic numbers or unexplained constants

Output format (strict):
SCORE: <integer 0-10 where 10 = excellent style>
ISSUES:
- [HIGH/MEDIUM/LOW] <concise issue description> (line ~N if known)
RECOMMENDATION:
<1-2 sentence refactor summary>

If no issues found, write ISSUES: None"""


def build_prompt(state: ReviewState) -> str:
    return f"""Language: {state['language']}
Structure: {state.get('ast_summary', 'N/A')}

Code:
```
{state['code']}
```"""


def run_style_review(state: ReviewState) -> dict:
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
        "style_review": text,
        "style_score": score,
    }


def _extract_score(text: str) -> float:
    for line in text.splitlines():
        if line.upper().startswith("SCORE:"):
            try:
                return float(line.split(":", 1)[1].strip().split()[0])
            except (ValueError, IndexError):
                pass
    return 5.0
