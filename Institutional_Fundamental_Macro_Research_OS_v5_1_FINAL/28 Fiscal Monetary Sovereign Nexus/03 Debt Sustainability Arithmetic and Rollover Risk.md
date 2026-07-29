---
title: "Debt Sustainability Arithmetic and Rollover Risk"
type: field-guide
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - 28-fiscal-monetary-sovereign-nexus
  - debt-sustainability-arithmetic-and-rollover-risk
  - institutional-fundamental
---
# Debt Sustainability Arithmetic and Rollover Risk

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Debt Sustainability Arithmetic and Rollover Risk**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

Fiscal analysis links primary balances, interest expense, maturity structure, Treasury cash management, issuance composition, and private-sector absorption.

For **Debt Sustainability Arithmetic and Rollover Risk**, the relevant institutional domain is **rates**: the path of policy rates, sovereign cash flows, duration supply, inflation compensation, collateral, funding, and term risk. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Debt Sustainability Arithmetic and Rollover Risk** represent, in what unit, population, instrument, and convention?
2. Which **Debt Sustainability Arithmetic and Rollover Risk** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Debt Sustainability Arithmetic and Rollover Risk** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Debt Sustainability Arithmetic and Rollover Risk** mechanism is active?
5. What rival model can create the same target move while **Debt Sustainability Arithmetic and Rollover Risk** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Debt Sustainability Arithmetic and Rollover Risk** decision?

## Identities and model skeleton

$$
\Delta d_t\approx\frac{r_t-g_t}{1+g_t}d_{t-1}-pb_t+SFA_t
$$

$$
NetMarketableBorrowing=Deficit+Redemptions-\Delta CashBalance-\mathrm{other\ financing}
$$

$$
DurationSupply=\sum_i MarketValue_i\times Duration_i
$$

For **Debt Sustainability Arithmetic and Rollover Risk**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Debt Sustainability Arithmetic and Rollover Risk:** receipts, outlays, primary balance, and interest.
- **Measurement 2 for Debt Sustainability Arithmetic and Rollover Risk:** debt maturity and floating-rate share.
- **Measurement 3 for Debt Sustainability Arithmetic and Rollover Risk:** TGA and daily cash flows.
- **Measurement 4 for Debt Sustainability Arithmetic and Rollover Risk:** bill/coupon/TIPS/FRN issuance.
- **Measurement 5 for Debt Sustainability Arithmetic and Rollover Risk:** dealer, household, fund, bank, and foreign absorption.

The **Debt Sustainability Arithmetic and Rollover Risk** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Debt Sustainability Arithmetic and Rollover Risk:** debt-dynamics scenarios.
- **Model layer 2 for Debt Sustainability Arithmetic and Rollover Risk:** financing-needs calendar.
- **Model layer 3 for Debt Sustainability Arithmetic and Rollover Risk:** duration-supply model.
- **Model layer 4 for Debt Sustainability Arithmetic and Rollover Risk:** fiscal impulse decomposition.
- **Model layer 5 for Debt Sustainability Arithmetic and Rollover Risk:** sovereign risk and term-premium stress.

Validate the **Debt Sustainability Arithmetic and Rollover Risk** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Structural | In the **Debt Sustainability Arithmetic and Rollover Risk** research object, neutral rate, debt structure, inflation regime, and investor base anchor the curve. |
| Cyclical | In the **Debt Sustainability Arithmetic and Rollover Risk** research object, policy path, inflation compensation, credit, and term premium evolve. |
| Tactical/Swing | In the **Debt Sustainability Arithmetic and Rollover Risk** research object, issuance, auctions, positioning, carry, and relative value dominate. |
| Daily/Event | In the **Debt Sustainability Arithmetic and Rollover Risk** research object, meeting pricing, WI levels, funding, and liquid futures lead the response. |

Conflicts involving **Debt Sustainability Arithmetic and Rollover Risk** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Debt Sustainability Arithmetic and Rollover Risk channel 1:** test `data and policy → expected short rates`.
2. **Debt Sustainability Arithmetic and Rollover Risk channel 2:** test `fiscal supply and risk appetite → term premium`.
3. **Debt Sustainability Arithmetic and Rollover Risk channel 3:** test `collateral and balance sheet → repo/basis`.
4. **Debt Sustainability Arithmetic and Rollover Risk channel 4:** test `rates → FX, equity duration, credit, housing, and gold`.

**Debt Sustainability Arithmetic and Rollover Risk asset translation:** Rates: separate expected short-rate changes, term premium, inflation compensation, carry/roll, and funding. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Debt Sustainability Arithmetic and Rollover Risk** posterior or activate a rival explanation.

## Fundamental decision application

- Intraday governance: [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]

## Multi-day decision application

- Multi-day governance: [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]

## Falsification and known failure modes

- **Failure test 1 for Debt Sustainability Arithmetic and Rollover Risk:** equating deficit with current impulse.
- **Failure test 2 for Debt Sustainability Arithmetic and Rollover Risk:** ignoring cash balance and redemptions.
- **Failure test 3 for Debt Sustainability Arithmetic and Rollover Risk:** using face value instead of duration supply.
- **Failure test 4 for Debt Sustainability Arithmetic and Rollover Risk:** assuming issuance mechanically raises yields.
- **Failure test 5 for Debt Sustainability Arithmetic and Rollover Risk:** ignoring currency and investor-base structure.

Score **Debt Sustainability Arithmetic and Rollover Risk** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required research record

- Schema: [[00 Core Standards/17 Context Object and Permission Schema Standard]]

## Primary source routes for Debt Sustainability Arithmetic and Rollover Risk

- [[65 Source Registry and Claim Lineage/UST_FISCAL — U.S. Treasury Fiscal Data]]
- [[65 Source Registry and Claim Lineage/UST_DTS — U.S. Treasury Daily Treasury Statement]]
- [[65 Source Registry and Claim Lineage/UST_REFUNDING — U.S. Treasury Quarterly Refunding]]
- [[65 Source Registry and Claim Lineage/UST_AUCTIONS — U.S. Treasury Auction Data]]
- [[65 Source Registry and Claim Lineage/CBO — Congressional Budget Office]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Implementation Governance]]
