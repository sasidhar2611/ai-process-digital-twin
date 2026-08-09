# Extended Shift Experiment

## 1. Overview
This is a synthetic operational experiment anchored to real Olist demand data. It does not represent observed warehouse shift-performance measurements.

This experiment evaluates extending the operating window from 08:00–18:00 (10 hours) to 07:00–19:00 (12 hours) while holding all worker counts and productivity factors constant.

## 2. Hypothesis
**Model Hypothesis:** "Extending the operating window from 08:00–18:00 to 07:00–19:00 will reduce waiting caused by shift boundaries and improve overall fulfillment flow time without changing worker counts or worker productivity."

## 3. Methodology
### 3.1 Experimental Configuration
- **Scenario ID**: `extended_shift`
- **Changed Variable**: Shift hours (08:00–18:00 → 07:00–19:00)
- **Controlled Variables**:
  - Processed input dataset (identical to baseline)
  - Eligible order population
  - Model version (1.0.0)
  - Random seed (42)
  - Queue policy (FIFO)
  - Productivity factor (1.00)
  - Stage worker counts (Baseline configuration)

### 3.2 Integrity and Validation
- Baseline outputs and configuration remain untouched.
- Output deterministic behavior is validated by running the identical configuration twice and ensuring matching results.
- The `productivity_factor` correction identified in Module 5.6.4 is active, keeping `productivity_factor` at a neutral 1.00.

## 4. Results

### 4.1 Primary Comparison Metrics
- **Mean Flow Time**: Decreased by 6,061.83s (-27.68%)
- **P95 Flow Time**: Decreased by 8,078.48s (-15.70%)
- **Mean Waiting Time**: Decreased by 6,061.93s (-28.72%)
- **P95 Waiting Time**: Decreased by 7,932.02s (-15.70%)
- **Stage 1 (Processing) Wait**: Decreased by 4,185.81s
- **Dispatch Wait**: Decreased by 1,665.67s
- **Dispatch Mean Queue**: Decreased by 12.44 average orders (from 42.34 to 29.90)
- **Dispatch Utilization**: Decreased by ~5.18% absolute (from ~31.15% to 25.97%)

### 4.2 KPI Summary

| Metric | Baseline (10h) | Extended Shift (12h) | Absolute Change | Percentage Change |
|--------|----------------|----------------------|-----------------|-------------------|
| Orders Processed | 99,281 | 99,281 | 0 | 0.00% |
| Mean Flow Time (s) | 21,901.68 | 15,839.85 | -6,061.83 | -27.68% |
| P95 Flow Time (s) | 51,452.34 | 43,373.86 | -8,078.48 | -15.70% |
| Mean Waiting Time (s)| 21,103.65 | 15,041.72 | -6,061.93 | -28.72% |
| SLA Achievement % | 100.00% | 100.00% | 0.00% | 0.00% |

## 5. Analysis
### 5.1 Shift-Boundary Effect
Relaxing the shift boundary constraint by 2 hours (+20% operational time per day) dramatically reduced waiting time (-28.72%). Most of this reduction occurred at initial arrival—Stage 1 (Processing) waiting time dropped by 4,185.81s, representing nearly 70% of the total system-level wait time reduction. By starting an hour earlier and ending an hour later, the facility significantly mitigated overnight rollover queues, processing late-arriving and early-arriving orders much closer to their arrival times.

### 5.2 Bottleneck Evidence
With 20% more time to process, Dispatch utilization dropped proportionately to 25.97% (down from 31.15%), and its queue dropped to 29.90 (down from 42.34). However, Dispatch remains the strongest proportional bottleneck in the system. The bottleneck structure remains unchanged, but the intensity of the constraint is heavily diluted by the longer operating window.

### 5.3 Hypothesis Evaluation
**SUPPORTED**. Extending the shift from 08:00–18:00 to 07:00–19:00 dramatically reduced waiting times caused by shift boundaries (especially at Stage 1), directly improving overall fulfillment flow time by over 27% without changing worker counts or productivity.

### 5.4 Limitations
- Assumes workers can maintain the exact same productivity over a 12-hour shift without fatigue or error accumulation.
- Does not account for variable shift differential costs or HR limits.
