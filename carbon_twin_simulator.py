def simulate_lifestyle_change(distance, electricity, food):

    reduction = 0

    if distance > 5:
        reduction += distance * 0.15

    if electricity > 5:
        reduction += electricity * 0.2

    if food == "Non-Vegetarian":
        reduction += 2

    return round(reduction, 2)