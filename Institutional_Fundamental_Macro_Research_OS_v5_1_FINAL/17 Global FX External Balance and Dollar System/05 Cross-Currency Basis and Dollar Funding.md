---
title: "Cross-Currency Basis and Dollar Funding"
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
  - 17-global-fx-external-balance-and-dollar-system
  - cross-currency-basis-and-dollar-funding
  - institutional-fundamental
---
# Cross-Currency Basis and Dollar Funding

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Cross-Currency Basis and Dollar Funding**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

Secured funding prices cash, collateral scarcity, counterparty balance sheet, settlement demand, and regulatory capacity. Cross-currency basis measures the cost of obtaining one currency through FX swaps relative to cash-market borrowing after accounting for conventions and balance-sheet frictions.

For **Cross-Currency Basis and Dollar Funding**, the relevant institutional domain is **fx**: relative monetary, external-balance, funding, hedging, valuation, and capital-flow forces across currencies. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Cross-Currency Basis and Dollar Funding** represent, in what unit, population, instrument, and convention?
2. Which **Cross-Currency Basis and Dollar Funding** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Cross-Currency Basis and Dollar Funding** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Cross-Currency Basis and Dollar Funding** mechanism is active?
5. What rival model can create the same target move while **Cross-Currency Basis and Dollar Funding** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Cross-Currency Basis and Dollar Funding** decision?

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

$$
F_{t,T}^{CIP}=S_t\frac{1+r_d\tau}{1+r_f\tau}
$$

$$
Basis\approx \frac{1}{\tau}\ln\left(\frac{F}{S}\right)-(r_d-r_f)
$$

$$
HedgedReturn_f\approx r_f+\frac{F-S}{S\tau}
$$

For **Cross-Currency Basis and Dollar Funding**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Cross-Currency Basis and Dollar Funding:** SOFR distribution and volumes.
- **Measurement 2 for Cross-Currency Basis and Dollar Funding:** general collateral and specials.
- **Measurement 3 for Cross-Currency Basis and Dollar Funding:** haircuts and fails.
- **Measurement 4 for Cross-Currency Basis and Dollar Funding:** dealer inventories and Treasury settlement.
- **Measurement 5 for Cross-Currency Basis and Dollar Funding:** sponsored repo and balance-sheet dates.
- **Measurement 6 for Cross-Currency Basis and Dollar Funding:** spot, forwards, OIS, and FX swaps.
- **Measurement 7 for Cross-Currency Basis and Dollar Funding:** tenor basis curve.
- **Measurement 8 for Cross-Currency Basis and Dollar Funding:** bank and institutional hedging demand.
- **Measurement 9 for Cross-Currency Basis and Dollar Funding:** quarter/year-end balance-sheet pressure.
- **Measurement 10 for Cross-Currency Basis and Dollar Funding:** cross-border credit and collateral.

The **Cross-Currency Basis and Dollar Funding** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Cross-Currency Basis and Dollar Funding:** funding-spread decomposition.
- **Model layer 2 for Cross-Currency Basis and Dollar Funding:** collateral-specialness map.
- **Model layer 3 for Cross-Currency Basis and Dollar Funding:** settlement-flow forecast.
- **Model layer 4 for Cross-Currency Basis and Dollar Funding:** basis stress test.
- **Model layer 5 for Cross-Currency Basis and Dollar Funding:** liquidity ladder.
- **Model layer 6 for Cross-Currency Basis and Dollar Funding:** CIP-consistent curve.
- **Model layer 7 for Cross-Currency Basis and Dollar Funding:** basis decomposition by funding/hedging.
- **Model layer 8 for Cross-Currency Basis and Dollar Funding:** tenor and turn analysis.
- **Model layer 9 for Cross-Currency Basis and Dollar Funding:** hedged-yield comparison.
- **Model layer 10 for Cross-Currency Basis and Dollar Funding:** stress and normalization scenarios.

Validate the **Cross-Currency Basis and Dollar Funding** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Structural | In the **Cross-Currency Basis and Dollar Funding** research object, productivity, net foreign assets, reserve regime, and institutions shape valuation. |
| Cyclical | In the **Cross-Currency Basis and Dollar Funding** research object, relative growth, inflation, policy, and external financing drive trends. |
| Tactical/Swing | In the **Cross-Currency Basis and Dollar Funding** research object, hedging, carry, intervention risk, and positioning shape persistence. |
| Daily/Event | In the **Cross-Currency Basis and Dollar Funding** research object, relative front-end rates, basis, and broad-dollar response are primary leaders. |

Conflicts involving **Cross-Currency Basis and Dollar Funding** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Cross-Currency Basis and Dollar Funding channel 1:** test `relative growth/inflation → policy paths`.
2. **Cross-Currency Basis and Dollar Funding channel 2:** test `policy and hedging → forward curves`.
3. **Cross-Currency Basis and Dollar Funding channel 3:** test `external funding stress → basis and spot`.
4. **Cross-Currency Basis and Dollar Funding channel 4:** test `capital flow and intervention → persistence or reversal`.

**Cross-Currency Basis and Dollar Funding asset translation:** FX: use relative rather than absolute state; include hedge cost, basis, intervention, and broad-dollar context. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Cross-Currency Basis and Dollar Funding** posterior or activate a rival explanation.

## Fundamental decision application

- Intraday governance: [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]

## Multi-day decision application

- Multi-day governance: [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]

## Falsification and known failure modes

- **Failure test 1 for Cross-Currency Basis and Dollar Funding:** treating SOFR as one frictionless rate.
- **Failure test 2 for Cross-Currency Basis and Dollar Funding:** ignoring collateral identity.
- **Failure test 3 for Cross-Currency Basis and Dollar Funding:** omitting haircut and margin liquidity.
- **Failure test 4 for Cross-Currency Basis and Dollar Funding:** using overnight funding for term exposure.
- **Failure test 5 for Cross-Currency Basis and Dollar Funding:** missing quarter-end balance-sheet effects.
- **Failure test 6 for Cross-Currency Basis and Dollar Funding:** sign-convention errors.
- **Failure test 7 for Cross-Currency Basis and Dollar Funding:** mixing unsecured rates with OIS.
- **Failure test 8 for Cross-Currency Basis and Dollar Funding:** ignoring settlement and collateral.
- **Failure test 9 for Cross-Currency Basis and Dollar Funding:** calling all basis dollar shortage.
- **Failure test 10 for Cross-Currency Basis and Dollar Funding:** using indicative quotes without executable depth.

Score **Cross-Currency Basis and Dollar Funding** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required research record

- Schema: [[00 Core Standards/17 Context Object and Permission Schema Standard]]

## Primary source routes for Cross-Currency Basis and Dollar Funding

- [[65 Source Registry and Claim Lineage/NYFED_SOFR — New York Fed — SOFR]]
- [[65 Source Registry and Claim Lineage/NYFED_DEALERS — New York Fed — Primary Dealer Statistics]]
- [[65 Source Registry and Claim Lineage/DTCC_UST — DTCC Fixed Income Clearing]]
- [[65 Source Registry and Claim Lineage/UST_AUCTIONS — U.S. Treasury Auction Data]]
- [[65 Source Registry and Claim Lineage/BIS_GLI — BIS Global Liquidity Indicators]]
- [[65 Source Registry and Claim Lineage/BIS — Bank for International Settlements]]
- [[65 Source Registry and Claim Lineage/UST_TIC — U.S. Treasury International Capital System]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Implementation Governance]]
