"""
DIMDEA - Emission Hotspot Detection Module
-------------------------------------------
Identifies emission hotspots using analytical models.

Contains:
✔ Sector ranking
✔ Threshold-based hotspot detection
✔ Baseline deviation analysis
✔ Concentration ratio modeling
✔ Multi-sector stress detection
✔ Risk scoring

Does NOT contain:
✖ API routes
✖ UI logic
✖ Authentication
✖ Database session handling
"""

from typing import Dict, List
from copy import deepcopy


class HotspotDetector:
    """
    Analytical engine for detecting emission hotspots.
    """

    REQUIRED_FIELDS = [
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

    def __init__(self, emission_data: Dict[str, float]):
        self._validate_input(emission_data)
        self.data = deepcopy(emission_data)
        self.baseline = emission_data["baseline"]

    # ==========================================================
    # MAIN ANALYSIS METHOD
    # ==========================================================

    def analyze(self, threshold_percent: float = 25.0) -> Dict:
        """
        Perform full hotspot analysis.
        """

        ranked = self._sector_ranking_model()
        severity = self._threshold_hotspot_model(threshold_percent)
        deviation = self._baseline_deviation_model()
        contribution = self._concentration_ratio_model()
        dominant = self._dominant_sector_detection(contribution)
        multi_stress = self._multi_sector_stress_detection(severity)

        overall_risk = self._calculate_overall_risk_score(
            severity, deviation
        )

        return {
            "ranked_sectors": ranked,
            "primary_hotspot": ranked[0][0],
            "severity_levels": severity,
            "baseline_deviation_percent": deviation,
            "sector_contribution_percent": contribution,
            "dominant_sectors": dominant,
            "multi_sector_stress": multi_stress,
            "overall_risk_score": round(overall_risk, 2)
        }

    # ==========================================================
    # MODEL IMPLEMENTATIONS
    # ==========================================================

    def _sector_ranking_model(self) -> List:
        """
        Rank sectors descending by emission value.
        """
        sectors = self._emission_only_data()
        return sorted(
            sectors.items(),
            key=lambda x: x[1],
            reverse=True
        )

    def _threshold_hotspot_model(self, threshold_percent: float) -> Dict:
        """
        Flag sectors exceeding threshold percentage of total emissions.
        """
        total = self._total_emissions()
        severity = {}

        for sector, value in self._emission_only_data().items():
            percent = (value / total) * 100 if total > 0 else 0

            if percent >= threshold_percent * 1.5:
                level = "Critical"
            elif percent >= threshold_percent:
                level = "High"
            elif percent >= threshold_percent / 2:
                level = "Medium"
            else:
                level = "Low"

            severity[sector] = level

        return severity

    def _baseline_deviation_model(self) -> Dict:
        """
        Calculate deviation percentage from baseline.
        """
        deviation = {}

        for sector, value in self._emission_only_data().items():
            percent = (value / self.baseline) * 100 if self.baseline > 0 else 0
            deviation[sector] = round(percent, 2)

        return deviation

    def _concentration_ratio_model(self) -> Dict:
        """
        Calculate sector contribution percentage.
        """
        total = self._total_emissions()
        contribution = {}

        for sector, value in self._emission_only_data().items():
            percent = (value / total) * 100 if total > 0 else 0
            contribution[sector] = round(percent, 2)

        return contribution

    def _dominant_sector_detection(self, contribution: Dict) -> List:
        """
        Identify sectors contributing more than 40%.
        """
        return [
            sector for sector, percent in contribution.items()
            if percent > 40
        ]

    def _multi_sector_stress_detection(self, severity: Dict) -> bool:
        """
        Detect if two or more sectors are High or Critical.
        """
        high_count = sum(
            1 for level in severity.values()
            if level in ["High", "Critical"]
        )
        return high_count >= 2

    def _calculate_overall_risk_score(self, severity: Dict, deviation: Dict) -> float:
        """
        Compute aggregated risk score.
        """
        severity_weight = {
            "Low": 1,
            "Medium": 2,
            "High": 3,
            "Critical": 4
        }

        severity_score = sum(
            severity_weight[level]
            for level in severity.values()
        )

        deviation_score = sum(deviation.values()) / len(deviation)

        return severity_score + deviation_score

    # ==========================================================
    # UTILITIES
    # ==========================================================

    def _emission_only_data(self) -> Dict:
        """
        Return emission sectors excluding baseline.
        """
        return {
            k: v for k, v in self.data.items()
            if k != "baseline"
        }

    def _total_emissions(self) -> float:
        """
        Calculate total emissions excluding baseline.
        """
        return sum(self._emission_only_data().values())

    def _validate_input(self, data: Dict):
        """
        Validate required fields and numeric types.
        """
        for field in self.REQUIRED_FIELDS:
            if field not in data:
                raise ValueError(f"Missing field: {field}")
            if not isinstance(data[field], (int, float)):
                raise TypeError(f"{field} must be numeric")
            if data[field] < 0:
                raise ValueError(f"{field} cannot be negative")


# ==========================================================
# TEST BLOCK
# ==========================================================

if __name__ == "__main__":

    sample_data = {
        "transportation": 2500,
        "energy": 4000,
        "industrial": 5000,
        "waste": 1200,
        "renewable": 800,
        "baseline": 15000
    }

    detector = HotspotDetector(sample_data)

    result = detector.analyze(threshold_percent=25)

    from pprint import pprint
    pprint(result)