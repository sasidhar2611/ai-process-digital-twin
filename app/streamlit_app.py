import streamlit as st

st.set_page_config(
    page_title="AI-Driven Process Digital Twin",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("PROJECT:")
st.sidebar.subheader("AI-Driven Process Digital Twin")

st.sidebar.markdown("### Navigation")
st.sidebar.page_link("pages/overview.py", label="Overview", icon="🏠")
# Bottleneck Analysis, What-If Analysis, Intervention Ranking will be added here later.

st.sidebar.markdown("---")
st.sidebar.markdown("### Data Source")
st.sidebar.caption("**Olist Brazilian E-Commerce Public Dataset**")
st.sidebar.info("Real historical e-commerce data anchors the demand, while operational process data is generated via a synthetic operational model.")

st.title("AI-Driven Process Digital Twin")
st.subheader("Bottleneck Analysis & Operational What-If Simulation")
st.markdown("An analytical digital twin that combines real Olist e-commerce data with a controlled synthetic fulfillment-process model to identify bottlenecks and evaluate operational interventions.")
st.markdown("---")

st.markdown("👈 **Please select a page from the sidebar to begin.**")
