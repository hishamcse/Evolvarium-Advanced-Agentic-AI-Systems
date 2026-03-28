from llm.model import get_llm
import json


class SimplicityAgent:
    def __init__(self):
        self.llm = get_llm()

    def evaluate(self, code: str) -> dict:
        prompt = f"""
Evaluate how SIMPLE and CLEAN this code is.

Return ONLY JSON:
{{
  "score": 0-10,
  "reason": "short reason"
}}

CODE:
{code}
"""

        res = self.llm.invoke(prompt)
        return self._parse(res.content)

    def _parse(self, text: str):
        try:
            return json.loads(text)
        except:
            return {"score": 5.0, "reason": "fallback"}
