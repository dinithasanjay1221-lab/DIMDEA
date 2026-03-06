# settings.py

import streamlit as st


def render():

    st.title("⚙️ DIMDEA Settings")

    st.markdown("Configure system behavior and AI preferences.")

    # -----------------------------
    # Initialize Session State
    # -----------------------------
    if "baseline" not in st.session_state:
        st.session_state.baseline = 15000

    if "risk_threshold" not in st.session_state:
        st.session_state.risk_threshold = 70

    if "anomaly_sensitivity" not in st.session_state:
        st.session_state.anomaly_sensitivity = "Medium"

    if "enable_privacy_guard" not in st.session_state:
        st.session_state.enable_privacy_guard = True

    if "enable_ethical_ai" not in st.session_state:
        st.session_state.enable_ethical_ai = True

    if "optimization_preference" not in st.session_state:
        st.session_state.optimization_preference = "Balanced"

    # -----------------------------
    # Carbon Configuration
    # -----------------------------
    st.subheader("🌍 Carbon Configuration")

    st.session_state.baseline = st.number_input(
        "Default Baseline Emissions",
        min_value=1000,
        max_value=100000,
        value=st.session_state.baseline,
        step=500
    )

    st.session_state.risk_threshold = st.slider(
        "Risk Threshold Level (%)",
        min_value=0,
        max_value=100,
        value=st.session_state.risk_threshold
    )

    # -----------------------------
    # AI Configuration
    # -----------------------------
    st.subheader("🤖 AI Configuration")

    st.session_state.anomaly_sensitivity = st.selectbox(
        "Anomaly Detection Sensitivity",
        ["Low", "Medium", "High"],
        index=["Low", "Medium", "High"].index(st.session_state.anomaly_sensitivity)
    )

    st.session_state.optimization_preference = st.radio(
        "Optimization Preference",
        ["Cost Priority", "Sustainability Priority", "Balanced"],
        index=["Cost Priority", "Sustainability Priority", "Balanced"].index(
            st.session_state.optimization_preference
        )
    )

    # -----------------------------
    # Privacy & Ethics
    # -----------------------------
    st.subheader("🔐 Privacy & Ethical Controls")

    st.session_state.enable_privacy_guard = st.toggle(
        "Enable Privacy Guard",
        value=st.session_state.enable_privacy_guard
    )

    st.session_state.enable_ethical_ai = st.toggle(
        "Enable Ethical AI Monitoring",
        value=st.session_state.enable_ethical_ai
    )

    # -----------------------------
    # Save Confirmation
    # -----------------------------
    if st.button("💾 Save Settings"):
        st.success("Settings saved successfully!")

    # -----------------------------
    # Show Current Settings
    # -----------------------------
    st.markdown("---")
    st.subheader("📊 Current Configuration")

    st.json({
        "baseline": st.session_state.baseline,
        "risk_threshold": st.session_state.risk_threshold,
        "anomaly_sensitivity": st.session_state.anomaly_sensitivity,
        "optimization_preference": st.session_state.optimization_preference,
        "privacy_guard": st.session_state.enable_privacy_guard,
        "ethical_ai": st.session_state.enable_ethical_ai
    })