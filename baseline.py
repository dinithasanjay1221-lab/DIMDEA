"""
baseline.py

Backend module for establishing baseline carbon emissions.
Pure Python logic only (no frontend, no Streamlit).
"""

from typing import Dict
import pandas as pd
import numpy as np


def _validate_dataframe(data: pd.DataFrame, required_columns: list) -> None:
    """
    Validate input DataFrame and required columns.
    """
    if data is None or data.empty:
        raise ValueError("Input DataFrame is empty.")

    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def calculate_baseline_emissions(
    data: pd.DataFrame,
    year_column: str,
    scope1_column: str,
    scope2_column: str,
    baseline_year: int,
) -> Dict[str, float]:
    """
    Calculate total Scope 1, Scope 2, and combined emissions
    for a specific baseline year.
    """
    _validate_dataframe(data, [year_column, scope1_column, scope2_column])

    filtered_data = data[data[year_column] == baseline_year]

    if filtered_data.empty:
        raise ValueError(f"No data found for baseline year: {baseline_year}")

    scope1_total = float(filtered_data[scope1_column].fillna(0).sum())
    scope2_total = float(filtered_data[scope2_column].fillna(0).sum())
    combined_total = float(scope1_total + scope2_total)

    return {
        "year": int(baseline_year),
        "scope1_total": scope1_total,
        "scope2_total": scope2_total,
        "combined_total": combined_total,
    }


def calculate_average_baseline(
    data: pd.DataFrame,
    year_column: str,
    scope1_column: str,
    scope2_column: str,
    start_year: int,
    end_year: int,
) -> Dict[str, float]:
    """
    Calculate average Scope 1, Scope 2, and combined emissions
    between start_year and end_year (inclusive).
    """
    if start_year > end_year:
        raise ValueError("start_year cannot be greater than end_year.")

    _validate_dataframe(data, [year_column, scope1_column, scope2_column])

    filtered_data = data[
        (data[year_column] >= start_year) &
        (data[year_column] <= end_year)
    ]

    if filtered_data.empty:
        raise ValueError("No data found within the given year range.")

    yearly_totals = (
        filtered_data
        .groupby(year_column)[[scope1_column, scope2_column]]
        .sum()
        .fillna(0)
    )

    avg_scope1 = float(yearly_totals[scope1_column].mean())
    avg_scope2 = float(yearly_totals[scope2_column].mean())
    avg_combined = float((yearly_totals[scope1_column] + yearly_totals[scope2_column]).mean())

    return {
        "start_year": int(start_year),
        "end_year": int(end_year),
        "avg_scope1": avg_scope1,
        "avg_scope2": avg_scope2,
        "avg_combined": avg_combined,
    }


def get_emission_growth_rate(
    data: pd.DataFrame,
    year_column: str,
    total_column: str,
) -> float:
    """
    Calculate percentage growth rate of total emissions
    from the first year to the last year.
    """
    _validate_dataframe(data, [year_column, total_column])

    sorted_data = data.sort_values(by=year_column)

    if sorted_data.shape[0] < 2:
        raise ValueError("At least two years of data are required to calculate growth rate.")

    first_value = float(sorted_data.iloc[0][total_column])
    last_value = float(sorted_data.iloc[-1][total_column])

    if first_value == 0:
        raise ValueError("Cannot calculate growth rate because the first year value is zero.")

    growth_rate = ((last_value - first_value) / first_value) * 100.0
    return float(growth_rate)


if __name__ == "__main__":
    # Sample test data
    sample_data = pd.DataFrame({
        "Year": [2020, 2021, 2022, 2023],
        "Scope1": [100.0, 120.0, 130.0, 150.0],
        "Scope2": [80.0, 90.0, 95.0, 110.0],
    })

    # Add combined total column for growth rate testing
    sample_data["Total"] = sample_data["Scope1"] + sample_data["Scope2"]

    print("Baseline Emissions (2022):")
    print(
        calculate_baseline_emissions(
            sample_data,
            year_column="Year",
            scope1_column="Scope1",
            scope2_column="Scope2",
            baseline_year=2022,
        )
    )

    print("\nAverage Baseline (2020-2023):")
    print(
        calculate_average_baseline(
            sample_data,
            year_column="Year",
            scope1_column="Scope1",
            scope2_column="Scope2",
            start_year=2020,
            end_year=2023,
        )
    )

    print("\nEmission Growth Rate:")
    print(
        get_emission_growth_rate(
            sample_data,
            year_column="Year",
            total_column="Total",
        )
    )