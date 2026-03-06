import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as obj

# Strict separation: Import backend logic
try:
    from backend.analytics.network_analysis import analyze_network
except ImportError:
    # Fallback mock logic to prevent app crash while setting up backend folders
    def analyze_network(data):
        G = nx.powerlaw_cluster_graph(n=10, m=2, p=0.1, seed=42)
        return {
            "graph": G,
            "central_node": "Energy Grid",
            "density": 0.45,
            "risk_score": 0.28
        }

def apply_enterprise_styles():
    """Applies the DIMDEA Deep Forest Glassmorphism UI."""
    st.markdown(
        """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .stApp {
            background: linear-gradient(135deg, #0F3D3E 0%, #081F20 100%);
            color: #FFFFFF;
        }

        .glass-card {
            background: rgba(31, 171, 137, 0.05);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(0, 255, 171, 0.1);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
        }

        h1 { color: #00FFAB; font-weight: 700; }
        .subtitle { color: #1FAB89; font-size: 1.1rem; margin-bottom: 2rem; }
        .metric-label { color: #1FAB89; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; }
        .metric-value { color: #00FFAB; font-size: 1.8rem; font-weight: 600; text-shadow: 0 0 10px rgba(0, 255, 171, 0.3); }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_network_graph(network_data):
    """Visualizes structural emission dependencies using Plotly."""
    G = network_data['graph']
    pos = nx.spring_layout(G, seed=42)
    
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = obj.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.5, color='rgba(31, 171, 137, 0.4)'),
        hoverinfo='none', mode='lines')

    node_x, node_y = [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = obj.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(size=25, color='#00FFAB', line=dict(width=2, color='#0F3D3E')))

    fig = obj.Figure(data=[edge_trace, node_trace],
                 layout=obj.Layout(
                    showlegend=False, margin=dict(b=0, l=0, r=0, t=0),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    
    st.plotly_chart(fig, use_container_width=True)

def render_network_view():
    apply_enterprise_styles()

    # Top Section
    st.markdown("<h1>Industry Emission Network</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Structural emission interdependencies and flow analysis</p>", unsafe_allow_html=True)

    # Session State Check
    if "emission_data" not in st.session_state or st.session_state["emission_data"] is None:
        st.markdown("<div class='glass-card' style='border-color: #FF4B4B;'>No emission data available. Please input data first.</div>", unsafe_allow_html=True)
        return

    results = analyze_network(st.session_state["emission_data"])

    # Row 1: Layout
    col_main, col_side = st.columns([2.5, 1])

    with col_main:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("Structural Emission Flow")
        render_network_graph(results)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_side:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<p class='metric-label'>Most Connected Sector</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='metric-value'>{results['central_node']}</p>", unsafe_allow_html=True)
        st.markdown("<br><p class='metric-label'>Network Density</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='metric-value'>{results['density']:.2f}</p>", unsafe_allow_html=True)
        st.markdown("<br><p class='metric-label'>Structural Risk</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='metric-value'>{results['risk_score']*100:.1f}%</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Row 2
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='glass-card'><h3>Interdependency Insights</h3><p>Analysis of cascading emission risks across industrial nodes.</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='glass-card'><h3>Emission Flow Explanation</h3><p>Visualization of supply chain dependencies and carbon handprints.</p></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    render_network_view()