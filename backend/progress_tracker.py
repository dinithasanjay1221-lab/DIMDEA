"""
progress_tracker.py

DIMDEA - Carbon Emission Intelligence System
Module: ProgressTracker

Purpose:
Track sustainability progress over time and generate
trend-based analytical insights.

NOTE:
- No database logic
- No API routes
- No frontend/UI rendering
- Pure analytical module
"""

from typing import Dict, List, Any


class ProgressTracker:
    """
    Track and analyze sustainability progress over time.
    """

    # -----------------------------
    # Configurable Thresholds
    # -----------------------------

    STAGNATION_THRESHOLD_PERCENT = 2.0   # Less than 2% change considered stagnation
    CONSECUTIVE_INCREASE_LIMIT = 2       # Flag if emissions increase for 2+ years

    def __init__(self, input_data: Dict[str, Any]):
        """
        Initialize ProgressTracker with structured time-series data.
        """
        self._validate_input(input_data)
        self.baseline = input_data["baseline_emission"]
        self.history = sorted(input_data["history"], key=lambda x: x["year"])

    # -----------------------------
    # Input Validation
    # -----------------------------

    def _validate_input(self, data: Dict[str, Any]) -> None:
        if "baseline_emission" not in data:
            raise ValueError("Missing baseline_emission.")
        if "history" not in data:
            raise ValueError("Missing history data.")

        if not isinstance(data["baseline_emission"], (int, float)):
            raise TypeError("baseline_emission must be numeric.")

        if data["baseline_emission"] <= 0:
            raise ValueError("baseline_emission must be greater than zero.")

        if not isinstance(data["history"], list) or len(data["history"]) == 0:
            raise ValueError("history must be a non-empty list.")

        for record in data["history"]:
            if "year" not in record or "total_emission" not in record:
                raise ValueError("Each history record must contain year and total_emission.")
            if not isinstance(record["year"], int):
                raise TypeError("year must be an integer.")
            if not isinstance(record["total_emission"], (int, float)):
                raise TypeError("total_emission must be numeric.")
            if record["total_emission"] < 0:
                raise ValueError("total_emission cannot be negative.")

    # -----------------------------
    # Progress Calculations
    # -----------------------------

    def _yearly_changes(self) -> List[Dict[str, float]]:
        """
        Calculate year-over-year percentage changes.
        """
        changes = []

        for i in range(1, len(self.history)):
            prev = self.history[i - 1]["total_emission"]
            curr = self.history[i]["total_emission"]

            percent_change = ((curr - prev) / prev) * 100 if prev > 0 else 0

            changes.append({
                "year": self.history[i]["year"],
                "percent_change_from_previous_year": round(percent_change, 2)
            })

        return changes

    def _overall_change_from_baseline(self) -> float:
        """
        Calculate overall change from baseline to latest year.
        """
        latest_emission = self.history[-1]["total_emission"]
        change = ((latest_emission - self.baseline) / self.baseline) * 100
        return round(change, 2)

    # -----------------------------
    # Trend Detection
    # -----------------------------

    def _detect_trend(self) -> str:
        """
        Determine if emissions are improving, stable, or worsening.
        """
        yearly = self._yearly_changes()

        if not yearly:
            return "Insufficient Data"

        improvements = sum(1 for y in yearly if y["percent_change_from_previous_year"] < 0)
        increases = sum(1 for y in yearly if y["percent_change_from_previous_year"] > 0)

        if improvements > increases:
            return "Improving"
        elif increases > improvements:
            return "Worsening"
        else:
            return "Stable"

    def _momentum_status(self) -> str:
        """
        Determine whether reduction is accelerating or slowing.
        """
        yearly = self._yearly_changes()

        reductions = [
            abs(y["percent_change_from_previous_year"])
            for y in yearly
            if y["percent_change_from_previous_year"] < 0
        ]

        if len(reductions) < 2:
            return "Insufficient Data"

        if reductions[-1] > reductions[-2]:
            return "Acceleration in Reduction"
        elif reductions[-1] < reductions[-2]:
            return "Reduction Slowing"
        else:
            return "Stable Reduction Rate"

    # -----------------------------
    # Risk Flags
    # -----------------------------

    def _risk_flags(self) -> List[str]:
        flags = []
        yearly = self._yearly_changes()

        # Consecutive increase detection
        consecutive_increase = 0
        for y in yearly:
            if y["percent_change_from_previous_year"] > 0:
                consecutive_increase += 1
                if consecutive_increase >= self.CONSECUTIVE_INCREASE_LIMIT:
                    flags.append("Emissions increasing for consecutive years.")
                    break
            else:
                consecutive_increase = 0

        # Baseline exceed check
        if self.history[-1]["total_emission"] > self.baseline:
            flags.append("Latest emissions exceed baseline level.")

        # Stagnation detection
        if len(yearly) >= 2:
            recent_changes = yearly[-2:]
            if all(abs(y["percent_change_from_previous_year"]) < self.STAGNATION_THRESHOLD_PERCENT for y in recent_changes):
                flags.append("Emission reduction stagnating.")

        return flags

    # -----------------------------
    # Public Analysis Method
    # -----------------------------

    def generate_progress_report(self) -> Dict[str, Any]:
        latest_emission = self.history[-1]["total_emission"]
        overall_change = self._overall_change_from_baseline()
        yearly_changes = self._yearly_changes()
        trend = self._detect_trend()
        momentum = self._momentum_status()
        risks = self._risk_flags()

        summary = (
            f"Latest emission: {latest_emission}. "
            f"Overall change from baseline: {overall_change}%. "
            f"Trend: {trend}. Momentum: {momentum}."
        )

        return {
            "baseline": self.baseline,
            "latest_emission": latest_emission,
            "overall_change_percent": overall_change,
            "yearly_changes": yearly_changes,
            "trend_direction": trend,
            "momentum_status": momentum,
            "risk_flags": risks,
            "analysis_summary": summary
        }


# ---------------------------------------
# Example Standalone Execution
# ---------------------------------------

if __name__ == "__main__":

    sample_input = {
        "baseline_emission": 10000,
        "history": [
            {"year": 2021, "total_emission": 9800},
            {"year": 2022, "total_emission": 9500},
            {"year": 2023, "total_emission": 9700}
        ]
    }

    try:
        tracker = ProgressTracker(sample_input)
        report = tracker.generate_progress_report()

        print("\n===== DIMDEA Sustainability Progress Report =====")
        for key, value in report.items():
            print(f"{key}: {value}")

    except Exception as e:
        print(f"Error: {e}")