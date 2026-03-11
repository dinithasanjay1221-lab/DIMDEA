"""
baseline.py

Backend module for establishing baseline carbon emissions.
Pure Python logic only (no frontend, no Streamlit).

Enhancements:
- Accepts pandas DataFrame or dictionary input
- Returns dict results for frontend-ready integration
- Validates input data
"""

from typing import Dict, Union, Any
import pandas as pd
import numpy as np

class BaselineCalculator:
    """
    Calculate baseline carbon emissions for organizations, sectors, or cities.
    """

    def __init__(self, input_data: Union[Dict[str, Any], pd.DataFrame]):
        """
        Initialize with structured input data.

        :param input_data: Dictionary with sector emission values or Pandas DataFrame
                           Expected columns: 'sector', 'emission'
        """
        if isinstance(input_data, pd.DataFrame):
            self.data = self._from_dataframe(input_data)
        else:
            self.data = self._validate_dict(input_data)

    # -----------------------------
    # Convert DataFrame to internal dict
    # -----------------------------
    def _from_dataframe(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        Convert DataFrame to dictionary format for baseline calculation.
        """
        required_cols = {"sector", "emission"}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"DataFrame must contain columns: {required_cols}")
        
        baseline_dict = {}
        for _, row in df.iterrows():
            sector = str(row["sector"])
            emission = float(row["emission"])
            baseline_dict[sector] = emission
        
        return baseline_dict

    # -----------------------------
    # Validate dictionary input
    # -----------------------------
    def _validate_dict(self, data: Dict[str, Any]) -> Dict[str, float]:
        if not isinstance(data, dict):
            raise TypeError("Input data must be a dictionary.")
        baseline_dict = {}
        for sector, emission in data.items():
            if not isinstance(emission, (int, float)):
                raise ValueError(f"Emission value for sector '{sector}' must be numeric.")
            baseline_dict[str(sector)] = float(emission)
        return baseline_dict

    # -----------------------------
    # Calculate Total Baseline
    # -----------------------------
    def total_baseline(self) -> float:
        """
        Calculate total baseline emission across all sectors.
        """
        return sum(self.data.values())

    # -----------------------------
    # Return Sector-wise Baseline
    # -----------------------------
    def sector_wise(self) -> Dict[str, float]:
        """
        Return the baseline emission per sector.
        """
        return self.data

    # -----------------------------
    # Return results as dict (frontend-ready)
    # -----------------------------
    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_baseline": self.total_baseline(),
            "sector_wise": self.sector_wise()
        }


# -----------------------------
# Example Standalone Execution
# -----------------------------
if __name__ == "__main__":
    # Example dictionary input
    sample_data = {
        "transportation": 1200,
        "energy": 3500,
        "industry": 2000,
        "waste": 500
    }

    # Example DataFrame input
    df_input = pd.DataFrame({
        "sector": ["transportation", "energy", "industry", "waste"],
        "emission": [1200, 3500, 2000, 500]
    })

    # Using dictionary
    calc_dict = BaselineCalculator(sample_data)
    print("Dictionary Input:", calc_dict.to_dict())

    # Using DataFrame
    calc_df = BaselineCalculator(df_input)
    print("DataFrame Input:", calc_df.to_dict())