# Calibration Strategy

Because actual warehouse processing times, queues, and shifts are unavailable in the Olist dataset, the synthetic operational model cannot claim to reproduce historically measured warehouse timelines exactly.

## Calibration Principles
1. **Consistency with Macroscopic Metrics**: The synthetic operational timeline (from Stage 1 to Stage 5) MUST fit logically within the real-world boundaries established by `order_approved_at` and `order_delivered_carrier_date`. The total synthetic time (processing + waiting) across all 5 stages should theoretically explain the delay between approval and carrier handover.
2. **Relative Operational Realism**: 
   - Picking and Dispatching are physically intensive and should have higher base processing times than digital Processing or Sorting.
   - Variances (e.g., Lognormal sigma parameters) should be constrained to avoid physically impossible extremes (e.g., a 24-hour single packing event).
3. **Sensitivity Analysis**: Parameters that are purely assumed (e.g., worker counts, base processing times) will be exposed for sensitivity analysis later. The model will define configuration bounds, not absolute truths.

## Future Research & Fine-Tuning
Currently, there are no fabricated external industry citations. If literature review later indicates that average e-commerce picking times are, for example, 3 minutes per item, the configuration object `StageConfiguration` will be updated to reflect that, and it will be documented as an external assumption.

## Provenance and Seed
Synthetic data will be reproducible.
- **Random Seed**: A fixed random seed (default: 42) ensures deterministic generation.
- **Version**: A `version` string in the configuration will tie generated datasets to specific calibration snapshots.
