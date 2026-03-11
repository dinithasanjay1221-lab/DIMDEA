"""
Ethical AI Engine
-----------------
Provides fairness evaluation, bias detection,
and ethical compliance checks for AI predictions.

Contains:
- Demographic Parity Check
- Equal Opportunity Check
- Bias Detection
- Explainability Summary
- Ethical Risk Scoring

No UI code included.
"""

from typing import List, Dict
from collections import defaultdict
from datetime import datetime
import logging


# -----------------------------------------------------
# ADDED: Logging (for backend monitoring)
# -----------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DIMDEA_ETHICAL_AI")


class EthicalAI:
    """
    Ethical AI evaluation engine.
    """

    # -----------------------------------------------------
    # ADDED: Safe Division Utility
    # -----------------------------------------------------
    @staticmethod
    def _safe_divide(a: float, b: float) -> float:
        if b == 0:
            return 0.0
        return a / b

    # -----------------------------------------------------
    # 1. Demographic Parity Check
    # -----------------------------------------------------
    @staticmethod
    def demographic_parity(
        predictions: List[int],
        sensitive_attributes: List[str]
    ) -> Dict[str, float]:
        """
        Checks whether positive prediction rate is similar across groups.
        """

        if len(predictions) != len(sensitive_attributes):
            raise ValueError("Predictions and sensitive attributes length mismatch.")

        if not predictions:
            return {}

        group_totals = defaultdict(int)
        group_positives = defaultdict(int)

        for pred, group in zip(predictions, sensitive_attributes):
            group_totals[group] += 1
            if pred == 1:
                group_positives[group] += 1

        rates = {}
        for group in group_totals:
            rates[group] = EthicalAI._safe_divide(
                group_positives[group],
                group_totals[group]
            )

        return rates

    # -----------------------------------------------------
    # 2. Equal Opportunity Check
    # -----------------------------------------------------
    @staticmethod
    def equal_opportunity(
        predictions: List[int],
        actuals: List[int],
        sensitive_attributes: List[str]
    ) -> Dict[str, float]:
        """
        Checks true positive rate across groups.
        """

        if not (len(predictions) == len(actuals) == len(sensitive_attributes)):
            raise ValueError("Input lists must have same length.")

        if not predictions:
            return {}

        group_tp = defaultdict(int)
        group_actual_positive = defaultdict(int)

        for pred, actual, group in zip(predictions, actuals, sensitive_attributes):
            if actual == 1:
                group_actual_positive[group] += 1
                if pred == 1:
                    group_tp[group] += 1

        tpr = {}
        for group in group_actual_positive:
            tpr[group] = EthicalAI._safe_divide(
                group_tp[group],
                group_actual_positive[group]
            )

        return tpr

    # -----------------------------------------------------
    # 3. Bias Detection (Threshold Based)
    # -----------------------------------------------------
    @staticmethod
    def detect_bias(metric: Dict[str, float], threshold: float = 0.1) -> bool:
        """
        Detects bias if difference between any two groups
        exceeds threshold.
        """

        values = list(metric.values())

        if not values:
            return False

        max_diff = max(values) - min(values)
        return max_diff > threshold

    # -----------------------------------------------------
    # 4. Explainability Summary
    # -----------------------------------------------------
    @staticmethod
    def explainability_summary(feature_importance: Dict[str, float]) -> List[str]:
        """
        Returns ranked feature importance explanation.
        """

        sorted_features = sorted(
            feature_importance.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )

        explanations = []

        for feature, score in sorted_features:
            explanations.append(
                f"Feature '{feature}' has influence score {round(score, 3)}"
            )

        return explanations

    # -----------------------------------------------------
    # 5. Ethical Risk Score
    # -----------------------------------------------------
    @staticmethod
    def ethical_risk_score(
        demographic_parity_bias: bool,
        equal_opportunity_bias: bool
    ) -> Dict[str, str]:
        """
        Calculates overall ethical risk classification.
        """

        risk_points = 0

        if demographic_parity_bias:
            risk_points += 1

        if equal_opportunity_bias:
            risk_points += 1

        if risk_points == 0:
            level = "Low Risk"
        elif risk_points == 1:
            level = "Moderate Risk"
        else:
            level = "High Risk"

        return {
            "risk_level": level,
            "risk_score": str(risk_points)
        }

    # -----------------------------------------------------
    # 6. Full Ethical Evaluation (Main Orchestrator)
    # -----------------------------------------------------
    def evaluate(
        self,
        predictions: List[int],
        actuals: List[int],
        sensitive_attributes: List[str],
        feature_importance: Dict[str, float]
    ) -> Dict[str, object]:
        """
        Runs full ethical AI evaluation pipeline.
        """

        logger.info("Running Ethical AI evaluation")

        # 1️⃣ Demographic Parity
        dp = self.demographic_parity(predictions, sensitive_attributes)

        # 2️⃣ Equal Opportunity
        eo = self.equal_opportunity(predictions, actuals, sensitive_attributes)

        # 3️⃣ Bias Detection
        dp_bias = self.detect_bias(dp)
        eo_bias = self.detect_bias(eo)

        # 4️⃣ Risk Score
        risk = self.ethical_risk_score(dp_bias, eo_bias)

        # 5️⃣ Explainability
        explanation = self.explainability_summary(feature_importance)

        result = {
            "demographic_parity": dp,
            "equal_opportunity": eo,
            "demographic_bias_detected": dp_bias,
            "equal_opportunity_bias_detected": eo_bias,
            "ethical_risk": risk,
            "explainability": explanation,

            # ADDED: Metadata for AI governance
            "evaluation_timestamp": datetime.utcnow().isoformat(),
            "engine": "DIMDEA Ethical AI Engine v1.0"
        }

        logger.info("Ethical AI evaluation complete")

        return result

    # -----------------------------------------------------
    # ADDED: API READY WRAPPER
    # -----------------------------------------------------
    def evaluate_for_api(
        self,
        predictions: List[int],
        actuals: List[int],
        sensitive_attributes: List[str],
        feature_importance: Dict[str, float]
    ) -> Dict[str, object]:
        """
        Wrapper designed for FastAPI endpoints.
        """

        try:
            return self.evaluate(
                predictions,
                actuals,
                sensitive_attributes,
                feature_importance
            )
        except Exception as e:

            logger.error(f"Ethical AI error: {str(e)}")

            return {
                "error": str(e),
                "engine": "DIMDEA Ethical AI Engine"
            }


