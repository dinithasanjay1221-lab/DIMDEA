import streamlit as st
import time

# --- INITIAL SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0
if "lockout_time" not in st.session_state:
    st.session_state.lockout_time = None

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Dimdea Auth", page_icon="🔵", layout="wide")

# --- CUSTOM CSS (HIGH VISIBILITY WHITE & BOLD) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: radial-gradient(circle at top, #0a192f, #020617);
        color: white;
    }

    /* Centered Large Blue Title */
    .hero-title {
        font-size: 80px;
        font-weight: 900;
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 50px;
        margin-bottom: 10px;
        text-align: center;
        filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.8));
    }

    .hero-subtitle {
        font-size: 22px;
        font-weight: 800;
        color: #ffffff !important;
        text-align: center;
        margin-bottom: 40px;
    }

    /* Force all labels and text to be White and Bold */
    label, p, .stMarkdown, [data-testid="stWidgetLabel"] p {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
    }

    /* Input Field Styling */
    .stTextInput>div>div>input {
        background-color: rgba(15, 23, 42, 0.9);
        color: #ffffff !important;
        font-weight: 700 !important;
        border: 2px solid #00c6ff;
    }

    /* Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: #ffffff !important;
        border: none;
        padding: 12px 20px;
        border-radius: 10px;
        font-weight: 900 !important;
        font-size: 18px !important;
        width: 100%;
        text-transform: uppercase;
        box-shadow: 0px 4px 15px rgba(0, 198, 255, 0.4);
    }

    /* Tab Text Visibility */
    button[data-baseweb="tab"] p {
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
    }
    
    a { 
        color: #00c6ff !important; 
        text-decoration: none; 
        font-weight: 800;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BACKEND MOCK FUNCTION ---
def validate_user(username, password):
    return username == "admin" and password == "password123"

# --- AUTHENTICATION UI ---
def login_ui():
    st.markdown('<div class="hero-title">DIMDEA</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">ACCESS CONTROL SYSTEM</div>', unsafe_allow_html=True)

    if st.session_state.lockout_time:
        elapsed = time.time() - st.session_state.lockout_time
        if elapsed < 30:
            st.error(f"ACCOUNT LOCKED. Please try again in {int(30 - elapsed)} seconds.")
            return
        else:
            st.session_state.login_attempts = 0
            st.session_state.lockout_time = None

    _, col_mid, _ = st.columns([1, 1.5, 1])

    with col_mid:
        tab1, tab2 = st.tabs(["🔑 LOGIN", "📝 REGISTER"])

        with tab1:
            user = st.text_input("USERNAME", placeholder="Enter your username", key="l_user")
            pwd = st.text_input("PASSWORD", type="password", placeholder="••••••••", key="l_pwd")
            
            st.write("---")
            st.markdown("**SECURITY VERIFICATION**")
            verify_choice = st.radio("", ["Email OTP", "SMS Code"], label_visibility="collapsed")
            
            if st.button("AUTHENTICATE"):
                if validate_user(user, pwd):
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.session_state.login_attempts += 1
                    if st.session_state.login_attempts >= 2:
                        st.session_state.lockout_time = time.time()
                        st.error("TOO MANY FAILED ATTEMPTS. LOCKOUT ACTIVATED.")
                        st.rerun()
                    else:
                        st.warning("INVALID CREDENTIALS. ONE ATTEMPT REMAINING.")
            
            st.markdown("<div style='text-align: center; margin-top:15px;'><a href='#'>FORGOT PASSWORD?</a></div>", unsafe_allow_html=True)

        with tab2:
            st.text_input("CHOOSE USERNAME", key="r_user")
            st.text_input("CREATE PASSWORD", type="password", key="r_pwd")
            st.text_input("CONFIRM PASSWORD", type="password", key="r_conf")
            if st.button("COMPLETE REGISTRATION"):
                st.info("REGISTRATION SUBMITTED FOR APPROVAL.")

# --- MAIN APP FLOW ---
if not st.session_state.logged_in:
    login_ui()
else:
    # --- FIX APPLIED HERE ---
    try:
        import home
        home.render()
    except Exception as e:
        st.success("AUTHENTICATED SUCCESSFULLY!")
        st.write("Ensure 'home.py' exists in your folder to load the dashboard.")