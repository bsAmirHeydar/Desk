---
title: "Rates Volatility Skew and Convexity"
type: field-guide
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - 16-rates-fixed-income-and-policy-pricing
  - rates-volatility-skew-and-convexity
  - institutional-fundamental
---
# Rates Volatility Skew and Convexity

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Rates Volatility Skew and Convexity**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

Fixed-income risk must be represented as price sensitivity to localized curve shocks rather than by notional or maturity alone. Volatility analysis distinguishes realized variation, option-implied risk-neutral expectations, variance risk premium, skew, term structure, supply/demand, and jump risk.

For **Rates Volatility Skew and Convexity**, the relevant institutional domain is **rates**: the path of policy rates, sovereign cash flows, duration supply, inflation compensation, collateral, funding, and term risk. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Rates Volatility Skew and Convexity** represent, in what unit, population, instrument, and convention?
2. Which **Rates Volatility Skew and Convexity** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Rates Volatility Skew and Convexity** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Rates Volatility Skew and Convexity** mechanism is active?
5. What rival model can create the same target move while **Rates Volatility Skew and Convexity** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Rates Volatility Skew and Convexity** decision?

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

$$
RV=\sqrt{\sum_{i=1}^{N}r_i^2}\sqrt{Annualization}
$$

$$
VRP=IV^2-E^P[RV^2]
$$

$$
VarianceSwapRate\approx \frac{2}{T}\int_0^\infty \frac{Q(K)}{K^2}\,dK
$$

For **Rates Volatility Skew and Convexity**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Rates Volatility Skew and Convexity:** cash flows and yield convention.
- **Measurement 2 for Rates Volatility Skew and Convexity:** modified and effective duration.
- **Measurement 3 for Rates Volatility Skew and Convexity:** key-rate durations.
- **Measurement 4 for Rates Volatility Skew and Convexity:** convexity and embedded options.
- **Measurement 5 for Rates Volatility Skew and Convexity:** carry, roll, financing, and hedge basis.
- **Measurement 6 for Rates Volatility Skew and Convexity:** realized volatility by horizon.
- **Measurement 7 for Rates Volatility Skew and Convexity:** ATM implied volatility and term structure.
- **Measurement 8 for Rates Volatility Skew and Convexity:** put/call skew and smile dynamics.
- **Measurement 9 for Rates Volatility Skew and Convexity:** vol-of-vol, correlation, and dispersion.
- **Measurement 10 for Rates Volatility Skew and Convexity:** open interest, flow, and event calendar.

The **Rates Volatility Skew and Convexity** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Rates Volatility Skew and Convexity:** cash-flow discounting.
- **Model layer 2 for Rates Volatility Skew and Convexity:** key-rate decomposition.
- **Model layer 3 for Rates Volatility Skew and Convexity:** scenario P&L.
- **Model layer 4 for Rates Volatility Skew and Convexity:** option-adjusted risk.
- **Model layer 5 for Rates Volatility Skew and Convexity:** DV01-neutral relative value.
- **Model layer 6 for Rates Volatility Skew and Convexity:** arbitrage-clean surface.
- **Model layer 7 for Rates Volatility Skew and Convexity:** HAR/GARCH benchmarks.
- **Model layer 8 for Rates Volatility Skew and Convexity:** variance-risk-premium decomposition.
- **Model layer 9 for Rates Volatility Skew and Convexity:** jump and event variance.
- **Model layer 10 for Rates Volatility Skew and Convexity:** risk-neutral density extraction.

Validate the **Rates Volatility Skew and Convexity** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Structural | In the **Rates Volatility Skew and Convexity** research object, neutral rate, debt structure, inflation regime, and investor base anchor the curve. |
| Cyclical | In the **Rates Volatility Skew and Convexity** research object, policy path, inflation compensation, credit, and term premium evolve. |
| Tactical/Swing | In the **Rates Volatility Skew and Convexity** research object, issuance, auctions, positioning, carry, and relative value dominate. |
| Daily/Event | In the **Rates Volatility Skew and Convexity** research object, meeting pricing, WI levels, funding, and liquid futures lead the response. |

Conflicts involving **Rates Volatility Skew and Convexity** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Rates Volatility Skew and Convexity channel 1:** test `data and policy → expected short rates`.
2. **Rates Volatility Skew and Convexity channel 2:** test `fiscal supply and risk appetite → term premium`.
3. **Rates Volatility Skew and Convexity channel 3:** test `collateral and balance sheet → repo/basis`.
4. **Rates Volatility Skew and Convexity channel 4:** test `rates → FX, equity duration, credit, housing, and gold`.

**Rates Volatility Skew and Convexity asset translation:** Rates: separate expected short-rate changes, term premium, inflation compensation, carry/roll, and funding. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Rates Volatility Skew and Convexity** posterior or activate a rival explanation.

## Fundamental decision application

- Intraday governance: [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]

## Multi-day decision application

- Multi-day governance: [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]

## Falsification and known failure modes

- **Failure test 1 for Rates Volatility Skew and Convexity:** sizing by notional.
- **Failure test 2 for Rates Volatility Skew and Convexity:** mixing price value and yield sensitivity.
- **Failure test 3 for Rates Volatility Skew and Convexity:** linearizing large shocks.
- **Failure test 4 for Rates Volatility Skew and Convexity:** ignoring option convexity.
- **Failure test 5 for Rates Volatility Skew and Convexity:** hedging one point while retaining curve risk.
- **Failure test 6 for Rates Volatility Skew and Convexity:** comparing mismatched IV/RV horizons.
- **Failure test 7 for Rates Volatility Skew and Convexity:** using VIX as fear sentiment only.
- **Failure test 8 for Rates Volatility Skew and Convexity:** ignoring strike liquidity.
- **Failure test 9 for Rates Volatility Skew and Convexity:** calling skew a directional forecast.
- **Failure test 10 for Rates Volatility Skew and Convexity:** omitting carry and convexity.

Score **Rates Volatility Skew and Convexity** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required research record

- Schema: [[00 Core Standards/17 Context Object and Permission Schema Standard]]

## Primary source routes for Rates Volatility Skew and Convexity

- [[65 Source Registry and Claim Lineage/CME_RATES — CME Interest Rate Products]]
- [[65 Source Registry and Claim Lineage/TREASURY_DIRECT — TreasuryDirect Marketable Securities]]
- [[65 Source Registry and Claim Lineage/BOE_YIELD_CURVES — Bank of England Yield Curves]]
- [[65 Source Registry and Claim Lineage/CBOE_VIX — Cboe VIX Methodology]]
- [[65 Source Registry and Claim Lineage/SEC_MARKETS — SEC Division of Trading and Markets]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Implementation Governance]]
