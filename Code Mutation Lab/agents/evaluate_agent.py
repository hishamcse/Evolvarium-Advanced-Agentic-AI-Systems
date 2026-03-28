from agents.evaluators.performance_agent import PerformanceAgent
from agents.evaluators.readability_agent import ReadabilityAgent
from agents.evaluators.simplicity_agent import SimplicityAgent


class EvaluateAgent:
    def __init__(self):
        self.performance = PerformanceAgent()
        self.readability = ReadabilityAgent()
        self.simplicity = SimplicityAgent()

    def evaluate(self, code: str) -> dict:
        p = self.performance.evaluate(code)
        r = self.readability.evaluate(code)
        s = self.simplicity.evaluate(code)

        final_score = round(
            (p["score"] + r["score"] + s["score"]) / 3, 2
        )

        return {
            "score": final_score,
            "feedback": (
                f"Performance: {p['reason']} | "
                f"Readability: {r['reason']} | "
                f"Simplicity: {s['reason']}"
            ),
            "breakdown": {
                "performance": p["score"],
                "readability": r["score"],
                "simplicity": s["score"]
            }
        }
