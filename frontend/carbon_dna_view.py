# frontend/carbon_dna_view.py

import streamlit as st
import matplotlib.pyplot as plt

def apply_dimdea_theme():
    """Applies the DIMDEA Dark Gradient Glassmorphism UI."""
    st.markdown(
        """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .stApp {
            background: linear-gradient(180deg, #050C16 0%, #0A192F 100%) !important;
            color: #FFFFFF !important;
        }

        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(0, 210, 255, 0.2);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.4);
        }

        h1, h2, h3 {
            color: #00D2FF !important;
            font-weight: 700 !important;
            text-transform: uppercase;
        }

        .subtitle {
            color: #00FFAB;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }

        .metric-label {
            color: #00FFAB;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .metric-value {
            color: #00D2FF;
            font-size: 1.8rem;
            font-weight: 600;
            text-shadow: 0 0 10px rgba(0, 210, 255, 0.3);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render():
    apply_dimdea_theme()

    st.title("🧬 Carbon DNA Breakdown")

    # ==================================================
    # Check if data exists
    # ==================================================
    if "emission_data" not in st.session_state or not st.session_state.emission_data:
        st.warning("No emission data found. Please enter data first.")
        return

    data = st.session_state.emission_data
    baseline = st.session_state.get("baseline", 15000)

    # ==================================================
    # Basic Calculations (Frontend Only)
    # ==================================================
    total_emissions = (
        data.get("transportation", 0)
        + data.get("energy", 0)
        + data.get("industrial", 0)
        + data.get("waste", 0)
        - data.get("renewable", 0)
    )

    if total_emissions <= 0:
        st.error("Total emissions must be greater than zero.")
        return

    sector_breakdown = {
        "Transportation": (data.get("transportation", 0) / total_emissions) * 100,
        "Energy": (data.get("energy", 0) / total_emissions) * 100,
        "Industrial": (data.get("industrial", 0) / total_emissions) * 100,
        "Waste": (data.get("waste", 0) / total_emissions) * 100,
    }

    # ==================================================
    # Display Overview
    # ==================================================
    st.subheader("📊 Carbon Overview")
    col1, col2 = st.columns(2)
    col1.metric("Total Emissions", f"{total_emissions:.2f}")
    col2.metric("Baseline", baseline)

    # ==================================================
    # Intensity Ratio
    # ==================================================
    st.subheader("⚖️ Emission Intensity Ratio")
    intensity_ratio = total_emissions / baseline
    st.write(f"Emission vs Baseline Ratio: **{intensity_ratio:.2f}**")

    if intensity_ratio > 1:
        st.error("Emissions exceed baseline.")
    else:
        st.success("Emissions are within baseline limit.")

    # ==================================================
    # Baseline Comparison
    # ==================================================
    st.subheader("📉 Baseline Comparison")
    difference = baseline - total_emissions
    if difference >= 0:
        st.success(f"{difference:.2f} below baseline")
    else:
        st.error(f"{abs(difference):.2f} above baseline")

    # ==================================================
    # Emission Contribution Chart
    # ==================================================
    st.subheader("📈 Sector Contribution")
    sectors = list(sector_breakdown.keys())
    values = list(sector_breakdown.values())

    fig, ax = plt.subplots()
    ax.pie(values, labels=sectors, autopct="%1.1f%%")
    ax.set_title("Emission Contribution by Sector")
    st.pyplot(fig)

    # ==================================================
    # Simple Suggestions
    # ==================================================
    st.subheader("💡 Improvement Suggestions")
    highest_sector = max(sector_breakdown, key=sector_breakdown.get)
    st.write(f"- Focus on reducing emissions in **{highest_sector}** sector.")
    st.write("- Increase renewable energy usage.")
    st.write("- Improve energy efficiency policies.")

if __name__ == "__main__":
    render()