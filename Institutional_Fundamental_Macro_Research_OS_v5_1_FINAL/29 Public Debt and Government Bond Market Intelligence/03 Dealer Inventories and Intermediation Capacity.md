---
title: "Dealer Inventories and Intermediation Capacity"
type: field-guide
status: supporting-legacy
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
retrieval_priority: 10
default_retrieval: false
canonical_registry: "[[82 Canonical Institutional Fundamental Research Library/00 Canonical Institutional Fundamental Research Library MOC]]"
tags:
  - 29-public-debt-and-government-bond-market-intelligence
  - dealer-inventories-and-intermediation-capacity
  - institutional-fundamental
---
# Dealer Inventories and Intermediation Capacity

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Dealer Inventories and Intermediation Capacity**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

Dealer-hedging analysis treats Greek exposure as a model-dependent inventory scenario, not a directly observed fact.

For **Dealer Inventories and Intermediation Capacity**, the relevant institutional domain is **rates**: the path of policy rates, sovereign cash flows, duration supply, inflation compensation, collateral, funding, and term risk. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Dealer Inventories and Intermediation Capacity** represent, in what unit, population, instrument, and convention?
2. Which **Dealer Inventories and Intermediation Capacity** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Dealer Inventories and Intermediation Capacity** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Dealer Inventories and Intermediation Capacity** mechanism is active?
5. What rival model can create the same target move while **Dealer Inventories and Intermediation Capacity** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Dealer Inventories and Intermediation Capacity** decision?

## Identities and model skeleton

$$
\Delta=\frac{\partial V}{\partial S},\quad \Gamma=\frac{\partial^2V}{\partial S^2}
$$

$$
Vanna=\frac{\partial^2V}{\partial S\,\partial \sigma},\quad Charm=\frac{\partial \Delta}{\partial t}
$$

$$
HedgeFlow\approx-\Gamma\,dS-\mathrm{Vanna}\,d\sigma-\mathrm{Charm}\,dt
$$

For **Dealer Inventories and Intermediation Capacity**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Dealer Inventories and Intermediation Capacity:** option open interest by strike/expiry.
- **Measurement 2 for Dealer Inventories and Intermediation Capacity:** customer/dealer side assumptions.
- **Measurement 3 for Dealer Inventories and Intermediation Capacity:** spot, vol surface, and time to expiry.
- **Measurement 4 for Dealer Inventories and Intermediation Capacity:** 0DTE versus longer-dated concentration.
- **Measurement 5 for Dealer Inventories and Intermediation Capacity:** realized response around strikes.

The **Dealer Inventories and Intermediation Capacity** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Dealer Inventories and Intermediation Capacity:** contract-level Greek aggregation.
- **Model layer 2 for Dealer Inventories and Intermediation Capacity:** side-allocation scenarios.
- **Model layer 3 for Dealer Inventories and Intermediation Capacity:** surface-shock Greeks.
- **Model layer 4 for Dealer Inventories and Intermediation Capacity:** expiry-time flow map.
- **Model layer 5 for Dealer Inventories and Intermediation Capacity:** empirical validation against intraday response.

Validate the **Dealer Inventories and Intermediation Capacity** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Structural | In the **Dealer Inventories and Intermediation Capacity** research object, neutral rate, debt structure, inflation regime, and investor base anchor the curve. |
| Cyclical | In the **Dealer Inventories and Intermediation Capacity** research object, policy path, inflation compensation, credit, and term premium evolve. |
| Tactical/Swing | In the **Dealer Inventories and Intermediation Capacity** research object, issuance, auctions, positioning, carry, and relative value dominate. |
| Daily/Event | In the **Dealer Inventories and Intermediation Capacity** research object, meeting pricing, WI levels, funding, and liquid futures lead the response. |

Conflicts involving **Dealer Inventories and Intermediation Capacity** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Dealer Inventories and Intermediation Capacity channel 1:** test `data and policy → expected short rates`.
2. **Dealer Inventories and Intermediation Capacity channel 2:** test `fiscal supply and risk appetite → term premium`.
3. **Dealer Inventories and Intermediation Capacity channel 3:** test `collateral and balance sheet → repo/basis`.
4. **Dealer Inventories and Intermediation Capacity channel 4:** test `rates → FX, equity duration, credit, housing, and gold`.

**Dealer Inventories and Intermediation Capacity asset translation:** Rates: separate expected short-rate changes, term premium, inflation compensation, carry/roll, and funding. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Dealer Inventories and Intermediation Capacity** posterior or activate a rival explanation.

## Fundamental decision application

- Intraday governance: [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]

## Multi-day decision application

- Multi-day governance: [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]

## Falsification and known failure modes

- **Failure test 1 for Dealer Inventories and Intermediation Capacity:** assuming all open interest is dealer-short.
- **Failure test 2 for Dealer Inventories and Intermediation Capacity:** using static Greeks.
- **Failure test 3 for Dealer Inventories and Intermediation Capacity:** ignoring vol-surface movement.
- **Failure test 4 for Dealer Inventories and Intermediation Capacity:** treating gamma level as price-support certainty.
- **Failure test 5 for Dealer Inventories and Intermediation Capacity:** failing to validate sign assumptions.

Score **Dealer Inventories and Intermediation Capacity** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required research record

- Schema: [[00 Core Standards/17 Context Object and Permission Schema Standard]]

## Primary source routes for Dealer Inventories and Intermediation Capacity

- [[65 Source Registry and Claim Lineage/CBOE_VIX — Cboe VIX Methodology]]
- [[65 Source Registry and Claim Lineage/SEC_MARKETS — SEC Division of Trading and Markets]]
- [[65 Source Registry and Claim Lineage/CME_RATES — CME Interest Rate Products]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Implementation Governance]]
