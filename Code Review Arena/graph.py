"""
LangGraph graph for Code Review Arena.
Architecture: parallel fan-out + aggregator
"""
import json
import re
import uuid

from config import (
    MEMORY_DIR, OLLAMA_BASE_URL, OLLAMA_MODEL, SCORE_WEIGHTS,
)
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from agents.logic_agent import run_logic_review
from agents.performance_agent import run_performance_review
from agents.security_agent import run_security_review
from agents.style_agent import run_style_review

# Import MCP tool logic directly — avoids async subprocess overhead
from mcp_server import (
    _detect_language,
    _lint_python,
    _parse_ast,
    _count_complexity,
)
from state import ReviewState


# ── Orchestrator node ─────────────────────────────────────────────────────────

def orchestrator_node(state: ReviewState) -> dict:
    code = state["code"]
    filename = state.get("filename") or ""

    lang = _detect_language(code, filename)
    lint = ""
    ast_summary = ""

    if lang == "python":
        lint = _lint_python(code)
        ast_summary = _parse_ast(code)
    else:
        complexity = _count_complexity(code)
        ast_summary = f"Complexity indicators: {json.dumps(complexity)}"

    return {
        "session_id": state.get("session_id") or uuid.uuid4().hex[:10],
        "language": lang or "unknown",
        "lint_output": lint,
        "ast_summary": ast_summary,
        "scores": {},
        "error": None,
    }


# ── Parallel reviewer nodes ───────────────────────────────────────────────────

def security_node(state: ReviewState) -> dict:
    return run_security_review(state)


def performance_node(state: ReviewState) -> dict:
    return run_performance_review(state)


def logic_node(state: ReviewState) -> dict:
    return run_logic_review(state)


def style_node(state: ReviewState) -> dict:
    return run_style_review(state)


# ── Aggregator node ───────────────────────────────────────────────────────────

def aggregator_node(state: ReviewState) -> dict:
    scores = {
        "security": state.get("security_score", 5.0),
        "performance": state.get("performance_score", 5.0),
        "logic": state.get("logic_score", 5.0),
        "style": state.get("style_score", 5.0),
    }

    # Weighted overall score
    overall = sum(
        scores.get(role, 5.0) * weight
        for role, weight in SCORE_WEIGHTS.items()
    )

    # Extract top issues from all reviews
    top_issues = []
    reviews = {
        "security": state.get("security_review", ""),
        "performance": state.get("performance_review", ""),
        "logic": state.get("logic_review", ""),
        "style": state.get("style_review", ""),
    }
    for role, text in reviews.items():
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("- ["):
                severity = re.findall(r"\[(.*?)\]", line)
                sev = severity[0] if severity else "LOW"
                desc = re.sub(r"\[.*?\]\s*", "", line.lstrip("- ")).strip()
                top_issues.append({"role": role, "severity": sev, "description": desc})

    # Sort by severity
    sev_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    top_issues.sort(key=lambda x: sev_order.get(x["severity"], 4))

    # Build final report with LLM
    llm = ChatOpenAI(
        base_url=OLLAMA_BASE_URL, api_key="ollama",
        model=OLLAMA_MODEL, temperature=0.2,
    )
    issues_text = "\n".join(
        f"[{i['severity']}] ({i['role']}) {i['description']}"
        for i in top_issues[:10]
    )
    prompt = f"""You are a lead engineer writing a final code review summary.
Overall score: {overall:.1f}/10
Top issues found:
{issues_text if issues_text else 'None'}

Language: {state.get('language')}

Write a 3-sentence executive summary of this code's quality, the most important risk, and one clear next step. Be direct and specific."""

    response = llm.invoke([HumanMessage(content=prompt)])
    summary = response.content.strip()

    # Build markdown final report
    final_report = _build_report(state, scores, overall, top_issues, summary)

    # Persist session
    _save_session(state, scores, overall, top_issues, summary)

    return {
        "overall_score": round(overall, 2),
        "top_issues": top_issues,
        "summary": summary,
        "final_report": final_report,
    }


def _build_report(state, scores, overall, top_issues, summary) -> str:
    lines = [
        f"# Code Review — {state.get('language', '').upper()} · Score {overall:.1f}/10",
        "",
        f"**Summary:** {summary}",
        "",
        "## Scores by dimension",
        f"- Security: {scores.get('security', 'N/A')}/10",
        f"- Performance: {scores.get('performance', 'N/A')}/10",
        f"- Logic: {scores.get('logic', 'N/A')}/10",
        f"- Style: {scores.get('style', 'N/A')}/10",
        "",
        "## Top issues",
    ]
    if top_issues:
        for issue in top_issues[:10]:
            lines.append(f"- **[{issue['severity']}]** `{issue['role']}` — {issue['description']}")
    else:
        lines.append("- No issues found.")

    lines += ["", "## Detailed reviews", ""]
    for role in ["security", "performance", "logic", "style"]:
        key = f"{role}_review"
        lines.append(f"### {role.capitalize()}")
        lines.append(state.get(key, "No review."))
        lines.append("")

    return "\n".join(lines)


def _save_session(state, scores, overall, top_issues, summary):
    sid = state.get("session_id", "unknown")
    data = {
        "session_id": sid,
        "language": state.get("language"),
        "overall_score": round(overall, 2),
        "scores": scores,
        "top_issues": top_issues[:10],
        "summary": summary,
        "code_snippet": state.get("code", "")[:200],
    }
    path = MEMORY_DIR / f"{sid}.json"
    path.write_text(json.dumps(data, indent=2))


# ── Build the graph ───────────────────────────────────────────────────────────

def build_graph():
    g = StateGraph(ReviewState)

    g.add_node("orchestrator", orchestrator_node)
    g.add_node("security", security_node)
    g.add_node("performance", performance_node)
    g.add_node("logic", logic_node)
    g.add_node("style", style_node)
    g.add_node("aggregator", aggregator_node)

    g.add_edge(START, "orchestrator")

    # Fan out to all 4 reviewers in parallel
    for reviewer in ["security", "performance", "logic", "style"]:
        g.add_edge("orchestrator", reviewer)
        g.add_edge(reviewer, "aggregator")

    g.add_edge("aggregator", END)

    return g.compile()


# ── Public entrypoint ─────────────────────────────────────────────────────────

class CodeReviewEngine:
    def __init__(self):
        self.graph = build_graph()

    def review(self, code: str, filename: str = "") -> ReviewState:
        initial: ReviewState = {
            "session_id": "",
            "code": code,
            "filename": filename,
            "language": "",
            "lint_output": "",
            "ast_summary": "",
            "security_review": "",
            "performance_review": "",
            "logic_review": "",
            "style_review": "",
            "overall_score": 0.0,
            "summary": "",
            "top_issues": [],
            "final_report": "",
            "error": None,
        }
        return self.graph.invoke(initial)

    def load_session(self, session_id: str) -> dict | None:
        path = MEMORY_DIR / f"{session_id}.json"
        if path.exists():
            return json.loads(path.read_text())
        return None

    def list_sessions(self) -> list[dict]:
        sessions = []
        for p in sorted(MEMORY_DIR.glob("*.json"), reverse=True)[:20]:
            try:
                data = json.loads(p.read_text())
                sessions.append({
                    "id": data.get("session_id"),
                    "language": data.get("language"),
                    "score": data.get("overall_score"),
                    "summary": data.get("summary", "")[:80],
                })
            except Exception:
                pass
        return sessions