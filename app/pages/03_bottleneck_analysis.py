import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Bottleneck Analysis", layout="wide")

st.title("Bottleneck Analysis")
st.markdown("""
Identify and analyze systemic constraints in the fulfillment process. This page evaluates the canonical baseline to pinpoint the active bottleneck and ranks theoretical interventions based on their system-level flow-time improvement.
""")

@st.cache_data
def load_bottleneck_data():
    try:
        req_files = [
            "data/dashboard/dashboard_bottleneck_summary.csv",
            "data/dashboard/dashboard_intervention_ranking.csv",
            "data/dashboard/dashboard_stage_metrics.csv"
        ]
        for f in req_files:
            if not os.path.exists(f):
                return None, None, None
                
        bottleneck_df = pd.read_csv("data/dashboard/dashboard_bottleneck_summary.csv")
        ranking_df = pd.read_csv("data/dashboard/dashboard_intervention_ranking.csv")
        stage_df = pd.read_csv("data/dashboard/dashboard_stage_metrics.csv")
        
        # Filter stage_df to only baseline
        baseline_stage_df = stage_df[stage_df["scenario"] == "baseline"].copy()
        
        return bottleneck_df, ranking_df, baseline_stage_df
    except Exception as e:
        st.error(f"Error loading bottleneck data: {e}")
        return None, None, None

bottleneck_df, ranking_df, baseline_stage_df = load_bottleneck_data()

if bottleneck_df is None or bottleneck_df.empty:
    st.warning("Bottleneck data is unavailable. Please ensure all required CSV files are present in data/dashboard/.")
else:
    # Identify active bottleneck
    active_bottleneck = bottleneck_df[bottleneck_df["bottleneck_role"] == "Active Process Bottleneck"].iloc[0]
    bottleneck_stage = active_bottleneck["stage"]
    
    st.header("Baseline Bottleneck Identification")
    st.info(f"**Primary Bottleneck Identified:** {bottleneck_stage}")
    
    st.markdown(f"""
    The **{bottleneck_stage}** stage is identified as the primary active bottleneck in the baseline scenario. 
    Although *PROCESSING* exhibits significant waiting times due to overnight shift delays (Boundary Queue Wait), 
    *{bottleneck_stage}* sustains the highest active utilization and peak queue lengths during operating hours, 
    making it the true constraint on continuous system throughput.
    """)
    
    # Bottleneck Score/Ranking Table
    st.subheader("Bottleneck Score & Ranking")
    display_bn_df = bottleneck_df.sort_values("bottleneck_rank").copy()
    display_bn_df.columns = [
        "Stage", "Utilization (%)", "Mean Queue Length", "P95 Queue", 
        "Mean Waiting Time (s)", "Bottleneck Score", "Bottleneck Rank", "Bottleneck Role"
    ]
    st.dataframe(display_bn_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Baseline Stage Metrics Visualizations
    st.header("Baseline Stage Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_util = px.bar(
            bottleneck_df, 
            x="stage", 
            y="utilization_percent",
            title="Stage Utilization (%)",
            color="bottleneck_role",
            color_discrete_map={
                "Active Process Bottleneck": "red",
                "Boundary Queue Wait": "orange",
                "Unconstrained Stage": "gray"
            }
        )
        st.plotly_chart(fig_util, use_container_width=True)
        
    with col2:
        fig_queue = px.bar(
            bottleneck_df, 
            x="stage", 
            y=["mean_queue", "p95_queue"],
            title="Mean and P95 Queue Lengths by Stage",
            barmode="group"
        )
        st.plotly_chart(fig_queue, use_container_width=True)
        
    # Waiting time contribution
    fig_wait = px.pie(
        bottleneck_df,
        names="stage",
        values="mean_waiting_time_seconds",
        title="Mean Waiting Time Contribution by Stage",
        hole=0.4
    )
    st.plotly_chart(fig_wait, use_container_width=True)
    
    st.divider()
    
    # Intervention Ranking
    st.header("Intervention Ranking & What-If Results")
    st.markdown("""
    The following table ranks the tested interventions by their overall improvement on Mean Flow Time.
    """)
    
    # Rank by improvement
    ranking_df = ranking_df.sort_values("mean_flow_time_improvement_percent", ascending=False)
    
    fig_rank = px.bar(
        ranking_df,
        x="scenario_label",
        y="mean_flow_time_improvement_percent",
        title="Mean Flow Time Improvement (%) by Intervention",
        color="recommendation_priority",
        color_discrete_map={
            "PRIMARY": "green",
            "SECONDARY": "blue",
            "LOW": "gray"
        }
    )
    st.plotly_chart(fig_rank, use_container_width=True)
    
    display_rank_df = ranking_df[[
        "rank", "scenario_label", "intervention_category", 
        "mean_flow_time_improvement_percent", "mean_waiting_time_improvement_percent", 
        "bottleneck_effect", "recommendation_priority"
    ]].copy()
    
    display_rank_df.columns = [
        "Rank", "Scenario", "Category", "Flow Time Improvement (%)",
        "Wait Time Improvement (%)", "Bottleneck Effect", "Priority"
    ]
    
    st.dataframe(display_rank_df, use_container_width=True, hide_index=True)
