import json, pandas as pd

c = json.load(open('data/results/scenarios/baseline_vs_extended_shift.json'))
b = pd.read_parquet('data/results/baseline/baseline_stage_metrics.parquet')
d = pd.read_parquet('data/results/scenarios/extended_shift/extended_shift_stage_metrics.parquet')

b_d = b[b['stage']=='DISPATCH'].iloc[0]
d_d = d[d['stage']=='DISPATCH'].iloc[0]

b_p = b[b['stage']=='PROCESSING'].iloc[0]
d_p = d[d['stage']=='PROCESSING'].iloc[0]

print(f"FT Change: {c['mean_flow_time']['absolute_change']:.2f} ({c['mean_flow_time']['percentage_change']:.2f}%)")
print(f"P95 FT Change: {c['p95_flow_time']['absolute_change']:.2f} ({c['p95_flow_time']['percentage_change']:.2f}%)")
print(f"Wait Change: {c['mean_waiting_time']['absolute_change']:.2f} ({c['mean_waiting_time']['percentage_change']:.2f}%)")
o_b = pd.read_parquet('data/results/baseline/baseline_order_metrics.parquet')
o_d = pd.read_parquet('data/results/scenarios/extended_shift/extended_shift_order_metrics.parquet')

p95_wait_b = o_b['total_waiting_time'].quantile(0.95)
p95_wait_d = o_d['total_waiting_time'].quantile(0.95)

print(f"P95 Wait Change: {p95_wait_d - p95_wait_b:.2f} ({(p95_wait_d - p95_wait_b) / p95_wait_b * 100:.2f}%)")
print(f"Stage 1 (Processing) Wait Change: {d_p['mean_waiting_time'] - b_p['mean_waiting_time']:.2f}")
print(f"Dispatch Wait Change: {d_d['mean_waiting_time'] - b_d['mean_waiting_time']:.2f}")
print(f"Dispatch Queue Change: {d_d['mean_queue_length'] - b_d['mean_queue_length']:.2f}")
print(f"Dispatch Util Change: {d_d['stage_utilization'] - b_d['stage_utilization']:.2f}%")
print("BOTTLENECKS:")
print(d[['stage', 'stage_utilization', 'mean_queue_length']].sort_values('stage_utilization', ascending=False).to_string())
print("\nSTAGE WAITING:")
print(d[['stage', 'mean_waiting_time']])
