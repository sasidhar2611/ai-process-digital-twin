import json, pandas as pd

c = json.load(open('data/results/scenarios/baseline_vs_picking_plus_5.json'))
b = pd.read_parquet('data/results/baseline/baseline_stage_metrics.parquet')
d = pd.read_parquet('data/results/scenarios/picking_plus_5/picking_plus_5_stage_metrics.parquet')

b_d = b[b['stage']=='PICKING'].iloc[0]
d_d = d[d['stage']=='PICKING'].iloc[0]

print(f"FT Change: {c['mean_flow_time']['absolute_change']:.2f} ({c['mean_flow_time']['percentage_change']:.2f}%)")
print(f"P95 FT Change: {c['p95_flow_time']['absolute_change']:.2f} ({c['p95_flow_time']['percentage_change']:.2f}%)")
print(f"Wait Change: {c['mean_waiting_time']['absolute_change']:.2f} ({c['mean_waiting_time']['percentage_change']:.2f}%)")
print(f"Picking Queue Change: {d_d['mean_queue_length'] - b_d['mean_queue_length']:.2f}")
print(f"Picking Util Change: {d_d['stage_utilization'] - b_d['stage_utilization']:.2f}%")
print(f"Picking Util Old: {b_d['stage_utilization']:.2f}%, New: {d_d['stage_utilization']:.2f}%")
print("BOTTLENECKS:")
print(d[['stage', 'stage_utilization', 'mean_queue_length']].sort_values('stage_utilization', ascending=False).to_string())
