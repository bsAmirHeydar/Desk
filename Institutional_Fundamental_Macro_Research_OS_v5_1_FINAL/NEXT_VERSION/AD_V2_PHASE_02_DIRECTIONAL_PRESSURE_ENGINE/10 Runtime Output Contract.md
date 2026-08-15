---
title: "P02 Runtime Output Contract"
type: runtime-contract
status: shadow-development
---
# P02 Runtime Output Contract

The P02 runtime emits `AlphaDesk_V2_DirectionalPressureState`.

Required top-level domains:

- identity / phase / deployment / horizon / cutoff;
- aggregation mode;
- pressure core;
- pressure dynamics;
- causal-root ledger;
- freshness and coverage;
- Fundamental Driver Consumption;
- Remaining Causal Pressure;
- Persistence;
- contradiction load;
- evidence/model confidence;
- provenance;
- integrity and diagnostics.

## Forbidden future domains

P02 output must not contain:

- `price_transmission`
- `unreleased_pressure`
- `opposing_move_maturity`
- `release_readiness`

Those are explicit anti-scope guards.
