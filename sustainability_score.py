def calculate_sustainability_score(total_emission):

    if total_emission <= 5:
        score = 90
    elif total_emission <= 10:
        score = 70
    elif total_emission <= 20:
        score = 50
    else:
        score = 30

    return score