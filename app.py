# main.py
import streamlit as st
from frontend import home, login, navigation, forgot_password

if "page" not in st.session_state:
    st.session_state.page = "home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def router():
    if st.session_state.page == "home":
        home.render()
    elif st.session_state.page == "login":
        login.render()
    elif st.session_state.page == "forgot_password":
        forgot_password.render()
    elif st.session_state.page == "navigation":
        if st.session_state.logged_in:
            navigation.render()
        else:
            st.session_state.page = "home"
            st.rerun()   # <-- use st.rerun

router()

def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()