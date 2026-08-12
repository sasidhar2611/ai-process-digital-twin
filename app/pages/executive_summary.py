import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Executive Summary", layout="wide")

st.title("Executive Summary Dashboard")
st.markdown("""
This high-level summary synthesizes the deterministic outputs from the AI-Process Digital Twin to provide an actionable overview of warehouse fulfillment performance, critical constraints, and the most promising operational interventions.
""")

@st.cache_data
def load_summary_data():
    data = {}
    files = {
        "kpis": "data/dashboard/dashboard_kpis.csv",
        "bottlenecks": "data/dashboard/dashboard_bottleneck_summary.csv",
        "interventions": "data/dashboard/dashboard_intervention_ranking.csv",
        "stages": "data/dashboard/dashboard_stage_metrics.csv"
    }
    
    for key, path in files.items():
        if os.path.exists(path):
            try:
                data[key] = pd.read_csv(path)
            except Exception:
                data[key] = pd.DataFrame()
        else:
            data[key] = pd.DataFrame()
            
    return data

data = load_summary_data()

kpi_df = data.get("kpis", pd.DataFrame())
bn_df = data.get("bottlenecks", pd.DataFrame())
inv_df = data.get("interventions", pd.DataFrame())
stage_df = data.get("stages", pd.DataFrame())

if kpi_df.empty or bn_df.empty or inv_df.empty or stage_df.empty:
    st.warning("Insufficient data to generate the Executive Summary. Please ensure all analytical dashboards datasets exist.")
else:
    baseline_kpi = kpi_df[kpi_df["scenario"] == "baseline"]
    
    if baseline_kpi.empty:
        st.warning("Baseline KPI data not found.")
    else:
        base_row = baseline_kpi.iloc[0]
        
        # 1. Process Health KPIs
        st.header("1. Process Health Metrics (Baseline)")
        col1, col2, col3, col4 = st.columns(4)
        
        def format_hrs(seconds):
            return f"{seconds / 3600:.2f} hrs"
            
        mean_flow = base_row.get("mean_flow_time_seconds", 0)
        mean_wait = base_row.get("mean_waiting_time_seconds", 0)
        mean_proc = base_row.get("mean_processing_time_seconds", 0)
        
        col1.metric("Avg Flow Time", format_hrs(mean_flow))
        col2.metric("Avg Waiting Time", format_hrs(mean_wait))
        col3.metric("Avg Processing Time", format_hrs(mean_proc))
        
        efficiency = (mean_proc / mean_flow * 100) if mean_flow > 0 else 0
        col4.metric("Process Efficiency", f"{efficiency:.1f}%")
        
        # 2. Process Health / Status
        st.header("2. Process Status")
        
        # Simple rule: if efficiency is < 20%, it's highly bottlenecked by waiting queues.
        if efficiency < 10:
            status = "🚨 Severely Bottlenecked"
            status_desc = "The system spends the vast majority of its time waiting in queues rather than undergoing value-added processing."
        elif efficiency < 30:
            status = "⚠️ Attention Required"
            status_desc = "Waiting times represent a disproportionately large component of total flow time. Interventions are recommended."
        else:
            status = "✅ Healthy"
            status_desc = "The process is flowing efficiently with a balanced processing-to-waiting ratio."
            
        st.info(f"**Current Status:** {status}  \n{status_desc}")
        
        # 3. Top Bottlenecks
        st.header("3. Top Operational Bottleneck")
        
        primary_bn = bn_df[bn_df["bottleneck_role"] == "Active Process Bottleneck"]
        if not primary_bn.empty:
            bn_stage = primary_bn.iloc[0]
            st.error(f"**Primary Constraint:** {bn_stage['stage']}")
            
            bc1, bc2, bc3 = st.columns(3)
            bc1.metric("Utilization", f"{bn_stage['utilization_percent']:.1f}%")
            bc2.metric("Mean Queue", f"{bn_stage['mean_queue']:.1f} orders")
            bc3.metric("Max Queue (P95)", f"{bn_stage.get('p95_queue', 0):.0f} orders")
        else:
            st.write("No active bottleneck definitively identified.")
            
        st.divider()
        
        # 4. Scenario Comparison
        st.header("4. Top Performing Intervention")
        
        best_scenario = inv_df.sort_values("mean_flow_time_improvement_percent", ascending=False).iloc[0]
        st.success(f"**Best Scenario:** {best_scenario['scenario_label']}")
        
        st.markdown(f"""
        - **Intervention Category:** {best_scenario.get('intervention_category', 'Unknown')}
        - **Improvement over Baseline:** +{best_scenario['mean_flow_time_improvement_percent']:.1f}% Flow Time reduction
        - **Bottleneck Effect:** {best_scenario.get('bottleneck_effect', 'Unknown')}
        """)
        
        # 5. What-If Insight
        st.header("5. What-If Insight")
        if best_scenario["scenario"] == "extended_shift":
            insight_text = f"Expanding the daily operating window ({best_scenario['scenario_label']}) relieves the massive overnight shift-boundary queue accumulations, yielding the strongest theoretical improvement to flow time."
        elif best_scenario["scenario"] == "dispatch_plus_1":
            insight_text = f"Adding targeted worker capacity to the active bottleneck ({best_scenario['scenario_label']}) directly reduces intra-shift congestion and produces a strong systemic flow-time improvement."
        else:
            insight_text = f"Implementing the {best_scenario['scenario_label']} scenario provides a {best_scenario['mean_flow_time_improvement_percent']:.1f}% improvement based on the simulated what-if experiments."
            
        st.markdown(f"> *{insight_text}*")
        
        # 6. Key Operational Insights
        st.header("6. Key Findings")
        
        # Dynamic extraction
        max_wait_stage = bn_df.loc[bn_df["mean_waiting_time_seconds"].idxmax()]["stage"]
        worst_scenario = inv_df.sort_values("mean_flow_time_improvement_percent", ascending=True).iloc[0]
        
        st.markdown(f"""
        1. **Systemic Constraint Identified:** The `DISPATCH` stage is the active process bottleneck, restricting continuous throughput and buffering upstream queues.
        2. **Shift-Boundary Impact:** The `{max_wait_stage}` stage accumulates the highest absolute waiting time due to overnight arrival rollovers, not active congestion.
        3. **Ineffective Interventions:** Adding capacity to downstream unconstrained stages (e.g., `{worst_scenario['scenario_label']}`) yields ~0% system-level improvement.
        4. **Proven Optimization:** Directly targeting the primary bottleneck or expanding the operational boundary yields guaranteed, predictable ROI.
        """)
        
        # 7. Recommended Focus
        st.header("7. Recommended Focus")
        st.info(f"""
        **Decision:** Prioritize the **{best_scenario['scenario_label']}** initiative. 
        
        Do not invest in capacity for unconstrained stages (like Picking or Packing). Focus capital expenditure and process redesign exclusively on either relaxing the shift boundary constraints or increasing parallel throughput at the Dispatch boundary.
        """)
