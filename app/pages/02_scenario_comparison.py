import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Scenario Comparison & What-If Analysis", layout="wide")

st.title("Scenario Comparison & What-If Analysis")
st.markdown("""
Compare simulated operational interventions against the historical-data-anchored baseline to identify improvements and unintended downstream effects.
""")

@st.cache_data
def load_data():
    try:
        if not os.path.exists("data/dashboard/dashboard_kpis.csv") or not os.path.exists("data/dashboard/dashboard_scenario_comparison.csv") or not os.path.exists("data/dashboard/dashboard_stage_metrics.csv"):
            return None, None, None
            
        kpis_df = pd.read_csv("data/dashboard/dashboard_kpis.csv")
        comparison_df = pd.read_csv("data/dashboard/dashboard_scenario_comparison.csv")
        stage_df = pd.read_csv("data/dashboard/dashboard_stage_metrics.csv")
        
        # Combine baseline KPI with comparison to get a unified dataframe for overall metrics
        # baseline has mean_flow_time_seconds, comparison has it too
        baseline_row = kpis_df[kpis_df["scenario"] == "baseline"].copy()
        baseline_row["mean_flow_time_change_percent"] = 0.0
        baseline_row["mean_waiting_time_change_percent"] = 0.0
        
        cols = ["scenario", "scenario_label", "mean_flow_time_seconds", "p95_flow_time_seconds", 
                "mean_waiting_time_seconds", "mean_processing_time_seconds", "sla_achievement_percent", 
                "mean_flow_time_change_percent", "mean_waiting_time_change_percent"]
                
        # Ensure columns exist before subsetting
        for c in cols:
            if c not in baseline_row.columns:
                if c == "mean_flow_time_change_percent" or c == "mean_waiting_time_change_percent":
                    pass
                else:
                    baseline_row[c] = 0.0
            if c not in comparison_df.columns:
                # Some might not exist in comparison_df like mean_processing_time_seconds, let's derive or handle
                if c == "mean_processing_time_seconds":
                    # Fallback to sum of processing time from stage_df
                    pass
        
        # We will build unified_df robustly
        unified_records = []
        
        # Add baseline
        if not baseline_row.empty:
            b = baseline_row.iloc[0]
            unified_records.append({
                "scenario": b.get("scenario", "baseline"),
                "scenario_label": b.get("scenario_label", "Baseline"),
                "mean_flow_time_seconds": b.get("mean_flow_time_seconds", 0),
                "p95_flow_time_seconds": b.get("p95_flow_time_seconds", 0),
                "mean_waiting_time_seconds": b.get("mean_waiting_time_seconds", 0),
                "mean_processing_time_seconds": b.get("mean_processing_time_seconds", 0),
                "sla_achievement_percent": b.get("sla_achievement_percent", 100.0),
                "mean_flow_time_change_percent": 0.0,
                "mean_waiting_time_change_percent": 0.0
            })
            
        for _, r in comparison_df.iterrows():
            # Get processing time from stage metrics if missing
            proc_time = 0
            if "mean_processing_time_seconds" in r:
                proc_time = r["mean_processing_time_seconds"]
            else:
                stg = stage_df[stage_df["scenario"] == r["scenario"]]
                if not stg.empty:
                    proc_time = stg["mean_processing_time_seconds"].sum()
                    
            unified_records.append({
                "scenario": r.get("scenario", ""),
                "scenario_label": r.get("scenario_label", ""),
                "mean_flow_time_seconds": r.get("mean_flow_time_seconds", 0),
                "p95_flow_time_seconds": r.get("p95_flow_time_seconds", 0),
                "mean_waiting_time_seconds": r.get("mean_waiting_time_seconds", 0),
                "mean_processing_time_seconds": proc_time,
                "sla_achievement_percent": r.get("sla_achievement_percent", 100.0),
                "mean_flow_time_change_percent": r.get("mean_flow_time_change_percent", 0),
                "mean_waiting_time_change_percent": r.get("mean_waiting_time_change_percent", 0)
            })
            
        unified_df = pd.DataFrame(unified_records)
        return kpis_df, unified_df, stage_df
    except Exception as e:
        st.error(f"Error loading dashboard data: {e}")
        return None, None, None

kpis_df, unified_df, stage_df = load_data()

if unified_df is None or unified_df.empty:
    st.warning("Dashboard data is unavailable or incomplete. Please ensure all required CSV files are present in data/dashboard/.")
