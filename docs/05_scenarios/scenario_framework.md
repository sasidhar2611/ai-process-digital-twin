# Operational Scenario Framework

This document outlines the architecture for managing controlled, deterministic experimental scenarios against the baseline synthetic warehouse digital twin.

## Core Principle
The scenario framework allows controlled "what-if" experimentation (Module 5.5+) while strictly preserving the validated Module 5.2 baseline. Baseline data and configuration are immutable. Every scenario must be constructed as a deterministic variation derived from the baseline configuration.

## Scenario Identification and Determinism
Every scenario is defined by:
- `scenario_id`: A unique, deterministic identifier (e.g. `picking_plus_5`).
- `scenario_name`: Human-readable label.
- `scenario_type`: A categorized experimental constraint.
- `configuration`: The explicit model state parameters for simulation.
- `random_seed`: Seed used for generation to isolate stochasticity (Default `42`).
- `base_config_version`: Version of the underlying model to enforce compatibility.

Configuration state is explicitly decoupled from data execution. Serialized scenario JSONs yield a deterministic `SHA-256` hash to guarantee experimental provenance.

## Scenario Types
1. **BASELINE**: Exact replica of historical synthetic assumptions. No modifications.
2. **CAPACITY_SCENARIO**: ALters worker counts while keeping productivity and shift constant.
3. **PRODUCTIVITY_SCENARIO**: Alters the theoretical worker speed multiplier.
4. **SHIFT_SCENARIO**: Modifies operating hours (e.g., expanding 08:00-18:00 to 07:00-19:00).
5. **DEMAND_SCENARIO**: (Future/Reserved) Scales input demand volume.
6. **VARIABILITY_SCENARIO**: Alters statistical variance applied to Lognormal base distributions.
7. **COMBINED_SCENARIO**: Alters multiple experimental factors simultaneously.

## Scenario Comparability
Scenarios can only be directly compared analytically if they share:
- The exact same historical processed input population (`processed_orders`).
- The same underlying logical simulation engine `version`.
- The exact same common random seed strategy (default 42).

If these foundational blocks shift, variations in waiting times or output flow may stem from engine differences rather than the targeted parameter change.

## Future Execution Interface
When scenario execution is unlocked, the system will output metrics including:
- Total throughput
- Mean/Median/P95 flow times
- Queue length distributions
- Stage and worker utilization statistics
- Bottleneck shift analysis
