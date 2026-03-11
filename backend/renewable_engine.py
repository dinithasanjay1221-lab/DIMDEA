"""
renewable_engine.py

DIMDEA - Carbon Emission Intelligence System
Module: RenewableEngine

Purpose:
Model renewable energy integration impact and calculate
carbon reduction potential.

NOTE:
- No database logic
- No API routes
- No UI logic
- Pure renewable energy modeling
"""

from typing import Dict, Any
import logging   # ✅ ADDED (for backend debugging)

# ======================================================
# LOGGER (SAFE DEBUGGING SUPPORT)
# ======================================================

logger = logging.getLogger("DIMDEA.RenewableEngine")


class RenewableEngine:
    """
    RenewableEngine models renewable energy transition impact
    on carbon emissions.
    """

    # -----------------------------
    # Configurable Thresholds
    # -----------------------------

    MIN_IMPACT_THRESHOLD = 5.0      # % reduction considered minor
    HIGH_IMPACT_THRESHOLD = 30.0    # % reduction considered high
    MAX_PERCENT = 100.0
    MIN_PERCENT = 0.0

    def __init__(self, input_data: Dict[str, float]):
        """
        Initialize RenewableEngine with structured renewable data.
        """
        logger.info("Initializing RenewableEngine")   # ✅ ADDED
        self._validate_input(input_data)
        self.data = input_data

    # -----------------------------
    # Input Validation
    # -----------------------------

    def _validate_input(self, data: Dict[str, float]) -> None:
        required_fields = [
            "current_energy_consumption",
            "current_energy_emissions",
            "renewable_share_percent",
            "target_renewable_percent",
            "emission_factor_grid",
            "emission_factor_renewable"
        ]

        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

            if not isinstance(data[field], (int, float)):
                raise TypeError(f"{field} must be numeric.")

        if not (self.MIN_PERCENT <= data["renewable_share_percent"] <= self.MAX_PERCENT):
            raise ValueError("Current renewable percent must be between 0 and 100.")

        if not (self.MIN_PERCENT <= data["target_renewable_percent"] <= self.MAX_PERCENT):
            raise ValueError("Target renewable percent must be between 0 and 100.")

        if data["target_renewable_percent"] < data["renewable_share_percent"]:
            raise ValueError("Target renewable percent cannot be less than current percent.")

    # -----------------------------
    # Core Calculations
    # -----------------------------

    def _calculate_emissions(self, renewable_percent: float) -> float:
        """
        Calculate emissions based on renewable share.
        """

        total_consumption = self.data["current_energy_consumption"]
        grid_factor = self.data["emission_factor_grid"]
        renewable_factor = self.data["emission_factor_renewable"]

        renewable_energy = (renewable_percent / 100) * total_consumption
        grid_energy = total_consumption - renewable_energy

        emissions = (grid_energy * grid_factor) + (renewable_energy * renewable_factor)

        return max(0.0, emissions)

    def _calculate_reduction(self, current: float, projected: float) -> Dict[str, float]:
        """
        Calculate emission reduction metrics.
        """
        reduction = current - projected
        reduction_percent = (reduction / current) * 100 if current > 0 else 0

        return {
            "reduction": round(max(0.0, reduction), 2),
            "reduction_percent": round(max(0.0, reduction_percent), 2)
        }

    def _impact_level(self, reduction_percent: float) -> str:
        """
        Classify renewable transition impact.
        """
        if reduction_percent < self.MIN_IMPACT_THRESHOLD:
            return "Low Impact"
        elif reduction_percent < self.HIGH_IMPACT_THRESHOLD:
            return "Moderate Impact"
        else:
            return "High Impact"

    # -----------------------------
    # Public Analysis Method
    # -----------------------------

    def analyze_transition(self) -> Dict[str, Any]:
        """
        Generate renewable transition analysis.
        """

        try:

            current_percent = self.data["renewable_share_percent"]
            target_percent = self.data["target_renewable_percent"]

            current_emissions = self._calculate_emissions(current_percent)
            projected_emissions = self._calculate_emissions(target_percent)

            reduction_data = self._calculate_reduction(
                current_emissions,
                projected_emissions
            )

            impact = self._impact_level(reduction_data["reduction_percent"])

            renewable_increase = target_percent - current_percent

            summary = (
                f"Renewable share increases by {renewable_increase:.2f}%. "
                f"Estimated emission reduction: {reduction_data['reduction_percent']}%. "
                f"Impact classification: {impact}."
            )

            result = {
                "current_emissions": round(current_emissions, 2),
                "projected_emissions": round(projected_emissions, 2),
                "emission_reduction": reduction_data["reduction"],
                "reduction_percent": reduction_data["reduction_percent"],
                "renewable_increase_needed": round(renewable_increase, 2),
                "impact_level": impact,
                "analysis_summary": summary
            }

            logger.info("Renewable transition analysis completed successfully")  # ✅ ADDED

            return result

        except Exception as e:

            logger.error(f"RenewableEngine analysis failed: {e}")  # ✅ ADDED

            raise


# ---------------------------------------
# Example Standalone Execution
# ---------------------------------------

if __name__ == "__main__":

    sample_input = {
        "current_energy_consumption": 10000,       # kWh
        "current_energy_emissions": 8000,          # baseline reference (not used directly in calc)
        "renewable_share_percent": 20,
        "target_renewable_percent": 50,
        "emission_factor_grid": 0.8,
        "emission_factor_renewable": 0.05
    }

    try:
        engine = RenewableEngine(sample_input)
        results = engine.analyze_transition()

        print("\n===== DIMDEA Renewable Transition Analysis =====")
        for key, value in results.items():
            print(f"{key}: {value}")

    except Exception as e:
        print(f"Error: {e}")