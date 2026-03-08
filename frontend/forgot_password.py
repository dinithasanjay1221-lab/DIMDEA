import streamlit as st
from api.auth import generate_otp, update_password

def forgot_password_ui():

    st.title("RESET PASSWORD")

    identifier = st.text_input("USERNAME / EMAIL / PHONE")

    if st.button("SEND OTP"):

        otp = generate_otp()
        st.session_state.reset_otp = otp
        st.info(f"OTP SENT: {otp}")

    if "reset_otp" in st.session_state:

        otp_input = st.text_input("ENTER OTP")

        new_password = st.text_input("NEW PASSWORD", type="password")

        confirm_password = st.text_input("CONFIRM PASSWORD", type="password")

        if st.button("CHANGE PASSWORD"):

            if otp_input == st.session_state.reset_otp:

                if new_password == confirm_password:

                    update_password(identifier, new_password)

                    st.success("PASSWORD UPDATED")

                else:
                    st.error("PASSWORDS DO NOT MATCH")

            else:
                st.error("INVALID OTP")

    if st.button("BACK TO LOGIN"):
        st.session_state.page = "login"
        st.rerun()