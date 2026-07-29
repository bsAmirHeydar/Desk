---
title: "Equity Duration and Discount-Rate Sensitivity"
type: field-guide
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - 18-equity-fundamental-macro-and-index-mechanics
  - equity-duration-and-discount-rate-sensitivity
  - institutional-fundamental
---
# Equity Duration and Discount-Rate Sensitivity

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Equity Duration and Discount-Rate Sensitivity**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

Fixed-income risk must be represented as price sensitivity to localized curve shocks rather than by notional or maturity alone.

For **Equity Duration and Discount-Rate Sensitivity**, the relevant institutional domain is **equity**: equity value as expected cash flows, discount rates, risk premia, capital allocation, competitive structure, and index flow. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Equity Duration and Discount-Rate Sensitivity** represent, in what unit, population, instrument, and convention?
2. Which **Equity Duration and Discount-Rate Sensitivity** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Equity Duration and Discount-Rate Sensitivity** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Equity Duration and Discount-Rate Sensitivity** mechanism is active?
5. What rival model can create the same target move while **Equity Duration and Discount-Rate Sensitivity** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Equity Duration and Discount-Rate Sensitivity** decision?

## Identities and model skeleton

$$
DV01=-\frac{\partial P}{\partial y}\times 10^{-4}
$$

$$
\Delta P\approx-DV01\,\Delta y_{bp}+\tfrac12 Convexity\,(\Delta y)^2P
$$

$$
PortfolioDV01=\sum_i q_i DV01_i
$$

For **Equity Duration and Discount-Rate Sensitivity**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Equity Duration and Discount-Rate Sensitivity:** cash flows and yield convention.
- **Measurement 2 for Equity Duration and Discount-Rate Sensitivity:** modified and effective duration.
- **Measurement 3 for Equity Duration and Discount-Rate Sensitivity:** key-rate durations.
- **Measurement 4 for Equity Duration and Discount-Rate Sensitivity:** convexity and embedded options.
- **Measurement 5 for Equity Duration and Discount-Rate Sensitivity:** carry, roll, financing, and hedge basis.

The **Equity Duration and Discount-Rate Sensitivity** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Equity Duration and Discount-Rate Sensitivity:** cash-flow discounting.
- **Model layer 2 for Equity Duration and Discount-Rate Sensitivity:** key-rate decomposition.
- **Model layer 3 for Equity Duration and Discount-Rate Sensitivity:** scenario P&L.
- **Model layer 4 for Equity Duration and Discount-Rate Sensitivity:** option-adjusted risk.
- **Model layer 5 for Equity Duration and Discount-Rate Sensitivity:** DV01-neutral relative value.

Validate the **Equity Duration and Discount-Rate Sensitivity** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Structural | In the **Equity Duration and Discount-Rate Sensitivity** research object, competitive advantage, capital intensity, dilution, and terminal economics dominate. |
| Cyclical | In the **Equity Duration and Discount-Rate Sensitivity** research object, revenue, margins, credit, and discount rates change earnings power. |
| Tactical/Swing | In the **Equity Duration and Discount-Rate Sensitivity** research object, guidance, revisions, positioning, buybacks, and index flows drive campaigns. |
| Daily/Event | In the **Equity Duration and Discount-Rate Sensitivity** research object, rates, sector leaders, breadth, and earnings surprise vectors test transmission. |

Conflicts involving **Equity Duration and Discount-Rate Sensitivity** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Equity Duration and Discount-Rate Sensitivity channel 1:** test `macro demand/cost → revenue and margins`.
2. **Equity Duration and Discount-Rate Sensitivity channel 2:** test `rates and risk premium → valuation`.
3. **Equity Duration and Discount-Rate Sensitivity channel 3:** test `earnings news → revisions and dispersion`.
4. **Equity Duration and Discount-Rate Sensitivity channel 4:** test `corporate/index flows → tactical price pressure`.

**Equity Duration and Discount-Rate Sensitivity asset translation:** Equities: decompose cash-flow news, discount-rate news, risk premium, breadth, and index concentration. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Equity Duration and Discount-Rate Sensitivity** posterior or activate a rival explanation.

## Fundamental decision application

- Intraday governance: [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]

## Multi-day decision application

- Multi-day governance: [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]

## Falsification and known failure modes

- **Failure test 1 for Equity Duration and Discount-Rate Sensitivity:** sizing by notional.
- **Failure test 2 for Equity Duration and Discount-Rate Sensitivity:** mixing price value and yield sensitivity.
- **Failure test 3 for Equity Duration and Discount-Rate Sensitivity:** linearizing large shocks.
- **Failure test 4 for Equity Duration and Discount-Rate Sensitivity:** ignoring option convexity.
- **Failure test 5 for Equity Duration and Discount-Rate Sensitivity:** hedging one point while retaining curve risk.

Score **Equity Duration and Discount-Rate Sensitivity** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required research record

- Schema: [[00 Core Standards/17 Context Object and Permission Schema Standard]]

## Primary source routes for Equity Duration and Discount-Rate Sensitivity

- [[65 Source Registry and Claim Lineage/CME_RATES — CME Interest Rate Products]]
- [[65 Source Registry and Claim Lineage/TREASURY_DIRECT — TreasuryDirect Marketable Securities]]
- [[65 Source Registry and Claim Lineage/BOE_YIELD_CURVES — Bank of England Yield Curves]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Implementation Governance]]
