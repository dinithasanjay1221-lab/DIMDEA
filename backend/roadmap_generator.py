"""
roadmap_generator.py

Backend module for generating structured sustainability roadmaps.
Contains roadmap planning logic only.
No UI, no datasets, no database connections.
"""

from typing import Dict, List
import math


# =========================
# Validation Utilities
# =========================

def _validate_positive_number(value: float, name: str) -> float:
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric.")
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")
    return float(value)


def _validate_percentage(value: float, name: str) -> float:
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric.")
    if not (0 <= value <= 1):
        raise ValueError(f"{name} must be between 0 and 1.")
    return float(value)


def _validate_years(value: int) -> int:
    if not isinstance(value, int):
        raise ValueError("years_to_target must be an integer.")
    if value <= 0:
        raise ValueError("years_to_target must be greater than zero.")
    return value


def _clamp_non_negative(value: float) -> float:
    return max(0.0, value)


# =========================
# Classification Utilities
# =========================

def _classify_action_intensity(annual_reduction_ratio: float) -> str:
    if annual_reduction_ratio < 0.05:
        return "Low"
    elif annual_reduction_ratio < 0.10:
        return "Moderate"
    elif annual_reduction_ratio < 0.20:
        return "High"
    else:
        return "Aggressive"


def _assess_risk(reduction_percentage: float, years: int) -> str:
    if reduction_percentage > 0.6 and years <= 3:
        return "High"
    elif reduction_percentage > 0.4:
        return "Medium"
    return "Low"


def _assess_feasibility(esg_score: float, annual_reduction: float) -> str:
    if esg_score >= 80 and annual_reduction < 0.10:
        return "Highly Feasible"
    elif esg_score >= 60:
        return "Feasible"
    elif esg_score >= 40:
        return "Challenging"
    return "Critical"


# =========================
# Roadmap Generator
# =========================

def generate_sustainability_roadmap(
    current_emissions: float,
    target_reduction_percentage: float,
    years_to_target: int,
    esg_score: float,
    budget: float
) -> Dict[str, object]:
    """
    Generate a structured sustainability roadmap.

    Parameters:
        current_emissions (float)
        target_reduction_percentage (0–1)
        years_to_target (int)
        esg_score (0–100)
        budget (float)

    Returns:
        Structured roadmap dictionary
    """

    emissions = _validate_positive_number(current_emissions, "current_emissions")
    reduction_pct = _validate_percentage(
        target_reduction_percentage,
        "target_reduction_percentage"
    )
    years = _validate_years(years_to_target)
    esg = _validate_positive_number(esg_score, "esg_score")
    budget_total = _validate_positive_number(budget, "budget")

    if esg > 100:
        raise ValueError("esg_score must not exceed 100.")

    total_reduction_required = emissions * reduction_pct
    annual_reduction_amount = total_reduction_required / years
    annual_reduction_ratio = annual_reduction_amount / emissions

    timeline: List[Dict[str, object]] = []

    remaining_emissions = emissions
    annual_budget = budget_total / years

    for year in range(1, years + 1):
        remaining_emissions -= annual_reduction_amount
        remaining_emissions = _clamp_non_negative(remaining_emissions)

        intensity = _classify_action_intensity(annual_reduction_ratio)

        timeline.append({
            "year": year,
            "target_emission_level": round(remaining_emissions, 2),
            "recommended_action_intensity": intensity,
            "allocated_budget": round(annual_budget, 2)
        })

    risk_level = _assess_risk(reduction_pct, years)
    feasibility = _assess_feasibility(esg, annual_reduction_ratio)

    return {
        "total_reduction_required": round(total_reduction_required, 2),
        "annual_reduction_target": round(annual_reduction_amount, 2),
        "timeline": timeline,
        "risk_level": risk_level,
        "feasibility": feasibility
    }


# =========================
# TEST BLOCK
# =========================

if __name__ == "__main__":

    print("=== Sustainability Roadmap Module Test ===")

    roadmap = generate_sustainability_roadmap(
        current_emissions=1000,
        target_reduction_percentage=0.5,
        years_to_target=5,
        esg_score=75,
        budget=500000
    )

    print(roadmap)