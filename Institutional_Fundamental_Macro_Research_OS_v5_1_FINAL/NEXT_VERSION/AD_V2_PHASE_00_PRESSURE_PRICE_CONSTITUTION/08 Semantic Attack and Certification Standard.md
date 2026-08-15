---
title: "Phase 00 Semantic Attack and Certification Standard"
type: validation-standard
status: shadow-development
version: "0.1.0"
---
# Phase 00 Semantic Attack and Certification Standard

Phase 00 is not accepted because its documents sound correct. It must survive machine-readable semantic attacks.

## Hard attacks

### 1. PRICE_CONTAMINATION_ATTACK

Hold all causal drivers constant. Change only target price from a large rally to a large selloff.

Expected:

- Pressure classification remains identical;
- transmission state may change;
- model-disagreement risk may change;
- trade permission may change.

Any direct Pressure change is `HARD_FAIL`.

### 2. MOMENTUM_TIEBREAKER_ATTACK

Provide balanced/insufficient causal pressure evidence and strong target-price momentum.

Expected:

- Pressure remains `MIXED/UNRESOLVED`;
- target momentum may affect timing/permission only.

### 3. PRICE_CONSUMPTION_ATTACK

Provide a very large target-price move without new causal evidence.

Expected:

- driver consumption cannot be inferred from distance alone;
- price consumption may be high.

### 4. HIDDEN_STATE_STORY_ATTACK

Provide a wick/stop-run-looking price path without flow, order-book or other independent evidence.

Expected:

- `LIQUIDITY_SWEEP` or `ABSORPTION` cannot be `OBSERVED/CONFIRMED`;
- at most a `PLAUSIBLE_HYPOTHESIS` is allowed.

### 5. CAUSAL_DRIVER_CHANGE_ATTACK

Keep target price unchanged but materially change causal evidence (for example DXY/real-yield/policy-path state under an accepted causal model).

Expected:

- Pressure may legitimately change.

This proves the system is not merely freezing Pressure.

### 6. RESEARCH_CALLBACK_ATTACK

Create severe price disagreement without new causal evidence.

Expected:

- `RESEARCH_ESCALATION` or equivalent diagnostic action;
- no direct Pressure mutation.

Then introduce independently sourced missing-driver evidence.

Expected:

- Pressure re-estimation is now permitted.

### 7. D4_RETROACTIVE_ATTACK

Reveal future outcome after a frozen cutoff.

Expected:

- original point-in-time Pressure state remains immutable;
- D4 may score/calibrate future mappings only.

## Acceptance policy

`tools/run_phase00_acceptance.py` must pass all declared cases and verify the constitution schema, authority graph, V1 critical baseline and development manifest.
