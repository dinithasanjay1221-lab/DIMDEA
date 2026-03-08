"""
optimization_engine.py

Backend optimization engine for DIMDEA.
Contains linear programming and ML-based optimization utilities.
No UI, no API routes, no hardcoded data.
"""

from typing import List, Dict, Any
import numpy as np
from scipy.optimize import linprog
from sklearn.linear_model import LinearRegression


def _validate_non_negative_list(values: List[float], name: str) -> np.ndarray:
    if not isinstance(values, list) or len(values) == 0:
        raise ValueError(f"{name} must be a non-empty list.")

    for v in values:
        if not isinstance(v, (int, float)):
            raise ValueError(f"All elements in {name} must be numeric.")
        if v < 0:
            raise ValueError(f"All elements in {name} must be non-negative.")

    return np.array(values, dtype=float)


def _validate_positive_number(value: float, name: str) -> float:
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric.")
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")
    return float(value)


def optimize_emission_reduction(
    cost_coefficients: List[float],
    reduction_potentials: List[float],
    budget: float
) -> Dict[str, Any]:

    costs = _validate_non_negative_list(cost_coefficients, "cost_coefficients")
    reductions = _validate_non_negative_list(reduction_potentials, "reduction_potentials")
    budget = _validate_positive_number(budget, "budget")

    if len(costs) != len(reductions):
        raise ValueError("cost_coefficients and reduction_potentials must have same length.")

    n = len(costs)

    c = costs
    A_ub = [costs]
    b_ub = [budget]
    bounds = [(0, 1) for _ in range(n)]

    result = linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    if not result.success:
        return {
            "optimal_allocation": [],
            "minimum_cost": 0.0,
            "status": result.message,
        }

    allocation = result.x.tolist()
    minimum_cost = float(np.dot(costs, result.x))

    return {
        "optimal_allocation": allocation,
        "minimum_cost": minimum_cost,
        "status": result.message,
    }


def optimize_for_target_reduction(
    reduction_potentials: List[float],
    target_reduction: float
) -> Dict[str, Any]:

    reductions = _validate_non_negative_list(reduction_potentials, "reduction_potentials")
    target = _validate_positive_number(target_reduction, "target_reduction")

    n = len(reductions)

    c = np.ones(n)
    A_ub = [-reductions]
    b_ub = [-target]
    bounds = [(0, 1) for _ in range(n)]

    result = linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    if not result.success:
        return {
            "optimal_allocation": [],
            "achieved_reduction": 0.0,
            "status": result.message,
        }

    allocation = result.x.tolist()
    achieved_reduction = float(np.dot(reductions, result.x))

    return {
        "optimal_allocation": allocation,
        "achieved_reduction": achieved_reduction,
        "status": result.message,
    }


def train_reduction_model(X: np.ndarray, y: np.ndarray) -> LinearRegression:

    if not isinstance(X, np.ndarray) or not isinstance(y, np.ndarray):
        raise ValueError("X and y must be numpy arrays.")

    if X.ndim != 2:
        raise ValueError("X must be a 2D array.")

    if y.ndim != 1:
        raise ValueError("y must be a 1D array.")

    if X.shape[0] != y.shape[0]:
        raise ValueError("X and y must have the same number of samples.")

    if X.shape[0] == 0:
        raise ValueError("Training data cannot be empty.")

    model = LinearRegression()
    model.fit(X, y)

    return model


# =========================
# TEST BLOCK
# =========================

if __name__ == "__main__":

    print("=== Testing optimize_emission_reduction ===")
    costs = [100, 150, 200]
    reductions = [10, 20, 30]
    budget = 300

    result1 = optimize_emission_reduction(costs, reductions, budget)
    print(result1)

    print("\n=== Testing optimize_for_target_reduction ===")
    target = 25
    result2 = optimize_for_target_reduction(reductions, target)
    print(result2)

    print("\n=== Testing train_reduction_model ===")
    X = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
    y = np.array([10, 15, 20, 25])

    model = train_reduction_model(X, y)
    prediction = model.predict(np.array([[5, 6]]))

    print("Prediction for [5,6]:", prediction)