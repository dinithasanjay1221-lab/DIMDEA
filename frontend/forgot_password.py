# frontend/forgot_password.py
import streamlit as st
from api.auth import generate_otp, update_password

def forgot_password_ui():

    st.title("RESET PASSWORD")

    identifier = st.text_input("USERNAME / EMAIL / PHONE", key="fp_identifier")

    # ------------------- SEND OTP -------------------
    if st.button("SEND OTP", key="fp_send_otp"):
        otp = generate_otp()
        st.session_state.reset_otp = otp
        st.info(f"OTP SENT: {otp}")

    # ------------------- RESET SECTION -------------------
    if "reset_otp" in st.session_state:

        otp_input = st.text_input("ENTER OTP", key="fp_otp_input")

        new_password = st.text_input("NEW PASSWORD", type="password", key="fp_new_password")

        confirm_password = st.text_input("CONFIRM PASSWORD", type="password", key="fp_confirm_password")

        if st.button("CHANGE PASSWORD", key="fp_change_password"):

            if otp_input == st.session_state.reset_otp:

                if new_password == confirm_password:

                    update_password(identifier, new_password)

                    st.success("PASSWORD UPDATED")

                    # Clear OTP after success
                    st.session_state.pop("reset_otp", None)

                else:
                    st.error("PASSWORDS DO NOT MATCH")

            else:
                st.error("INVALID OTP")

    # ------------------- BACK TO LOGIN -------------------
    if st.button("BACK TO LOGIN", key="fp_back_login"):
        st.session_state.page = "login"
        st.rerun()