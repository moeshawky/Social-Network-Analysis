from typing import Dict, Any

class ConfidenceScorer:
    WEIGHTS = {
        "name_similarity": 0.30,
        "handle_similarity": 0.15,
        "company_match": 0.20,
        "title_match": 0.10,
        "mutual_connections": 0.25
    }

    def score(self, signals: Dict[str, float]) -> float:
        """
        Weighted confidence score.
        Each signal is 0.0-1.0, output is weighted average.
        """
        total_weight = 0.0
        weighted_sum = 0.0

        for key, value in signals.items():
            if key in self.WEIGHTS:
                weight = self.WEIGHTS[key]
                weighted_sum += value * weight
                total_weight += weight
            else:
                # Handle unexpected signals if necessary, or ignore
                pass

        if total_weight == 0:
            return 0.0

        return weighted_sum / total_weight

    def explain(self, signals: Dict[str, float]) -> Dict[str, Any]:
        """
        Return human-readable explanation of the score.
        """
        final_score = self.score(signals)
        explanation = {
            "overall_confidence": final_score,
            "signals": {}
        }

        if final_score >= 0.90:
            explanation["tier"] = "auto_merge"
        elif final_score >= 0.50:
            explanation["tier"] = "flag_for_review"
        else:
            explanation["tier"] = "no_match"

        for key, value in signals.items():
            if key in self.WEIGHTS:
                weight = self.WEIGHTS[key]
                contrib = value * weight
                # Generate a simple note based on score
                if value > 0.9:
                    note = "Strong match"
                elif value > 0.5:
                    note = "Partial match"
                else:
                    note = "Weak match"

                explanation["signals"][key] = {
                    "score": value,
                    "weight": weight,
                    "contribution": contrib,
                    "note": note
                }

        return explanation
