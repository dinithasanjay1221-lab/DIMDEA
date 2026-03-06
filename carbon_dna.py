"""
carbon_dna.py

DIMDEA - Carbon Emission Intelligence System
Module: CarbonDNA

Purpose:
Generate a unique Carbon Emission Profile (Carbon DNA)
for an organization or city based on sector emissions.
"""

from typing import Dict, Any


class CarbonDNA:
    """
    CarbonDNA class generates a structured carbon emission profile.

    Features:
    - Calculates total emissions
    - Computes sector-wise percentages
    - Compares against baseline
    - Classifies risk level
    - Generates sustainability score (0–100)
    - Provides improvement suggestions
    """

    # Default sector list
    REQUIRED_SECTORS = [
        "transportation",
        "energy",
        "industry",
        "waste",
        "renewable"
    ]

    # Emission risk thresholds (example baseline values)
    RISK_THRESHOLDS = {
        "Low": 0.5,
        "Moderate": 1.0,
        "High": 1.5,
        "Critical": float("inf")
    }

    def __init__(self, emissions_data: Dict[str, float], baseline: float):
        """
        Initialize CarbonDNA object.

        :param emissions_data: Dictionary with sector emission values (in tons CO2)
        :param baseline: Baseline emission value for comparison
        """
        self._validate_input(emissions_data, baseline)
        self.emissions_data = emissions_data
        self.baseline = baseline

    # -------------------------
    # Input Validation
    # -------------------------

    def _validate_input(self, emissions_data: Dict[str, float], baseline: float) -> None:
        """
        Validate input data.
        """

        if not isinstance(emissions_data, dict):
            raise TypeError("Emissions data must be a dictionary.")

        for sector in self.REQUIRED_SECTORS:
            if sector not in emissions_data:
                raise ValueError(f"Missing required sector: {sector}")

            if not isinstance(emissions_data[sector], (int, float)):
                raise TypeError(f"Emission value for {sector} must be numeric.")

            if emissions_data[sector] < 0:
                raise ValueError(f"Emission value for {sector} cannot be negative.")

        if not isinstance(baseline, (int, float)):
            raise TypeError("Baseline must be numeric.")

        if baseline <= 0:
            raise ValueError("Baseline must be greater than zero.")

    # -------------------------
    # Core Calculations
    # -------------------------

    def calculate_total_emissions(self) -> float:
        """Calculate total carbon emissions."""
        return sum(self.emissions_data.values())

    def calculate_sector_percentages(self) -> Dict[str, float]:
        """Calculate percentage contribution of each sector."""
        total = self.calculate_total_emissions()
        if total == 0:
            return {sector: 0.0 for sector in self.REQUIRED_SECTORS}

        return {
            sector: round((value / total) * 100, 2)
            for sector, value in self.emissions_data.items()
        }

    def classify_risk_level(self) -> str:
        """
        Classify emission risk level based on baseline comparison.
        """
        total = self.calculate_total_emissions()
        ratio = total / self.baseline

        for level, threshold in self.RISK_THRESHOLDS.items():
            if ratio <= threshold:
                return level

        return "Critical"

    def calculate_sustainability_score(self) -> float:
        """
        Calculate sustainability score (0–100).
        Higher emissions reduce score.
        """
        total = self.calculate_total_emissions()
        score = 100 - ((total / self.baseline) * 100)

        # Bound the score between 0 and 100
        return max(0, min(100, round(score, 2)))

    def generate_suggestions(self) -> list:
        """
        Generate basic improvement suggestions based on dominant sector.
        """
        percentages = self.calculate_sector_percentages()
        dominant_sector = max(percentages, key=percentages.get)

        suggestions = {
            "transportation": "Improve public transport usage and adopt electric vehicles.",
            "energy": "Switch to renewable energy sources and improve energy efficiency.",
            "industry": "Optimize industrial processes and adopt cleaner technologies.",
            "waste": "Implement recycling programs and reduce landfill dependency.",
            "renewable": "Increase renewable energy share to offset emissions."
        }

        return [
            f"Dominant emission sector: {dominant_sector}",
            suggestions.get(dominant_sector, "Improve sustainability practices.")
        ]

    # -------------------------
    # Carbon DNA Profile
    # -------------------------

    def generate_profile(self) -> Dict[str, Any]:
        """
        Generate complete Carbon DNA profile.
        """
        return {
            "total_emissions": round(self.calculate_total_emissions(), 2),
            "sector_breakdown_percent": self.calculate_sector_percentages(),
            "risk_level": self.classify_risk_level(),
            "carbon_dna_score": self.calculate_sustainability_score(),
            "suggestions": self.generate_suggestions()
        }


# -------------------------
# Example Test Execution
# -------------------------

if __name__ == "__main__":
    # Example structured input (tons CO2)
    sample_data = {
        "transportation": 1200,
        "energy": 2000,
        "industry": 1500,
        "waste": 500,
        "renewable": 300
    }

    baseline_value = 6000  # Example baseline emission

    try:
        carbon_dna = CarbonDNA(sample_data, baseline_value)
        profile = carbon_dna.generate_profile()

        print("\n===== DIMDEA Carbon DNA Profile =====")
        for key, value in profile.items():
            print(f"{key}: {value}")

    except Exception as e:
        print(f"Error: {e}")