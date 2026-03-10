def validate_positive_number(value):

    if value < 0:
        raise ValueError("Value cannot be negative")

    return value


def validate_food_type(food):

    allowed = ["Vegetarian", "Non-Vegetarian"]

    if food not in allowed:
        raise ValueError("Invalid food type")

    return food