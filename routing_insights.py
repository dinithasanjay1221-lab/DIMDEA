"""
routing_insights.py

DIMDEA - Carbon Emission Intelligence System
Module: RoutingInsights

Purpose:
Analyze routing optimization results and generate
efficiency, carbon, and time-based insights.

NOTE:
- No database logic
- No API routes
- No raw data storage
"""

from typing import Dict, List, Any
import statistics


class RoutingInsights:
    """
    Analyze routing results and generate structured insights.
    """

    # -----------------------------
    # Configurable Thresholds
    # -----------------------------

    EMISSION_INTENSITY_THRESHOLD = 0.8  # emissions per km threshold
    DOMINANCE_THRESHOLD = 0.5  # 50% dominance flag
    EMISSION_LIMIT = 10000  # total emission upper limit
    TIME_IMBALANCE_THRESHOLD = 0.4  # 40% deviation

    # -----------------------------
    # Constructor
    # -----------------------------

    def __init__(self, routing_data: Dict[str, Any]):
        """
        Initialize RoutingInsights with structured routing data.
        """
        self._validate_input(routing_data)
        self.routing_data = routing_data

    # -----------------------------
    # Input Validation
    # -----------------------------

    def _validate_input(self, data: Dict[str, Any]) -> None:
        required_fields = [
            "total_distance",
            "total_time",
            "total_emissions",
            "fuel_consumption",
            "number_of_routes",
            "route_breakdown"
        ]

        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        if not isinstance(data["route_breakdown"], list):
            raise TypeError("route_breakdown must be a list.")

        for route in data["route_breakdown"]:
            for key in ["route_id", "distance", "time", "emissions"]:
                if key not in route:
                    raise ValueError(f"Missing {key} in route breakdown.")

    # -----------------------------
    # Efficiency Analytics
    # -----------------------------

    def _efficiency_metrics(self) -> Dict[str, Any]:
        routes = self.routing_data.get("route_breakdown", [])

        if not routes:
            return {
                "status": "No routing data available",
                "longest_route": None,
                "shortest_route": None
            }

        longest_route = max(routes, key=lambda x: x["distance"])
        shortest_route = min(routes, key=lambda x: x["distance"])

        return {
            "longest_route": longest_route,
            "shortest_route": shortest_route
        }

    # -----------------------------
    # Carbon Analysis
    # -----------------------------

    def _carbon_analysis(self) -> Dict[str, Any]:
        total_distance = self.routing_data["total_distance"]
        total_emissions = self.routing_data["total_emissions"]

        emission_intensity = (
            total_emissions / total_distance if total_distance > 0 else 0
        )

        is_efficient = emission_intensity <= self.EMISSION_INTENSITY_THRESHOLD

        return {
            "emission_intensity_per_km": round(emission_intensity, 3),
            "carbon_efficient": is_efficient
        }

    # -----------------------------
    # Time Analysis
    # -----------------------------

    def _time_analysis(self) -> Dict[str, Any]:
        routes = self.routing_data.get("route_breakdown", [])

        if not routes:
            return {
                "average_route_time": 0,
                "time_variance": 0,
                "time_imbalance_detected": False
            }

        times = [r["time"] for r in routes]

        avg_time = statistics.mean(times)
        variance = statistics.pstdev(times) if len(times) > 1 else 0

        imbalance_flag = (
            variance / avg_time > self.TIME_IMBALANCE_THRESHOLD
            if avg_time > 0 else False
        )

        return {
            "average_route_time": round(avg_time, 2),
            "time_variance": round(variance, 2),
            "time_imbalance_detected": imbalance_flag
        }

    # -----------------------------
    # Risk Flags
    # -----------------------------

    def _risk_flags(self) -> List[str]:
        flags = []

        total_emissions = self.routing_data["total_emissions"]
        routes = self.routing_data.get("route_breakdown", [])

        if total_emissions > self.EMISSION_LIMIT:
            flags.append("Total emissions exceed safe operational limit.")

        if routes and total_emissions > 0:
            highest_route = max(routes, key=lambda x: x["emissions"])

            if highest_route["emissions"] / total_emissions > self.DOMINANCE_THRESHOLD:
                flags.append("Single route dominates total emissions.")

        carbon_data = self._carbon_analysis()
        if not carbon_data["carbon_efficient"]:
            flags.append("Emission intensity per km exceeds efficiency threshold.")

        return flags

    # -----------------------------
    # Summary Generator
    # -----------------------------

    def generate_insights(self) -> Dict[str, Any]:
        efficiency = self._efficiency_metrics()
        carbon = self._carbon_analysis()
        time = self._time_analysis()
        risks = self._risk_flags()

        summary = "Routing analysis completed. "
        if risks:
            summary += "Potential operational risks detected."
        else:
            summary += "Routing performance is within optimal limits."

        return {
            "efficiency_metrics": efficiency,
            "carbon_analysis": carbon,
            "time_analysis": time,
            "risk_flags": risks,
            "insight_summary": summary
        }


# ---------------------------------------
# Standalone Test
# ---------------------------------------

if __name__ == "__main__":

    sample_routing_data = {
        "total_distance": 1500,
        "total_time": 120,
        "total_emissions": 900,
        "fuel_consumption": 300,
        "number_of_routes": 3,
        "route_breakdown": [
            {"route_id": "R1", "distance": 500, "time": 40, "emissions": 300},
            {"route_id": "R2", "distance": 600, "time": 50, "emissions": 400},
            {"route_id": "R3", "distance": 400, "time": 30, "emissions": 200}
        ]
    }

    analyzer = RoutingInsights(sample_routing_data)
    insights = analyzer.generate_insights()

    print("\n===== DIMDEA Routing Insights =====")
    for key, value in insights.items():
        print(f"{key}: {value}")