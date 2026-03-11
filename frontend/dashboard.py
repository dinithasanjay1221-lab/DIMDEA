import streamlit as st
from frontend import api_client
import pandas as pd
import plotly.express as px
from datetime import datetime
from frontend.api_client import calculate_emissions, get_ai_insights

# --------------------------------------------------
# ADDED: BACKEND STATUS CHECK
# --------------------------------------------------

import requests


def get_hotspot_data():
    try:
        url = "http://127.0.0.1:8000/hotspot-analysis"

        payload = {
            "transportation": 20,
            "energy": 30,
            "industrial": 10,
            "waste": 5,
            "renewable": 2,
            "baseline": 15000
        }

        r = requests.post(url, json=payload, timeout=5)

        if r.status_code == 200:
            return r.json()

    except:
        return None


def check_backend():
    try:
        r = requests.get("http://127.0.0.1:8000", timeout=3)
        if r.status_code == 200:
            return True
    except Exception:
        return False
    return False


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="DIMDEA | Carbon Intelligence Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------
# BACKEND STATUS INDICATOR
# --------------------------------------------------

backend_running = check_backend()

hotspot_data = None

if backend_running:
    hotspot_data = get_hotspot_data()

if backend_running:
    st.success("Backend Connected")
else:
    st.warning("Backend Not Running")


# --------------------------------------------------
# THEME
# --------------------------------------------------

st.markdown("""
<style>

.stApp{
    background: radial-gradient(circle at top, #0a192f, #020617);
    color:white;
}

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
# USE BACKEND HOTSPOT DATA IF AVAILABLE
# --------------------------------------------------

primary_hotspot = mock_data["primary_hotspot"]
sector_df = pd.DataFrame({
    "Sector": mock_data["sectors"],
    "Emission": mock_data["emissions"]
})

severity = mock_data["hotspot_details"]["severity"]
contribution = mock_data["hotspot_details"]["contribution"]
stress_indicator = mock_data["hotspot_details"]["stress_indicator"]

if hotspot_data:

    primary_hotspot = hotspot_data.get("primary_hotspot", primary_hotspot)

    sector_contribution = hotspot_data.get("sector_contribution_percent")

    if sector_contribution:
        sector_df = pd.DataFrame({
            "Sector": list(sector_contribution.keys()),
            "Emission": list(sector_contribution.values())
        })

    severity_levels = hotspot_data.get("severity_levels")

    if severity_levels and primary_hotspot in severity_levels:
        severity = severity_levels[primary_hotspot]

    if sector_contribution and primary_hotspot in sector_contribution:
        contribution = f"{sector_contribution[primary_hotspot]}%"

    stress_indicator = hotspot_data.get("overall_risk_score", stress_indicator)


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
    <div class="metric-value">{primary_hotspot}</div>
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

col1,col2 = st.columns(2)

with col1:

    fig = px.pie(
        sector_df,
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
        sector_df.sort_values("Emission"),
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

    <b>Primary Sector :</b> {primary_hotspot}<br><br>

    <b>Severity :</b> <span style="color:#ff4b4b">{severity}</span><br><br>

    <b>Contribution :</b> {contribution}<br><br>

    <b>Stress Indicator :</b> {stress_indicator}

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

backend_insights = get_ai_insights()

if backend_insights:

    insights=[
        backend_insights["forecast"],
        f"Priority Strategy: {backend_insights['priority']}",
        f"Sustainability Score: {backend_insights['sustainability_score']}"
    ]

else:

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

# --------------------------------------------------
# ORIGINAL BACKEND CALL (NOT MODIFIED)
# --------------------------------------------------

data = {
    "transportation": 20,
    "energy": 30,
    "industrial": 10
}

result = calculate_emissions(data)

# ADDED SAFE CHECK
if result:
    st.metric("Total Emissions", result["total_emissions"])
else:
    st.warning("Backend not running or API error.")

# --------------------------------------------------
# ROUTING INSIGHTS ANALYTICS (ADDED)
# --------------------------------------------------

st.write("")
st.subheader("Routing Optimization Insights")

routing_payload = {
    "total_distance": 1500,
    "total_time": 120,
    "total_emissions": 900,
    "fuel_consumption": 300,
    "number_of_routes": 3,
    "route_breakdown": [
        {"route_id": "R1", "distance": 500, "time": 40, "emissions": 300},
        {"route_id": "R2", "distance": 600, "time": 50, "emissions": 400},
        {"route_id": "R3", "distance": 400, "time": 30, "emissions": 200}
    ]
}

routing_result = api_client.routing_insights(routing_payload)

if routing_result:

    efficiency = routing_result.get("efficiency_metrics", {})
    carbon = routing_result.get("carbon_analysis", {})
    time_analysis = routing_result.get("time_analysis", {})
    risks = routing_result.get("risk_flags", [])
    summary = routing_result.get("insight_summary", "")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="metric-card">
        <div class="metric-title">Emission Intensity</div>
        <div class="metric-value">{}</div>
        <div class="metric-desc">CO₂ per km</div>
        </div>
        """.format(carbon.get("emission_intensity_per_km",0)), unsafe_allow_html=True)

        st.markdown("""
        <div class="metric-card">
        <div class="metric-title">Carbon Efficiency</div>
        <div class="metric-value">{}</div>
        <div class="metric-desc">Threshold check</div>
        </div>
        """.format(carbon.get("carbon_efficient",False)), unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="metric-card">
        <div class="metric-title">Average Route Time</div>
        <div class="metric-value">{}</div>
        <div class="metric-desc">Minutes per route</div>
        </div>
        """.format(time_analysis.get("average_route_time",0)), unsafe_allow_html=True)

        st.markdown("""
        <div class="metric-card">
        <div class="metric-title">Time Imbalance</div>
        <div class="metric-value">{}</div>
        <div class="metric-desc">Route distribution stability</div>
        </div>
        """.format(time_analysis.get("time_imbalance_detected",False)), unsafe_allow_html=True)

    st.write("")
    st.subheader("Operational Risk Flags")

    if risks:
        for r in risks:
            st.warning(r)
    else:
        st.success("No routing risks detected")

    st.write("")
    st.subheader("Routing Insight Summary")

    st.markdown(f'<div class="insight-panel">{summary}</div>', unsafe_allow_html=True)

else:
    st.warning("Routing insights service unavailable.")