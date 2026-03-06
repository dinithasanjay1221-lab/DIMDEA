"""
Sustainability Score Engine
---------------------------
This module calculates sustainability scores based on:
- Carbon emissions
- Energy efficiency
- Waste management
- Water usage
- Renewable energy usage

No authentication logic included.
"""

from typing import Dict


class SustainabilityScoreEngine:
    """
    Calculates sustainability score using weighted metrics.
    """

    def __init__(
        self,
        weight_emissions: float = 0.30,
        weight_energy: float = 0.20,
        weight_waste: float = 0.15,
        weight_water: float = 0.15,
        weight_renewable: float = 0.20,
    ):
        total_weight = (
            weight_emissions
            + weight_energy
            + weight_waste
            + weight_water
            + weight_renewable
        )

        if round(total_weight, 2) != 1.0:
            raise ValueError("Total weights must sum to 1.0")

        self.weights = {
            "emissions": weight_emissions,
            "energy": weight_energy,
            "waste": weight_waste,
            "water": weight_water,
            "renewable": weight_renewable,
        }

    # -----------------------------
    # Normalization Functions
    # -----------------------------

    @staticmethod
    def normalize_inverse(value: float, max_value: float) -> float:
        """
        Lower is better (e.g., emissions, water usage)
        """
        if max_value <= 0:
            raise ValueError("max_value must be greater than 0")

        score = max(0.0, 1 - (value / max_value))
        return min(score, 1.0)

    @staticmethod
    def normalize_direct(value: float, max_value: float) -> float:
        """
        Higher is better (e.g., renewable usage, efficiency)
        """
        if max_value <= 0:
            raise ValueError("max_value must be greater than 0")

        score = value / max_value
        return min(max(score, 0.0), 1.0)

    # -----------------------------
    # Core Score Calculation
    # -----------------------------

    def calculate_score(self, metrics: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate sustainability score.
        Required metrics:
            emissions
            energy_efficiency
            waste_recycling
            water_usage
            renewable_usage
        """

        required_fields = [
            "emissions",
            "energy_efficiency",
            "waste_recycling",
            "water_usage",
            "renewable_usage",
        ]

        for field in required_fields:
            if field not in metrics:
                raise ValueError(f"Missing required metric: {field}")

        # Normalize metrics
        normalized = {
            "emissions": self.normalize_inverse(metrics["emissions"], 1000),
            "energy": self.normalize_direct(metrics["energy_efficiency"], 100),
            "waste": self.normalize_direct(metrics["waste_recycling"], 100),
            "water": self.normalize_inverse(metrics["water_usage"], 500),
            "renewable": self.normalize_direct(metrics["renewable_usage"], 100),
        }

        # Weighted score calculation
        final_score = 0.0
        for key in normalized:
            final_score += normalized[key] * self.weights[key]

        # Convert to 0–100 scale
        final_score_percentage = round(final_score * 100, 2)

        return {
            "normalized_metrics": normalized,
            "sustainability_score": final_score_percentage,
            "rating": self._get_rating(final_score_percentage),
        }

    @staticmethod
    def _get_rating(score: float) -> str:
        if score >= 85:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 50:
            return "Moderate"
        else:
            return "Needs Improvement"


# -----------------------------
# Example Usage (Safe to Run)
# -----------------------------
if __name__ == "__main__":
    engine = SustainabilityScoreEngine()

    sample_data = {
        "emissions": 400,           # tons CO2
        "energy_efficiency": 78,    # %
        "waste_recycling": 65,      # %
        "water_usage": 200,         # cubic meters
        "renewable_usage": 55,      # %
    }

    result = engine.calculate_score(sample_data)

    print("\nSUSTAINABILITY SCORE RESULT")
    print("----------------------------")
    print("Score:", result["sustainability_score"])
    print("Rating:", result["rating"])
    print("Normalized Metrics:", result["normalized_metrics"])