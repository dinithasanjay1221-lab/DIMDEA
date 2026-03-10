def check_emission_threshold(total_emission):

    if total_emission > 20:
        return "⚠ High carbon emission detected today!"

    if total_emission > 10:
        return "⚠ Moderate emission level."

    return "✅ Your emissions are within a healthy range."