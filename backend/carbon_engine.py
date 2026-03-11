"""
carbon_engine.py

Core carbon footprint calculation algorithms.
Enhanced for backend → frontend integration.

Enhancements:
- Accepts dictionary or DataFrame input for emissions
- Returns structured dictionary for frontend use
- Preserves all original logic
"""

from typing import Union, Dict

Number = Union[int, float]


def _validate_non_negative(value: Number, name: str) -> float:
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a numeric value.")
    if value < 0:
        raise ValueError(f"{name} cannot be negative.")
    return float(value)


def calculate_scope1_emissions(activity_data: Number, emission_factor: Number) -> float:
    activity = _validate_non_negative(activity_data, "activity_data")
    factor = _validate_non_negative(emission_factor, "emission_factor")
    return activity * factor


def calculate_scope2_emissions(electricity_usage: Number, grid_emission_factor: Number) -> float:
    usage = _validate_non_negative(electricity_usage, "electricity_usage")
    factor = _validate_non_negative(grid_emission_factor, "grid_emission_factor")
    return usage * factor


def calculate_total_emissions(scope1: Number, scope2: Number) -> float:
    s1 = _validate_non_negative(scope1, "scope1")
    s2 = _validate_non_negative(scope2, "scope2")
    return s1 + s2


def calculate_carbon_intensity(total_emissions: Number, production_output: Number) -> float:
    total = _validate_non_negative(total_emissions, "total_emissions")
    if not isinstance(production_output, (int, float)) or production_output <= 0:
        raise ValueError("production_output must be numeric and > 0.")
    return total / float(production_output)


def calculate_emission_reduction(baseline_emission: Number, current_emission: Number) -> float:
    if not isinstance(baseline_emission, (int, float)) or baseline_emission <= 0:
        raise ValueError("baseline_emission must be numeric and > 0.")
    if not isinstance(current_emission, (int, float)) or current_emission < 0:
        raise ValueError("current_emission must be numeric and >= 0.")
    return ((baseline_emission - current_emission) / baseline_emission) * 100.0


# -------------------------
# FRONTEND-INTEGRATION WRAPPER
# -------------------------
def calculate_carbon_report(emissions_data: Dict[str, Number], production_output: Number, baseline_emission: Number) -> Dict:
    """
    Frontend-ready function:
    Input: emissions_data dict with keys: 'scope1_activity', 'scope1_factor', 'electricity_usage', 'grid_factor'
    Returns structured dictionary with all calculations
    """
    s1 = calculate_scope1_emissions(emissions_data.get("scope1_activity", 0),
                                    emissions_data.get("scope1_factor", 0))
    s2 = calculate_scope2_emissions(emissions_data.get("electricity_usage", 0),
                                    emissions_data.get("grid_factor", 0))
    total = calculate_total_emissions(s1, s2)
    intensity = calculate_carbon_intensity(total, production_output)
    reduction = calculate_emission_reduction(baseline_emission, total)

    return {
        "scope1_emissions": round(s1, 3),
        "scope2_emissions": round(s2, 3),
        "total_emissions": round(total, 3),
        "carbon_intensity": round(intensity, 3),
        "emission_reduction_percent": round(reduction, 2)
    }


# -------------------------
# Example Standalone Execution
# -------------------------
if __name__ == "__main__":
    emissions_input = {
        "scope1_activity": 1000,
        "scope1_factor": 2.5,
        "electricity_usage": 5000,
        "grid_factor": 0.82
    }
    production = 10000
    baseline = 20000

    report = calculate_carbon_report(emissions_input, production, baseline)

    print("\n===== DIMDEA Carbon Report =====")
    for key, value in report.items():
        print(f"{key}: {value}")