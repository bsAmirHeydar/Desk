---
title: "Direction, Confidence, Edge and Permission Separation"
type: canonical-operational-standard
status: canonical
version: 14.1.0
---
# Direction, Confidence, Edge and Permission Separation

These four objects must remain distinct:

- **Direction:** estimated causal directional state for a specified horizon.
- **Confidence:** ordinal coherence and evidence quality, not calibrated success probability.
- **Edge:** whether the current state creates a usable asymmetric opportunity after activation, transmission, pressure, consumption, reversal and event-risk checks.
- **Permission:** the minimal machine-facing gate for new entries.

A strong directional view may still be `BIAS_ONLY` or `EDGE_CONDITIONAL`. A high-confidence state may still be `NO_TRADE` if the opportunity is consumed, reversal hazard is high, event reset is imminent, or transmission is incomplete.
