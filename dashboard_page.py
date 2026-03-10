import streamlit as st
import pandas as pd
from backend.sustainability_score import calculate_sustainability_score
from backend.carbon_twin_simulator import simulate_lifestyle_change


def show_dashboard_page():

    st.title("Carbon Dashboard")

    if not st.session_state.activity_data:
        st.warning("No data available.")
        return

    df = pd.DataFrame(st.session_state.activity_data)

    st.metric(
        "Total Emission",
        f"{round(st.session_state.total_emission,2)} kg"
    )

    score = calculate_sustainability_score(
        st.session_state.total_emission
    )

    st.write(f"Sustainability Score: {score}/100")

    st.bar_chart(df[["transport", "electricity"]])

    last = st.session_state.activity_data[-1]

    reduction = simulate_lifestyle_change(
        last["transport"],
        last["electricity"],
        last["food"]
    )

    st.success(
        f"You could reduce {reduction} kg CO₂ by improving habits."
    )