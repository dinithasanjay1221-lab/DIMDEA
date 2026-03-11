import streamlit as st
import time
import sys
import os
import requests

# ------------------- PATH SETUP -------------------
sys.path.append(os.path.abspath("backend"))

from api.auth import validate_user, register_user, generate_otp
from frontend.forgot_password import forgot_password_ui  # relative import

# ------------------- SESSION STATE -------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0

if "lockout_time" not in st.session_state:
    st.session_state.lockout_time = None

if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False

if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = None

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="DIMDEA Auth", page_icon="🔵", layout="wide")

# ------------------- CSS -------------------
st.markdown("""
<style>
.stApp {background: radial-gradient(circle at top,#0a192f,#020617);color:white;}
.hero-title{font-size:80px;font-weight:900;background:linear-gradient(90deg,#00c6ff,#0072ff);
-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-top:50px;margin-bottom:10px;text-align:center;}
.hero-subtitle{font-size:22px;font-weight:800;color:#ffffff;text-align:center;margin-bottom:40px;}
label,p,.stMarkdown,[data-testid="stWidgetLabel"] p{color:#ffffff !important;font-weight:800 !important;font-size:1.1rem;}
.stTextInput>div>div>input{background-color:rgba(15,23,42,0.9);color:#ffffff;border:2px solid #00c6ff;}
.stButton>button{background:linear-gradient(90deg,#00c6ff,#0072ff);color:white;border:none;padding:12px 20px;
border-radius:10px;font-weight:900;font-size:18px;width:100%;}
button[data-baseweb="tab"] p{color:white;font-weight:800;}
.stTabs [data-baseweb="tab-list"]{justify-content:center;}
a{color:#00c6ff;text-decoration:none;font-weight:800;}
</style>
""", unsafe_allow_html=True)

# ------------------- LOGIN UI -------------------
def login_ui():
    st.markdown('<div class="hero-title">DIMDEA</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">ACCESS CONTROL SYSTEM</div>', unsafe_allow_html=True)

    _, col_mid, _ = st.columns([1, 1.5, 1])

    with col_mid:
        tab1, tab2 = st.tabs(["🔑 LOGIN", "📝 REGISTER"])

        # ---------- LOGIN ----------
        with tab1:
            identifier = st.text_input("USERNAME OR EMAIL", key="login_identifier")
            login_password = st.text_input("PASSWORD", type="password", key="login_password")

            st.write("---")
            st.markdown("**SECURITY VERIFICATION**")
            verify_choice = st.radio("", ["Email OTP", "SMS Code"], label_visibility="collapsed", key="login_verify_choice")

            if st.button("AUTHENTICATE", key="login_authenticate"):
                if validate_user(identifier, login_password):
                    st.session_state.generated_otp = generate_otp()
                    st.session_state.otp_sent = True
                    st.info(f"OTP SENT : {st.session_state.generated_otp}")
                else:
                    st.session_state.login_attempts += 1
                    if st.session_state.login_attempts >= 2:
                        st.session_state.lockout_time = time.time()
                        st.error("TOO MANY FAILED ATTEMPTS")
                        st.rerun()
                    else:
                        st.warning("INVALID CREDENTIALS")

            if st.session_state.otp_sent:
                otp_input = st.text_input("ENTER 6 DIGIT OTP", key="login_otp")
                if st.button("VERIFY OTP", key="login_verify_otp"):
                    if otp_input == st.session_state.generated_otp:
                        st.session_state.logged_in = True
                        st.success("LOGIN SUCCESS")
                        st.rerun()
                    else:
                        st.error("INVALID OTP")

            st.markdown("<div style='text-align:center;margin-top:15px;'>", unsafe_allow_html=True)
            if st.button("FORGOT PASSWORD?", key="login_forgot"):
                st.session_state.page = "forgot"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        # ---------- REGISTER ----------
        with tab2:
            reg_username = st.text_input("CHOOSE USERNAME", key="register_username")
            reg_password = st.text_input("CREATE PASSWORD", type="password", key="register_password")
            reg_email = st.text_input("EMAIL", key="register_email")
            reg_phone = st.text_input("PHONE NUMBER", key="register_phone")

            if st.button("COMPLETE REGISTRATION", key="register_submit"):
                ok = register_user(reg_username, reg_password, reg_email, reg_phone)
                if ok:
                    st.success("USER REGISTERED SUCCESSFULLY")
                else:
                    st.error("USER ALREADY EXISTS")

def render():
    if st.session_state.page == "login":
        login_ui()
    elif st.session_state.page == "forgot":
        forgot_password_ui()
    elif st.session_state.logged_in:
        from frontend import navigation
        navigation.run_navigation()

def render():
    login_ui()