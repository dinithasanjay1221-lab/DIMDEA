# frontend/navigation.py

import streamlit as st
from frontend import (
    home,
    data_input,
    dashboard,
    carbon_dna_view,
    roadmap_view,
    settings
)


def render_navigation():

    page = st.sidebar.radio(
        "Navigate",
        [
            "Home",
            "Data Input",
            "Dashboard",
            "Carbon DNA",
            "Roadmap",
            "Settings"
        ]
    )

    if page == "Home":
        home.render()

    elif page == "Data Input":
        data_input.render()

    elif page == "Dashboard":
        dashboard.render()

    elif page == "Carbon DNA":
        carbon_dna_view.render()

    elif page == "Roadmap":
        roadmap_view.render()

    elif page == "Settings":
        settings.render()