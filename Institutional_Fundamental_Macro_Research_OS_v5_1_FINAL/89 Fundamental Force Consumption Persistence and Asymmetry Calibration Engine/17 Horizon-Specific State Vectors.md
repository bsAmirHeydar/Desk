---
title: "Horizon-Specific State Vectors"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Horizon-Specific State Vectors

## Decision purpose

Prevent horizon leakage by requiring separate state vectors for micro, hourly, session, daily, multi-day, cyclical and structural decisions.

## Governing distinctions

- A shock can be exhausted intraday but structurally important.
- A structural prior constrains, but does not dictate, tactical direction.
- Flow overlays often have shorter half-lives than economic-state changes.
- Cross-horizon conflict is information, not an error to average away.

## Operating method

1. Select all horizons material to the task.
2. Create independent state vectors at each horizon.
3. Record inherited priors and tactical overrides.
4. Resolve conflicts with causal timing and expiry rules.
5. Prohibit unlabeled score copying across horizons.

## Required outputs

- `horizon_state_vectors`
- `inheritance_map`
- `conflict_state`
- `dominant_horizon`
- `tactical_override`
- `next_horizon_checkpoint`

## Failure modes and controls

- **Failure:** One score reused everywhere  
  **Control:** Validator requires distinct horizon records or an explicit equality rationale.
- **Failure:** Structural bullishness blocks tactical bearish state  
  **Control:** Allow signed conflict with separate evidence.
- **Failure:** Micro price response validates cyclical thesis  
  **Control:** Respect evidence and horizon boundaries.

## Mandatory horizon grid

| Code | Intended object |
|---|---|
| `MICRO_0_15M` | immediate parsing and first mechanical response |
| `SHORT_15_60M` | initial expectation and cross-asset repricing |
| `SESSION_1_6H` | session propagation, flow and liquidity |
| `DAILY_OPEN_TO_CLOSE` | full-day state and close-related flows |
| `MULTI_DAY_2_10D` | policy, earnings, physical or risk-premium campaign |
| `CYCLICAL` | business/earnings/policy cycle |
| `STRUCTURAL` | durable institutional or balance-sheet state |

Every horizon owns a separate direction, force, consumption, remaining-pressure, persistence, reversal-risk and edge record. Inheritance must be explicit; copying is prohibited.

## Canonical dependencies

- [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/01 Architecture and Horizon Separation]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.

## V21 Horizon Direction Tensor
Module 103 makes the horizon array a first-class runtime Tensor and adds `SWING_2_8W` as a cognitive overlay between multi-day and cyclical horizons. The active strategy horizon must be declared before permission. Cross-horizon conflict is preserved as information; structural state is a prior, not an automatic tactical command.

## V21.1 canonical SWING ownership
`SWING_2_8W` is no longer only a Module 103 overlay. It is a canonical Module 89 Fundamental horizon between `MULTI_DAY_2_10D` and `CYCLICAL`; Module 103 may reason over it but cannot create its Direction. This closes the authority ambiguity introduced by V21.0.
