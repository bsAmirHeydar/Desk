---
title: "Term Premium Supply and Convexity Interaction"
type: field-guide
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - 29-public-debt-and-government-bond-market-intelligence
  - term-premium-supply-and-convexity-interaction
  - institutional-fundamental
---
# Term Premium Supply and Convexity Interaction

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Term Premium Supply and Convexity Interaction**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

A nominal yield is decomposed into the expected path of short rates and compensation for bearing duration, inflation, supply, and model risk. Fixed-income risk must be represented as price sensitivity to localized curve shocks rather than by notional or maturity alone.

For **Term Premium Supply and Convexity Interaction**, the relevant institutional domain is **rates**: the path of policy rates, sovereign cash flows, duration supply, inflation compensation, collateral, funding, and term risk. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Term Premium Supply and Convexity Interaction** represent, in what unit, population, instrument, and convention?
2. Which **Term Premium Supply and Convexity Interaction** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Term Premium Supply and Convexity Interaction** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Term Premium Supply and Convexity Interaction** mechanism is active?
5. What rival model can create the same target move while **Term Premium Supply and Convexity Interaction** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Term Premium Supply and Convexity Interaction** decision?

## Identities and model skeleton

$$
y_t^{(n)}=\frac1n\sum_{j=0}^{n-1}E_t(i_{t+j})+TP_t^{(n)}
$$

$$
P_t^{(n)}=\exp(A_n+B_n^\top X_t)
$$

$$
RX_{t+1}^{(n)}=\alpha_n+\beta_n^\top X_t+\varepsilon_{t+1}^{(n)}
$$

$$
DV01=-\frac{\partial P}{\partial y}\times 10^{-4}
$$

$$
\Delta P\approx-DV01\,\Delta y_{bp}+\tfrac12 Convexity\,(\Delta y)^2P
$$

$$
PortfolioDV01=\sum_i q_i DV01_i
$$

For **Term Premium Supply and Convexity Interaction**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Term Premium Supply and Convexity Interaction:** zero-coupon nominal curve.
- **Measurement 2 for Term Premium Supply and Convexity Interaction:** survey expectations.
- **Measurement 3 for Term Premium Supply and Convexity Interaction:** forward rates.
- **Measurement 4 for Term Premium Supply and Convexity Interaction:** duration supply and foreign demand.
- **Measurement 5 for Term Premium Supply and Convexity Interaction:** term-premium estimates from multiple models.
- **Measurement 6 for Term Premium Supply and Convexity Interaction:** cash flows and yield convention.
- **Measurement 7 for Term Premium Supply and Convexity Interaction:** modified and effective duration.
- **Measurement 8 for Term Premium Supply and Convexity Interaction:** key-rate durations.
- **Measurement 9 for Term Premium Supply and Convexity Interaction:** convexity and embedded options.
- **Measurement 10 for Term Premium Supply and Convexity Interaction:** carry, roll, financing, and hedge basis.

The **Term Premium Supply and Convexity Interaction** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Term Premium Supply and Convexity Interaction:** affine no-arbitrage term structure.
- **Model layer 2 for Term Premium Supply and Convexity Interaction:** ACM excess-return regression.
- **Model layer 3 for Term Premium Supply and Convexity Interaction:** survey-augmented decomposition.
- **Model layer 4 for Term Premium Supply and Convexity Interaction:** PCA factor models.
- **Model layer 5 for Term Premium Supply and Convexity Interaction:** model-ensemble and residual attribution.
- **Model layer 6 for Term Premium Supply and Convexity Interaction:** cash-flow discounting.
- **Model layer 7 for Term Premium Supply and Convexity Interaction:** key-rate decomposition.
- **Model layer 8 for Term Premium Supply and Convexity Interaction:** scenario P&L.
- **Model layer 9 for Term Premium Supply and Convexity Interaction:** option-adjusted risk.
- **Model layer 10 for Term Premium Supply and Convexity Interaction:** DV01-neutral relative value.

Validate the **Term Premium Supply and Convexity Interaction** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Structural | In the **Term Premium Supply and Convexity Interaction** research object, neutral rate, debt structure, inflation regime, and investor base anchor the curve. |
| Cyclical | In the **Term Premium Supply and Convexity Interaction** research object, policy path, inflation compensation, credit, and term premium evolve. |
| Tactical/Swing | In the **Term Premium Supply and Convexity Interaction** research object, issuance, auctions, positioning, carry, and relative value dominate. |
| Daily/Event | In the **Term Premium Supply and Convexity Interaction** research object, meeting pricing, WI levels, funding, and liquid futures lead the response. |

Conflicts involving **Term Premium Supply and Convexity Interaction** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Term Premium Supply and Convexity Interaction channel 1:** test `data and policy → expected short rates`.
2. **Term Premium Supply and Convexity Interaction channel 2:** test `fiscal supply and risk appetite → term premium`.
3. **Term Premium Supply and Convexity Interaction channel 3:** test `collateral and balance sheet → repo/basis`.
4. **Term Premium Supply and Convexity Interaction channel 4:** test `rates → FX, equity duration, credit, housing, and gold`.

**Term Premium Supply and Convexity Interaction asset translation:** Rates: separate expected short-rate changes, term premium, inflation compensation, carry/roll, and funding. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Term Premium Supply and Convexity Interaction** posterior or activate a rival explanation.

## Fundamental decision application

- Intraday governance: [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]

## Multi-day decision application

- Multi-day governance: [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]

## Falsification and known failure modes

- **Failure test 1 for Term Premium Supply and Convexity Interaction:** treating one model estimate as observed truth.
- **Failure test 2 for Term Premium Supply and Convexity Interaction:** conflating term premium with fiscal risk alone.
- **Failure test 3 for Term Premium Supply and Convexity Interaction:** using par yields in place of zero rates.
- **Failure test 4 for Term Premium Supply and Convexity Interaction:** ignoring convexity and carry.
- **Failure test 5 for Term Premium Supply and Convexity Interaction:** failing to reconcile model disagreement.
- **Failure test 6 for Term Premium Supply and Convexity Interaction:** sizing by notional.
- **Failure test 7 for Term Premium Supply and Convexity Interaction:** mixing price value and yield sensitivity.
- **Failure test 8 for Term Premium Supply and Convexity Interaction:** linearizing large shocks.
- **Failure test 9 for Term Premium Supply and Convexity Interaction:** ignoring option convexity.
- **Failure test 10 for Term Premium Supply and Convexity Interaction:** hedging one point while retaining curve risk.

Score **Term Premium Supply and Convexity Interaction** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required research record

- Schema: [[00 Core Standards/17 Context Object and Permission Schema Standard]]

## Primary source routes for Term Premium Supply and Convexity Interaction

- [[65 Source Registry and Claim Lineage/NYFED_TERM_PREMIA — New York Fed — Term Premia]]
- [[65 Source Registry and Claim Lineage/FED_MONETARY — Federal Reserve — Monetary Policy]]
- [[65 Source Registry and Claim Lineage/BOE_YIELD_CURVES — Bank of England Yield Curves]]
- [[65 Source Registry and Claim Lineage/UST_REFUNDING — U.S. Treasury Quarterly Refunding]]
- [[65 Source Registry and Claim Lineage/CME_RATES — CME Interest Rate Products]]
- [[65 Source Registry and Claim Lineage/TREASURY_DIRECT — TreasuryDirect Marketable Securities]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Implementation Governance]]
