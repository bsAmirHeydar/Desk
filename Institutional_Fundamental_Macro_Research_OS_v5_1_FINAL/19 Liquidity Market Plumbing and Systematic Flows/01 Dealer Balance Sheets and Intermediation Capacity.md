---
title: "Dealer Balance Sheets and Intermediation Capacity"
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
  - 19-liquidity-market-plumbing-and-systematic-flows
  - dealer-balance-sheets-and-intermediation-capacity
  - institutional-fundamental
---
# Dealer Balance Sheets and Intermediation Capacity

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Dealer Balance Sheets and Intermediation Capacity**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

Dealer-hedging analysis treats Greek exposure as a model-dependent inventory scenario, not a directly observed fact. Balance-sheet analysis maps operating assets and liabilities, financing, liquidity, duration, contingent claims, and working-capital behavior.

For **Dealer Balance Sheets and Intermediation Capacity**, the relevant institutional domain is **microstructure**: how information and forced demand meet liquidity, dealer balance sheets, order books, derivatives hedging, and execution constraints. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Dealer Balance Sheets and Intermediation Capacity** represent, in what unit, population, instrument, and convention?
2. Which **Dealer Balance Sheets and Intermediation Capacity** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Dealer Balance Sheets and Intermediation Capacity** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Dealer Balance Sheets and Intermediation Capacity** mechanism is active?
5. What rival model can create the same target move while **Dealer Balance Sheets and Intermediation Capacity** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Dealer Balance Sheets and Intermediation Capacity** decision?

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

$$
NetWorkingCapital=OperatingCurrentAssets-OperatingCurrentLiabilities
$$

$$
CashConversionCycle=DSO+DIO-DPO
$$

$$
NetDebt=Debt-Cash
$$

For **Dealer Balance Sheets and Intermediation Capacity**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Dealer Balance Sheets and Intermediation Capacity:** option open interest by strike/expiry.
- **Measurement 2 for Dealer Balance Sheets and Intermediation Capacity:** customer/dealer side assumptions.
- **Measurement 3 for Dealer Balance Sheets and Intermediation Capacity:** spot, vol surface, and time to expiry.
- **Measurement 4 for Dealer Balance Sheets and Intermediation Capacity:** 0DTE versus longer-dated concentration.
- **Measurement 5 for Dealer Balance Sheets and Intermediation Capacity:** realized response around strikes.
- **Measurement 6 for Dealer Balance Sheets and Intermediation Capacity:** receivables, inventory, and payables.
- **Measurement 7 for Dealer Balance Sheets and Intermediation Capacity:** cash restrictions and short-term investments.
- **Measurement 8 for Dealer Balance Sheets and Intermediation Capacity:** debt maturity, rate, covenants, and collateral.
- **Measurement 9 for Dealer Balance Sheets and Intermediation Capacity:** leases, pensions, guarantees, and contingencies.
- **Measurement 10 for Dealer Balance Sheets and Intermediation Capacity:** acquisition goodwill, intangibles, and deferred taxes.

The **Dealer Balance Sheets and Intermediation Capacity** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Dealer Balance Sheets and Intermediation Capacity:** contract-level Greek aggregation.
- **Model layer 2 for Dealer Balance Sheets and Intermediation Capacity:** side-allocation scenarios.
- **Model layer 3 for Dealer Balance Sheets and Intermediation Capacity:** surface-shock Greeks.
- **Model layer 4 for Dealer Balance Sheets and Intermediation Capacity:** expiry-time flow map.
- **Model layer 5 for Dealer Balance Sheets and Intermediation Capacity:** empirical validation against intraday response.
- **Model layer 6 for Dealer Balance Sheets and Intermediation Capacity:** working-capital bridge.
- **Model layer 7 for Dealer Balance Sheets and Intermediation Capacity:** liquidity runway.
- **Model layer 8 for Dealer Balance Sheets and Intermediation Capacity:** maturity ladder.
- **Model layer 9 for Dealer Balance Sheets and Intermediation Capacity:** asset-quality and impairment analysis.
- **Model layer 10 for Dealer Balance Sheets and Intermediation Capacity:** scenario balance sheet.

Validate the **Dealer Balance Sheets and Intermediation Capacity** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Structural | In the **Dealer Balance Sheets and Intermediation Capacity** research object, venue rules, clearing, dealer capacity, and participant ecology set market behavior. |
| Cyclical | In the **Dealer Balance Sheets and Intermediation Capacity** research object, volatility and balance-sheet capacity alter depth and impact. |
| Tactical/Swing | In the **Dealer Balance Sheets and Intermediation Capacity** research object, positioning, expiry, systematic triggers, and flow persistence matter. |
| Intraday | In the **Dealer Balance Sheets and Intermediation Capacity** research object, spread, depth, queue, auction, and hedge feedback determine path and cost. |

Conflicts involving **Dealer Balance Sheets and Intermediation Capacity** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Dealer Balance Sheets and Intermediation Capacity channel 1:** test `information → order imbalance`.
2. **Dealer Balance Sheets and Intermediation Capacity channel 2:** test `options exposure → hedge flow`.
3. **Dealer Balance Sheets and Intermediation Capacity channel 3:** test `volatility/price → systematic rebalance`.
4. **Dealer Balance Sheets and Intermediation Capacity channel 4:** test `liquidity withdrawal → nonlinear impact and gaps`.

**Dealer Balance Sheets and Intermediation Capacity asset translation:** Execution: validate estimated flow against spread, depth, volume, and realized response. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Dealer Balance Sheets and Intermediation Capacity** posterior or activate a rival explanation.

## Fundamental decision application

- Intraday governance: [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]

## Multi-day decision application

- Multi-day governance: [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]

## Falsification and known failure modes

- **Failure test 1 for Dealer Balance Sheets and Intermediation Capacity:** assuming all open interest is dealer-short.
- **Failure test 2 for Dealer Balance Sheets and Intermediation Capacity:** using static Greeks.
- **Failure test 3 for Dealer Balance Sheets and Intermediation Capacity:** ignoring vol-surface movement.
- **Failure test 4 for Dealer Balance Sheets and Intermediation Capacity:** treating gamma level as price-support certainty.
- **Failure test 5 for Dealer Balance Sheets and Intermediation Capacity:** failing to validate sign assumptions.
- **Failure test 6 for Dealer Balance Sheets and Intermediation Capacity:** receivables growth ahead of sales.
- **Failure test 7 for Dealer Balance Sheets and Intermediation Capacity:** inventory obsolescence.
- **Failure test 8 for Dealer Balance Sheets and Intermediation Capacity:** supplier financing hidden in payables.
- **Failure test 9 for Dealer Balance Sheets and Intermediation Capacity:** restricted cash treated as available.
- **Failure test 10 for Dealer Balance Sheets and Intermediation Capacity:** off-balance-sheet claims omitted.

Score **Dealer Balance Sheets and Intermediation Capacity** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required research record

- Schema: [[00 Core Standards/17 Context Object and Permission Schema Standard]]

## Primary source routes for Dealer Balance Sheets and Intermediation Capacity

- [[65 Source Registry and Claim Lineage/CBOE_VIX — Cboe VIX Methodology]]
- [[65 Source Registry and Claim Lineage/SEC_MARKETS — SEC Division of Trading and Markets]]
- [[65 Source Registry and Claim Lineage/CME_RATES — CME Interest Rate Products]]
- [[65 Source Registry and Claim Lineage/SEC_EDGAR — SEC EDGAR]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Implementation Governance]]
