---
title: "Signed Magnitude and Pressure Classification"
type: scientific-contract
status: shadow-development
---
# Signed Magnitude and Pressure Classification

## Vocabulary

P02 uses an analytical ordinal scale. It is **not a probability** and is not claimed to be empirically calibrated.

Magnitude bands:

- `VERY_LOW`: 0–19.999
- `LOW`: 20–39.999
- `MEDIUM`: 40–59.999
- `HIGH`: 60–74.999
- `VERY_HIGH`: 75–89.999
- `EXTREME`: 90–100

Signed headline classes are formed from sign + magnitude, for example `BUY_HIGH` or `SELL_VERY_HIGH`.

## Range first, class second

The authoritative object is a range, not a point. P02 reports:

- signed lower/upper interval;
- midpoint as a diagnostic convenience;
- low/high ordinal classes implied by the interval;
- headline class from the midpoint;
- precision state from interval width.

If the signed interval crosses zero, headline sign becomes `CONTESTED_OR_UNDETERMINED` regardless of midpoint.

## V1-compatible wrap

When reading P01/Module 89, P02 takes:

- sign from exact-horizon Fundamental Direction;
- magnitude from exact-horizon Module 89 Force range;
- never from target price.

This finally gives P01's raw force range an explicit V2 signed pressure vocabulary.
