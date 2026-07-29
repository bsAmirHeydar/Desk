---
title: "OIS Curves and Policy-Path Extraction"
type: field-guide
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - 16-rates-fixed-income-and-policy-pricing
  - ois-curves-and-policy-path-extraction
  - institutional-fundamental
---
# OIS Curves and Policy-Path Extraction

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **OIS Curves and Policy-Path Extraction**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

Policy pricing must be reconstructed from instruments whose accrual periods often span more than one central-bank regime or meeting outcome. A reaction function maps the policymaker information set, mandate, risk asymmetry, financial conditions, and institutional constraints into a policy distribution.

For **OIS Curves and Policy-Path Extraction**, the relevant institutional domain is **rates**: the path of policy rates, sovereign cash flows, duration supply, inflation compensation, collateral, funding, and term risk. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **OIS Curves and Policy-Path Extraction** represent, in what unit, population, instrument, and convention?
2. Which **OIS Curves and Policy-Path Extraction** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **OIS Curves and Policy-Path Extraction** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **OIS Curves and Policy-Path Extraction** mechanism is active?
5. What rival model can create the same target move while **OIS Curves and Policy-Path Extraction** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **OIS Curves and Policy-Path Extraction** decision?

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

$$
i_t=r_t^*+\pi_t+\phi_\pi(\pi_t-\pi^*)+\phi_y \tilde y_t+\varepsilon_t
$$

$$
P(i_{t+1}|I_t)=\sum_s P(i_{t+1}|s,I_t)P(s|I_t)
$$

For **OIS Curves and Policy-Path Extraction**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for OIS Curves and Policy-Path Extraction:** effective overnight rate.
- **Measurement 2 for OIS Curves and Policy-Path Extraction:** meeting calendar and day counts.
- **Measurement 3 for OIS Curves and Policy-Path Extraction:** monthly futures and OIS.
- **Measurement 4 for OIS Curves and Policy-Path Extraction:** basis and turn effects.
- **Measurement 5 for OIS Curves and Policy-Path Extraction:** survey and options distributions.
- **Measurement 6 for OIS Curves and Policy-Path Extraction:** official forecast and risk language.
- **Measurement 7 for OIS Curves and Policy-Path Extraction:** meeting-dated pricing.
- **Measurement 8 for OIS Curves and Policy-Path Extraction:** inflation/growth/labor forecast errors.
- **Measurement 9 for OIS Curves and Policy-Path Extraction:** financial conditions and stability constraints.
- **Measurement 10 for OIS Curves and Policy-Path Extraction:** votes, speeches, balance-sheet operations, and implementation.

The **OIS Curves and Policy-Path Extraction** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for OIS Curves and Policy-Path Extraction:** meeting-date curve stripping.
- **Model layer 2 for OIS Curves and Policy-Path Extraction:** discrete outcome probability tree.
- **Model layer 3 for OIS Curves and Policy-Path Extraction:** OIS bootstrapping.
- **Model layer 4 for OIS Curves and Policy-Path Extraction:** basis-adjusted futures mapping.
- **Model layer 5 for OIS Curves and Policy-Path Extraction:** scenario repricing decomposition.
- **Model layer 6 for OIS Curves and Policy-Path Extraction:** Taylor-rule benchmarks.
- **Model layer 7 for OIS Curves and Policy-Path Extraction:** ordered-choice policy model.
- **Model layer 8 for OIS Curves and Policy-Path Extraction:** text and language change analysis.
- **Model layer 9 for OIS Curves and Policy-Path Extraction:** scenario probability tree.
- **Model layer 10 for OIS Curves and Policy-Path Extraction:** cross-central-bank relative reaction mapping.

Validate the **OIS Curves and Policy-Path Extraction** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Structural | In the **OIS Curves and Policy-Path Extraction** research object, neutral rate, debt structure, inflation regime, and investor base anchor the curve. |
| Cyclical | In the **OIS Curves and Policy-Path Extraction** research object, policy path, inflation compensation, credit, and term premium evolve. |
| Tactical/Swing | In the **OIS Curves and Policy-Path Extraction** research object, issuance, auctions, positioning, carry, and relative value dominate. |
| Daily/Event | In the **OIS Curves and Policy-Path Extraction** research object, meeting pricing, WI levels, funding, and liquid futures lead the response. |

Conflicts involving **OIS Curves and Policy-Path Extraction** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **OIS Curves and Policy-Path Extraction channel 1:** test `data and policy → expected short rates`.
2. **OIS Curves and Policy-Path Extraction channel 2:** test `fiscal supply and risk appetite → term premium`.
3. **OIS Curves and Policy-Path Extraction channel 3:** test `collateral and balance sheet → repo/basis`.
4. **OIS Curves and Policy-Path Extraction channel 4:** test `rates → FX, equity duration, credit, housing, and gold`.

**OIS Curves and Policy-Path Extraction asset translation:** Rates: separate expected short-rate changes, term premium, inflation compensation, carry/roll, and funding. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **OIS Curves and Policy-Path Extraction** posterior or activate a rival explanation.

## Fundamental decision application

- Intraday governance: [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]

## Multi-day decision application

- Multi-day governance: [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]

## Falsification and known failure modes

- **Failure test 1 for OIS Curves and Policy-Path Extraction:** reading a monthly contract as a meeting-date rate.
- **Failure test 2 for OIS Curves and Policy-Path Extraction:** ignoring day weights.
- **Failure test 3 for OIS Curves and Policy-Path Extraction:** forcing probabilities from an underidentified curve.
- **Failure test 4 for OIS Curves and Policy-Path Extraction:** mixing target and effective rates.
- **Failure test 5 for OIS Curves and Policy-Path Extraction:** ignoring basis around turns.
- **Failure test 6 for OIS Curves and Policy-Path Extraction:** treating guidance as commitment.
- **Failure test 7 for OIS Curves and Policy-Path Extraction:** ignoring implementation mechanics.
- **Failure test 8 for OIS Curves and Policy-Path Extraction:** using one Taylor rule as truth.
- **Failure test 9 for OIS Curves and Policy-Path Extraction:** missing risk-management asymmetry.
- **Failure test 10 for OIS Curves and Policy-Path Extraction:** confusing information effect with policy shock.

Score **OIS Curves and Policy-Path Extraction** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required research record

- Schema: [[00 Core Standards/17 Context Object and Permission Schema Standard]]

## Primary source routes for OIS Curves and Policy-Path Extraction

- [[65 Source Registry and Claim Lineage/CME_FEDWATCH — CME FedWatch]]
- [[65 Source Registry and Claim Lineage/FED_FOMC — Federal Reserve — FOMC]]
- [[65 Source Registry and Claim Lineage/NYFED_SOFR — New York Fed — SOFR]]
- [[65 Source Registry and Claim Lineage/CME_RATES — CME Interest Rate Products]]
- [[65 Source Registry and Claim Lineage/ECB — European Central Bank]]
- [[65 Source Registry and Claim Lineage/BOE — Bank of England]]
- [[65 Source Registry and Claim Lineage/BOJ — Bank of Japan]]
- [[65 Source Registry and Claim Lineage/BOC — Bank of Canada]]
- [[65 Source Registry and Claim Lineage/RBA — Reserve Bank of Australia]]
- [[65 Source Registry and Claim Lineage/SNB — Swiss National Bank]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Implementation Governance]]
