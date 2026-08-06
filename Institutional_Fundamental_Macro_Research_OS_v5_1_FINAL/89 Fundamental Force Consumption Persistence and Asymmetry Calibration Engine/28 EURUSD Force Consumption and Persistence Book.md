---
title: "EURUSD Force Consumption and Persistence Book"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# EURUSD Force Consumption and Persistence Book

## Decision purpose

Translate V11 into a relative-price system. EURUSD is driven by the difference between US and euro-area policy, real rates, growth/inflation surprises, balance-of-payments and capital flows, global dollar funding, energy terms of trade, political/fiscal risk, hedging and fixing flows. Absolute “good” or “bad” news is insufficient.

## Governing distinctions

- Every macro observation must be evaluated relatively across the US and euro area.
- DXY and EURUSD are mechanically related, not independent confirmations.
- Policy-path differentials may be priced before meetings; statement direction and remaining pressure can therefore diverge.
- Month/quarter-end, fixing, hedging and repatriation can dominate intraday path without changing the medium-horizon thesis.
- Energy terms of trade and global dollar funding can override domestic surprise.

## Operating method

1. Freeze Fed/ECB curves, relative real-rate differentials, relative surprise, dollar funding, political/fiscal risks and available flow proxies.
2. Separate absolute country shocks from the bilateral differential.
3. Identify the causal leader among front-end curves, real-rate differentials, terms of trade, risk premium and flow effects.
4. Estimate event-family counterfactual repricing in differential space before translating to spot.
5. Score consumption across curves, spot, crosses, options/positioning proxies and fixing/flow adjustment.
6. Estimate persistence for policy divergence, relative growth, energy balance, fiscal risk and mechanical flows.
7. State the rival model and next fixing/event hazard.

## Required outputs

- `eurusd_relative_state`
- `fed_ecb_path_differential`
- `relative_real_rate_state`
- `dollar_funding_state`
- `flow_overlay`
- `eurusd_consumption_vector`
- `eurusd_remaining_pressure_range`
- `eurusd_persistence_stack`

## Failure modes and controls

- **Failure:** Analyzing only US data  
  **Control:** Require bilateral relative comparison.
- **Failure:** Double-counting DXY as confirmation  
  **Control:** Use non-mechanical crosses or causal inputs.
- **Failure:** Calling a fixing move fundamental  
  **Control:** Separate flow overlay from state revision.
- **Failure:** Ignoring prior meeting pricing  
  **Control:** Freeze pre-event curve.
- **Failure:** Using a stable beta across energy and funding regimes  
  **Control:** Condition counterfactuals on regime.

## Relative-driver hierarchy

1. Front-end Fed–ECB policy-path differential.
2. Relative real-rate and term-premium configuration.
3. Relative growth/inflation surprise and expected revisions.
4. Global dollar funding and risk regime.
5. Energy terms of trade and external balance.
6. Political/fiscal risk premium.
7. Hedging, fixing, month/quarter-end and repatriation flow.

The hierarchy is conditional, not permanent. Every record must name the currently dominant driver and the evidence that would transfer dominance to a rival.

## Canonical dependencies

- [[04 Surprise Materiality and Expectation Revision]]
- [[18 Regime-Conditional Interpretation and Structural Breaks]]
- [[19 Cross-Asset Confirmation and Causal-Leader Adjudication]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
