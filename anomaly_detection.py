"""
anomaly_detection.py

DIMDEA - Carbon Emission Intelligence System
Module: AnomalyDetector

Purpose:
Detect anomalies in carbon emission time-series data
using statistical methods (Z-score and IQR).

NOTE:
- No database logic
- No API routes
- No UI logic
- Pure analytical module
"""

from typing import Dict, List, Any
import numpy as np


class AnomalyDetector:
    """
    Detect anomalies in time-series carbon emission data.
    """

    # -----------------------------
    # Configurable Thresholds
    # -----------------------------

    Z_THRESHOLD = 2.5              # Z-score threshold
    IQR_MULTIPLIER = 1.5           # IQR multiplier
    MIN_NOISE_PERCENT = 1.0        # Ignore fluctuations <1%

    def __init__(self, input_data: Dict[str, Any], method: str = "zscore"):
        """
        Initialize anomaly detector.

        :param input_data: Structured time-series data
        :param method: 'zscore' or 'iqr'
        """
        self._validate_input(input_data)
        self.metric_name = input_data["metric_name"]
        self.data = input_data["data"]
        self.method = method.lower()

        if self.method not in ["zscore", "iqr"]:
            raise ValueError("Method must be 'zscore' or 'iqr'.")

    # -----------------------------
    # Input Validation
    # -----------------------------

    def _validate_input(self, data: Dict[str, Any]) -> None:
        if "metric_name" not in data or "data" not in data:
            raise ValueError("Input must contain 'metric_name' and 'data'.")

        if not isinstance(data["data"], list) or len(data["data"]) < 2:
            raise ValueError("Data must be a list with at least 2 data points.")

        for entry in data["data"]:
            if "timestamp" not in entry or "value" not in entry:
                raise ValueError("Each data point must contain 'timestamp' and 'value'.")
            if not isinstance(entry["value"], (int, float)):
                raise TypeError("Value must be numeric.")

    # -----------------------------
    # Z-Score Detection
    # -----------------------------

    def _zscore_detection(self) -> List[Dict[str, Any]]:
        values = np.array([point["value"] for point in self.data])
        mean = np.mean(values)
        std_dev = np.std(values)

        anomalies = []

        if std_dev == 0:
            return anomalies  # No variation → no anomaly

        for point in self.data:
            z_score = (point["value"] - mean) / std_dev
            percent_change = abs((point["value"] - mean) / mean) * 100 if mean != 0 else 0

            if abs(z_score) >= self.Z_THRESHOLD and percent_change >= self.MIN_NOISE_PERCENT:
                anomalies.append({
                    "timestamp": point["timestamp"],
                    "value": point["value"],
                    "deviation_score": round(float(z_score), 3),
                    "severity": self._classify_severity(abs(z_score))
                })

        return anomalies

    # -----------------------------
    # IQR Detection
    # -----------------------------

    def _iqr_detection(self) -> List[Dict[str, Any]]:
        values = np.array([point["value"] for point in self.data])

        q1 = np.percentile(values, 25)
        q3 = np.percentile(values, 75)
        iqr = q3 - q1

        lower_bound = q1 - self.IQR_MULTIPLIER * iqr
        upper_bound = q3 + self.IQR_MULTIPLIER * iqr

        anomalies = []

        for point in self.data:
            if point["value"] < lower_bound or point["value"] > upper_bound:
                deviation = abs(point["value"] - np.median(values))
                anomalies.append({
                    "timestamp": point["timestamp"],
                    "value": point["value"],
                    "deviation_score": round(float(deviation), 3),
                    "severity": self._classify_severity(deviation)
                })

        return anomalies

    # -----------------------------
    # Severity Classification
    # -----------------------------

    def _classify_severity(self, deviation: float) -> str:
        """
        Classify anomaly severity based on deviation magnitude.
        """
        if deviation < self.Z_THRESHOLD:
            return "Minor"
        elif deviation < self.Z_THRESHOLD * 1.5:
            return "Moderate"
        else:
            return "Severe"

    # -----------------------------
    # Public Detection Method
    # -----------------------------

    def detect(self) -> Dict[str, Any]:
        """
        Execute anomaly detection using selected method.
        """

        if self.method == "zscore":
            anomalies = self._zscore_detection()
        else:
            anomalies = self._iqr_detection()

        summary = (
            f"{len(anomalies)} anomalies detected using {self.method.upper()} method."
            if anomalies else
            f"No significant anomalies detected using {self.method.upper()} method."
        )

        return {
            "metric_name": self.metric_name,
            "total_points": len(self.data),
            "anomalies_detected": len(anomalies),
            "anomaly_details": anomalies,
            "detection_method": self.method,
            "analysis_summary": summary
        }


# ---------------------------------------
# Example Standalone Execution
# ---------------------------------------

if __name__ == "__main__":

    sample_input = {
        "metric_name": "total_emission",
        "data": [
            {"timestamp": "2023-01", "value": 1000},
            {"timestamp": "2023-02", "value": 1020},
            {"timestamp": "2023-03", "value": 980},
            {"timestamp": "2023-04", "value": 2500},  # Spike anomaly
            {"timestamp": "2023-05", "value": 1010},
            {"timestamp": "2023-06", "value": 990}
        ]
    }

    try:
        detector = AnomalyDetector(sample_input, method="zscore")
        result = detector.detect()

        print("\n===== DIMDEA Anomaly Detection Report =====")
        for key, value in result.items():
            print(f"{key}: {value}")

    except Exception as e:
        print(f"Error: {e}")