---
title: "Target Price Transmission Constitution"
type: constitutional-method
status: shadow-development
version: "0.1.0"
---
# Target Price Transmission Constitution

## Definition

**Price Transmission** is the downstream relationship between an already-estimated causal Pressure state and the observed response of the target asset.

The target price is therefore a response variable, diagnostic variable and timing variable. It is not upstream Directional Pressure authority.

## Allowed target-price uses

Target price may be used to estimate or classify:

- response sign and magnitude;
- response latency;
- alignment versus divergence with expected signatures;
- transmission efficiency;
- compression and delayed response;
- over-transmission / price over-consumption;
- path asymmetry;
- timing and technical trigger state;
- trade quality and permission modulation;
- model disagreement and unmodeled-driver risk;
- D4 outcome metrics after the decision cutoff.

## Core transmission states reserved for later implementation

Phase 00 reserves, but does not yet operationalize, the following qualitative vocabulary:

- `ALIGNED`
- `DELAYED`
- `NEGATIVE`
- `COMPRESSED`
- `FRAGMENTED`
- `RELEASE_STARTING`
- `RELEASED`
- `OVER_TRANSMITTED`
- `UNDETERMINED`

The vocabulary is constitutional, not yet a production schema.

## Valid divergence

A strong Pressure state and an opposite target-price move may coexist for a meaningful period. The system must not collapse this into a single average state.

Example:

```text
Directional Pressure = BUY_HIGH
Target Price Response = DOWN
Price Transmission = NEGATIVE
Unmodeled Driver Risk = HIGH
Trade Permission = WAIT / NO_TRADE
```

The correct next action is diagnostic escalation, not automatic conversion of `BUY_HIGH` to `BUY_MEDIUM` or `SELL`.

## Price is allowed to matter greatly

Separating Price from Pressure does **not** make price irrelevant. A severe negative transmission can:

- make a trade premature;
- raise stop-out/path risk;
- trigger early review;
- increase uncertainty;
- block permission;
- force a missing-driver search;
- reveal that a rival causal model deserves more weight.

What it cannot do is bypass the causal-evidence layer and directly rewrite Pressure.

## Two consumptions

V2 must preserve two separate concepts:

1. `driver_consumption` — how much of the causal information/force process is processed or exhausted;
2. `price_consumption` — how much price response/expansion has already occurred relative to the active model or reference class.

Target price may inform the second. It cannot by itself determine the first.
