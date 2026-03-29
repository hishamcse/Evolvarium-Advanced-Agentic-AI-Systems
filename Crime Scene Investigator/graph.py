"""
Crime Scene Investigator — LangGraph graph
Architecture: adversarial debate + jury vote

Flow:
  bootstrap → forensics → [prosecution ‖ defense] → judge → persist
"""
import json
import uuid

from langgraph.graph import END, START, StateGraph

from agents.forensics_agent  import run_forensics
from agents.prosecutor_agent import run_prosecution
from agents.defense_agent    import run_defense
from agents.judge_agent      import run_judge
from config import MEMORY_DIR
from state  import CaseState


# ── nodes ─────────────────────────────────────────────────────────────────────

def bootstrap_node(state: CaseState) -> dict:
    return {
        "case_id": state.get("case_id") or uuid.uuid4().hex[:10],
        "error":   None,
    }


def forensics_node(state: CaseState) -> dict:
    return run_forensics(state)


def prosecution_node(state: CaseState) -> dict:
    return run_prosecution(state)


def defense_node(state: CaseState) -> dict:
    return run_defense(state)


def judge_node(state: CaseState) -> dict:
    return run_judge(state)


def persist_node(state: CaseState) -> dict:
    data = {k: state.get(k) for k in [
        "case_id", "case_title", "verdict", "confidence",
        "final_summary", "key_evidence", "reasonable_doubts",
    ]}
    path = MEMORY_DIR / f"{state['case_id']}.json"
    path.write_text(json.dumps(data, indent=2))
    return {}


# ── graph builder ──────────────────────────────────────────────────────────────

def build_graph():
    g = StateGraph(CaseState)

    g.add_node("bootstrap",    bootstrap_node)
    g.add_node("forensics",    forensics_node)
    g.add_node("prosecution",  prosecution_node)
    g.add_node("defense",      defense_node)
    g.add_node("judge",        judge_node)
    g.add_node("persist",      persist_node)

    g.add_edge(START,         "bootstrap")
    g.add_edge("bootstrap",   "forensics")

    # Prosecution and defense run sequentially — defense reads prosecution's arg
    g.add_edge("forensics",   "prosecution")
    g.add_edge("prosecution", "defense")
    g.add_edge("defense",     "judge")
    g.add_edge("judge",       "persist")
    g.add_edge("persist",     END)

    return g.compile()


# ── public engine ──────────────────────────────────────────────────────────────

class CSIEngine:
    def __init__(self):
        self.graph = build_graph()

    def investigate(
        self,
        case_title: str,
        case_brief: str,
        evidence_list: str,
    ) -> CaseState:
        initial: CaseState = {
            "case_id":              "",
            "case_title":           case_title,
            "case_brief":           case_brief,
            "evidence_list":        evidence_list,
            "forensics_report":     "",
            "prosecution_argument": "",
            "defense_argument":     "",
            "judge_reasoning":      "",
            "verdict":              "",
            "confidence":           0.0,
            "key_evidence":         [],
            "reasonable_doubts":    [],
            "final_summary":        "",
            "error":                None,
        }
        return self.graph.invoke(initial)

    def list_cases(self) -> list[dict]:
        cases = []
        for p in sorted(MEMORY_DIR.glob("*.json"), reverse=True)[:20]:
            try:
                d = json.loads(p.read_text())
                cases.append(d)
            except Exception:
                pass
        return cases