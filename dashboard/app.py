import streamlit as st
from components.styling import apply_global_style

# Page configuration
st.set_page_config(
    page_title="F1 Championship Predictor",
    page_icon="🏎️",
    layout="wide"
)

# Apply global styling
apply_global_style()

# ===== HEADER =====
st.markdown(
    """
    <div class="main-title">
        F1 CHAMPIONSHIP PREDICTOR
    </div>
    <div class="accent-line"></div>
    <div class="sub-title">
        2026 Season Analytics Engine
    </div>
    <div class="custom-divider"></div>
    """,
    unsafe_allow_html=True
)

# ===== SIDEBAR =====
st.sidebar.markdown("### F1 Championship Predictor")
st.sidebar.markdown("2026 Season Simulation Platform")

st.sidebar.markdown("---")
st.sidebar.caption("Developed by Jean Jeasen")

# ===== FOOTER =====
st.markdown("---")
st.caption("Built & Designed by Jean Jeasen | 2026 Season Simulation Engine")