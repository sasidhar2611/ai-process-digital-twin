import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Operational Flow Analysis", layout="wide")

st.title("Operational Flow & Process Analysis")
st.markdown("""
Analyze where time is spent across the fulfillment pipeline. This dashboard decomposes end-to-end flow time into active processing and queuing delays, illustrating the true sequential constraints of the synthetic process.
""")

@st.cache_data
def load_flow_data():
    try:
        if not os.path.exists("data/dashboard/dashboard_stage_metrics.csv") or not os.path.exists("data/dashboard/dashboard_kpis.csv"):
            return None, None
            
        stage_df = pd.read_csv("data/dashboard/dashboard_stage_metrics.csv")
        kpi_df = pd.read_csv("data/dashboard/dashboard_kpis.csv")
        return stage_df, kpi_df
    except Exception as e:
        st.error(f"Error loading dashboard data: {e}")
        return None, None

stage_df, kpi_df = load_flow_data()

if stage_df is None or stage_df.empty:
    st.warning("Dashboard data is unavailable. Please ensure all required CSV files are present in data/dashboard/.")
else:
    # 1. Interactive Filters
    st.sidebar.header("Controls")
    scenarios = stage_df["scenario_label"].unique()
    selected_scenario = st.sidebar.selectbox("Select Scenario to Analyze", scenarios, index=0)
    
    # Filter data for selected scenario
    sc_stage_df = stage_df[stage_df["scenario_label"] == selected_scenario].copy()
    sc_kpi_df = kpi_df[kpi_df["scenario_label"] == selected_scenario].copy()
    
    # Process Flow Explanation
    st.markdown("### 1. Process Flow Sequence")
    st.markdown("""
    **`PROCESSING`** ➔ **`PICKING`** ➔ **`PACKING`** ➔ **`SORTING`** ➔ **`DISPATCH`**
    
    The simulated pipeline is strictly sequential. Orders accumulate wait time before each stage if workers are unavailable or if the daily operating shift has ended.
    """)
    st.divider()
    
    # Sort stage df by sequence just in case
    if "stage_sequence" in sc_stage_df.columns:
        sc_stage_df = sc_stage_df.sort_values("stage_sequence")
        
    # Extract overall metrics
    if not sc_kpi_df.empty:
        overall_mean_flow = sc_kpi_df.iloc[0].get("mean_flow_time_seconds", 0)
        overall_mean_wait = sc_kpi_df.iloc[0].get("mean_waiting_time_seconds", 0)
        overall_mean_proc = sc_kpi_df.iloc[0].get("mean_processing_time_seconds", 0)
        
        # Calculate % breakdown
        wait_pct = (overall_mean_wait / overall_mean_flow) * 100 if overall_mean_flow > 0 else 0
        proc_pct = (overall_mean_proc / overall_mean_flow) * 100 if overall_mean_flow > 0 else 0
        
        # Dynamic Insights
        st.markdown("### Dynamic Insights")
        highest_wait_stage = sc_stage_df.loc[sc_stage_df["mean_waiting_time_seconds"].idxmax(), "stage"]
        highest_util_stage = sc_stage_df.loc[sc_stage_df["utilization_percent"].idxmax(), "stage"]
        highest_queue_stage = sc_stage_df.loc[sc_stage_df["mean_queue"].idxmax(), "stage"]
        
        col_insight1, col_insight2 = st.columns(2)
        
        with col_insight1:
            st.info(f"""
            - **Dominant Time Component:** Waiting accounts for **{wait_pct:.1f}%** of total flow time.
            - **Highest Waiting Time:** `{highest_wait_stage}`
            - **Highest Queue Length:** `{highest_queue_stage}`
            - **Highest Utilization:** `{highest_util_stage}`
            """)
            
        with col_insight2:
            st.warning("""
            **CRITICAL INTERPRETATION:**
            The `PROCESSING` stage often exhibits the largest waiting-time contribution primarily due to **shift-boundary and overnight rollover effects**, where incoming orders accumulate while the warehouse is closed. 
            However, `DISPATCH` remains the primary active capacity bottleneck (highest utilization), fundamentally restricting continuous throughput during active operating hours.
            """)
            
        st.divider()
        
        st.header("Overall Flow-Time Breakdown")
        # Visual Breakdown
        fig_breakdown = px.pie(
            names=["Waiting Time", "Processing Time"],
            values=[overall_mean_wait, overall_mean_proc],
            title="Total Mean Flow Time Breakdown",
            color_discrete_sequence=["#FF7F0E", "#1F77B4"],
            hole=0.4
        )
        st.plotly_chart(fig_breakdown, use_container_width=True)
    
    st.divider()
    
    st.header("Stage-Level Analytics")
    colA, colB = st.columns(2)
    
    with colA:
        # Stage Processing Time
        fig_proc = px.bar(
            sc_stage_df,
            x="stage",
            y="mean_processing_time_seconds",
            title="Mean Processing Time by Stage (Seconds)",
            color_discrete_sequence=["#1F77B4"]
        )
        st.plotly_chart(fig_proc, use_container_width=True)
        
        # Stage Utilization
        fig_util = px.bar(
            sc_stage_df,
            x="stage",
            y="utilization_percent",
            title="Stage Utilization (%)",
            color="stage"
        )
        st.plotly_chart(fig_util, use_container_width=True)
        
    with colB:
        # Stage Waiting Time
        fig_wait = px.bar(
            sc_stage_df,
            x="stage",
            y="mean_waiting_time_seconds",
            title="Mean Waiting Time by Stage (Seconds)",
            color_discrete_sequence=["#FF7F0E"]
        )
        st.plotly_chart(fig_wait, use_container_width=True)
        
        # Stage Queue Analysis
        fig_queue = px.bar(
            sc_stage_df,
            x="stage",
            y=["mean_queue", "p95_queue"],
            title="Mean & P95 Queue Lengths by Stage",
            barmode="group"
        )
        st.plotly_chart(fig_queue, use_container_width=True)
        
    st.divider()
    
    # Detailed Data Table
    st.subheader("Detailed Stage Metrics Table")
    display_cols = ["stage", "worker_count", "utilization_percent", "mean_queue", "p95_queue", 
                    "mean_processing_time_seconds", "mean_waiting_time_seconds"]
    disp_df = sc_stage_df[display_cols].copy()
    disp_df.columns = ["Stage", "Workers", "Utilization (%)", "Mean Queue", "P95 Queue", "Mean Processing (s)", "Mean Waiting (s)"]
    st.dataframe(disp_df, use_container_width=True, hide_index=True)
