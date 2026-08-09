# Intervention Comparison & Ranking

## 1. Overview
This document compares the five "What-If" scenarios executed against the baseline model. The purpose is to evaluate which interventions provided the most significant systemic improvements versus those that only provided localized relief.

**Disclaimer**: The intervention findings represent behavior of the developed synthetic digital twin under model assumptions and should not be interpreted as direct measurements of Olist warehouses.

## 2. Scenario Ranking
The completed interventions are ranked by their ability to improve the system's **Mean Flow Time** (the total time from order approval to final dispatch).

| Rank | Scenario | Flow Time Imp. (s) | Flow Time Imp. (%) | Wait Time Imp. (s) | Type |
|------|----------|--------------------|--------------------|--------------------|------|
| **1** | **Extended Shift (10h to 12h)** | -6,061.83 | -27.68% | -6,061.93 | Process Boundary |
| **2** | **Dispatch Capacity +1** | -2,484.28 | -11.34% | -2,484.28 | Worker Capacity |
| **3** | **Productivity Factor +10%** | -1,307.83 | -5.97% | -1,233.96 | Efficiency |
| **4** | **Packing Capacity +2** | -1.02 | 0.00% | -1.01 | Worker Capacity |
| **5** | **Picking Capacity +5** | +1.52 | +0.01% | +1.47 | Worker Capacity |

*(Note: Negative values represent a reduction in time, which is an improvement. Positive values represent degradation).*

## 3. Detailed Comparison

### 3.1 Greatest System-Level Improvement
The **Extended Shift** intervention produced the greatest system-level improvement (-27.68%). By extending the daily operating window from 10 hours to 12 hours (+20% capacity time), the model significantly reduced overnight rollover queues. This directly attacked the largest source of waiting time (Stage 1 Processing wait).

### 3.2 Most Effective Worker-Capacity Intervention
**Dispatch Capacity +1** was the most effective worker-capacity intervention. Because Dispatch is the active baseline bottleneck, adding just a single worker (+33% local capacity) yielded an 11.34% improvement to overall system flow time. It relieved the primary source of in-process congestion.

### 3.3 Most Effective Productivity Intervention
**Productivity Factor +10%** yielded a highly meaningful system improvement of nearly 6%. This demonstrates that global efficiency improvements scale powerfully across the entire system, naturally reducing queuing friction proportionally at all stages.

### 3.4 Local vs. Systemic Improvements
Some interventions produced purely local improvements that failed to benefit the whole system:
- **Picking Capacity +5**: This intervention dramatically reduced the local queue at Picking. However, because Dispatch was the true downstream bottleneck, the system simply moved orders faster into the Dispatch queue, causing downstream congestion to swell. The overall flow time did not improve.
- **Packing Capacity +2**: Packing was not a bottleneck and had negligible queuing. Adding workers to an unconstrained stage produced a negligible system-level effect (~0.00%).

## 4. Synthesis
The analysis reveals three distinct roles in operations management:
1. **Operating Time (Shift Boundaries)**: Controls systemic macro-queuing (overnight rollovers). It exerts the single largest mathematical leverage on total flow time.
2. **Worker Capacity**: Only improves system throughput when applied directly to the primary bottleneck (Dispatch). Applying it elsewhere (Picking, Packing) creates stranded capacity or shifts bottlenecks.
3. **Productivity**: Acts as a friction reducer. A global productivity boost organically improves flow without requiring targeted bottleneck identification, though it may be harder to achieve in reality.
