import streamlit as st
import pandas as pd
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

        h1, h2, h3 {
            color: #00D2FF !important;
            font-weight: 700 !important;
            text-transform: uppercase;
        }

        .stButton>button {
            background-color: #00D2FF !important;
            color: #0A192F !important;
            font-weight: 700;
            border-radius: 6px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #00FFAB !important;
            color: #050C16 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render():
    apply_dimdea_theme()

    st.title("🛣 Sustainability Roadmap")

    st.write("Strategic roadmap for reducing carbon emissions.")

    roadmap_steps = [
        "Year 1: Improve energy efficiency",
        "Year 2: Increase renewable energy usage",
        "Year 3: Optimize transportation routes",
        "Year 4: Reduce industrial emissions",
        "Year 5: Achieve carbon neutrality"
    ]

    st.subheader("Reduction Strategy")

    for step in roadmap_steps:
        st.write("•", step)

    st.divider()

    st.subheader("Emission Reduction Timeline")

    years = [1,2,3,4,5]
    emissions = [100,80,60,40,20]

    df = pd.DataFrame({
        "Year": years,
        "Projected Emissions": emissions
    })

    fig, ax = plt.subplots()

    ax.plot(df["Year"], df["Projected Emissions"], marker="o", color="#00D2FF")

    ax.set_xlabel("Year")
    ax.set_ylabel("Projected Emissions")
    ax.set_title("Reduction Timeline")

    st.pyplot(fig)

    st.divider()

    roadmap_text = "\n".join(roadmap_steps)

    st.download_button(
        "Download Roadmap",
        roadmap_text,
        "dimdea_roadmap.txt"
    )

if __name__ == "__main__":
    render()