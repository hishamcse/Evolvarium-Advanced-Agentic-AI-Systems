from llm.model import get_llm
from agents.mutation_strategies import STRATEGIES
import json
import random


class MutateAgent:
    def __init__(self):
        self.llm = get_llm()

    def mutate(self, code: str, n_variants: int = 3) -> list[dict]:
        # pick distinct strategies
        chosen = random.sample(STRATEGIES, k=min(n_variants, len(STRATEGIES)))

        variants = []

        for strategy in chosen:
            prompt = f"""
You are an expert software engineer.

Apply the following transformation strategy to the code:

STRATEGY:
{strategy}

RULES:
- Keep functionality correct
- Make meaningful improvements
- Do NOT explain anything
- Return ONLY JSON

FORMAT:
{{
  "strategy": "{strategy}",
  "code": "improved code"
}}

CODE:
{code}
"""

            response = self.llm.invoke(prompt)
            text = response.content

            parsed = self._parse(text, strategy)
            variants.append(parsed)

        return variants

    def _parse(self, text: str, strategy: str):
        try:
            data = json.loads(text)
            return {
                "strategy": data.get("strategy", strategy),
                "code": data.get("code", "")
            }
        except:
            return {
                "strategy": strategy,
                "code": text.strip()
            }
