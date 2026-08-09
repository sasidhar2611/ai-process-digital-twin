# Dispatch +1 Capacity Experiment

## 1. Overview
The Dispatch +1 scenario represents a synthetic model experiment anchored to real Olist demand data. It does not represent observed warehouse intervention results.

This experiment tests the addition of a single worker to the Dispatch stage, increasing capacity from 3 to 4 workers, while maintaining all other baseline parameters.

## 2. Hypothesis
**Model Hypothesis:** "Increasing Dispatch capacity by one worker will reduce Dispatch queue accumulation and waiting time, resulting in improved overall flow-time performance."

## 3. Methodology
### 3.1 Experimental Configuration
- **Scenario ID**: `dispatch_plus_1`
- **Changed Variable**: Dispatch worker count (3 → 4)
- **Controlled Variables**:
  - Processed input dataset (identical to baseline)
  - Eligible order population
  - Model version (1.0.0)
  - Random seed (42)
  - Shift configuration (08:00 - 18:00)
  - Queue policy (FIFO)
  - Productivity assumptions (1.0x)
  - All other stage worker counts

### 3.2 Integrity and Validation
- Baseline outputs and configuration remain untouched.
- Output deterministic behavior is validated by running the identical configuration twice and ensuring matching results.

## 4. Results

### 4.1 Primary Comparison Metrics
- **Mean Flow Time**: Decreased by 2484.28s (-11.34%)
- **P95 Flow Time**: Decreased by 1532.51s (-2.98%)
- **Mean Waiting Time**: Decreased by 2484.28s (-11.77%)
- **Dispatch Mean Queue**: Decreased by 14.03 orders (from 42.34 to 28.31)
- **Dispatch Utilization**: Decreased by ~7.79% absolute (from ~31.15% to 23.36%)

### 4.2 KPI Summary

| Metric | Baseline | Dispatch +1 | Absolute Change | Percentage Change |
|--------|----------|-------------|-----------------|-------------------|
| Orders Processed | 99,281 | 99,281 | 0 | 0.00% |
| Mean Flow Time (s) | 21,901.68 | 19,417.40 | -2,484.28 | -11.34% |
| P95 Flow Time (s) | 51,452.34 | 49,919.83 | -1,532.51 | -2.98% |
| Mean Waiting Time (s)| 21,103.65 | 18,619.37 | -2,484.28 | -11.77% |
| SLA Achievement % | 100.00% | 100.00% | 0.00% | 0.00% |

## 5. Analysis
### 5.1 Bottleneck Effect
Adding 1 worker to Dispatch reduced its utilization from ~31.15% down to 23.36%. The mean queue length dropped significantly from ~42 to ~28. Processing is now the stage with the highest queue lengths (~37), but Dispatch remains the highest utilized stage (23.36% vs Picking at 10.24%). Dispatch is still the primary bottleneck, but its severity is notably reduced.

### 5.2 Hypothesis Evaluation
**SUPPORTED**. The model hypothesis is supported by the simulation data. Adding one worker to the Dispatch stage decreased the mean wait time by over 11%, driving a proportional 11.34% improvement in average flow time. The queue accumulation at Dispatch was demonstrably mitigated.

### 5.3 Limitations
- The scenario represents a synthetic model experiment based on digital approximations of processing times.
- Does not account for spatial constraints, physical congestion, or diminishing returns from adding workers to a confined area.
