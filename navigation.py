import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="DIMDEA", page_icon="🌍", layout="wide")

# --------------------------------------------------
# GLOBAL THEME (COPIED FROM HOME.PY)
# --------------------------------------------------
st.markdown("""
<style>

/* Main Background */
.stApp {
    background: radial-gradient(circle at top, #0a192f, #020617);
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* Sidebar Text */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Gradient Title */
.gradient-title {
    font-size: 40px;
    font-weight: 800;
    background: linear-gradient(90deg, #00c6ff, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 20px;
}

/* Glass Card */
.glass-card {
    background: rgba(15, 23, 42, 0.8);
    padding: 25px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.1);
    transition: 0.3s ease;
}

.glass-card:hover {
    box-shadow: 0px 10px 30px rgba(0,198,255,0.4);
    border: 1px solid #00c6ff;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 10px;
    border: none;
}

.stButton>button:hover {
    box-shadow: 0px 0px 20px rgba(0,198,255,0.6);
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------
st.sidebar.markdown("## 🌍 DIMDEA Navigation")

page = st.sidebar.radio("Go to", [
    "Home",
    "Emission Input",
    "Carbon DNA",
    "Routing",
    "Simulator",
    "Insights",
    "Help"
])

# --------------------------------------------------
# HOME
# --------------------------------------------------
if page == "Home":
    st.markdown('<div class="gradient-title">DIMDEA Dashboard</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
    Welcome to DIMDEA – AI-Driven Carbon Neutralization Planning System.
    Use the sidebar to navigate across modules.
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# EMISSION INPUT
# --------------------------------------------------
elif page == "Emission Input":
    st.markdown('<div class="gradient-title">Emission Data Input</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        t = st.number_input("Transportation Emission (tons CO2)", min_value=0.0, value=50.0)
        i = st.number_input("Industrial Emission (tons CO2)", min_value=0.0, value=80.0)
        e = st.number_input("Energy Emission (tons CO2)", min_value=0.0, value=100.0)

        st.info("Demo mode — no backend calculations connected.")

        st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# CARBON DNA
# --------------------------------------------------
elif page == "Carbon DNA":
    st.markdown('<div class="gradient-title">Carbon DNA Analyzer</div>', unsafe_allow_html=True)

    labels = ["Transportation", "Industry", "Energy"]
    values = [50, 80, 100]

    fig, ax = plt.subplots()
    ax.pie(values,
           labels=labels,
           autopct="%1.1f%%",
           colors=["#00c6ff", "#22d3ee", "#00d26a"])
    fig.patch.set_facecolor("#020617")

    st.pyplot(fig)

# --------------------------------------------------
# ROUTING
# --------------------------------------------------
elif page == "Routing":
    st.markdown('<div class="gradient-title">Routing & Optimization</div>', unsafe_allow_html=True)

    st.image("https://via.placeholder.com/700x400.png?text=Baseline+vs+Optimized+Route",
             use_container_width=True)

# --------------------------------------------------
# SIMULATOR
# --------------------------------------------------
elif page == "Simulator":
    st.markdown('<div class="gradient-title">Emission Reduction Simulator</div>', unsafe_allow_html=True)

    traffic = st.slider("Traffic Level", 0, 100, 50)
    fuel = st.slider("Fuel Efficiency (%)", 0, 100, 70)
    renewable = st.slider("Renewable Energy (%)", 0, 100, 30)

    reduction = round((fuel * 0.3 + renewable * 0.5 - traffic * 0.1), 1)
    st.metric("Estimated CO2 Reduction", f"{reduction}%")

# --------------------------------------------------
# INSIGHTS
# --------------------------------------------------
elif page == "Insights":
    st.markdown('<div class="gradient-title">Insights & Reports</div>', unsafe_allow_html=True)

    df = pd.DataFrame({
        "Sector": ["Transportation", "Industry", "Energy"],
        "CO2": [50, 80, 100]
    })

    st.bar_chart(df.set_index("Sector"))

# --------------------------------------------------
# HELP
# --------------------------------------------------
elif page == "Help":
    st.markdown('<div class="gradient-title">Help / About DIMDEA</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
    DIMDEA is a modular Climate Intelligence Platform prototype.
    This navigation demo is frontend-only.
    </div>
    """, unsafe_allow_html=True)