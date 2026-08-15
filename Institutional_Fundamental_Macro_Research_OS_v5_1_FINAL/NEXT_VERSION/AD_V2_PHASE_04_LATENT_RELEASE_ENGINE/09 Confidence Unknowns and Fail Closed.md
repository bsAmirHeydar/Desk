---
title: "P04 Confidence, Unknowns and Fail-Closed Behavior"
type: scientific-contract
status: shadow-development
---
# Confidence is separate from state

P04 can report:

`Unreleased Pressure = HIGH, Confidence = LOW`.

This is preferable to silently deleting missing evidence.

## Fail-closed conditions

P04 must fail closed when:

- P02 or P03 integrity is not `PASS`;
- P03 does not reference the exact supplied P02 Pressure fingerprint;
- active horizons differ;
- independent evidence contains target-price-derived observations;
- a required evidence item is future-dated;
- empirical claims lack a validation reference;
- a new causal driver is incorrectly treated as merely a maturity signal;
- Release is attempted without independent confirmation.
