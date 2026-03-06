import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- THEME & UI CONFIGURATION ---
def apply_climate_tech_theme():
    st.markdown(f"""
        <style>
        /* Main Background Gradient matching previous home screen */
        .stApp {{
            background: linear-gradient(160deg, #0F3D3E 0%, #081C1C 100%) !important;
            color: #FFFFFF !important;
        }}

        /* Clean UI: Removes default white/gray Streamlit containers */
        [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {{
            background: rgba(0,0,0,0) !important;
            display: none;
        }}
        
        /* Glassmorphism Card Design */
        .glass-card {{
            background: rgba(31, 171, 137, 0.15);
            border-radius: 12px;
            border: 1px solid rgba(0, 255, 171, 0.3);
            padding: 25px;
            margin-bottom: 25px;
            backdrop-filter: blur(12px);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        }}

        /* High Contrast Bold Typography */
        h1, h2, h3 {{
            color: #00FFAB !important; /* Mint Glow */
            font-weight: 800 !important;
            text-transform: uppercase;
        }}
        
        p, span, label, .stMetric {{
            color: #FFFFFF !important;
            font-weight: 700 !important; /* Extra bold for visibility */
        }}

        .stTable {{
            background-color: rgba(15, 61, 62, 0.8);
            border-radius: 10px;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- CORE INTELLIGENCE ENGINES ---

def anomaly_detection(data):
    # Identifies data points 1.5 standard deviations from mean
    threshold = data['value'].mean() + (1.5 * data['value'].std())
    return data[data['value'] > threshold]

def optimization_engine():
    """FIXED: Added required parentheses for function definition"""
    return [
        "Transition to 24/7 Carbon-Free Energy (CFE) matching.",
        "Optimize Scope 3 logistics via AI route-batching.",
        "Implement thermal storage to offset peak demand."
    ]

def xai_reasoning_layer(context):
    reasons = {
        "Risk": "Reasoning: Detected volatility in regional carbon credit pricing.",
        "Trend": "Reasoning: Correlation between humidity and HVAC load is > 0.85."
    }
    return reasons.get(context, "AI Logic: Grounded in ESG reporting standards.")

# --- DASHBOARD LAYOUT ---

def render_insights_dashboard():
    apply_climate_tech_theme()
    
    st.title("🌱 AI DECISION INTELLIGENCE")
    st.markdown("### DIMDEA Production Version 2.0")

    # Mock Data for Analysis
    dates = [datetime.now() - timedelta(days=x) for x in range(30)]
    df = pd.DataFrame({'date': dates, 'value': np.random.normal(50, 10, 30)})

    # 1. Anomaly Detection & 4. Risk Alerts
    anomalies = anomaly_detection(df)
    if not anomalies.empty:
        st.error(f"⚠️ **ADAPTIVE RISK ALERT:** {len(anomalies)} carbon flux anomalies detected.")

    # KPI Row: 7. Sustainability, 12. Decision Score, 8. Confidence
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.metric("Sustainability Score", "8