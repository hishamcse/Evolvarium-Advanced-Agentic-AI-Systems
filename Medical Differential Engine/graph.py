"""
Medical Differential Engine — LangGraph graph
Architecture: Cascading Bayesian Refinement

Flow:
  bootstrap → symptom_parser → prior_scorer → rare_probe → comorbidity_mapper
           → evidence_weigher → differential_ranker → persist → END

Each layer receives the full state (including all prior layers' outputs)
and writes its own slot. Probabilities cascade and update downstream.
"""
import json
import uuid

from langgraph.graph import END, START, StateGraph

from agents.symptom_parser_agent     import run_symptom_parser
from agents.prior_scorer_agent       import run_prior_scorer
from agents.rare_disease_probe_agent import run_rare_probe
from agents.comorbidity_mapper_agent import run_comorbidity_mapper
from agents.evidence_weigher_agent   import run_evidence_weigher
from agents.differential_ranker_agent import run_differential_ranker

from config import MEMORY_DIR
from state  import EngineState


# ── nodes ──────────────────────────────────────────────────────────────────────

def bootstrap_node(state: EngineState) -> dict:
    return {
        "case_id": state.get("case_id") or uuid.uuid4().hex[:10],
        "error":   None,
    }

def symptom_parser_node(state: EngineState) -> dict:
    return run_symptom_parser(state)

def prior_scorer_node(state: EngineState) -> dict:
    return run_prior_scorer(state)

def rare_probe_node(state: EngineState) -> dict:
    return run_rare_probe(state)

def comorbidity_node(state: EngineState) -> dict:
    return run_comorbidity_mapper(state)

def evidence_weigher_node(state: EngineState) -> dict:
    return run_evidence_weigher(state)

def ranker_node(state: EngineState) -> dict:
    return run_differential_ranker(state)

def persist_node(state: EngineState) -> dict:
    data = {k: state.get(k) for k in [
        "case_id", "patient_age", "patient_sex",
        "chief_complaint", "symptoms", "vitals", "history", "exam_findings",
        "parsed_features", "prior_candidates", "refined_candidates",
        "comorbidity_flags", "weighted_candidates",
        "differential", "red_flags", "workup_plan",
        "disposition", "clinical_summary", "probability_narrative",
    ]}
    path = MEMORY_DIR / f"{state['case_id']}.json"
    path.write_text(json.dumps(data, indent=2))
    return {}


# ── graph builder ───────────────────────────────────────────────────────────────

def build_graph():
    g = StateGraph(EngineState)

    g.add_node("bootstrap",          bootstrap_node)
    g.add_node("symptom_parser",     symptom_parser_node)
    g.add_node("prior_scorer",       prior_scorer_node)
    g.add_node("rare_probe",         rare_probe_node)
    g.add_node("comorbidity_mapper", comorbidity_node)
    g.add_node("evidence_weigher",   evidence_weigher_node)
    g.add_node("ranker",             ranker_node)
    g.add_node("persist",            persist_node)

    # Sequential cascade — each layer feeds the next
    g.add_edge(START,                "bootstrap")
    g.add_edge("bootstrap",          "symptom_parser")
    g.add_edge("symptom_parser",     "prior_scorer")
    g.add_edge("prior_scorer",       "rare_probe")
    g.add_edge("rare_probe",         "comorbidity_mapper")
    g.add_edge("comorbidity_mapper", "evidence_weigher")
    g.add_edge("evidence_weigher",   "ranker")
    g.add_edge("ranker",             "persist")
    g.add_edge("persist",            END)

    return g.compile()


# ── public engine ───────────────────────────────────────────────────────────────

class DifferentialEngine:
    def __init__(self):
        self.graph = build_graph()

    def analyse(
        self,
        patient_age: str,
        patient_sex: str,
        chief_complaint: str,
        symptoms: str,
        vitals: str,
        history: str,
        exam_findings: str,
    ) -> EngineState:
        initial: EngineState = {
            "case_id":          "",
            "patient_age":      patient_age,
            "patient_sex":      patient_sex,
            "chief_complaint":  chief_complaint,
            "symptoms":         symptoms,
            "vitals":           vitals,
            "history":          history,
            "exam_findings":    exam_findings,

            "parsed_features":   {},
            "prior_candidates":  [],
            "refined_candidates": [],
            "comorbidity_flags": [],
            "weighted_candidates": [],

            "differential":     [],
            "red_flags":        [],
            "workup_plan":      [],
            "disposition":      "",
            "clinical_summary": "",
            "probability_narrative": "",
            "error":            None,
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

    def load_case(self, case_id: str) -> dict | None:
        path = MEMORY_DIR / f"{case_id}.json"
        if path.exists():
            return json.loads(path.read_text())
        return None