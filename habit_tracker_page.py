import streamlit as st
import pandas as pd


def show_habit_tracker_page():

    st.title("Habit Tracker")

    walk = st.checkbox("Walk instead of driving")

    vegetarian = st.checkbox("Eat vegetarian meals")

    energy = st.checkbox("Save electricity")

    if st.button("Save Habit"):

        habit = {
            "walk": walk,
            "vegetarian": vegetarian,
            "energy": energy
        }

        st.session_state.habit_data.append(habit)

        st.success("Habit saved")

    if st.session_state.habit_data:

        df = pd.DataFrame(st.session_state.habit_data)

        st.dataframe(df)