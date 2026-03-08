import streamlit as st
from datetime import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="DIMDEA | Carbon & AI Insights",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. MODULAR IMPORTS ---
try:
    from pages import (
        home, dashboard, onboarding, data_input, upload,
        industry_network, carbon_dna, hotspots, control_panel,
        simulator, roadmap, ai_insights, chatbox, settings
    )
except ImportError:
    def placeholder_render(title):
        st.title(title)
        st.info(f"The module for {title} is being connected.")

# --- 3. CUSTOM CSS ---
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #001f3f 0%, #003366 50%, #004080 100%);
    }
    [data-testid="stSidebar"] .stText, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] .stMarkdown p {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def render_navigation():
    st.sidebar.title("🌍 DIMDEA")
    st.sidebar.caption("Carbon Emission & AI Insights")
    st.sidebar.markdown("---")

    # --- UPDATED MENU ORDER ---
    menu_options = {
        "Home": "🏠",
        "Dashboard": "📊",
        "Onboarding": "👋",
        "Data Input": "📥",
        "Upload": "📤",
        "Industry Network": "🕸️",
        "Carbon DNA": "🧬",
        "Hotspots": "📍",
        "Control Panel": "🎛️",
        "Simulator": "🎮",
        "Roadmap": "🗺️",
        "AI Insights": "🧠",
        "Chatbox": "💬",
        "Settings": "⚙️",
        "Logout": "🚪"
    }

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"

    selection = st.sidebar.radio(
        "Navigation Menu",
        options=list(menu_options.keys()),
        format_func=lambda x: f"{menu_options[x]} {x}",
        index=list(menu_options.keys()).index(st.session_state.current_page)
    )

    st.sidebar.markdown("---")
    st.sidebar.write("© 2026 DIMDEA System")

    # --- UPDATED ROUTING LOGIC ---
    if selection == "Home":
        st.session_state.current_page = "Home"
        home.render() if 'home' in globals() else placeholder_render("Home")
    
    elif selection == "Dashboard":
        st.session_state.current_page = "Dashboard"
        dashboard.render() if 'dashboard' in globals() else placeholder_render("Dashboard")

    elif selection == "Onboarding":
        st.session_state.current_page = "Onboarding"
        onboarding.render() if 'onboarding' in globals() else placeholder_render("Onboarding")

    elif selection == "Data Input":
        st.session_state.current_page = "Data Input"
        data_input.render() if 'data_input' in globals() else placeholder_render("Data Input")

    elif selection == "Upload":
        st.session_state.current_page = "Upload"
        upload.render() if 'upload' in globals() else placeholder_render("Upload")

    elif selection == "Industry Network":
        st.session_state.current_page = "Industry Network"
        industry_network.render() if 'industry_network' in globals() else placeholder_render("Industry Network")

    elif selection == "Carbon DNA":
        st.session_state.current_page = "Carbon DNA"
        carbon_dna.render() if 'carbon_dna' in globals() else placeholder_render("Carbon DNA")

    elif selection == "Hotspots":
        st.session_state.current_page = "Hotspots"
        hotspots.render() if 'hotspots' in globals() else placeholder_render("Hotspots")

    elif selection == "Control Panel":
        st.session_state.current_page = "Control Panel"
        control_panel.render() if 'control_panel' in globals() else placeholder_render("Control Panel")

    elif selection == "Simulator":
        st.session_state.current_page = "Simulator"
        simulator.render() if 'simulator' in globals() else placeholder_render("Simulator")

    elif selection == "Roadmap":
        st.session_state.current_page = "Roadmap"
        roadmap.render() if 'roadmap' in globals() else placeholder_render("Roadmap")

    elif selection == "AI Insights":
        st.session_state.current_page = "AI Insights"
        ai_insights.render() if 'ai_insights' in globals() else placeholder_render("AI Insights")

    elif selection == "Chatbox":
        st.session_state.current_page = "Chatbox"
        chatbox.render() if 'chatbox' in globals() else placeholder_render("Chatbox")

    elif selection == "Settings":
        st.session_state.current_page = "Settings"
        settings.render() if 'settings' in globals() else placeholder_render("Settings")

    elif selection == "Logout":
        if st.button("Confirm Logout"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    render_navigation()