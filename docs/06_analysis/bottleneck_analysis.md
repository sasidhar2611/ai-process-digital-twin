# Formal Bottleneck Analysis

## 1. Overview
This document analyzes the canonical baseline operational metrics to identify the primary constraints (bottlenecks) in the synthetic digital twin model of the Olist fulfillment process. 

**Disclaimer**: The bottleneck findings represent behavior of the developed synthetic digital twin under model assumptions and should not be interpreted as direct measurements of Olist warehouses.

## 2. Bottleneck Scoring Methodology
A bottleneck is often incorrectly identified using stage utilization alone. This analysis employs a transparent, multi-dimensional scoring methodology that aggregates four critical metrics for each stage:
- **Stage Utilization**: Proportion of total available worker time actively spent processing.
- **Mean Queue Length**: Average number of orders waiting at the stage.
- **P95 Queue Length**: 95th percentile queue length, indicating peak congestion.
- **Mean Waiting Time**: Average time an order spends waiting for a worker at the stage.

**Scoring Logic**:
For each of the four metrics, the stage's value is normalized against the maximum observed value across all five stages.
`Normalized Score = Stage Value / Max Observed Value`
The theoretical maximum score for a stage is 4.0 (if a stage holds the maximum value in all four metrics). The stage with the highest aggregated score is designated the overall bottleneck candidate.

## 3. Baseline Findings

### 3.1 Stage-Level Scores
| Stage | Utilization | Mean Queue | Mean Wait (s) | Bottleneck Score |
|-------|-------------|------------|---------------|------------------|
| **DISPATCH** | 31.15% | 42.34 | 4,514.58 | **3.29** |
| **PROCESSING** | 5.56% | 37.30 | 15,574.42 | **2.95** |
| **PICKING** | 10.24% | 17.34 | 603.66 | **1.19** |
| **PACKING** | 6.33% | 0.01 | 298.31 | **0.22** |
| **SORTING** | 4.17% | 0.01 | 112.69 | **0.14** |

### 3.2 Constraint Diagnosis
1. **Highest Utilization Stage**: **DISPATCH (31.15%)**. Dispatch workers spend the highest proportion of their shift actively engaged.
2. **Highest Queue Stage**: **DISPATCH (42.34)**. The average number of pending orders is highest at Dispatch, closely followed by Processing.
3. **Strongest Waiting Contributor**: **PROCESSING (15,574.42s)**. The first stage absorbs the entirety of off-shift overnight arrivals. This represents system boundary wait time rather than active in-process congestion.
4. **Overall Bottleneck Candidate**: **DISPATCH (Score: 3.29)**. Dispatch demonstrates the strongest internal process bottleneck evidence.

### 3.3 Discussion
It is critical to explicitly distinguish "highest queue" and "largest waiting contributor." **Processing** has a massive waiting contribution because it is the first stage in the system—orders arrive 24/7 in the real Olist data, but the synthetic model only processes them during a 10-hour shift. This creates a massive overnight rollover wait. However, once an order enters the system, **Dispatch** acts as the primary in-process bottleneck, holding both the highest utilization and the highest active queue accumulation.
