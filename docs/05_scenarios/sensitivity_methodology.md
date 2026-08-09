# Sensitivity Methodology

This document outlines the strict statistical methodology guiding experimental scenario evaluation within the digital twin.

## One-Factor-At-A-Time (OFAT) Principle
By default, the simulation relies on the **One-Factor-At-A-Time** principle. 

Every sensitivity scenario must isolate exactly ONE experimental parameter delta from the baseline. For example, scenario `dispatch_plus_1` alters ONLY the Dispatch worker count from 3 to 4, leaving picking capacity, packing capacity, productivity, shifts, and seeds strictly identical.

This mathematical isolation is strictly required because warehouse queues are highly non-linear. If we simultaneously increase packing speed and dispatch capacity, we cannot logically untangle which lever solved the shift-rollover bottleneck.

## Common Random Seed Strategy (CRSS)
The synthetic generator incorporates stochastic variation (e.g. Lognormal baseline variation and worker productivity multipliers per task).

To isolate the effect of the parameter change from simple statistical noise, we employ a **Common Random Seed Strategy**. 
- All derived scenarios share the exact same random seed (Default `42`).
- This guarantees that the stream of generated random numbers dictating processing speeds remains identical. Order #12345 in the Baseline takes exactly the same underlying physical time to pick as Order #12345 in `dispatch_plus_1` scenario (unless the scenario specifically alters picking parameters).

*Disclaimer*: Utilizing a single common seed does not eliminate stochastic uncertainty entirely; it simply isolates the relative delta between scenarios. A robust future sensitivity analysis may evaluate these scenarios across an ensemble of 10-30 varied seeds to produce confidence intervals. 

## Defined Experimental Ranges
For future operational evaluation, analytical boundaries (not to be confused with historical measurements) are established to guide plausible bounds:
- **Dispatch Workers**: 2 to 6
- **Picking Workers**: 10 to 25
- **Packing Workers**: 6 to 15
- **Productivity Multiplier**: 0.90 (-10%) to 1.20 (+20%)
- **Shift Duration**: 8 to 12 Hours

These ranges are theoretical scenario assumptions, NOT claims about the physical ground truth operations of the historical Olist dataset.

## Data Lineage
It is critical to distinguish between:
1. **REAL DATA**: Immutable source observations (e.g., historical approval dates).
2. **DERIVED DATA**: Processed physical computations (e.g., total volume).
3. **MODEL PARAMETER**: Theoretical structural definitions (e.g., Lognormal base 300s).
4. **SCENARIO ASSUMPTION**: Theoretical experimental levers applied (e.g., +5 picking workers).
5. **EXPERIMENTAL RANGE**: The analytical limits applied to scenario assumptions.

## Executed Scenarios
- **Baseline**: Module 5.5
- **Dispatch Capacity +1** (`dispatch_plus_1`): Evaluated in Module 5.6.1. Demonstrates the strict application of OFAT by modifying only the Dispatch worker count.
- **Picking Capacity +5** (`picking_plus_5`): Evaluated in Module 5.6.2. Demonstrates OFAT isolation by exclusively expanding Picking worker count.
