---
title: "10 Clock Collision and Temporal Dominance Engine"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
---
# Clock Collision and Temporal Dominance Engine

Institutional days often contain overlapping clocks: NFP + Treasury supply + month-end + WMR + expiry + cash open. Do not count them as independent votes.

Rank clocks by causal materiality, participant/notional breadth, proximity, persistence, information novelty, liquidity sensitivity, target-asset linkage and evidence quality.

Classify interactions: `REINFORCING`, `OFFSETTING`, `SEQUENTIAL`, `MASKING`, `LIQUIDITY_AMPLIFYING`, `MECHANICAL_OVERRIDE`, `UNDETERMINED`.

Output: `CLEAR_DOMINANT_CLOCK`, `CO_DOMINANT_REINFORCING`, `CO_DOMINANT_OFFSETTING`, `SEQUENTIAL_CLOCKS`, `TEMPORALLY_FRAGMENTED`, or `CLOCK_UNRESOLVED`.
