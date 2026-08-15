---
title: "Phase 01 Runtime Repair Handoff"
type: handoff-contract
status: shadow-development
version: "0.1.0"
---
# Phase 01 Runtime Repair Handoff

Phase 00 intentionally avoids active runtime mutation. Phase 01 must repair semantic wiring before the new V2 science is implemented.

## Known handoff targets identified during V1 inspection

The next phase should explicitly inspect and repair the live mappings for:

1. `force_lifecycle` construction in the Unified Research Interface;
2. the source of `force` versus `driver_transition.state`;
3. `consumption_state.lifecycle_state` versus generic state/status fallbacks;
4. `remaining_pressure` versus `remaining_asymmetry` fallback behavior;
5. semantic integrity gates that currently verify field presence more strongly than field provenance/ownership.

## Phase 01 acceptance target

After Phase 01:

- every lifecycle field must have one legal owner and source path;
- no field may silently substitute for a different semantic object;
- provenance must be machine-testable;
- V1-compatible reads remain possible;
- V2-native writes remain shadow until the later Pressure/Transmission phases are implemented.

## Explicit non-scope for Phase 01

Phase 01 should not yet implement Unreleased Pressure, release readiness, Gold-specific latent states, or empirical calibration. It prepares a clean runtime substrate for them.
