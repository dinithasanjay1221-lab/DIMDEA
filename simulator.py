"""
simulator.py
-----------------------------------------
Emission Scenario Simulation Engine

✔ No authentication logic
✔ No API logic
✔ Pure emission modeling
✔ Self-contained
✔ Ready for Streamlit / FastAPI integration
"""

from typing import Dict, Optional
from copy import deepcopy


class EmissionSimulator:
    """
    Core engine for modeling carbon emission scenarios.
    """

    REQUIRED_KEYS = [
        "transportation",
        "energy",
        "industrial",
        "waste",
        "renewable",
        "baseline"
    ]

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(self, base_data: Dict[str, float]):
        self._validate_input(base_data)
        self.base_data = deepcopy(base_data)
        self.baseline = base_data["baseline"]

    # ==========================================================
    # PUBLIC METHOD
    # ==========================================================

    def run_simulation(
        self,
        sector_reduction: Optional[Dict[str, float]] = None,
        renewable_growth_percent: float = 0.0,
        annual_reduction_percent: float = 0.0,
        years: int = 0,
        risk_factor: float = 1.0
    ) -> Dict:
        """
        Runs full emission simulation model.
        """

        sector_reduction = sector_reduction or {}
        simulated = deepcopy(self.base_data)

        # 1️⃣ Sector Reduction
        simulated = self._apply_sector_reduction(simulated, sector_reduction)

        # 2️⃣ Renewable Growth Impact
        if renewable_growth_percent > 0:
            simulated = self._apply_renewable_growth(
                simulated, renewable_growth_percent
            )

        # 3️⃣ Risk Adjustment
        if risk_factor != 1.0:
            simulated = self._apply_risk_factor(simulated, risk_factor)

        total_before = self._calculate_total(self.base_data)
        total_after = self._calculate_total(simulated)

        emission_reduction = total_before - total_after
        improvement_percent = (
            (emission_reduction / total_before) * 100
            if total_before > 0 else 0
        )

        projection = {}
        if years > 0 and annual_reduction_percent > 0:
            projection = self._time_projection(
                simulated, years, annual_reduction_percent
            )

        risk_before = self._classify_risk(total_before)
        risk_after = self._classify_risk(total_after)

        return {
            # Core totals
            "total_before": round(total_before, 2),
            "total_after": round(total_after, 2),

            # Emission metrics
            "emission_before": round(total_before, 2),
            "emission_after": round(total_after, 2),
            "emission_reduction": round(emission_reduction, 2),
            "reduction_percent": round(improvement_percent, 2),

            # Carbon DNA
            "carbon_dna_score_before": round((total_before / self.baseline) * 100, 2),
            "carbon_dna_score_after": round((total_after / self.baseline) * 100, 2),

            # ✅ NEW REQUIRED FIELDS
            "risk_level_before": risk_before,
            "risk_level_after": risk_after,
            "sustainability_improvement_percent": round(improvement_percent, 2),

            # Detailed info
            "original_emissions": self.base_data,
            "simulated_emissions": simulated,
            "yearly_projection": projection
        }

    # ==========================================================
    # PRIVATE METHODS
    # ==========================================================

    def _apply_sector_reduction(self, data, reduction_plan):
        modified = deepcopy(data)

        for sector, percent in reduction_plan.items():
            if sector in modified and 0 <= percent <= 100:
                reduction_amount = modified[sector] * (percent / 100)
                modified[sector] = max(0, modified[sector] - reduction_amount)

        return modified

    def _apply_renewable_growth(self, data, growth_percent):
        modified = deepcopy(data)

        renewable_gain = modified["renewable"] * (growth_percent / 100)
        modified["renewable"] += renewable_gain

        fossil_sectors = ["transportation", "energy", "industrial"]

        total_fossil = sum(modified[s] for s in fossil_sectors)

        if total_fossil > 0:
            for sector in fossil_sectors:
                share = modified[sector] / total_fossil
                reduction = renewable_gain * share
                modified[sector] = max(0, modified[sector] - reduction)

        return modified

    def _apply_risk_factor(self, data, factor):
        modified = deepcopy(data)

        for sector in ["transportation", "energy", "industrial", "waste"]:
            modified[sector] *= factor

        return modified

    def _time_projection(self, data, years, annual_percent):
        projection = {}
        current = deepcopy(data)

        for year in range(1, years + 1):
            for sector in ["transportation", "energy", "industrial", "waste"]:
                reduction = current[sector] * (annual_percent / 100)
                current[sector] = max(0, current[sector] - reduction)

            projection[year] = round(self._calculate_total(current), 2)

        return projection

    def _calculate_total(self, data):
        return (
            data["transportation"]
            + data["energy"]
            + data["industrial"]
            + data["waste"]
            - data["renewable"]
        )

    def _validate_input(self, data):
        for key in self.REQUIRED_KEYS:
            if key not in data:
                raise ValueError(f"Missing key: {key}")

            if not isinstance(data[key], (int, float)):
                raise TypeError(f"{key} must be numeric")

            if data[key] < 0:
                raise ValueError(f"{key} cannot be negative")
     
    def _classify_risk(self, total_emission):
        """
        Classify risk level based on emission ratio to baseline.
        """
        if self.baseline == 0:
            return "Unknown"

        ratio = (total_emission / self.baseline) * 100

        if ratio >= 90:
            return "Severe"
        elif ratio >= 70:
            return "High"
        elif ratio >= 40:
            return "Moderate"
        else:
            return "Low"

# ==========================================================
# TEST BLOCK (Safe to Run Directly)
# ==========================================================

if __name__ == "__main__":

    sample_data = {
        "transportation": 2000,
        "energy": 3000,
        "industrial": 4000,
        "waste": 1000,
        "renewable": 500,
        "baseline": 10000
    }

    simulator = EmissionSimulator(sample_data)

    result = simulator.run_simulation(
        sector_reduction={"industrial": 20, "energy": 10},
        renewable_growth_percent=15,
        annual_reduction_percent=5,
        years=5,
        risk_factor=0.95
    )

    from pprint import pprint
    pprint(result)