# -----------------------------------------------------
# Example Usage (Safe to Run)
# -----------------------------------------------------
if __name__ == "__main__":

    engine = EthicalAI()

    # Sample AI outputs
    predictions = [1, 0, 1, 1, 0, 1, 0, 1]
    actuals =      [1, 0, 1, 0, 0, 1, 1, 1]
    sensitive =    ["A", "A", "B", "B", "A", "B", "A", "B"]

    print("\n--- Demographic Parity ---")
    dp = engine.demographic_parity(predictions, sensitive)
    print(dp)

    print("\n--- Equal Opportunity ---")
    eo = engine.equal_opportunity(predictions, actuals, sensitive)
    print(eo)

    dp_bias = engine.detect_bias(dp)
    eo_bias = engine.detect_bias(eo)

    print("\nBias Detected (DP):", dp_bias)
    print("Bias Detected (EO):", eo_bias)

    print("\n--- Ethical Risk Score ---")
    risk = engine.ethical_risk_score(dp_bias, eo_bias)
    print(risk)

    print("\n--- Explainability ---")

    feature_importance = {
        "age": 0.45,
        "income": 0.32,
        "education": 0.21,
        "zip_code": 0.05
    }

    explanations = engine.explainability_summary(feature_importance)

    for e in explanations:
        print(e)