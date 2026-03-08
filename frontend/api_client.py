import requests

BASE_URL = "http://127.0.0.1:8000/api"


def calculate_emissions(data):

    response = requests.post(
        f"{BASE_URL}/calculate",
        json=data
    )

    return response.json()