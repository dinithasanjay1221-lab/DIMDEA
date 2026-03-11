import streamlit as st
import pandas as pd
import numpy as np

# Backend API Client
from frontend.api_client import run_simulation

# Mock Backend Call (Fallback if backend fails)
def mock_simulator(reduction_val, year):
    """Simulates a data fetch from the backend."""
    years = np.arange(2024, year + 1)
    baseline = np.linspace(100, 100 + (year - 2024) * 2, len(years))
    simulated = baseline * (1 - (reduction_val / 100))
    return pd.DataFrame({"Year": years, "Baseline": baseline, "Simulated": simulated})


# --- UI Configuration & Styling ---
st.set_page_config(layout="wide", page_title="Climate-Tech Simulator")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #050C16 0%, #0A192F 100%) !important;
        color: #FFFFFF !important;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(0, 210, 255, 0.2);
        margin-bottom: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    }

    .stButton>button {
        background-color: #00D2FF;
        color: #0A192F;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        width: 100%;
    }

    .stButton>button:hover {
        background-color: #00FFAB;
        color: #050C16;
    }
    </style>
""", unsafe_allow_html=True)


# --- Layout Structure ---
left_col, right_col = st.columns([1, 2], gap="large")


# =========================================================
# LEFT PANEL (Controls)
# =========================================================
with left_col:

    st.markdown(
        """
        <div class="glass-card">
            <h2>Control Panel</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    carbon_reduction = st.slider("Carbon Reduction (%)", 0, 100, 20)
    energy_efficiency = st.slider("Energy Efficiency (%)", 0, 100, 15)

    target_year = st.select_slider(
        "Simulation Timeframe",
        options=[2030, 2040, 2050, 2060]
    )

    if st.button("Apply Simulation"):

        reduction_value = carbon_reduction + (energy_efficiency / 2)

        # Try Backend Simulation First
        results = run_simulation(reduction_value, target_year)

        # Fallback if backend not available
        if results is None:
            results = mock_simulator(reduction_value, target_year)

        st.session_state["results"] = results


# =========================================================
# RIGHT PANEL (Visualization)
# =========================================================
with right_col:

    if "results" in st.session_state:

        df = st.session_state["results"]

        # Projection Graph
        st.subheader("Simulation Projection")
        st.line_chart(df.set_index("Year"), color=["#00D2FF", "#00FFAB"])

        # Emission Delta Summary
        latest_baseline = df["Baseline"].iloc[-1]
        latest_sim = df["Simulated"].iloc[-1]

        delta = ((latest_baseline - latest_sim) / latest_baseline) * 100

        st.markdown(
            """
            <div class="glass-card">
                <h3>Emission Delta Summary</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        c1, c2 = st.columns(2)

        c1.metric(
            "Baseline Emission",
            f"{latest_baseline:.1f} Mt"
        )

        c2.metric(
            "Simulated Emission",
            f"{latest_sim:.1f} Mt",
            delta=f"-{delta:.1f}%",
            delta_color="normal"
        )

    else:
        st.info(
            "Adjust the parameters and click 'Apply Simulation' to view projections."
        )