# frontend/logout.py
import streamlit as st

def render():
    st.title("🚪 Logout")

    st.write("You have been logged out successfully.")

    # Reset login state
    st.session_state.logged_in = False
    st.session_state.page = "home"

    # Keep other data in session_state so it can be reused after login
    st.info("Return to Home. Please login again to access your dashboard.")

    # Optional button to go back immediately
    if st.button("Go to Home"):
        st.session_state.page = "home"
        st.experimental_rerun()