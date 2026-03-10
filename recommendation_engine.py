def generate_recommendations(activity_data):

    if len(activity_data) == 0:
        return ["Start logging your activities to get recommendations."]

    latest = activity_data[-1]

    suggestions = []

    if latest["transport"] > 10:
        suggestions.append("Use public transport or cycling to reduce emissions.")

    if latest["electricity"] > 8:
        suggestions.append("Reduce electricity usage and switch to energy-efficient appliances.")

    if latest["food"] == "Non-Vegetarian":
        suggestions.append("Try plant-based meals more often.")

    if len(suggestions) == 0:
        suggestions.append("Great job! Your lifestyle is eco-friendly.")

    return suggestions