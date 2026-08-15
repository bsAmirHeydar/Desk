---
title: "Pressure Trend Acceleration and Snapshot Dynamics"
type: scientific-contract
status: shadow-development
---
# Pressure Trend and Acceleration

Pressure dynamics compare **Pressure snapshots to Pressure snapshots**.

They do not compare target-price returns.

## Trend

P02 preserves raw signed midpoint delta and maps it to:

- `RISING_FAST`
- `RISING`
- `STABLE`
- `FALLING`
- `FALLING_FAST`
- `UNKNOWN`

Thresholds are versioned analytical thresholds, not statistical probabilities.

## Acceleration

With at least two prior snapshots P02 computes the second difference of signed Pressure:

- `BUYWARD_ACCELERATION`
- `SELLWARD_ACCELERATION`
- `STEADY`
- `UNKNOWN`

## Point-in-time rule

Every snapshot carries its own cutoff. Later outcomes cannot alter prior Pressure history. Historical recomputation must use point-in-time evidence vintages.
