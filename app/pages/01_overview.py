import streamlit as st
import plotly.express as px
from app.data_loader import load_kpis, load_stage_metrics, load_bottleneck_summary

st.set_page_config(page_title="Overview", page_icon="🏠", layout="wide")

st.title("Overview: Baseline Performance")

try:
    kpis_df = load_kpis()
    stage_df = load_stage_metrics()
    bottleneck_df = load_bottleneck_summary()
except Exception as e:
    st.error(f"Failed to load dashboard data: {str(e)}")
    st.stop()

baseline_kpi = kpis_df[kpis_df["scenario"] == "baseline"].iloc[0]
baseline_stages = stage_df[stage_df["scenario"] == "baseline"].sort_values("stage_sequence")

# KPI CARDS
st.markdown("### Executive Summary")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Orders Processed", f"{baseline_kpi['orders_processed']:,}")
col2.metric("Mean Flow Time", f"{baseline_kpi['mean_flow_time_hours']:.2f} hrs")
col3.metric("Mean Waiting Time", f"{baseline_kpi['mean_waiting_time_hours']:.2f} hrs")
col4.metric("P95 Flow Time", f"{baseline_kpi['p95_flow_time_seconds'] / 3600.0:.2f} hrs")

bottleneck = bottleneck_df.iloc[0]
col5.metric("Bottleneck", bottleneck["stage"])

st.markdown("---")
# PROCESS FLOW
st.markdown("### Fulfillment Process Flow")
flow_html = " ➔ ".join([f"**{stage}**" for stage in baseline_stages["stage"]])
st.markdown(f"<h4 style='text-align: center; color: #4CAF50;'>{flow_html}</h4>", unsafe_allow_html=True)

st.markdown("---")
# BASELINE STAGE SUMMARY
st.markdown("### Baseline Stage Summary")
display_df = baseline_stages[["stage", "utilization_percent", "mean_queue", "p95_queue", "mean_waiting_time_seconds"]].copy()
display_df["mean_waiting_time_hours"] = display_df["mean_waiting_time_seconds"] / 3600.0
display_df = display_df.rename(columns={
    "stage": "Stage",
    "utilization_percent": "Utilization (%)",
    "mean_queue": "Mean Queue",
    "p95_queue": "P95 Queue",
    "mean_waiting_time_hours": "Mean Waiting Time (hrs)"
})
display_df["Utilization (%)"] = display_df["Utilization (%)"].apply(lambda x: f"{x:.2f}%")
display_df["Mean Queue"] = display_df["Mean Queue"].apply(lambda x: f"{x:.2f}")
display_df["P95 Queue"] = display_df["P95 Queue"].apply(lambda x: f"{x:.2f}")
display_df["Mean Waiting Time (hrs)"] = display_df["Mean Waiting Time (hrs)"].apply(lambda x: f"{x:.2f}")

st.table(display_df[["Stage", "Utilization (%)", "Mean Queue", "P95 Queue", "Mean Waiting Time (hrs)"]])

st.markdown("---")
# BOTTLENECK HIGHLIGHT
st.markdown("### Baseline Bottleneck")
st.error(f"**{bottleneck['stage']}** is the primary bottleneck.")
st.markdown(f"- **Utilization**: {bottleneck['utilization_percent']:.2f}%")
st.markdown(f"- **Mean Queue**: {bottleneck['mean_queue']:.2f}")
st.markdown(f"- **Bottleneck Score**: {bottleneck['bottleneck_score']:.2f} / 4.00")
st.markdown(f"{bottleneck['stage'].capitalize()} is the highest-utilized and highest-queue stage in the baseline simulation and is therefore identified as the primary bottleneck under the current model assumptions.")
st.info("These findings represent behavior of the synthetic digital twin and should not be interpreted as direct measurements of a real warehouse.")

st.markdown("---")
# VISUALIZATIONS
st.markdown("### Stage Analytics")
col_chart1, col_chart2 = st.columns(2)

fig1 = px.bar(baseline_stages, x="stage", y="utilization_percent", title="Stage Utilization (%)", labels={"stage": "Stage", "utilization_percent": "Utilization (%)"})
col_chart1.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(baseline_stages, x="stage", y="mean_queue", title="Mean Queue by Stage", labels={"stage": "Stage", "mean_queue": "Mean Queue"})
col_chart2.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.markdown("### Project Information")
st.markdown("""
- **Real Data**: Olist e-commerce order/product/customer information
- **Synthetic Data**: Operational timestamps, worker assignments, queues, processing times and waiting times
- **Purpose**: Evaluate process bottlenecks and operational scenarios.
""")

st.caption("Operational process timestamps and worker-level variables are synthetically modeled. Results represent controlled simulation behavior rather than direct measurements of an actual warehouse.")
