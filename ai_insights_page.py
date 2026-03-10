import streamlit as st
from backend.ai_prediction_model import predict_future_emissions
from backend.recommendation_engine import generate_recommendations


def show_ai_insights_page():

    st.title("AI Insights")

    prediction = predict_future_emissions(
        st.session_state.activity_data
    )

    st.metric(
        "Predicted Weekly Emission",
        f"{prediction} kg CO₂"
    )

    tips = generate_recommendations(
        st.session_state.activity_data
    )

    for tip in tips:
        st.success(tip)