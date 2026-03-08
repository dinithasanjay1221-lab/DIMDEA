import streamlit as st
from streamlit_lottie import st_lottie
import requests

# 1. Page Config
st.set_page_config(page_title="DIMDEA Carbon Intelligence", layout="centered")

# 2. Asset Loader for Animated Earth
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_earth = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_m6cu9m9o.json")

# 3. Custom CSS (DIMDEA Dark Gradient Theme)
st.markdown(f"""
    <style>
    /* Gradient Background */
    .stApp {{
        background: linear-gradient(180deg, #050C16 0%, #0A192F 100%) !important;
        color: #FFFFFF !important;
    }}
    
    .chat-container {{
        background-color: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(0, 210, 255, 0.2);
    }}

    .user-msg {{
        text-align: right;
        background-color: #00D2FF;
        color: #0A192F;
        border-radius: 15px 15px 2px 15px;
        padding: 12px 18px;
        margin: 10px 0 10px auto;
        width: fit-content;
        max-width: 80%;
        font-weight: 600;
    }}

    .assistant-msg {{
        text-align: left;
        background-color: rgba(255, 255, 255, 0.08);
        color: #00FFAB;
        border-radius: 15px 15px 15px 2px;
        padding: 12px 18px;
        margin: 10px 0;
        width: fit-content;
        max-width: 80%;
        border: 1px solid rgba(0, 210, 255, 0.3);
        font-weight: 600;
    }}
    </style>
""", unsafe_allow_html=True)

# 4. Header with Animated Earth
col1, col2 = st.columns([1, 4])
with col1:
    if lottie_earth:
        st_lottie(lottie_earth, height=80, key="earth")
with col2:
    st.title("DIMDEA Carbon")
    st.caption("ESG Intelligence & Mobility Insights")

# 5. State & Logic
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def ai_chat_engine(input_text):
    return f"Analysis complete for: '{input_text}'. Integrating real-time ESG metrics..."

# 6. Chat Display
chat_placeholder = st.container()
with chat_placeholder:
    for chat in st.session_state.chat_history:
        div_class = "user-msg" if chat['role'] == 'user' else "assistant-msg"
        st.markdown(f"<div class='{div_class}'>{chat['message']}</div>", unsafe_allow_html=True)

# 7. Input
if prompt := st.chat_input("Query the DIMDEA database..."):
    st.session_state.chat_history.append({"role": "user", "message": prompt})
    response = ai_chat_engine(prompt)
    st.session_state.chat_history.append({"role": "assistant", "message": response})
    st.rerun()