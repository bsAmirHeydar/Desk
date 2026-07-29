---
title: "Repo SOFR and Secured Funding"
type: field-guide
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - 16-rates-fixed-income-and-policy-pricing
  - repo-sofr-and-secured-funding
  - institutional-fundamental
---
# Repo SOFR and Secured Funding

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Repo SOFR and Secured Funding**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

Secured funding prices cash, collateral scarcity, counterparty balance sheet, settlement demand, and regulatory capacity.

For **Repo SOFR and Secured Funding**, the relevant institutional domain is **rates**: the path of policy rates, sovereign cash flows, duration supply, inflation compensation, collateral, funding, and term risk. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Repo SOFR and Secured Funding** represent, in what unit, population, instrument, and convention?
2. Which **Repo SOFR and Secured Funding** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Repo SOFR and Secured Funding** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Repo SOFR and Secured Funding** mechanism is active?
5. What rival model can create the same target move while **Repo SOFR and Secured Funding** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Repo SOFR and Secured Funding** decision?

## Identities and model skeleton

$$
RepoInterest=CashPrincipal\times RepoRate\times \frac{Days}{360}
$$

$$
Haircut=1-\frac{CashLent}{CollateralMarketValue}
$$

$$
BasisPnL=CashReturn-FuturesHedge-Funding-CapitalCost
$$

For **Repo SOFR and Secured Funding**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Repo SOFR and Secured Funding:** SOFR distribution and volumes.
- **Measurement 2 for Repo SOFR and Secured Funding:** general collateral and specials.
- **Measurement 3 for Repo SOFR and Secured Funding:** haircuts and fails.
- **Measurement 4 for Repo SOFR and Secured Funding:** dealer inventories and Treasury settlement.
- **Measurement 5 for Repo SOFR and Secured Funding:** sponsored repo and balance-sheet dates.

The **Repo SOFR and Secured Funding** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Repo SOFR and Secured Funding:** funding-spread decomposition.
- **Model layer 2 for Repo SOFR and Secured Funding:** collateral-specialness map.
- **Model layer 3 for Repo SOFR and Secured Funding:** settlement-flow forecast.
- **Model layer 4 for Repo SOFR and Secured Funding:** basis stress test.
- **Model layer 5 for Repo SOFR and Secured Funding:** liquidity ladder.

Validate the **Repo SOFR and Secured Funding** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Structural | In the **Repo SOFR and Secured Funding** research object, neutral rate, debt structure, inflation regime, and investor base anchor the curve. |
| Cyclical | In the **Repo SOFR and Secured Funding** research object, policy path, inflation compensation, credit, and term premium evolve. |
| Tactical/Swing | In the **Repo SOFR and Secured Funding** research object, issuance, auctions, positioning, carry, and relative value dominate. |
| Daily/Event | In the **Repo SOFR and Secured Funding** research object, meeting pricing, WI levels, funding, and liquid futures lead the response. |

Conflicts involving **Repo SOFR and Secured Funding** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Repo SOFR and Secured Funding channel 1:** test `data and policy → expected short rates`.
2. **Repo SOFR and Secured Funding channel 2:** test `fiscal supply and risk appetite → term premium`.
3. **Repo SOFR and Secured Funding channel 3:** test `collateral and balance sheet → repo/basis`.
4. **Repo SOFR and Secured Funding channel 4:** test `rates → FX, equity duration, credit, housing, and gold`.

**Repo SOFR and Secured Funding asset translation:** Rates: separate expected short-rate changes, term premium, inflation compensation, carry/roll, and funding. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Repo SOFR and Secured Funding** posterior or activate a rival explanation.

## Fundamental decision application

- Intraday governance: [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]

## Multi-day decision application

- Multi-day governance: [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]

## Falsification and known failure modes

- **Failure test 1 for Repo SOFR and Secured Funding:** treating SOFR as one frictionless rate.
- **Failure test 2 for Repo SOFR and Secured Funding:** ignoring collateral identity.
- **Failure test 3 for Repo SOFR and Secured Funding:** omitting haircut and margin liquidity.
- **Failure test 4 for Repo SOFR and Secured Funding:** using overnight funding for term exposure.
- **Failure test 5 for Repo SOFR and Secured Funding:** missing quarter-end balance-sheet effects.

Score **Repo SOFR and Secured Funding** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required research record

- Schema: [[00 Core Standards/17 Context Object and Permission Schema Standard]]

## Primary source routes for Repo SOFR and Secured Funding

- [[65 Source Registry and Claim Lineage/NYFED_SOFR — New York Fed — SOFR]]
- [[65 Source Registry and Claim Lineage/NYFED_DEALERS — New York Fed — Primary Dealer Statistics]]
- [[65 Source Registry and Claim Lineage/DTCC_UST — DTCC Fixed Income Clearing]]
- [[65 Source Registry and Claim Lineage/UST_AUCTIONS — U.S. Treasury Auction Data]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Implementation Governance]]
