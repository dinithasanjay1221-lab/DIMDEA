"""
carbon_dna.py

DIMDEA - Carbon Emission Intelligence System
Module: CarbonDNA

Purpose:
Generate a unique Carbon Emission Profile (Carbon DNA)
for an organization or city based on sector emissions.

Enhancements:
- Accepts dictionary or Pandas DataFrame input
- Returns frontend-ready dictionary profile
- Preserves all original logic
"""

from typing import Dict, Any, Union
import pandas as pd


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

    def __init__(self, emissions_data: Union[Dict[str, float], pd.DataFrame], baseline: float):
        """
        Initialize CarbonDNA object.

        :param emissions_data: Dictionary or DataFrame with sector emission values (in tons CO2)
                               If DataFrame, expected columns: 'sector', 'emission'
        :param baseline: Baseline emission value for comparison
        """
        self.emissions_data = self._prepare_input(emissions_data)
        self.baseline = baseline
        self._validate_input(self.emissions_data, baseline)

    # -------------------------
    # Input Preparation
    # -------------------------
    def _prepare_input(self, data: Union[Dict[str, float], pd.DataFrame]) -> Dict[str, float]:
        """
        Convert DataFrame to dictionary if needed and validate sectors.
        """
        if isinstance(data, pd.DataFrame):
            required_cols = {"sector", "emission"}
            if not required_cols.issubset(data.columns):
                raise ValueError(f"DataFrame must contain columns: {required_cols}")
            return {str(row["sector"]): float(row["emission"]) for _, row in data.iterrows()}
        elif isinstance(data, dict):
            return {str(k): float(v) for k, v in data.items()}
        else:
            raise TypeError("Emissions data must be a dictionary or Pandas DataFrame.")

    # -------------------------
    # Input Validation
    # -------------------------
    def _validate_input(self, emissions_data: Dict[str, float], baseline: float) -> None:
        """
        Validate input data.
        """
        for sector in self.REQUIRED_SECTORS:
            if sector not in emissions_data:
                raise ValueError(f"Missing required sector: {sector}")

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
        return sum(self.emissions_data.values())

    def calculate_sector_percentages(self) -> Dict[str, float]:
        total = self.calculate_total_emissions()
        if total == 0:
            return {sector: 0.0 for sector in self.REQUIRED_SECTORS}
        return {sector: round((value / total) * 100, 2) for sector, value in self.emissions_data.items()}

    def classify_risk_level(self) -> str:
        total = self.calculate_total_emissions()
        ratio = total / self.baseline
        for level, threshold in self.RISK_THRESHOLDS.items():
            if ratio <= threshold:
                return level
        return "Critical"

    def calculate_sustainability_score(self) -> float:
        total = self.calculate_total_emissions()
        score = 100 - ((total / self.baseline) * 100)
        return max(0, min(100, round(score, 2)))

    def generate_suggestions(self) -> list:
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
        return {
            "total_emissions": round(self.calculate_total_emissions(), 2),
            "sector_breakdown_percent": self.calculate_sector_percentages(),
            "risk_level": self.classify_risk_level(),
            "carbon_dna_score": self.calculate_sustainability_score(),
            "suggestions": self.generate_suggestions()
        }


# -------------------------
# Example Standalone Execution
# -------------------------
if __name__ == "__main__":
    import pandas as pd

    sample_data_dict = {
        "transportation": 1200,
        "energy": 2000,
        "industry": 1500,
        "waste": 500,
        "renewable": 300
    }

    sample_data_df = pd.DataFrame({
        "sector": ["transportation", "energy", "industry", "waste", "renewable"],
        "emission": [1200, 2000, 1500, 500, 300]
    })

    baseline_value = 6000

    # Using dictionary input
    profile1 = CarbonDNA(sample_data_dict, baseline_value).generate_profile()
    print("Dictionary Input Profile:", profile1)

    # Using DataFrame input
    profile2 = CarbonDNA(sample_data_df, baseline_value).generate_profile()
    print("DataFrame Input Profile:", profile2)