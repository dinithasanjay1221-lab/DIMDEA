import streamlit as st

def render():

    # ------------------- PAGE CONFIG -------------------
    st.set_page_config(
        page_title="DIMDEA",
        page_icon="🌍",
        layout="wide"
    )

    # ------------------- CUSTOM CSS -------------------
    st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top, #0a192f, #020617);
        color: white;
    }

    /* LOGIN BUTTON STYLE */
    div.stButton > button {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 18px;
        font-weight: 600;
        transition: 0.3s;
    }

    div.stButton > button:hover {
        background: linear-gradient(90deg, #22d3ee, #2563eb);
        transform: scale(1.05);
    }

    .hero-title {
        font-size: 70px;
        font-weight: 900;
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        text-align: center;
    }

    .hero-subtitle {
        font-size: 24px;
        color: #cbd5e1;
        margin-bottom: 15px;
        text-align: center;
    }

    .hero-tagline {
        font-size: 18px;
        color: #94a3b8;
        margin-bottom: 40px;
        text-align: center;
    }

    .earth-wrapper {
        position: relative;
        width: 480px;
        height: 480px;
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
        animation: rotateEarth 120s linear infinite;
        position: absolute;
    }

    @keyframes rotateEarth {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

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

    .section-title {
        font-size: 34px;
        font-weight: 800;
        margin-top: 60px;
        margin-bottom: 25px;
        text-align: center;
        background: linear-gradient(90deg, #00c6ff, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .feature-card {
        background: rgba(15, 23, 42, 0.8);
        padding: 25px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.1);
        transition: 0.4s ease;
        height: 190px;
    }

    .feature-card:hover {
        transform: translateY(-6px);
        box-shadow: 0px 10px 30px rgba(0, 198, 255, 0.4);
        border: 1px solid #00c6ff;
    }

    .feature-title {
        font-size: 20px;
        font-weight: 700;
        color: #22d3ee;
        margin-bottom: 10px;
    }

    .feature-desc {
        font-size: 15px;
        color: #cbd5e1;
    }

    .footer {
        text-align: center;
        margin-top: 80px;
        padding-bottom: 40px;
        font-size: 15px;
        color: #64748b;
    }

    </style>
    """, unsafe_allow_html=True)

    # ------------------- TOP RIGHT LOGIN BUTTON -------------------
    col1, col2, col3 = st.columns([8,1,1])
    with col3:
        if st.button("🔐 Login"):
            st.session_state.page = "login"
            st.rerun()  # Navigate to login module

    # ------------------- HERO SECTION -------------------
    st.markdown('<div class="hero-title">DIMDEA</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">AI-Driven Carbon Neutralization Planning System</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-tagline">Transforming Emission Data into Intelligent Sustainability Strategy</div>', unsafe_allow_html=True)

    # ------------------- ABOUT + EARTH -------------------
    col_left, col_right = st.columns([1,1])
    with col_left:
        st.markdown("""
        <div style="font-size:18px; color:#cbd5e1; padding:40px;">
        <h2 style="color:#22d3ee;">About DIMDEA</h2>
        DIMDEA is an advanced sustainability intelligence platform that empowers
        organizations to analyze emissions, detect environmental risks, optimize
        resources, and generate AI-driven carbon neutrality roadmaps.

        <br><br>

        Built on a modular AI architecture, DIMDEA ensures scalable,
        enterprise-grade sustainability transformation.
        </div>
        """, unsafe_allow_html=True)
    with col_right:
        st.markdown("""
        <div class="earth-wrapper">
            <div class="earth"></div>
            <div class="carbon-layer"></div>
            <div class="energy-lines"></div>
        </div>
        """, unsafe_allow_html=True)

    # ------------------- FEATURES -------------------
    st.markdown('<div class="section-title">Core Intelligence Modules</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Carbon Intelligence</div>
            <div class="feature-desc">
            Sector-wise emission profiling and structured carbon DNA modeling.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Renewable Transition</div>
            <div class="feature-desc">
            Simulate renewable adoption and evaluate emission reduction impact.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">AI Anomaly Detection</div>
            <div class="feature-desc">
            Identify abnormal emission spikes using statistical intelligence.
            </div>
        </div>
        """, unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Sustainability Tracking</div>
            <div class="feature-desc">
            Monitor long-term environmental performance trends.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">ESG Reporting</div>
            <div class="feature-desc">
            Structured environmental, social & governance insights.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col6:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">Ethical & Privacy Layer</div>
            <div class="feature-desc">
            Built-in ethical AI governance and privacy protection.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ------------------- FOOTER -------------------
    st.markdown('<div class="footer">Built for Intelligent Sustainability 🌍 | Powered by AI</div>', unsafe_allow_html=True)


# ------------------- RUN MODULE -------------------
if __name__ == "__main__":
    render()