import streamlit as st

st.set_page_config(
    page_title="AI-Driven Process Digital Twin",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("PROJECT:")
st.sidebar.subheader("AI-Driven Process Digital Twin")

st.markdown("👈 **Please select a page from the sidebar to begin.**")

# Make Executive Summary the default landing page
st.switch_page("pages/00_executive_summary.py")