else:
    # 1. Interactive Controls
    st.sidebar.header("Controls")
    
    scenarios_available = unified_df["scenario_label"].tolist()
    
    # Let user select ALL or specific scenarios
    selection_mode = st.sidebar.radio("Scenario Selection", ["All Scenarios", "Specific Scenarios"])
    selected_scenarios = scenarios_available
    
    if selection_mode == "Specific Scenarios":
        selected_scenarios = st.sidebar.multiselect("Select Scenarios", scenarios_available, default=["Baseline"])
        if not selected_scenarios:
            st.warning("Please select at least one scenario.")
            st.stop()
            
    filtered_df = unified_df[unified_df["scenario_label"].isin(selected_scenarios)].copy()
    filtered_stage_df = stage_df[stage_df["scenario_label"].isin(selected_scenarios)].copy()
    
    kpi_options = {
        "Mean Flow Time (hrs)": ("mean_flow_time_seconds", 3600),
        "P95 Flow Time (hrs)": ("p95_flow_time_seconds", 3600),
        "Mean Waiting Time (hrs)": ("mean_waiting_time_seconds", 3600),
        "Mean Processing Time (hrs)": ("mean_processing_time_seconds", 3600),
        "SLA Achievement (%)": ("sla_achievement_percent", 1)
    }
    
    selected_kpi_label = st.sidebar.selectbox("Compare KPI", list(kpi_options.keys()))
    kpi_col, kpi_div = kpi_options[selected_kpi_label]
    
    filtered_df[selected_kpi_label] = filtered_df[kpi_col] / kpi_div
    
    # 2. Dynamic Insights
    st.markdown("### Key Insights")
    
    try:
        # Lowest mean flow time
        best_scenario_row = unified_df.loc[unified_df["mean_flow_time_seconds"].idxmin()]
        best_scenario = best_scenario_row["scenario_label"]
        
        # Largest improvement (most negative change percent)
        largest_improvement_row = unified_df.loc[unified_df["mean_flow_time_change_percent"].idxmin()]
        largest_improvement_scenario = largest_improvement_row["scenario_label"]
        largest_improvement_val = abs(largest_improvement_row["mean_flow_time_change_percent"])
        
        # Negligible improvement (change percent > -1 and <= 0, excluding baseline)
        negligible = unified_df[(unified_df["scenario"] != "baseline") & (unified_df["mean_flow_time_change_percent"] > -1.0)]["scenario_label"].tolist()
        
        st.info(f"""
        - **Lowest Flow Time Scenario:** {best_scenario}
        - **Largest Improvement:** {largest_improvement_scenario} ({largest_improvement_val:.2f}%)
        - **Negligible Flow Time Interventions (<1% improvement):** {', '.join(negligible) if negligible else 'None'}
        """)
    except Exception as e:
        st.warning(f"Could not calculate automated insights. Check data validity.")
        
    st.divider()

    # 3. Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Scenario vs Mean Flow Time
        fig1 = px.bar(
            filtered_df, 
            x="scenario_label", 
            y="mean_flow_time_seconds",
            title="Scenario vs Mean Flow Time (Seconds)",
            color="scenario",
            color_discrete_map={"baseline": "red"}
        )
        # Convert to hours for readability
        fig1.update_yaxes(title="Seconds")
        fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        # Scenario vs Mean Waiting Time
        fig2 = px.bar(
            filtered_df, 
            x="scenario_label", 
            y="mean_waiting_time_seconds",
            title="Scenario vs Mean Waiting Time (Seconds)",
            color="scenario",
            color_discrete_map={"baseline": "red"}
        )
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
        
    # Scenario improvement percentage
    # Invert the change so that improvement is positive
    filtered_df["Improvement (%)"] = -filtered_df["mean_flow_time_change_percent"]
    
    fig3 = px.bar(
        filtered_df,
        x="scenario_label",
        y="Improvement (%)",
        title="Flow Time Improvement (%) vs Baseline",
        color="scenario",
        color_discrete_map={"baseline": "gray"}
    )
    fig3.update_layout(showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)
    
    # 4. Scenario Comparison Table
    st.markdown("### Scenario Comparison Metrics")
    display_df = filtered_df[[
        "scenario_label", "mean_flow_time_seconds", "p95_flow_time_seconds", 
        "mean_waiting_time_seconds", "mean_processing_time_seconds", 
        "sla_achievement_percent", "mean_flow_time_change_percent", "mean_waiting_time_change_percent"
    ]].copy()
    
    display_df.columns = [
        "Scenario", "Mean Flow Time (s)", "P95 Flow Time (s)", 
        "Mean Waiting Time (s)", "Mean Processing Time (s)", 
        "SLA Achievement (%)", "Flow Time Change (%)", "Waiting Time Change (%)"
    ]
    
    st.dataframe(display_df, use_container_width=True)
    
    st.divider()
    
    # 5. Bottleneck / Stage Comparison
    st.markdown("### Stage Comparison")
    
    if not filtered_stage_df.empty:
        stage_metric_opt = st.radio("Select Stage Metric to Compare:", ["Utilization (%)", "Mean Queue Length"])
        
        if stage_metric_opt == "Utilization (%)":
            y_col = "utilization_percent"
            title = "Stage Utilization by Scenario"
        else:
            y_col = "mean_queue"
            title = "Mean Queue Length by Stage and Scenario"
            
        fig4 = px.bar(
            filtered_stage_df,
            x="stage",
            y=y_col,
            color="scenario_label",
            barmode="group",
            title=title
        )
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.warning("No stage-level metrics available for selected scenarios.")
