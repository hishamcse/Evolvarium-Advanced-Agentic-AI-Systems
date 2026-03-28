"""Performance reviewer — complexity, inefficient patterns, memory issues."""
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from config import OLLAMA_BASE_URL, OLLAMA_MODEL, TEMPERATURE
from state import ReviewState

SYSTEM_PROMPT = """You are a performance engineering expert.
Review the provided code exclusively for PERFORMANCE issues.

Focus on:
- Algorithmic complexity (O(n²) or worse where better exists)
- Unnecessary loops, redundant computation
- Memory leaks or large object retention
- N+1 query patterns or repeated I/O in loops
- Missing caching of expensive computations
- Inefficient data structures for the use case

Output format (strict):
SCORE: <integer 0-10 where 10 = highly optimized>
ISSUES:
- [HIGH/MEDIUM/LOW] <concise issue description> (line ~N if known)
RECOMMENDATION:
<1-2 sentence fix summary>

If no issues found, write ISSUES: None"""


def build_prompt(state: ReviewState) -> str:
    complexity = state.get("ast_summary", "N/A")
    return f"""Language: {state['language']}
AST / complexity info: {complexity}

Code:
```
{state['code']}
```"""


def run_performance_review(state: ReviewState) -> dict:
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
        "performance_review": text,
        "performance_score": score,
    }


def _extract_score(text: str) -> float:
    for line in text.splitlines():
        if line.upper().startswith("SCORE:"):
            try:
                return float(line.split(":", 1)[1].strip().split()[0])
            except (ValueError, IndexError):
                pass
    return 5.0
