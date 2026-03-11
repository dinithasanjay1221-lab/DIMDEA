import streamlit as st
import sys
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
    from frontend import (
        home, dashboard, onboarding, data_input, upload,
        industry_network, carbon_dna, hotspots, control_panel,
        simulator, roadmap, ai_insights, chatbox, settings
    )
except ImportError:
    # Placeholder for missing pages
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

# --- 4. NAVIGATION FUNCTION ---
def render_navigation():
    st.sidebar.title("🌍 DIMDEA")
    st.sidebar.caption("Carbon Emission & AI Insights")
    st.sidebar.markdown("---")

    # --- MENU OPTIONS ---
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
    st.sidebar.caption("© 2026 DIMDEA System")

    # --- PAGE ROUTING ---
    page_mapping = {
        "Home": "home",
        "Dashboard": "dashboard",
        "Onboarding": "onboarding",
        "Data Input": "data_input",
        "Upload": "upload",
        "Industry Network": "industry_network",
        "Carbon DNA": "carbon_dna",
        "Hotspots": "hotspots",
        "Control Panel": "control_panel",
        "Simulator": "simulator",
        "Roadmap": "roadmap",
        "AI Insights": "ai_insights",
        "Chatbox": "chatbox",
        "Settings": "settings"
    }

    if selection == "Logout":
        if st.sidebar.button("Confirm Logout"):
            st.session_state.clear()
            st.experimental_rerun()
    else:
        st.session_state.current_page = selection
        module_name = page_mapping.get(selection)

        # Check in sys.modules with frontend namespace
        if module_name and f"frontend.{module_name}" in sys.modules:
            getattr(sys.modules[f"frontend.{module_name}"], "render")()
        else:
            # Try importing dynamically
            try:
                module = __import__(f"frontend.{module_name}", fromlist=["render"])
                module.render()
            except:
                placeholder_render(selection)

# --- 5. RUN NAVIGATION ---
if __name__ == "__main__":
    render_navigation()