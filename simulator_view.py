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

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(180deg, #0F3D3E 0%, #081a1a 100%);
        color: white;
    }}
    /* Glassmorphism Card Style */
    .glass-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }}
    /* Custom Slider & Button Colors */
    .stButton>button {{
        background-color: #1FAB89;
        color: white;
        border-radius: 8px;
        border: none;
        width: 100%;
    }}
    .stButton>button:hover {{
        background-color: #00FFAB;
        color: #0F3D3E;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- Layout Structure ---
left_col, right_col = st.columns([1, 2], gap="large")

with left_col:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("Control Panel")
    
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
    
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    if 'results' in st.session_state:
        df = st.session_state['results']
        
        # Projection Graph
        st.subheader("Simulation Projection")
        st.line_chart(df.set_index("Year"), color=["#1FAB89", "#00FFAB"])
        
        # Emission Delta Summary
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        latest_baseline = df["Baseline"].iloc[-1]
        latest_sim = df["Simulated"].iloc[-1]
        delta = ((latest_baseline - latest_sim) / latest_baseline) * 100
        
        c1, c2 = st.columns(2)
        c1.metric("Baseline Emission", f"{latest_baseline:.1f} Mt")
        c2.metric("Simulated Emission", f"{latest_sim:.1f} Mt", delta=f"-{delta:.1f}%", delta_color="normal")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Adjust the parameters and click 'Apply Simulation' to view projections.")