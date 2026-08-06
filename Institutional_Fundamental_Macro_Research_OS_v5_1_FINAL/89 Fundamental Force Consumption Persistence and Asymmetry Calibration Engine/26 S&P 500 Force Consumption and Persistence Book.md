---
title: "S&P 500 Force Consumption and Persistence Book"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# S&P 500 Force Consumption and Persistence Book

## Decision purpose

Translate V11 into a broad US-equity system where aggregate earnings, sector breadth, margins, nominal growth, credit, fiscal impulse, buybacks, concentration, banks, energy, volatility and valuation interact. The book prevents a mega-cap move from being mistaken for the state of the full corporate sector.

## Governing distinctions

- Index direction, equal-weight direction and sector breadth are distinct observations.
- Nominal growth can lift revenue while inflation, wages or rates compress margins and valuation.
- Credit is both a funding channel and an independent rival explanation for equity moves.
- Buybacks, issuance and passive flows affect path and absorption but do not replace earnings analysis.
- Fiscal impulse can improve near-term cash flow while raising term premium or future policy risk.

## Operating method

1. Freeze aggregate and sector earnings expectations, margins, policy path, term premium, credit, valuation and concentration.
2. Decompose the event into revenue, margin, discount-rate, risk-premium, fiscal, credit and flow channels.
3. Test whether the causal leader is broad or concentrated using equal-weight, cyclicals/defensives, banks, credit and volatility.
4. Estimate the repricing envelope by event family and regime.
5. Score consumption separately for index, sector breadth, rates/credit transmission and positioning adjustment.
6. Estimate persistence for earnings revisions, fiscal impulse, credit conditions and mechanical flows.
7. State invalidation and payoff compression before issuing an edge classification.

## Required outputs

- `spx_driver_vector`
- `spx_breadth_state`
- `spx_margin_revision`
- `spx_credit_confirmation`
- `spx_consumption_vector`
- `spx_remaining_pressure_range`
- `spx_persistence_stack`
- `spx_path_asymmetry_class`

## Failure modes and controls

- **Failure:** Equating market-cap index gains with broad earnings improvement  
  **Control:** Require equal-weight and sector evidence.
- **Failure:** Treating lower yields as uniformly bullish  
  **Control:** Separate benign disinflation from recessionary deterioration.
- **Failure:** Ignoring margin transmission  
  **Control:** Bridge wages, commodities, pricing power and productivity.
- **Failure:** Counting buybacks as permanent fundamental demand  
  **Control:** Classify window, financing and persistence.
- **Failure:** Using valuation as a timing trigger  
  **Control:** Use valuation as payoff compression and reversal-risk input.

## S&P driver matrix

| Family | Primary transmission | Required discriminator |
|---|---|---|
| Aggregate earnings | expected free cash flow | breadth of forward revisions |
| Margins | profit conversion | pricing power versus input/labor costs |
| Rates | discount and financial conditions | benign disinflation versus growth scare |
| Credit | financing and risk premium | spreads, issuance access, defaults |
| Fiscal | demand and term premium | sector incidence and funding consequence |
| Buybacks/issuance | net corporate demand | blackout calendar and financing |
| Concentration | index arithmetic | equal-weight and sector participation |
| Banks/energy | cyclical transmission | curve/credit and commodity balance |

A high-direction score may coexist with falling edge availability when valuation payoff compresses, breadth narrows and the remaining repricing gap closes.

## Canonical dependencies

- [[03 Fundamental Force and Intensity Decomposition]]
- [[13 Remaining Fundamental Pressure Decomposition]]
- [[16 Fundamental Path Asymmetry and Edge Availability]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
