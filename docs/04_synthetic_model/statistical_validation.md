# Statistical Validation

This document reports the statistical distributions and physical correlations observed within the synthetic operational dataset.

## External Calibration Plausibility
The external carrier handover timestamp (`order_delivered_carrier_date`) acts as a plausibility limit for the modeled warehouse workflow.

- **Orders Evaluated**: 97,644
- **Warehouse Complete BEFORE Carrier Date**: 96.80%
- **Warehouse Complete AFTER Carrier Date (Anomaly)**: 3.20%

### Anomaly Investigation (3.20% Beyond Boundary)
The 3.20% of orders finishing "after" the carrier timestamp exhibit the following characteristics:
- **Mean Item Count**: 1.12 (vs ~1.1 overall)
- **Mean Total Weight**: 2113g (vs ~2100g overall)
- **Mean Dispatch Queue**: 243 items (vs ~42 overall)
- **Mean Dispatch Wait**: 35,404s (~9.8 hrs) (vs ~1.2 hrs overall)

**Conclusion**: These anomalies are heavily driven by simulated queue congestion at DISPATCH (Stage 5), delaying completion past the true historical carrier date. This is an expected artifact of assigning static worker counts to dynamic historical demand peaks. We do NOT tune the model to force 100% compliance, as the historical warehouse capacity was likely elastic.

## Queue/Wait Relationships

There is a logical correlation between the size of the queue upon arrival and the subsequent waiting time:
- **PICKING**: correlation = 0.44
- **PACKING**: correlation = 0.49
- **SORTING**: correlation = 0.34
- **DISPATCH**: correlation = 0.90 (High queue directly drives massive dispatch waits during shift rollovers)

## Physical Complexity Relationships

Processing time scales with explicit real-world drivers configured in the simulation (Lognormal baseline × complexity multiplier).
- **PICKING vs Volume**: correlation = 0.58
- **PICKING vs Item Count**: correlation = 0.36
- **PACKING vs Weight**: correlation = 0.71
- **PACKING vs Item Count**: correlation = 0.34

*Note: Correlations are not 1.0 due to the Lognormal stochastic noise and varying worker productivity factors applied during generation.*

## Detailed Waiting Time Statistics
Waiting time distributions are heavily skewed by shift behavior. For example, 43% of PROCESSING tasks and 98% of PACKING tasks wait exactly 0 seconds (immediate worker availability), while others accrue long off-shift delays.
- **PROCESSING**: Mean 4.3h, 43% zero wait.
- **PICKING**: Mean 10m, 53% zero wait.
- **PACKING**: Mean 5m, 98% zero wait.
- **SORTING**: Mean 1.8m, 98% zero wait.
- **DISPATCH**: Mean 1.25h, 32% zero wait.
