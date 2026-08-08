# Calibration Results

This document presents the calibration and distribution statistics of the generated synthetic warehouse dataset.

## Carrier Plausibility Validation
`order_delivered_carrier_date` acts strictly as an external plausibility boundary. The warehouse synthetic pipeline should ideally complete dispatch before this carrier handover.
- **Orders evaluated**: 97,644
- **Percentage completing warehouse before carrier date**: 96.80%
- **Percentage extending beyond carrier date**: 3.20%

*Conclusion*: The macroscopic scaling factors are highly plausible. The vast majority of warehouse simulation traces conclude logically before carrier handover.

## Stage Distribution Statistics

### Stage 1 (PROCESSING)
- **Processing Time**: mean=61.75s, p50=60.19s, p95=87.12s, min=24.48s, max=170.35s
- **Waiting Time**: mean=15,574s (4.3 hrs), p50=4,572s (1.2 hrs), max=55,777s (15.5 hrs)
- **Queue Length**: mean=37.30, p50=7, max=867
- **Productivity Factor**: mean=1.00, p50=1.00, min=0.55, max=1.42

### Stage 2 (PICKING)
- **Processing Time**: mean=341.48s, p50=325.87s, p95=507.84s, min=122.85s, max=4,920.39s
- **Waiting Time**: mean=603.66s, p50=0s, p95=1,508.25s, max=55,902.82s
- **Queue Length**: mean=17.34, p50=0, max=498

### Stage 3 (PACKING)
- **Processing Time**: mean=140.67s, p50=132.06s, p95=218.21s, min=48.05s, max=2,722.29s
- **Waiting Time**: mean=298.31s, p50=0s, max=50,399.81s
- **Queue Length**: mean=0.01, p50=0, max=14

### Stage 4 (SORTING)
- **Processing Time**: mean=46.39s, p50=45.20s, p95=65.35s, min=16.90s, max=113.47s
- **Waiting Time**: mean=112.69s, p50=0s, max=50,399.75s
- **Queue Length**: mean=0.01, p50=0, max=7

### Stage 5 (DISPATCH)
- **Processing Time**: mean=207.74s, p50=196.11s, p95=319.10s, min=75.95s, max=2,575.47s
- **Waiting Time**: mean=4,514.58s, p50=943.13s, p95=13,067.30s, max=155,020.05s
- **Queue Length**: mean=42.34, p50=13, max=779
