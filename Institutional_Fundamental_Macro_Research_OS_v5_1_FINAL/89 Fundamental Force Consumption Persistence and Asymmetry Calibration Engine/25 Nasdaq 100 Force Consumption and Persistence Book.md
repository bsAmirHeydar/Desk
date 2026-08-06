---
title: "Nasdaq 100 Force Consumption and Persistence Book"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Nasdaq 100 Force Consumption and Persistence Book

## Decision purpose

Translate the common V11 state ontology into the causal system that actually drives Nasdaq 100. The book prevents analysts from calling every technology rally “duration,” every earnings beat “bullish,” or every index move “fundamental.” It separates mega-cap cash-flow revision, real-rate duration, AI/semiconductor capital expenditure, concentration, dollar/liquidity, credit and mechanical index-flow effects.

## Governing distinctions

- A fall in real yields can support valuation without improving earnings; an earnings revision can improve value even when yields rise.
- Index-level evidence must be decomposed into concentration leaders, equal-weight breadth and sector/industry transmission.
- AI-capex news has distinct beneficiaries, funding burdens, depreciation lags and supply-chain bottlenecks; it is not one undifferentiated factor.
- Dealer/CTA/passive flows can propagate or reverse a move without changing the slow fundamental state.
- Fast event force, session repricing and multi-day earnings/policy persistence require separate horizon records.

## Operating method

1. Freeze pre-event policy pricing, real-yield curve, mega-cap earnings expectations, valuation state, concentration and available flow/volatility proxies.
2. Classify the catalyst into policy/rates, cash-flow/revision, AI-capex/supply chain, credit/liquidity, fiscal/regulatory, geopolitical or mechanical-flow families.
3. Map direct channels: discount rate, expected free cash flow, terminal growth, risk premium, dollar translation, financing conditions and index concentration.
4. Identify the causal leader and test independence across front-end rates, real yields, credit, semiconductors, mega-cap leaders, equal-weight indices and volatility.
5. Estimate the counterfactual repricing envelope with the method appropriate to the catalyst; never use one universal beta.
6. Score consumption by expectation incorporation, target-instrument repricing, breadth, flow exhaustion, narrative saturation and valuation payoff compression.
7. Estimate persistence separately for the event, policy path, earnings revisions, capex cycle and mechanical flow.
8. Publish rival models, invalidation, remaining-pressure range and a fundamental execution handoff.

## Required outputs

- `ndx_driver_vector`
- `ndx_causal_leader`
- `ndx_concentration_state`
- `ndx_force_components`
- `ndx_consumption_vector`
- `ndx_remaining_pressure_range`
- `ndx_persistence_stack`
- `ndx_rival_models`
- `ndx_execution_handoff_status`

## Failure modes and controls

- **Failure:** Calling a price-led squeeze an earnings re-rating  
  **Control:** Require contemporaneous forward revisions or independent cash-flow evidence.
- **Failure:** Double-counting NQ futures, QQQ and Nasdaq 100 cash as independent confirmation  
  **Control:** Treat them as one instrument family.
- **Failure:** Ignoring concentration  
  **Control:** Report top-contributor and equal-weight diagnostics.
- **Failure:** Treating all AI spending as immediate index earnings  
  **Control:** Bridge capex to revenue, margins, depreciation and supplier/customer incidence.
- **Failure:** High confidence with no dealer or prime-broker data  
  **Control:** Use public proxies and apply the flow-confidence cap.

## Nasdaq 100 driver hierarchy

| Driver family | Direct object | Fast evidence | Slow prior | Key rival |
|---|---|---|---|---|
| Policy/real rates | discount rate and terminal multiple | SOFR/OIS path, real yields | inflation regime, term premium | growth scare |
| Mega-cap earnings | index cash flow | guidance, revisions, margins | competitive advantage, capex cycle | one-off accounting/timing |
| Semiconductors/AI | capex and supply-chain earnings | orders, guidance, restrictions | adoption and capacity cycle | inventory pull-forward |
| Dollar/global liquidity | translation and risk appetite | broad dollar, funding proxies | reserve/liquidity regime | US exceptionalism |
| Credit/funding | discount and survival | spreads, issuance, funding stress | leverage/refinancing wall | equity-only positioning |
| Mechanical flows | path, not thesis | volatility, expiry, CTA/public proxies | market structure | genuine fundamental repricing |

## Horizon map

- `MICRO_0_15M`: surprise recognition, policy-curve jump, index/mega-cap first response.
- `SHORT_15_60M`: causal-leader confirmation, breadth and first flow propagation.
- `SESSION_1_6H`: repricing completion, dealer/systematic overlays, US cash participation.
- `MULTI_DAY_2_10D`: analyst revisions, management follow-through, policy repricing persistence.
- `CYCLICAL/STRUCTURAL`: AI capex, market concentration, productivity and margin architecture.

## Invalidation examples

A bullish Nasdaq state is weakened when the proposed driver fails its own transmission test: earnings optimism without revisions, rate relief caused by recessionary cash-flow deterioration, AI capex without monetization, or an index rally isolated to mechanical concentration while credit and breadth deteriorate.

## Canonical dependencies

- [[03 Fundamental Force and Intensity Decomposition]]
- [[09 Repricing Completion and Counterfactual Baselines]]
- [[19 Cross-Asset Confirmation and Causal-Leader Adjudication]]
- [[20 Observability Data Tiers and Confidence Caps]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
