import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from frontend.api_client import calculate_emissions


# PAGE CONFIG
st.set_page_config(
    page_title="DIMDEA | Carbon Intelligence Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------
# THEME (MATCHES home.py)
# --------------------------------------------------

st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp{
    background: radial-gradient(circle at top, #0a192f, #020617);
    color:white;
}

/* METRIC CARDS */

.metric-card{
    background: rgba(15,23,42,0.8);
    backdrop-filter: blur(10px);
    border-radius:18px;
    padding:22px;
    border:1px solid rgba(255,255,255,0.1);
    transition:0.4s;
}

.metric-card:hover{
    transform:translateY(-6px);
    box-shadow:0px 10px 30px rgba(0,198,255,0.35);
    border:1px solid #00c6ff;
}

/* TITLES */

.metric-title{
    font-size:14px;
    color:#22d3ee;
    font-weight:700;
    letter-spacing:1px;
}

.metric-value{
    font-size:28px;
    font-weight:800;
    color:#00c6ff;
}

.metric-desc{
    font-size:13px;
    color:#cbd5e1;
}

/* INSIGHT PANEL */

.insight-panel{
    background:rgba(15,23,42,0.8);
    border-left:4px solid #22d3ee;
    padding:14px;
    border-radius:6px;
    margin-bottom:12px;
}

.section-title{
    font-size:28px;
    font-weight:800;
    background:linear-gradient(90deg,#00c6ff,#22d3ee);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# MOCK DATA
# --------------------------------------------------

mock_data = {
    "total_emissions": 4250.8,
    "carbon_intensity": 0.42,
    "primary_hotspot": "Energy",
    "sustainability_score": 82,
    "sectors": ["Transportation","Energy","Industry","Waste","Renewable"],
    "emissions": [850,1600,1200,400,200],
    "esg": {"Environmental":78,"Social":85,"Governance":90},
    "hotspot_details":{
        "severity":"High",
        "contribution":"37.6%",
        "stress_indicator":0.85
    }
}

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown('<div class="section-title">Carbon Intelligence Dashboard</div>', unsafe_allow_html=True)

st.markdown("---")

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-title">TOTAL EMISSIONS</div>
    <div class="metric-value">{mock_data['total_emissions']} tCO₂e</div>
    <div class="metric-desc">Aggregate emissions across sectors</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-title">CARBON INTENSITY</div>
    <div class="metric-value">{mock_data['carbon_intensity']}</div>
    <div class="metric-desc">Emission rate relative to energy output</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-title">PRIMARY HOTSPOT</div>
    <div class="metric-value">{mock_data['primary_hotspot']}</div>
    <div class="metric-desc">Highest emission sector</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-title">SUSTAINABILITY SCORE</div>
    <div class="metric-value">{mock_data['sustainability_score']}/100</div>
    <div class="metric-desc">Overall ESG performance</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# --------------------------------------------------
# EMISSION ANALYTICS
# --------------------------------------------------

st.subheader("Sector Emission Analytics")

df = pd.DataFrame({
    "Sector": mock_data["sectors"],
    "Emission": mock_data["emissions"]
})

col1,col2 = st.columns(2)

with col1:

    fig = px.pie(
        df,
        values="Emission",
        names="Sector",
        hole=0.55,
        color_discrete_sequence=[
            "#00c6ff","#22d3ee","#38bdf8","#0ea5e9","#0284c7"
        ]
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(fig,use_container_width=True)

with col2:

    fig = px.bar(
        df.sort_values("Emission"),
        x="Emission",
        y="Sector",
        orientation="h",
        color="Emission",
        color_continuous_scale=["#22d3ee","#0072ff"]
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        showlegend=False
    )

    st.plotly_chart(fig,use_container_width=True)

# --------------------------------------------------
# HOTSPOT + CARBON DNA
# --------------------------------------------------

col_hot,col_dna = st.columns(2)

with col_hot:

    st.subheader("Hotspot Analysis")

    st.markdown(f"""
    <div class="metric-card">

    <b>Primary Sector :</b> {mock_data['primary_hotspot']}<br><br>

    <b>Severity :</b> <span style="color:#ff4b4b">{mock_data['hotspot_details']['severity']}</span><br><br>

    <b>Contribution :</b> {mock_data['hotspot_details']['contribution']}<br><br>

    <b>Stress Indicator :</b> {mock_data['hotspot_details']['stress_indicator']*100}%

    </div>
    """, unsafe_allow_html=True)


with col_dna:

    st.subheader("Carbon DNA")

    st.markdown("""
    <div class="metric-card">

    <b>Intensity Pattern</b><br>
    Cyclical / Industrial<br><br>

    <b>Baseline Comparison</b><br>
    <span style="color:#22d3ee">-12.4% vs Last Year</span>

    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# ESG
# --------------------------------------------------

st.write("")
st.subheader("Sustainability & ESG")

cols = st.columns(3)

for i,(k,v) in enumerate(mock_data["esg"].items()):

    with cols[i]:
        st.write(f"**{k} Score**")
        st.progress(v/100)
        st.caption(f"{v}%")

# --------------------------------------------------
# AI INSIGHTS
# --------------------------------------------------

st.write("")
st.subheader("AI Decision Insights")

insights=[
"Energy sector responsible for highest emissions (37.6%).",
"Industrial emissions exceed 2026 baseline by 5%.",
"Renewable adoption could reduce intensity by 18%."
]

for i in insights:
    st.markdown(f'<div class="insight-panel">{i}</div>', unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

c1,c2=st.columns(2)

with c1:
    st.caption("Source : DIMDEA Data Engine")

with c2:
    st.caption(f"Last Updated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

st.markdown("<center><small>DIMDEA v2.0 | Carbon Intelligence Platform</small></center>",unsafe_allow_html=True)
data = {
    "transportation": 20,
    "energy": 30,
    "industrial": 10
}

result = calculate_emissions(data)

st.metric("Total Emissions", result["total_emissions"])