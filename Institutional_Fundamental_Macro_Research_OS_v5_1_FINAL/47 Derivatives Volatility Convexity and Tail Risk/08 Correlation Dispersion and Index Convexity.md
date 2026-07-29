---
title: "Correlation Dispersion and Index Convexity"
type: field-guide
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - 47-derivatives-volatility-convexity-and-tail-risk
  - correlation-dispersion-and-index-convexity
  - institutional-fundamental
---
# Correlation Dispersion and Index Convexity

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Correlation Dispersion and Index Convexity**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

Fixed-income risk must be represented as price sensitivity to localized curve shocks rather than by notional or maturity alone.

For **Correlation Dispersion and Index Convexity**, the relevant institutional domain is **microstructure**: how information and forced demand meet liquidity, dealer balance sheets, order books, derivatives hedging, and execution constraints. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Correlation Dispersion and Index Convexity** represent, in what unit, population, instrument, and convention?
2. Which **Correlation Dispersion and Index Convexity** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Correlation Dispersion and Index Convexity** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Correlation Dispersion and Index Convexity** mechanism is active?
5. What rival model can create the same target move while **Correlation Dispersion and Index Convexity** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Correlation Dispersion and Index Convexity** decision?

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

For **Correlation Dispersion and Index Convexity**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Correlation Dispersion and Index Convexity:** cash flows and yield convention.
- **Measurement 2 for Correlation Dispersion and Index Convexity:** modified and effective duration.
- **Measurement 3 for Correlation Dispersion and Index Convexity:** key-rate durations.
- **Measurement 4 for Correlation Dispersion and Index Convexity:** convexity and embedded options.
- **Measurement 5 for Correlation Dispersion and Index Convexity:** carry, roll, financing, and hedge basis.

The **Correlation Dispersion and Index Convexity** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Correlation Dispersion and Index Convexity:** cash-flow discounting.
- **Model layer 2 for Correlation Dispersion and Index Convexity:** key-rate decomposition.
- **Model layer 3 for Correlation Dispersion and Index Convexity:** scenario P&L.
- **Model layer 4 for Correlation Dispersion and Index Convexity:** option-adjusted risk.
- **Model layer 5 for Correlation Dispersion and Index Convexity:** DV01-neutral relative value.

Validate the **Correlation Dispersion and Index Convexity** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Structural | In the **Correlation Dispersion and Index Convexity** research object, venue rules, clearing, dealer capacity, and participant ecology set market behavior. |
| Cyclical | In the **Correlation Dispersion and Index Convexity** research object, volatility and balance-sheet capacity alter depth and impact. |
| Tactical/Swing | In the **Correlation Dispersion and Index Convexity** research object, positioning, expiry, systematic triggers, and flow persistence matter. |
| Intraday | In the **Correlation Dispersion and Index Convexity** research object, spread, depth, queue, auction, and hedge feedback determine path and cost. |

Conflicts involving **Correlation Dispersion and Index Convexity** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Correlation Dispersion and Index Convexity channel 1:** test `information → order imbalance`.
2. **Correlation Dispersion and Index Convexity channel 2:** test `options exposure → hedge flow`.
3. **Correlation Dispersion and Index Convexity channel 3:** test `volatility/price → systematic rebalance`.
4. **Correlation Dispersion and Index Convexity channel 4:** test `liquidity withdrawal → nonlinear impact and gaps`.

**Correlation Dispersion and Index Convexity asset translation:** Execution: validate estimated flow against spread, depth, volume, and realized response. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Correlation Dispersion and Index Convexity** posterior or activate a rival explanation.

## Fundamental decision application

- Intraday governance: [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]

## Multi-day decision application

- Multi-day governance: [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]

## Falsification and known failure modes

- **Failure test 1 for Correlation Dispersion and Index Convexity:** sizing by notional.
- **Failure test 2 for Correlation Dispersion and Index Convexity:** mixing price value and yield sensitivity.
- **Failure test 3 for Correlation Dispersion and Index Convexity:** linearizing large shocks.
- **Failure test 4 for Correlation Dispersion and Index Convexity:** ignoring option convexity.
- **Failure test 5 for Correlation Dispersion and Index Convexity:** hedging one point while retaining curve risk.

Score **Correlation Dispersion and Index Convexity** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required research record

- Schema: [[00 Core Standards/17 Context Object and Permission Schema Standard]]

## Primary source routes for Correlation Dispersion and Index Convexity

- [[65 Source Registry and Claim Lineage/CME_RATES — CME Interest Rate Products]]
- [[65 Source Registry and Claim Lineage/TREASURY_DIRECT — TreasuryDirect Marketable Securities]]
- [[65 Source Registry and Claim Lineage/BOE_YIELD_CURVES — Bank of England Yield Curves]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Implementation Governance]]
