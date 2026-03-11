# frontend/logout.py
import streamlit as st

def render():
    st.title("🚪 Logout")

    st.write("You have been logged out successfully.")

    # ------------------- SAFE RESET -------------------
    if "logged_in" in st.session_state:
        st.session_state.logged_in = False
    else:
        st.session_state.logged_in = False

    if "page" in st.session_state:
        st.session_state.page = "home"
    else:
        st.session_state.page = "home"

    # Keep other data in session_state so it can be reused after login
    st.info("Return to Home. Please login again to access your dashboard.")

    # ------------------- IMMEDIATE NAVIGATION -------------------
    if st.button("Go to Home"):
        st.session_state.page = "home"
        st.experimental_rerun()