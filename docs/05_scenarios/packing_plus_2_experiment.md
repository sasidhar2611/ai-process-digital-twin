# Packing +2 Capacity Experiment

## 1. Overview
The Packing +2 scenario represents a synthetic model experiment anchored to real Olist demand data. It does not represent observed warehouse intervention results.

This experiment tests the addition of two workers to the Packing stage, increasing capacity from 10 to 12 workers, while maintaining all other baseline parameters.

## 2. Hypothesis
**Model Hypothesis:** "Increasing Packing capacity by two workers will reduce Packing congestion, but because Packing has very low baseline queueing and utilization, the intervention may produce little or no system-level improvement."

## 3. Methodology
### 3.1 Experimental Configuration
- **Scenario ID**: `packing_plus_2`
- **Changed Variable**: Packing worker count (10 → 12)
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
- **Mean Flow Time**: Decreased by 1.02s (0.00%)
- **P95 Flow Time**: Decreased by 4.34s (0.01%)
- **Mean Waiting Time**: Decreased by 1.01s (0.00%)
- **Packing Mean Queue**: Decreased by ~0.00 orders (remained at ~0.01)
- **Packing Utilization**: Decreased by 1.05% absolute (from ~6.33% to 5.27%)

### 4.2 KPI Summary

| Metric | Baseline | Packing +2 | Absolute Change | Percentage Change |
|--------|----------|------------|-----------------|-------------------|
| Orders Processed | 99,281 | 99,281 | 0 | 0.00% |
| Mean Flow Time (s) | 21,901.68 | 21,900.67 | -1.02 | 0.00% |
| P95 Flow Time (s) | 51,452.34 | 51,448.00 | -4.34 | -0.01% |
| Mean Waiting Time (s)| 21,103.65 | 21,102.64 | -1.01 | 0.00% |
| SLA Achievement % | 100.00% | 100.00% | 0.00% | 0.00% |

## 5. Analysis
### 5.1 System-Level Effect
The Packing stage already operated efficiently in the baseline with almost zero queuing (mean queue ~0.01) and low utilization (6.33%). Adding 2 additional workers to Packing predictably resulted in a negligible system-level impact. Overall mean flow time improved by just 1 second out of a 21,901-second baseline (a 0.00% improvement). The intervention improves Packing locally by reducing utilization slightly, but has negligible system-level effect.

### 5.2 Bottleneck Evidence
The primary bottleneck remains completely unchanged. Dispatch is still the most utilized stage (31.15%), and Processing still holds the highest queue accumulation (37.30). Packing was never a bottleneck, and increasing its capacity did not shift any bottlenecks.

### 5.3 Hypothesis Evaluation
**SUPPORTED**. The hypothesis accurately predicted that the intervention would produce little or no system-level improvement due to Packing's already low baseline queueing and utilization. The data confirms this, showing a near-zero impact on overall flow time and queues.

### 5.4 Limitations
- The scenario represents a synthetic model experiment based on digital approximations of processing times.
- Does not account for spatial constraints, physical congestion, or diminishing returns from adding workers to a confined area.
