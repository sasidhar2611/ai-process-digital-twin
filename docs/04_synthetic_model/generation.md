# Generation Log

This document records the exact generation methodology and outcomes for the synthetic operational dataset.

## Generation Execution
- **Timestamp**: 2026-08-08 (UTC)
- **Model Version**: 1.0.0
- **Random Seed**: 42
- **Source Orders Analyzed**: 99,441
- **Eligible Orders Processed**: 99,281
- **Total Stage Records Generated**: 496,405
- **Stages Per Order**: 5

## Configuration Parameters
- **Shift Hours**: 08:00 - 18:00
- **Queue Policy**: FIFO

### Processing Stage Defaults
1. **PROCESSING**: Base 60s, Drivers: [order_status]
2. **PICKING**: Base 300s, Drivers: [item_count, total_volume_cm3]
3. **PACKING**: Base 120s, Drivers: [item_count, total_weight_g]
4. **SORTING**: Base 45s, Drivers: [customer_state]
5. **DISPATCH**: Base 180s, Drivers: [total_weight_g]

## Output Details
- **File**: `data/synthetic/synthetic_operational_data.parquet`
- **Metadata**: `data/synthetic/synthetic_generation_metadata.json`
- **Config**: `data/synthetic/synthetic_generation_config.json`
