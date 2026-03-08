"""
carbon_engine.py

Core carbon footprint calculation algorithms.
Pure backend logic only (no UI, no API routes, no Streamlit).
"""

from typing import Union


Number = Union[int, float]


def _validate_non_negative(value: Number, name: str) -> float:
    """
    Validate that a numeric value is non-negative.
    """
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a numeric value.")
    if value < 0:
        raise ValueError(f"{name} cannot be negative.")
    return float(value)


def calculate_scope1_emissions(
    activity_data: Number,
    emission_factor: Number
) -> float:
    """
    Calculate Scope 1 emissions.

    Formula:
        Emissions = Activity Data × Emission Factor
    """
    activity = _validate_non_negative(activity_data, "activity_data")
    factor = _validate_non_negative(emission_factor, "emission_factor")

    emissions = activity * factor
    return float(emissions)


def calculate_scope2_emissions(
    electricity_usage: Number,
    grid_emission_factor: Number
) -> float:
    """
    Calculate Scope 2 emissions.

    Formula:
        Emissions = Electricity Usage × Grid Emission Factor
    """
    usage = _validate_non_negative(electricity_usage, "electricity_usage")
    factor = _validate_non_negative(grid_emission_factor, "grid_emission_factor")

    emissions = usage * factor
    return float(emissions)


def calculate_total_emissions(
    scope1: Number,
    scope2: Number
) -> float:
    """
    Calculate total emissions from Scope 1 and Scope 2.
    """
    s1 = _validate_non_negative(scope1, "scope1")
    s2 = _validate_non_negative(scope2, "scope2")

    total = s1 + s2
    return float(total)


def calculate_carbon_intensity(
    total_emissions: Number,
    production_output: Number
) -> float:
    """
    Calculate carbon intensity.

    Formula:
        Carbon Intensity = Total Emissions / Production Output
    """
    total = _validate_non_negative(total_emissions, "total_emissions")

    if not isinstance(production_output, (int, float)):
        raise ValueError("production_output must be a numeric value.")
    if production_output <= 0:
        raise ValueError("production_output must be greater than zero.")

    intensity = total / float(production_output)
    return float(intensity)


def calculate_emission_reduction(
    baseline_emission: Number,
    current_emission: Number
) -> float:
    """
    Calculate percentage emission reduction.

    Formula:
        ((baseline - current) / baseline) × 100
    """
    if not isinstance(baseline_emission, (int, float)):
        raise ValueError("baseline_emission must be numeric.")
    if baseline_emission <= 0:
        raise ValueError("baseline_emission must be greater than zero.")

    if not isinstance(current_emission, (int, float)):
        raise ValueError("current_emission must be numeric.")
    if current_emission < 0:
        raise ValueError("current_emission cannot be negative.")

    reduction = ((baseline_emission - current_emission) / baseline_emission) * 100.0
    return float(reduction)


if __name__ == "__main__":
    # Example test values
    fuel_consumption = 1000          # e.g., liters
    fuel_emission_factor = 2.5       # kg CO2 per liter

    electricity_usage = 5000         # kWh
    grid_factor = 0.82               # kg CO2 per kWh

    production_output = 10000        # units produced

    # Scope calculations
    scope1 = calculate_scope1_emissions(fuel_consumption, fuel_emission_factor)
    scope2 = calculate_scope2_emissions(electricity_usage, grid_factor)

    # Total emissions
    total = calculate_total_emissions(scope1, scope2)

    # Carbon intensity
    intensity = calculate_carbon_intensity(total, production_output)

    # Emission reduction example
    baseline = 20000
    current = total
    reduction_percent = calculate_emission_reduction(baseline, current)

    print("Scope 1 Emissions:", scope1)
    print("Scope 2 Emissions:", scope2)
    print("Total Emissions:", total)
    print("Carbon Intensity:", intensity)
    print("Emission Reduction (%):", reduction_percent)