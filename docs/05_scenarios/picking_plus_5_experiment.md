# Picking +5 Capacity Experiment

## 1. Overview
The Picking +5 scenario represents a synthetic model experiment anchored to real Olist demand data. It does not represent observed warehouse intervention results.

This experiment tests the addition of five workers to the Picking stage, increasing capacity from 15 to 20 workers, while maintaining all other baseline parameters.

## 2. Hypothesis
**Model Hypothesis:** "Increasing Picking capacity by five workers will reduce Picking queue accumulation and waiting time and may improve overall fulfillment flow time."

## 3. Methodology
### 3.1 Experimental Configuration
- **Scenario ID**: `picking_plus_5`
- **Changed Variable**: Picking worker count (15 → 20)
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
- **Mean Flow Time**: Increased by 1.52s (+0.01%)
- **P95 Flow Time**: Increased by 72.00s (+0.14%)
- **Mean Waiting Time**: Increased by 1.47s (+0.01%)
- **Picking Mean Queue**: Decreased by 7.84 orders (from ~17.34 to 9.50)
- **Picking Utilization**: Decreased by 2.56% absolute (from 10.24% down to 7.68%)

### 4.2 KPI Summary

| Metric | Baseline | Picking +5 | Absolute Change | Percentage Change |
|--------|----------|------------|-----------------|-------------------|
| Orders Processed | 99,281 | 99,281 | 0 | 0.00% |
| Mean Flow Time (s) | 21,901.68 | 21,903.20 | +1.52 | +0.01% |
| P95 Flow Time (s) | 51,452.34 | 51,524.34 | +72.00 | +0.14% |
| Mean Waiting Time (s)| 21,103.65 | 21,105.12 | +1.47 | +0.01% |
| SLA Achievement % | 100.00% | 100.00% | 0.00% | 0.00% |

## 5. Analysis
### 5.1 Bottleneck Effect
Adding 5 workers to Picking successfully reduced its own queue (dropping by 7.84 average orders) and its utilization (dropping from 10.24% to 7.68%). However, pushing orders faster through the Picking stage simply shifted the congestion downstream to the Dispatch stage. Dispatch queues worsened (rising to ~45 average orders), and Dispatch remained heavily utilized (31.15%). The intervention produced no meaningful system-level improvement and actually marginally increased overall flow time due to downstream accumulation.

### 5.2 Hypothesis Evaluation
**PARTIALLY SUPPORTED**. The first half of the hypothesis was supported (Picking queue accumulation and wait times were reduced). However, the second half (improving overall fulfillment flow time) was strictly NOT SUPPORTED. Overall flow time slightly degraded (+1.52s) because pushing inventory faster through a non-bottleneck simply shifts queues down to the true bottleneck (Dispatch).

### 5.3 Limitations
- The scenario represents a synthetic model experiment based on digital approximations of processing times.
- Does not account for spatial constraints, physical congestion, or diminishing returns from adding workers to a confined area.
