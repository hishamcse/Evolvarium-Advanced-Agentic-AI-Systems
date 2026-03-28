"""Security reviewer — finds vulnerabilities, injection risks, unsafe patterns."""
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from config import OLLAMA_BASE_URL, OLLAMA_MODEL, TEMPERATURE
from state import ReviewState

SYSTEM_PROMPT = """You are a senior application security engineer.
Review the provided code exclusively for SECURITY issues.

Focus on:
- Injection vulnerabilities (SQL, command, XSS, path traversal)
- Hardcoded secrets, API keys, passwords
- Insecure deserialization or eval usage
- Unsafe random number generation for crypto
- Missing input validation or sanitization
- Dangerous imports or subprocess usage

Output format (strict):
SCORE: <integer 0-10 where 10 = perfectly secure>
ISSUES:
- [CRITICAL/HIGH/MEDIUM/LOW] <concise issue description> (line ~N if known)
RECOMMENDATION:
<1-2 sentence fix summary>

If no issues found, write ISSUES: None"""


def build_prompt(state: ReviewState) -> str:
    return f"""Language: {state['language']}
Lint output: {state.get('lint_output', 'N/A')}

Code:
```
{state['code']}
```"""


def run_security_review(state: ReviewState) -> dict:
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
        "security_review": text,
        "security_score": score,
    }


def _extract_score(text: str) -> float:
    for line in text.splitlines():
        if line.upper().startswith("SCORE:"):
            try:
                return float(line.split(":", 1)[1].strip().split()[0])
            except (ValueError, IndexError):
                pass
    return 5.0
