import random


def predict_future_emissions(activity_data):

    if len(activity_data) == 0:
        return 0

    emissions = [item["emission"] for item in activity_data]

    avg = sum(emissions) / len(emissions)

    prediction = avg + random.uniform(-1, 1)

    return round(prediction * 7, 2)