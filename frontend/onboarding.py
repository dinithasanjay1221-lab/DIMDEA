import streamlit as st

def render():

    st.set_page_config(
        page_title="DIMDEA Onboarding",
        page_icon="🌍",
        layout="wide"
    )

    # --------------------------------------------------
    # SAME CUSTOM CSS FROM home.py
    # --------------------------------------------------
    st.markdown("""
    <style>

    /* Main Background */
    .stApp {
        background: radial-gradient(circle at top, #0a192f, #020617);
        color: white;
    }

    /* Hero Title */
    .hero-title {
        font-size: 60px;
        font-weight: 900;
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        text-align: center;
    }

    /* Subtitle */
    .hero-subtitle {
        font-size: 22px;
        color: #cbd5e1;
        margin-bottom: 40px;
        text-align: center;
    }

    /* Section Title */
    .section-title {
        font-size: 30px;
        font-weight: 800;
        margin-top: 40px;
        margin-bottom: 25px;
        text-align: center;
        background: linear-gradient(90deg, #00c6ff, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Glass Card */
    .feature-card {
        background: rgba(15, 23, 42, 0.8);
        padding: 30px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.1);
        transition: 0.4s ease;
    }

    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0px 10px 30px rgba(0, 198, 255, 0.4);
        border: 1px solid #00c6ff;
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

    # --------------------------------------------------
    # HERO SECTION
    # --------------------------------------------------
    st.markdown('<div class="hero-title">DIMDEA Onboarding</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Initialize Your Carbon Intelligence Journey</div>', unsafe_allow_html=True)

    # --------------------------------------------------
    # ONBOARDING STEPS
    # --------------------------------------------------
    st.markdown('<div class="section-title">Setup Process</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
        <h3 style="color:#22d3ee;">1️⃣ Organization Details</h3>
        Register your organization and define sustainability objectives.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
        <h3 style="color:#22d3ee;">2️⃣ Emission Baseline</h3>
        Provide transportation, industrial, and energy emission inputs.
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
        <h3 style="color:#22d3ee;">3️⃣ Activate Intelligence</h3>
        Launch AI-driven carbon analysis and sustainability modeling.
        </div>
        """, unsafe_allow_html=True)

    # --------------------------------------------------
    # FORM SECTION
    # --------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)

    with st.container():

        org_name = st.text_input("Organization Name")

        industry = st.selectbox("Industry Sector", [
            "Transportation",
            "Manufacturing",
            "Energy",
            "Logistics",
            "Smart Cities"
        ])

        goal = st.selectbox("Primary Sustainability Goal", [
            "Carbon Neutrality",
            "Net Zero",
            "Emission Reduction",
            "ESG Compliance"
        ])

        if st.button("🚀 Start Setup"):
            st.success("Onboarding initialized (Demo Mode).")

    # --------------------------------------------------
    # FOOTER
    # --------------------------------------------------
    st.markdown('<div class="footer">Built for Intelligent Sustainability 🌍 | Powered by AI</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    render()