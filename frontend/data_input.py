import streamlit as st
import sys, os

# Ensure Python can find the frontend package
sys.path.append(os.path.abspath("frontend"))

from frontend.api_client import calculate_emissions


def render():
    # --------------------------------------------------
    # CUSTOM CSS
    # --------------------------------------------------
    st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top, #0a192f, #020617);
        color: white;
    }
    .hero-title {
        font-size: 60px;
        font-weight: 900;
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
    }
    .hero-subtitle {
        font-size: 22px;
        color: #cbd5e1;
        text-align: center;
        margin-bottom: 40px;
    }
    .section-title {
        font-size: 30px;
        font-weight: 800;
        margin-top: 40px;
        margin-bottom: 20px;
        text-align: center;
        background: linear-gradient(90deg, #00c6ff, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 30px;
        border: none;
        display: block;
        margin: 0 auto;
    }
    .stButton>button:hover {
        box-shadow: 0px 0px 20px rgba(0,198,255,0.6);
    }
    </style>
    """, unsafe_allow_html=True)

    # --------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------
    st.markdown('<div class="hero-title">DIMDEA Data Input</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Enter organization activity data to begin carbon analysis</div>', unsafe_allow_html=True)

    # --------------------------------------------------
    # SCOPE 1 – DIRECT EMISSIONS
    # --------------------------------------------------
    st.markdown('<div class="section-title">🔥 Scope 1 – Direct Emissions</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        fuel_used = st.number_input("Fuel Consumption (liters)", min_value=0.0, step=1.0)
    with col2:
        vehicle_distance = st.number_input("Vehicle Distance Travelled (km)", min_value=0.0, step=1.0)

    # --------------------------------------------------
    # SCOPE 2 – ELECTRICITY
    # --------------------------------------------------
    st.markdown('<div class="section-title">⚡ Scope 2 – Electricity Emissions</div>', unsafe_allow_html=True)
    electricity = st.number_input("Electricity Consumption (kWh)", min_value=0.0, step=1.0)

    # --------------------------------------------------
    # SCOPE 3 – INDIRECT
    # --------------------------------------------------
    st.markdown('<div class="section-title">🌎 Scope 3 – Indirect Emissions</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        waste = st.number_input("Waste Generated (kg)", min_value=0.0, step=1.0)
    with col4:
        business_travel = st.number_input("Business Travel Distance (km)", min_value=0.0, step=1.0)

    # --------------------------------------------------
    # CALCULATE BUTTON
    # --------------------------------------------------
    if st.button("Calculate Emissions"):
        transportation = vehicle_distance + business_travel
        energy = electricity
        industrial = fuel_used + waste
        payload = {"transportation": transportation, "energy": energy, "industrial": industrial}

        try:
            result = calculate_emissions(payload)
            if isinstance(result, dict) and "total_emissions" in result:
                st.success(f"🌍 Total Emissions: {result['total_emissions']}")
            else:
                st.warning("⚠ Backend returned unexpected data.")
        except Exception as error:
            st.error(f"❌ Backend connection failed: {error}")

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------
    # SUBMIT BUTTON
    # --------------------------------------------------
    if st.button("🚀 Submit Data"):
        st.success("Data captured successfully! Proceed to dashboard analysis.")


if __name__ == "__main__":
    render()