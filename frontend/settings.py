# frontend/settings.py
import streamlit as st
import json
import os

# Page configuration
st.set_page_config(page_title="DIMDEA Settings", page_icon="⚙", layout="wide")

SETTINGS_FILE = "settings.json"

# ------------------------------ LOAD SETTINGS ------------------------------
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {}

saved_settings = load_settings()

# ------------------------------ INITIALIZE SESSION STATE ------------------------------
defaults = {
    "name": "",
    "email": "",
    "organization": "",
    "country": "India",
    "state": "",
    "city": "",
    "language": "English",
    "emission_alert": False,
    "hotspot_alert": False,
    "ai_alert": False,
    "weekly_report": False,
    "theme": "Dark Mode",
    "voice": False,
    "speech": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = saved_settings.get(key, value)

# ------------------------------ CSS THEME ------------------------------
st.markdown("""
<style>
:root {
    --primary: #050C16;
    --secondary: #0A192F;
    --accent: #00FFAB;
}
.stApp {
    background: linear-gradient(180deg, var(--primary) 0%, var(--secondary) 100%) !important;
    color: #FFFFFF !important;
}
h1, h2, h3 { color: #00D2FF !important; font-weight: 700 !important; text-transform: uppercase; }
hr { border: 1px solid rgba(0, 210, 255, 0.2); }
.stTextInput>div>input, .stSelectbox>div>div>select {
    background-color: rgba(255,255,255,0.05);
    color: #FFFFFF;
    border: 1px solid rgba(0,210,255,0.3);
    border-radius: 6px;
}
.stButton>button {
    background-color: #00D2FF !important;
    color: #0A192F !important;
    font-weight: 700;
    border-radius: 6px;
    border: none;
}
.stButton>button:hover {
    background-color: var(--accent) !important;
    color: var(--primary) !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------ TITLE ------------------------------
st.title("⚙ DIMDEA Settings")

# ------------------------------ PROFILE ------------------------------
st.subheader("👤 Profile")
st.session_state.name = st.text_input("Full Name", value=st.session_state.name)
st.session_state.email = st.text_input("Email", value=st.session_state.email)
st.session_state.organization = st.text_input("Organization", value=st.session_state.organization)
st.divider()

# ------------------------------ LOCATION ------------------------------
st.subheader("📍 Location")
countries = ["India", "USA", "UK", "Germany", "Australia"]
st.session_state.country = st.selectbox(
    "Country",
    countries,
    index=countries.index(st.session_state.country) if st.session_state.country in countries else 0
)
st.session_state.state = st.text_input("State / Region", value=st.session_state.state)
st.session_state.city = st.text_input("City", value=st.session_state.city)
st.divider()

# ------------------------------ LANGUAGE ------------------------------
st.subheader("🌐 Language")
languages = ["English", "Tamil", "Kannada", "Telugu", "Malayalam", "Hindi"]
st.session_state.language = st.selectbox(
    "Select Language",
    languages,
    index=languages.index(st.session_state.language) if st.session_state.language in languages else 0
)
st.divider()

# ------------------------------ NOTIFICATIONS ------------------------------
st.subheader("🔔 Notification Preferences")
st.session_state.emission_alert = st.checkbox("Emission Spike Alerts", value=st.session_state.emission_alert)
st.session_state.hotspot_alert = st.checkbox("Hotspot Alerts", value=st.session_state.hotspot_alert)
st.session_state.ai_alert = st.checkbox("AI Sustainability Recommendations", value=st.session_state.ai_alert)
st.session_state.weekly_report = st.checkbox("Weekly Sustainability Report", value=st.session_state.weekly_report)
st.divider()

# ------------------------------ THEME ------------------------------
st.subheader("🎨 Theme")
themes = ["Dark Mode", "Light Mode"]
st.session_state.theme = st.selectbox(
    "Theme Mode",
    themes,
    index=themes.index(st.session_state.theme) if st.session_state.theme in themes else 0
)
st.divider()

# ------------------------------ VOICE SETTINGS ------------------------------
st.subheader("🎙 Voice Settings")
st.session_state.voice = st.checkbox("Enable Voice Assistant", value=st.session_state.voice)
st.session_state.speech = st.checkbox("Enable Speech Recognition", value=st.session_state.speech)
st.divider()

# ------------------------------ SAVE SETTINGS ------------------------------
if st.button("Save Settings"):
    settings_data = {k: v for k, v in st.session_state.items() if k in defaults.keys()}
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings_data, f, indent=4)
    st.success("✅ Settings saved permanently!")