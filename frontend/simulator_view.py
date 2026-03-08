import streamlit as st
import pandas as pd
import numpy as np

# Mock Backend Call (Replace with your actual import)
# from backend.simulation import simulator

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
        /* Updated background to match DIMDEA dashboard style */
        background: linear-gradient(180deg, #050C16 0%, #0A192F 100%) !important;
        color: #FFFFFF !important;
    }
    /* Glassmorphism Card Style */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(0, 210, 255, 0.2);
        margin-bottom: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    }
    /* Custom Slider & Button Colors */
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

with left_col:
    st.markdown(
        """
        <div class="glass-card">
            <h2>Control Panel</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Reduction Sliders
    carbon_reduction = st.slider("Carbon Reduction (%)", 0, 100, 20)
    energy_efficiency = st.slider("Energy Efficiency (%)", 0, 100, 15)
    
    # Year Selector
    target_year = st.select_slider("Simulation Timeframe", options=[2030, 2040, 2050, 2060])
    
    # Action Button
    if st.button("Apply Simulation"):
        # Technical Workflow: Execute Backend Call
        results = mock_simulator(carbon_reduction + (energy_efficiency/2), target_year)
        st.session_state['results'] = results

with right_col:
    if 'results' in st.session_state:
        df = st.session_state['results']
        
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
        c1.metric("Baseline Emission", f"{latest_baseline:.1f} Mt")
        c2.metric("Simulated Emission", f"{latest_sim:.1f} Mt", delta=f"-{delta:.1f}%", delta_color="normal")
    else:
        st.info("Adjust the parameters and click 'Apply Simulation' to view projections.")