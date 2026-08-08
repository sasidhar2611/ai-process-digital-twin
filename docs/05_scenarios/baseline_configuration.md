# Baseline Configuration

This document specifies the immutable parameters defining the canonical `baseline` scenario, representing the verified state from Module 5.2. 

## Experimental Constraint
**DO NOT MUTATE BASELINE IN-PLACE.** The Baseline is an analytical anchor. All subsequent scenarios are constructed via deep-copy derivations.

## Worker Configuration (Base Capacity)
| Stage | Assigned Workers |
|-------|------------------|
| PROCESSING | 5 |
| PICKING | 15 |
| PACKING | 10 |
| SORTING | 5 |
| DISPATCH | 3 |

- **Dynamic Reallocation**: DISABLED (Workers are strictly bound to their assigned stage).

## Operating Constraints
- **Shift Hours**: 08:00 to 18:00 (Active work is paused outside this window; wait time accrues).
- **Queue Policy**: FIFO (First-In, First-Out by arrival timestamp at that specific stage).

## Productivity Configuration
- **Productivity Factor**: `1.0` (Standard baseline multiplier).

## Simulation Control
- **Random Seed**: `42`
- **Model Version**: `1.0.0`

## Initial Registered Scenarios
Derived strictly from this baseline via explicit one-factor deltas:
1. `baseline`: No changes.
2. `dispatch_plus_1`: Dispatch workers 3 -> 4.
3. `picking_plus_5`: Picking workers 15 -> 20.
4. `packing_plus_2`: Packing workers 10 -> 12.
5. `productivity_plus_10`: Productivity factor -> 1.10.
6. `extended_shift`: Shift hours -> 07:00 to 19:00.
