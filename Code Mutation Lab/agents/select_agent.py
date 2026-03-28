class SelectAgent:
    def select(self, variants: list[dict]) -> dict:
        if not variants:
            return {
                "code": "",
                "score": 0.0,
                "feedback": "No variants available"
            }

        # Select highest scoring variant
        best = max(variants, key=lambda x: x.get("score", 0))

        return best
