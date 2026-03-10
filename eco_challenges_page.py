import streamlit as st
from backend.gamification_engine import generate_challenges, calculate_points


def show_eco_challenges_page():

    st.title("Eco Challenges")

    challenges = generate_challenges()

    completed = 0

    for c in challenges:
        if st.checkbox(c):
            completed += 1

    points = calculate_points(completed)

    st.metric("Eco Points", points)