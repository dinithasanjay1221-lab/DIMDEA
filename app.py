# ============================================================
# DIMDEA — AI Driven Carbon Neutralization Platform
# Final Integrated Version | Heat Map Added | Enhanced Visuals
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="DIMDEA", layout="wide")

# ============================================================
# SESSION STATE
# ============================================================
if "calculated" not in st.session_state:
    st.session_state.calculated = False

# ============================================================
# GLOBAL THEME + ADVANCED EARTH ANIMATION
# ============================================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Montserrat:wght@400;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 70% 40%, #0A1F44 0%, #050D1A 75%);
    color: white;
}

/* TITLE */
.dimdea-title {
    font-family: 'Cinzel', serif;
    font-size: 88px;
    letter-spacing: 7px;
    background: linear-gradient(90deg, #00D26A, #00CFFF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.gold-line {
    height: 4px;
    width: 300px;
    background: #FFB800;
    margin-top: 12px;
}

.tagline {
    font-family: 'Montserrat', sans-serif;
    font-size: 20px;
    margin-top: 25px;
    letter-spacing: 2px;
}

.feature-box {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(0,210,106,0.3);
    border-radius: 15px;
    padding: 18px;
    margin-top: 20px;
    backdrop-filter: blur(6px);
}

/* EARTH */
.earth-wrapper {
    position: relative;
    width: 520px;
    height: 520px;
    margin: auto;
}

.earth {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: url('https://upload.wikimedia.org/wikipedia/commons/9/97/The_Earth_seen_from_Apollo_17.jpg');
    background-size: cover;
    box-shadow:
        0 0 140px rgba(0,207,255,0.35),
        inset -60px -60px 120px rgba(0,0,0,0.9);
    animation: rotate 120s linear infinite;
    position: absolute;
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* COLOR CARBON LAYER */
.carbon-layer {
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    animation: carbonToGreen 8s ease-in-out infinite alternate;
}

@keyframes carbonToGreen {
    from {
        background:
        radial-gradient(circle at 35% 45%, rgba(198,40,40,0.7), transparent 55%),
        radial-gradient(circle at 65% 60%, rgba(198,40,40,0.6), transparent 60%);
    }
    to {
        background:
        radial-gradient(circle at 35% 45%, rgba(0,210,106,0.6), transparent 55%),
        radial-gradient(circle at 65% 60%, rgba(0,210,106,0.5), transparent 60%);
    }
}

/* ENERGY LINES */
.energy-lines {
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    border: 1px dashed rgba(0,207,255,0.5);
    animation: pulse 6s ease-in-out infinite;
}

@keyframes pulse {
    0% { opacity: 0.3; transform: scale(0.97); }
    50% { opacity: 0.7; transform: scale(1.03); }
    100% { opacity: 0.3; transform: scale(0.97); }
}

.metric-box {
    font-size: 18px;
    margin-top: 15px;
    color: #00D26A;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# NAVIGATION TABS
# ============================================================
tabs = st.tabs([
    "🌍 DIMDEA Home",
    "📊 Carbon Calculator",
    "📈 Analytics Dashboard"
])

# ============================================================
# CARBON SCORE FUNCTION
# ============================================================
def calculate_score(adjusted, intensity, renewable):

    emission_factor = max(0, 100 - adjusted * 0.05)
    intensity_factor = max(0, 100 - intensity * 10)
    renewable_factor = renewable

    score = (
        emission_factor * 0.4 +
        intensity_factor * 0.3 +
        renewable_factor * 0.3
    )

    return max(0, min(100, score))


# ============================================================
# HOME TAB
# ============================================================
with tabs[0]:

    col1, col2 = st.columns([1.1, 1])

    with col1:
        st.markdown('<div class="dimdea-title">DIMDEA</div>', unsafe_allow_html=True)
        st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)
        st.markdown('<div class="tagline">AI-Driven Carbon Neutralization Planning System</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-box">
            🌱 AI Carbon Forecasting Engine<br>
            🌍 Global Emission Heat Mapping<br>
            ⚡ Renewable Transition Simulation<br>
            📊 Net-Zero Strategy Optimization
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="metric-box">Projected CO₂ Reduction: 42%</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-box">Renewable Transition Acceleration: 67%</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="earth-wrapper">
            <div class="energy-lines"></div>
            <div class="earth"></div>
            <div class="carbon-layer"></div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# CARBON CALCULATOR
# ============================================================
with tabs[1]:

    st.title("📊 Carbon Data Input & Processing")

    ELECTRICITY_EF = 0.82
    FUEL_EF = 2.68

    col1, col2 = st.columns(2)

    with col1:
        electricity = st.number_input("Electricity (kWh)", min_value=0.0)
        fuel = st.number_input("Fuel (liters)", min_value=0.0)
        production = st.number_input("Production Units", min_value=0.0)

    with col2:
        renewable = st.slider("Renewable %", 0, 100)
        location = st.selectbox("Location", ["Chennai", "Mumbai", "Delhi", "Bangalore"])
        month = st.selectbox("Month", ["Jan","Feb","Mar","Apr","May","Jun"])

    if st.button("🚀 Calculate Emissions"):

        if production == 0:
            st.warning("Production cannot be zero")
            st.session_state.calculated = False

        else:
            scope1 = fuel * FUEL_EF
            scope2 = electricity * ELECTRICITY_EF
            total = scope1 + scope2

            adjusted = total * (1 - renewable/100)
            intensity = adjusted / production

            score = calculate_score(adjusted, intensity, renewable)

            st.session_state.calculated = True
            st.session_state.results = {
                "scope1": scope1,
                "scope2": scope2,
                "total": total,
                "adjusted": adjusted,
                "intensity": intensity,
                "score": score
            }

    if st.session_state.calculated:

        r = st.session_state.results

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Emissions", f"{r['total']:.2f}")
        k2.metric("Carbon Intensity", f"{r['intensity']:.2f}")
        k3.metric("Adjusted Emissions", f"{r['adjusted']:.2f}")
        k4.metric("Carbon Score", f"{r['score']:.1f}")

        # ==============================
        # BEAUTIFUL BAR
        # ==============================
        fig_bar = px.bar(
            x=["Scope 1","Scope 2"],
            y=[r["scope1"], r["scope2"]],
            color=["Scope 1","Scope 2"],
            color_discrete_sequence=["#00D26A","#00CFFF"],
            title="Emission Breakdown"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # ==============================
        # PIE
        # ==============================
        pie = px.pie(
            names=["Scope 1","Scope 2"],
            values=[r["scope1"], r["scope2"]],
            color_discrete_sequence=["#FF6B6B","#4ECDC4"],
            title="Emission Share"
        )
        st.plotly_chart(pie, use_container_width=True)

        # ==============================
        # DONUT ENERGY MIX
        # ==============================
        donut = px.pie(
            names=["Renewable","Non‑Renewable"],
            values=[renewable, 100-renewable],
            hole=0.6,
            color_discrete_sequence=["#00D26A","#FFB800"],
            title="Energy Mix"
        )
        st.plotly_chart(donut, use_container_width=True)

        # ==============================
        # GAUGE
        # ==============================
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=r["score"],
            title={'text': "Carbon Sustainability Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#00D26A"},
                'steps': [
                    {'range': [0, 40], 'color': "#FF4D4D"},
                    {'range': [40, 70], 'color': "#FFB800"},
                    {'range': [70, 100], 'color': "#00D26A"},
                ]
            }
        ))
        st.plotly_chart(gauge, use_container_width=True)


# ============================================================
# ANALYTICS DASHBOARD
# ============================================================
with tabs[2]:

    st.title("📈 Emission Analytics Dashboard")

    # SAMPLE DATA
    data = pd.DataFrame({
        "Country": ["India","USA","China","Germany","UK"],
        "Emissions":[250, 400, 500, 180, 120],
        "iso_alpha":["IND","USA","CHN","DEU","GBR"]
    })

        # ============================================================
    # 🌍 ADVANCED GLOBAL EMISSION HEAT MAP (ADDITIONAL FEATURE)
    # ============================================================

    st.subheader("🌍 Global Emission Intelligence Heat Map")

    heat_data = pd.DataFrame({
        "Country": ["India", "USA", "China", "Germany", "UK", "Brazil", "Australia"],
        "Emissions": [250, 400, 500, 180, 120, 210, 160],
        "iso_alpha": ["IND", "USA", "CHN", "DEU", "GBR", "BRA", "AUS"]
    })

    heat_map = px.choropleth(
        heat_data,
        locations="iso_alpha",
        color="Emissions",
        hover_name="Country",
        color_continuous_scale=[
            "#00FF9C",
            "#00CFFF",
            "#FFD166",
            "#FF6B6B",
            "#FF3B3B"
        ],
        title="Global Carbon Emission Distribution"
    )

    # Theme‑matching futuristic styling
    heat_map.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo=dict(
            bgcolor="rgba(0,0,0,0)",
            showframe=False,
            showcoastlines=True,
            coastlinecolor="#00CFFF",
            projection_type="natural earth",
            landcolor="rgba(20,30,60,0.6)",
            oceancolor="rgba(5,15,35,0.9)",
            showocean=True,
        ),
        title_font=dict(size=22, color="#00CFFF"),
        margin=dict(l=0, r=0, t=50, b=0)
    )

    st.plotly_chart(heat_map, use_container_width=True)

    # ==============================
    # SOURCE BAR
    # ==============================
    source = pd.DataFrame({
        "Source": ["Transport","Energy","Manufacturing","Waste"],
        "Emissions":[120, 300, 250, 90]
    })

    fig = px.bar(
        source,
        x="Source",
        y="Emissions",
        color="Emissions",
        color_continuous_scale=["green","red"],
        title="Top Emission Sources"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # TREND LINE
    # ==============================
    trend = pd.DataFrame({
        "Month":["Jan","Feb","Mar","Apr"],
        "Total":[400, 420, 390, 450]
    })

    fig2 = px.line(
        trend,
        x="Month",
        y="Total",
        markers=True,
        title="Monthly Emission Trend"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ============================================================
# END
# ============================================================