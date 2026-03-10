import json
import os

DATA_PATH = os.path.join("data", "emission_factors.json")


def load_emission_factors():
    try:
        with open(DATA_PATH) as f:
            return json.load(f)
    except:
        return {
            "car_per_km": 0.21,
            "electricity_per_kwh": 0.85,
            "vegetarian_meal": 1.5,
            "non_vegetarian_meal": 5.0
        }


def calculate_total_emission(distance_km, electricity_kwh, food_type):

    factors = load_emission_factors()

    transport = distance_km * factors["car_per_km"]
    electricity = electricity_kwh * factors["electricity_per_kwh"]

    if food_type == "Vegetarian":
        food = factors["vegetarian_meal"]
    else:
        food = factors["non_vegetarian_meal"]

    return round(transport + electricity + food, 2)