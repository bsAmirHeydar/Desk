---
title: "Quiet-Day Non-Event and Slow-Burn State Change"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Quiet-Day Non-Event and Slow-Burn State Change

## Decision purpose

Make the model sensitive to meaningful state changes without a new headline: curve drift, revision diffusion, funding deterioration, slow physical imbalance, positioning adjustment, valuation compression and consumption decay.

## Governing distinctions

- No headline is not no information.
- State decay is evidence-driven, not a fixed clock.
- Market-implied expectations can move continuously.
- Quiet-day flow can consume edge without changing the thesis.
- Slow processes can strengthen while catalyst freshness falls.

## Operating method

1. Carry forward the last immutable state as the prior.
2. Re-observe the causal leader, expectation curves, revisions, credit/funding, physical data and flow proxies.
3. Classify each change as new evidence, market-implied repricing, flow adjustment, consumption, contradiction or noise.
4. Update only fields whose evidence changed and record reason codes.
5. Run rival-model and confidence-cap checks.
6. Publish a no-change record when no material field changes.

## Required outputs

- `state_delta_ledger`
- `no_change_flag`
- `decay_basis`
- `quiet_day_repricing`
- `slow_burn_force`
- `consumption_update`
- `next_reassessment`

## Failure modes and controls

- **Failure:** Inventing a narrative for every price move  
  **Control:** Permit no-change and unknown.
- **Failure:** Mechanical daily score decay  
  **Control:** Require observed decay basis.
- **Failure:** Missing slow revisions  
  **Control:** Track revisions and curve drift independently of headlines.
- **Failure:** Overwriting the prior state  
  **Control:** Append an immutable delta record.

## Permitted quiet-day reason codes

`CURVE_REPRICING`, `REVISION_DIFFUSION`, `CREDIT_CHANGE`, `FUNDING_CHANGE`, `PHYSICAL_BALANCE_CHANGE`, `POSITIONING_ADJUSTMENT`, `FLOW_EXHAUSTION`, `VALUATION_COMPRESSION`, `CROSS_ASSET_CONFIRMATION`, `CONTRADICTION`, `NO_MATERIAL_CHANGE`, `DATA_QUALITY_CHANGE`.

## Canonical dependencies

- [[12 Catalyst Freshness Reinforcement and Reopening]]
- [[14 Persistence Half-Life and State Survival]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
