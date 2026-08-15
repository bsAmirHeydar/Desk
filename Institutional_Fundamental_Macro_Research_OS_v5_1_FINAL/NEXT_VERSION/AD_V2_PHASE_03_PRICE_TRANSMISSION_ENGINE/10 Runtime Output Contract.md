---
title: "P03 Runtime Output Contract"
type: runtime-contract
status: shadow-development
---
# P03 Runtime Output Contract

P03 emits a separate `PriceTransmissionState` object.

Required top-level namespaces:

- `upstream_pressure_reference`
- `expected_signature_reference`
- `response_window`
- `target_response`
- `transmission_state`
- `counterfactual_residual`
- `transmission_efficiency`
- `pathway_diagnostics`
- `model_disagreement`
- `missing_driver_escalation`
- `transmission_confidence`
- `integrity`

## Forbidden output namespaces

P03 must not emit authoritative:

- `directional_pressure` modifications;
- `unreleased_pressure`;
- `opposing_move_maturity`;
- `release_readiness`;
- `release_state`;
- `confirmed_absorption`;
- `confirmed_liquidity_grab`;
- positive `trade_permission`;
- broker instructions.

The upstream Pressure fingerprint is stored so downstream consumers can prove P03 did not replace or silently alter P02 state.
