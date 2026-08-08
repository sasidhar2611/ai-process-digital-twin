# Baseline Execution

This document records the official KPIs for the `baseline` scenario, representing the canonical simulation of the historical Olist orders through the synthetic warehouse constraints.

## Execution Provenance
- **Scenario ID**: `baseline`
- **Model Version**: `1.0.0`
- **Random Seed**: `42`
- **Orders Processed**: 99,281

## Baseline KPI Summary
| Metric | Value |
|--------|-------|
| Mean Flow Time | 21,901.68s (~6.08 hrs) |
| Median Flow Time | 19,561.57s (~5.43 hrs) |
| P95 Flow Time | 51,452.34s (~14.29 hrs) |
| P99 Flow Time | 115,805.20s (~32.16 hrs) |
| Mean Total Processing Time | 798.03s (~13.3 mins) |
| Mean Total Waiting Time | 21,103.65s (~5.86 hrs) |
| SLA Achievement (5 Days) | 100.0% |
| SLA Breach Count | 0 |

*Note: The SLA threshold of 5 days (432,000s) was achieved 100% in the baseline configuration.*

## Stage Performance Summary
| Stage (Seq) | Workers | Mean Proc (s) | Mean Wait (s) | Mean Queue | Max Queue | Utilization |
|-------------|---------|---------------|---------------|------------|-----------|-------------|
| PROCESSING (1) | 5 | 61.75 | 15,574.41 | 37.30 | 867 | 5.56% |
| PICKING (2) | 15 | 341.48 | 603.66 | 17.34 | 498 | 10.24% |
| PACKING (3) | 10 | 140.67 | 298.31 | 0.01 | 14 | 6.33% |
| SORTING (4) | 5 | 46.39 | 112.69 | 0.01 | 7 | 4.17% |
| DISPATCH (5) | 3 | 207.74 | 4,514.58 | 42.34 | 779 | 31.15% |

## Bottleneck Assessment
The highest utilization occurs at **DISPATCH (31.15%)**, combined with the highest mean queue (42.34 items). PROCESSING has a large mean wait time (15,574s) reflecting massive overnight rollover accumulation, but its actual theoretical capacity is barely utilized (5.56%). This indicates that the simulated baseline is heavily overstaffed relative to the mean flow, with long flow times driven purely by the strict 10-hour operating shift boundary rather than capacity saturation.
