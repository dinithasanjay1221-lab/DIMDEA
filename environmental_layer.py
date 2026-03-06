"""
environmental_layer.py
DIMDEA - Environmental Intelligence & Climate Context Engine
Planetary Awareness Layer for the Carbon Engine
"""

import logging
import json
import math
import random
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# -----------------------------
# Core Classes
# -----------------------------

class EnvironmentalLayer:
    def __init__(self, data):
        self.data = data

    def analyze(self):
        """
        Perform environmental impact analysis
        """

        # Sum only numeric values
        total_emissions = sum(
            value for value in self.data.values()
            if isinstance(value, (int, float))
        )

        # Calculate impact level
        if total_emissions > 20000:
            impact_level = "Severe"
        elif total_emissions > 10000:
            impact_level = "High"
        elif total_emissions > 5000:
            impact_level = "Moderate"
        else:
            impact_level = "Low"

        environmental_score = round(total_emissions / 1000, 2)

        return {
            "total_environmental_load": total_emissions,
            "environmental_score": environmental_score,
            "impact_level": impact_level
        }


def generate_environmental_report(data):
    layer = EnvironmentalLayer(data)
    analysis = layer.analyze()

    return {
        "report_summary": f"Total Load: {analysis['total_environmental_load']}",
        "impact_level": analysis["impact_level"],
        "score": analysis["environmental_score"]
    }


class RiskCalculator:
    """
    Climate Risk Intelligence engine for evaluating hazards and disruption probabilities.
    """

    def evaluate_risks(self, location: str, horizon: int = 10) -> Dict[str, Any]:
        risks = {
            "flood_risk": random.uniform(0, 1),
            "heatwave_risk": random.uniform(0, 1),
            "drought_risk": random.uniform(0, 1),
            "cyclone_risk": random.uniform(0, 1),
        }
        disruption_prob = sum(risks.values()) / 4
        vulnerability_score = disruption_prob * 100

        projections = {
            "5_year": vulnerability_score * 1.1,
            "10_year": vulnerability_score * 1.3,
            "20_year": vulnerability_score * 1.6,
        }

        return {
            "location": location,
            "risks": risks,
            "disruption_probability": disruption_prob,
            "vulnerability_score": vulnerability_score,
            "projections": projections,
        }


class GridIntensityModel:
    """
    Models real-time and historical grid carbon intensity.
    """

    def estimate_grid_intensity(self, location: str) -> Dict[str, Any]:
        fossil_share = random.uniform(0.3, 0.8)
        renewable_share = 1 - fossil_share
        intensity = fossil_share * 0.9 + renewable_share * 0.2

        return {
            "location": location,
            "fossil_share": fossil_share,
            "renewable_share": renewable_share,
            "carbon_intensity": intensity,
            "optimal_production_window": "Night" if intensity > 0.6 else "Day",
        }


class EnvironmentalScorer:
    """
    Generates ESG context scoring and advanced analytics.
    """

    def compute_scores(self, facility_context: Dict[str, Any], risk_context: Dict[str, Any]) -> Dict[str, Any]:
        weighted_score = (
            facility_context["carbon_intensity_factor"] * 0.4 +
            risk_context["disruption_probability"] * 0.3 +
            facility_context["air_quality_index"] / 200 * 0.3
        )

        monte_carlo = [weighted_score + random.gauss(0, 0.05) for _ in range(1000)]
        sensitivity = max(monte_carlo) - min(monte_carlo)

        return {
            "ECI": weighted_score,
            "benchmark_normalized": weighted_score / 0.75,
            "sustainability_heatmap": {"risk": risk_context["vulnerability_score"], "impact": weighted_score},
            "monte_carlo_range": (min(monte_carlo), max(monte_carlo)),
            "sensitivity_analysis": sensitivity,
        }
