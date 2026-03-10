def calculate_average_emission(activity_data):

    if not activity_data:
        return 0

    emissions = [item["emission"] for item in activity_data]

    return round(sum(emissions) / len(emissions), 2)


def format_co2(value):

    return f"{round(value,2)} kg CO₂"