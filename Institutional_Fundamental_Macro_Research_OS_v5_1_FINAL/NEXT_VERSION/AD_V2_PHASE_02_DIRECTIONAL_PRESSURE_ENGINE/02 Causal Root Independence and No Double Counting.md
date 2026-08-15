---
title: "Causal Root Independence and No Double Counting"
type: scientific-contract
status: shadow-development
---
# Causal Root Independence

P02 distinguishes **root drivers** from dependent signatures.

A root driver may carry aggregation weight. A dependent signature may provide evidence about its root but must not receive a second independent weight.

## Example — Gold

A policy-path revision may transmit through:

- front-end yields;
- real yields;
- DXY;
- rate-volatility;
- cross-asset positioning.

If the active causal model declares these as downstream manifestations of one policy/discount-rate root, they cannot all be added as independent roots.

If evidence supports genuinely independent causal roots — for example official-sector physical demand and a policy-path repricing — those roots may carry separate weight.

## Explicit-root mode

Every weighted P02 root must declare:

- `root_id`;
- `weight`;
- `polarity`;
- magnitude range;
- `source_kind`;
- `mechanism`;
- provenance and confidence;
- horizon;
- applicability;
- freshness information.

Top-level roots may not declare `depends_on_root_ids`. Dependence belongs in `dependent_signals` nested under a root. This makes double-counting machine-detectable.
