---
title: "Fed Funds Futures and Meeting Probabilities"
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
  - 16-rates-fixed-income-and-policy-pricing
  - fed-funds-futures-and-meeting-probabilities
  - institutional-fundamental
---
# Fed Funds Futures and Meeting Probabilities

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Fed Funds Futures and Meeting Probabilities**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

Policy pricing must be reconstructed from instruments whose accrual periods often span more than one central-bank regime or meeting outcome.

For **Fed Funds Futures and Meeting Probabilities**, the relevant institutional domain is **rates**: the path of policy rates, sovereign cash flows, duration supply, inflation compensation, collateral, funding, and term risk. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Fed Funds Futures and Meeting Probabilities** represent, in what unit, population, instrument, and convention?
2. Which **Fed Funds Futures and Meeting Probabilities** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Fed Funds Futures and Meeting Probabilities** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Fed Funds Futures and Meeting Probabilities** mechanism is active?
5. What rival model can create the same target move while **Fed Funds Futures and Meeting Probabilities** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Fed Funds Futures and Meeting Probabilities** decision?

## Identities and model skeleton

$$
F_t\approx 100-E_t[\bar r_{eff}]
$$

$$
E[\bar r_{month}]=\frac{d_0 r_0+d_1E[r_1]+\cdots}{D}
$$

$$
P(\mathrm{outcome}_j)=\frac{w_j}{\sum_k w_k}
$$

For **Fed Funds Futures and Meeting Probabilities**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Fed Funds Futures and Meeting Probabilities:** effective overnight rate.
- **Measurement 2 for Fed Funds Futures and Meeting Probabilities:** meeting calendar and day counts.
- **Measurement 3 for Fed Funds Futures and Meeting Probabilities:** monthly futures and OIS.
- **Measurement 4 for Fed Funds Futures and Meeting Probabilities:** basis and turn effects.
- **Measurement 5 for Fed Funds Futures and Meeting Probabilities:** survey and options distributions.

The **Fed Funds Futures and Meeting Probabilities** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Fed Funds Futures and Meeting Probabilities:** meeting-date curve stripping.
- **Model layer 2 for Fed Funds Futures and Meeting Probabilities:** discrete outcome probability tree.
- **Model layer 3 for Fed Funds Futures and Meeting Probabilities:** OIS bootstrapping.
- **Model layer 4 for Fed Funds Futures and Meeting Probabilities:** basis-adjusted futures mapping.
- **Model layer 5 for Fed Funds Futures and Meeting Probabilities:** scenario repricing decomposition.

Validate the **Fed Funds Futures and Meeting Probabilities** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Structural | In the **Fed Funds Futures and Meeting Probabilities** research object, neutral rate, debt structure, inflation regime, and investor base anchor the curve. |
| Cyclical | In the **Fed Funds Futures and Meeting Probabilities** research object, policy path, inflation compensation, credit, and term premium evolve. |
| Tactical/Swing | In the **Fed Funds Futures and Meeting Probabilities** research object, issuance, auctions, positioning, carry, and relative value dominate. |
| Daily/Event | In the **Fed Funds Futures and Meeting Probabilities** research object, meeting pricing, WI levels, funding, and liquid futures lead the response. |

Conflicts involving **Fed Funds Futures and Meeting Probabilities** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Fed Funds Futures and Meeting Probabilities channel 1:** test `data and policy → expected short rates`.
2. **Fed Funds Futures and Meeting Probabilities channel 2:** test `fiscal supply and risk appetite → term premium`.
3. **Fed Funds Futures and Meeting Probabilities channel 3:** test `collateral and balance sheet → repo/basis`.
4. **Fed Funds Futures and Meeting Probabilities channel 4:** test `rates → FX, equity duration, credit, housing, and gold`.

**Fed Funds Futures and Meeting Probabilities asset translation:** Rates: separate expected short-rate changes, term premium, inflation compensation, carry/roll, and funding. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Fed Funds Futures and Meeting Probabilities** posterior or activate a rival explanation.

## Fundamental decision application

- Intraday governance: [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]

## Multi-day decision application

- Multi-day governance: [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]

## Falsification and known failure modes

- **Failure test 1 for Fed Funds Futures and Meeting Probabilities:** reading a monthly contract as a meeting-date rate.
- **Failure test 2 for Fed Funds Futures and Meeting Probabilities:** ignoring day weights.
- **Failure test 3 for Fed Funds Futures and Meeting Probabilities:** forcing probabilities from an underidentified curve.
- **Failure test 4 for Fed Funds Futures and Meeting Probabilities:** mixing target and effective rates.
- **Failure test 5 for Fed Funds Futures and Meeting Probabilities:** ignoring basis around turns.

Score **Fed Funds Futures and Meeting Probabilities** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required research record

- Schema: [[00 Core Standards/17 Context Object and Permission Schema Standard]]

## Primary source routes for Fed Funds Futures and Meeting Probabilities

- [[65 Source Registry and Claim Lineage/CME_FEDWATCH — CME FedWatch]]
- [[65 Source Registry and Claim Lineage/FED_FOMC — Federal Reserve — FOMC]]
- [[65 Source Registry and Claim Lineage/NYFED_SOFR — New York Fed — SOFR]]
- [[65 Source Registry and Claim Lineage/CME_RATES — CME Interest Rate Products]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Implementation Governance]]
