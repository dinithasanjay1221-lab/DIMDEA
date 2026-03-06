# frontend/carbon_dna_view.py

import streamlit as st
import matplotlib.pyplot as plt


def render():

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

    # Avoid division by zero
    if total_emissions <= 0:
        st.error("Total emissions must be greater than zero.")
        return

    # Sector percentage contribution
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
    # Simple Suggestions (Frontend Logic Only)
    # ==================================================
    st.subheader("💡 Improvement Suggestions")

    highest_sector = max(sector_breakdown, key=sector_breakdown.get)

    st.write(f"- Focus on reducing emissions in **{highest_sector}** sector.")
    st.write("- Increase renewable energy usage.")
    st.write("- Improve energy efficiency policies.")


if __name__ == "__main__":
    render()