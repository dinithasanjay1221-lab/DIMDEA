import streamlit as st
from backend.carbon_calculator import calculate_total_emission
from backend.alerts_system import check_emission_threshold


def show_activity_input_page():

    st.title("Daily Activity Input")

    transport = st.number_input("Distance traveled (km)", 0.0)

    electricity = st.number_input("Electricity used (kWh)", 0.0)

    food = st.selectbox(
        "Food Type",
        ["Vegetarian", "Non-Vegetarian"]
    )

    if st.button("Calculate Carbon Footprint"):

        total = calculate_total_emission(
            transport,
            electricity,
            food
        )

        activity = {
            "transport": transport,
            "electricity": electricity,
            "food": food,
            "emission": total
        }

        st.session_state.activity_data.append(activity)
        st.session_state.total_emission += total

        st.success(f"Carbon Footprint: {total} kg CO₂")

        alert = check_emission_threshold(total)

        st.info(alert)