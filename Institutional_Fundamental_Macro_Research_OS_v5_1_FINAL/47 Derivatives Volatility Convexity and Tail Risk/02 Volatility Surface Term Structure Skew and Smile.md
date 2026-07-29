---
title: "Volatility Surface Term Structure Skew and Smile"
type: field-guide
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - 47-derivatives-volatility-convexity-and-tail-risk
  - volatility-surface-term-structure-skew-and-smile
  - institutional-fundamental
---
# Volatility Surface Term Structure Skew and Smile

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Volatility Surface Term Structure Skew and Smile**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

Volatility analysis distinguishes realized variation, option-implied risk-neutral expectations, variance risk premium, skew, term structure, supply/demand, and jump risk.

For **Volatility Surface Term Structure Skew and Smile**, the relevant institutional domain is **microstructure**: how information and forced demand meet liquidity, dealer balance sheets, order books, derivatives hedging, and execution constraints. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Volatility Surface Term Structure Skew and Smile** represent, in what unit, population, instrument, and convention?
2. Which **Volatility Surface Term Structure Skew and Smile** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Volatility Surface Term Structure Skew and Smile** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Volatility Surface Term Structure Skew and Smile** mechanism is active?
5. What rival model can create the same target move while **Volatility Surface Term Structure Skew and Smile** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Volatility Surface Term Structure Skew and Smile** decision?

## Identities and model skeleton

$$
RV=\sqrt{\sum_{i=1}^{N}r_i^2}\sqrt{Annualization}
$$

$$
VRP=IV^2-E^P[RV^2]
$$

$$
VarianceSwapRate\approx \frac{2}{T}\int_0^\infty \frac{Q(K)}{K^2}\,dK
$$

For **Volatility Surface Term Structure Skew and Smile**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Volatility Surface Term Structure Skew and Smile:** realized volatility by horizon.
- **Measurement 2 for Volatility Surface Term Structure Skew and Smile:** ATM implied volatility and term structure.
- **Measurement 3 for Volatility Surface Term Structure Skew and Smile:** put/call skew and smile dynamics.
- **Measurement 4 for Volatility Surface Term Structure Skew and Smile:** vol-of-vol, correlation, and dispersion.
- **Measurement 5 for Volatility Surface Term Structure Skew and Smile:** open interest, flow, and event calendar.

The **Volatility Surface Term Structure Skew and Smile** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Volatility Surface Term Structure Skew and Smile:** arbitrage-clean surface.
- **Model layer 2 for Volatility Surface Term Structure Skew and Smile:** HAR/GARCH benchmarks.
- **Model layer 3 for Volatility Surface Term Structure Skew and Smile:** variance-risk-premium decomposition.
- **Model layer 4 for Volatility Surface Term Structure Skew and Smile:** jump and event variance.
- **Model layer 5 for Volatility Surface Term Structure Skew and Smile:** risk-neutral density extraction.

Validate the **Volatility Surface Term Structure Skew and Smile** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Structural | In the **Volatility Surface Term Structure Skew and Smile** research object, venue rules, clearing, dealer capacity, and participant ecology set market behavior. |
| Cyclical | In the **Volatility Surface Term Structure Skew and Smile** research object, volatility and balance-sheet capacity alter depth and impact. |
| Tactical/Swing | In the **Volatility Surface Term Structure Skew and Smile** research object, positioning, expiry, systematic triggers, and flow persistence matter. |
| Intraday | In the **Volatility Surface Term Structure Skew and Smile** research object, spread, depth, queue, auction, and hedge feedback determine path and cost. |

Conflicts involving **Volatility Surface Term Structure Skew and Smile** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Volatility Surface Term Structure Skew and Smile channel 1:** test `information → order imbalance`.
2. **Volatility Surface Term Structure Skew and Smile channel 2:** test `options exposure → hedge flow`.
3. **Volatility Surface Term Structure Skew and Smile channel 3:** test `volatility/price → systematic rebalance`.
4. **Volatility Surface Term Structure Skew and Smile channel 4:** test `liquidity withdrawal → nonlinear impact and gaps`.

**Volatility Surface Term Structure Skew and Smile asset translation:** Execution: validate estimated flow against spread, depth, volume, and realized response. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Volatility Surface Term Structure Skew and Smile** posterior or activate a rival explanation.

## Fundamental decision application

- Intraday governance: [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]

## Multi-day decision application

- Multi-day governance: [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]

## Falsification and known failure modes

- **Failure test 1 for Volatility Surface Term Structure Skew and Smile:** comparing mismatched IV/RV horizons.
- **Failure test 2 for Volatility Surface Term Structure Skew and Smile:** using VIX as fear sentiment only.
- **Failure test 3 for Volatility Surface Term Structure Skew and Smile:** ignoring strike liquidity.
- **Failure test 4 for Volatility Surface Term Structure Skew and Smile:** calling skew a directional forecast.
- **Failure test 5 for Volatility Surface Term Structure Skew and Smile:** omitting carry and convexity.

Score **Volatility Surface Term Structure Skew and Smile** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required research record

- Schema: [[00 Core Standards/17 Context Object and Permission Schema Standard]]

## Primary source routes for Volatility Surface Term Structure Skew and Smile

- [[65 Source Registry and Claim Lineage/CBOE_VIX — Cboe VIX Methodology]]
- [[65 Source Registry and Claim Lineage/CME_RATES — CME Interest Rate Products]]
- [[65 Source Registry and Claim Lineage/SEC_MARKETS — SEC Division of Trading and Markets]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Implementation Governance]]
