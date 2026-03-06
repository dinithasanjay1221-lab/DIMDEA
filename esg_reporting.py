"""
esg_reporting.py

Backend ESG (Environmental, Social, Governance) reporting logic for DIMDEA.
Contains ESG score calculations and composite report generation.
No UI rendering, no API routes.
"""

from typing import Dict
import numpy as np


# =========================
# Utility Functions
# =========================

def _validate_numeric(value: float, name: str) -> float:
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric.")
    return float(value)


def _clamp_score(score: float) -> float:
    return max(0.0, min(100.0, score))


# =========================
# Environmental Score
# =========================

def calculate_environmental_score(
    carbon_emissions: float,
    energy_consumption: float,
    waste_generated: float,
    renewable_energy_ratio: float
) -> float:
    """
    Calculate Environmental Score (0–100).
    Lower emissions/waste = better.
    Higher renewable ratio = better.
    """

    carbon = _validate_numeric(carbon_emissions, "carbon_emissions")
    energy = _validate_numeric(energy_consumption, "energy_consumption")
    waste = _validate_numeric(waste_generated, "waste_generated")
    renewable = _validate_numeric(renewable_energy_ratio, "renewable_energy_ratio")

    if renewable < 0 or renewable > 1:
        raise ValueError("renewable_energy_ratio must be between 0 and 1.")

    # Normalize negatively contributing factors
    environmental_raw = (
        (100 / (1 + carbon)) * 0.35 +
        (100 / (1 + energy)) * 0.25 +
        (100 / (1 + waste)) * 0.20 +
        (renewable * 100) * 0.20
    )

    return _clamp_score(environmental_raw)


# =========================
# Social Score
# =========================

def calculate_social_score(
    employee_welfare: float,
    community_engagement: float,
    diversity_ratio: float,
    workplace_safety: float
) -> float:
    """
    Calculate Social Score (0–100).
    Inputs expected between 0 and 100 except diversity_ratio (0–1).
    """

    welfare = _validate_numeric(employee_welfare, "employee_welfare")
    community = _validate_numeric(community_engagement, "community_engagement")
    diversity = _validate_numeric(diversity_ratio, "diversity_ratio")
    safety = _validate_numeric(workplace_safety, "workplace_safety")

    if not (0 <= diversity <= 1):
        raise ValueError("diversity_ratio must be between 0 and 1.")

    social_raw = (
        welfare * 0.30 +
        community * 0.25 +
        (diversity * 100) * 0.20 +
        safety * 0.25
    )

    return _clamp_score(social_raw)


# =========================
# Governance Score
# =========================

def calculate_governance_score(
    compliance_rating: float,
    transparency_index: float,
    board_independence_ratio: float,
    risk_management_score: float
) -> float:
    """
    Calculate Governance Score (0–100).
    board_independence_ratio expected between 0 and 1.
    """

    compliance = _validate_numeric(compliance_rating, "compliance_rating")
    transparency = _validate_numeric(transparency_index, "transparency_index")
    board_ratio = _validate_numeric(board_independence_ratio, "board_independence_ratio")
    risk = _validate_numeric(risk_management_score, "risk_management_score")

    if not (0 <= board_ratio <= 1):
        raise ValueError("board_independence_ratio must be between 0 and 1.")

    governance_raw = (
        compliance * 0.30 +
        transparency * 0.25 +
        (board_ratio * 100) * 0.20 +
        risk * 0.25
    )

    return _clamp_score(governance_raw)


# =========================
# ESG Composite Report
# =========================

def generate_esg_report(
    environmental_score: float,
    social_score: float,
    governance_score: float
) -> Dict[str, float]:
    """
    Generate ESG composite report and rating.
    """

    env = _validate_numeric(environmental_score, "environmental_score")
    soc = _validate_numeric(social_score, "social_score")
    gov = _validate_numeric(governance_score, "governance_score")

    composite = (env * 0.4) + (soc * 0.3) + (gov * 0.3)
    composite = _clamp_score(composite)

    if composite >= 85:
        rating = "Excellent"
    elif composite >= 70:
        rating = "Good"
    elif composite >= 50:
        rating = "Moderate"
    else:
        rating = "Poor"

    return {
        "environmental_score": env,
        "social_score": soc,
        "governance_score": gov,
        "composite_score": composite,
        "rating": rating
    }


# =========================
# TEST BLOCK
# =========================

if __name__ == "__main__":

    print("=== ESG Reporting Module Test ===")

    env_score = calculate_environmental_score(
        carbon_emissions=50,
        energy_consumption=40,
        waste_generated=30,
        renewable_energy_ratio=0.6
    )

    soc_score = calculate_social_score(
        employee_welfare=80,
        community_engagement=75,
        diversity_ratio=0.7,
        workplace_safety=85
    )

    gov_score = calculate_governance_score(
        compliance_rating=90,
        transparency_index=85,
        board_independence_ratio=0.65,
        risk_management_score=88
    )

    report = generate_esg_report(env_score, soc_score, gov_score)

    print(report)