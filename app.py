import streamlit as st

from frontend.home_page import show_home_page
from frontend.activity_input_page import show_activity_input_page
from frontend.dashboard_page import show_dashboard_page
from frontend.ai_insights_page import show_ai_insights_page
from frontend.eco_challenges_page import show_eco_challenges_page
from frontend.habit_tracker_page import show_habit_tracker_page


st.set_page_config(
    page_title="AI Personal Carbon Footprint Tracker",
    page_icon="🌍",
    layout="wide"
)

# Initialize session state

if "activity_data" not in st.session_state:
    st.session_state.activity_data = []

if "total_emission" not in st.session_state:
    st.session_state.total_emission = 0

if "habit_data" not in st.session_state:
    st.session_state.habit_data = []

st.sidebar.title("🌍 Carbon Tracker")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Activity Input",
        "Dashboard",
        "AI Insights",
        "Eco Challenges",
        "Habit Tracker"
    ]
)

if page == "Home":
    show_home_page()

elif page == "Activity Input":
    show_activity_input_page()

elif page == "Dashboard":
    show_dashboard_page()

elif page == "AI Insights":
    show_ai_insights_page()

elif page == "Eco Challenges":
    show_eco_challenges_page()

elif page == "Habit Tracker":
    show_habit_tracker_page()