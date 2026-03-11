import streamlit as st
from frontend import home, login, forgot_password
from frontend.navigation import render_navigation  # Use the unified navigation

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Carbon Footprint Platform",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# Load Global CSS
# -----------------------------
def load_css():
    try:
        with open("assets/styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css()

# -----------------------------
# Session State Initialization
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -----------------------------
# Router Function
# -----------------------------
def router():
    """
    Routes between public pages and protected pages with sidebar navigation.
    """
    if st.session_state.page == "home":
        home.render()

    elif st.session_state.page == "login":
        login.render()

    elif st.session_state.page == "forgot_password":
        forgot_password.render()

    else:
        # All other pages handled by navigation
        if st.session_state.logged_in:
            render_navigation()
        else:
            st.session_state.page = "home"
            st.experimental_rerun()

# -----------------------------
# Run Application
# -----------------------------
router()