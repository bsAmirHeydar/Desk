---
title: "Major FX"
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
  - 04-asset-playbooks
  - major-fx
  - institutional-fundamental
---
# Major FX

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Major FX**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

Major-FX analysis is a relative system of policy paths, external balances, funding/hedging, terms of trade, global risk, intervention, and positioning.

For **Major FX**, the relevant institutional domain is **trading**: conversion of macro information into horizon-specific permissions, scenario paths, implementation handoffs, and auditable trade management. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Major FX** represent, in what unit, population, instrument, and convention?
2. Which **Major FX** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Major FX** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Major FX** mechanism is active?
5. What rival model can create the same target move while **Major FX** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Major FX** decision?

## Identities and model skeleton

$$
ExpectedExcessReturn\approx Carry+SpotChange+Roll-Cost
$$

$$
F=S\frac{1+r_d\tau}{1+r_f\tau}+\mathrm{basis\ adjustment}
$$

For **Major FX**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Major FX:** relative OIS and forecast revisions.
- **Measurement 2 for Major FX:** basis and hedge cost.
- **Measurement 3 for Major FX:** external balance and terms of trade.
- **Measurement 4 for Major FX:** risk beta and commodity exposure.
- **Measurement 5 for Major FX:** positioning, options, and intervention.

The **Major FX** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Major FX:** relative macro score.
- **Model layer 2 for Major FX:** hedged-carry model.
- **Model layer 3 for Major FX:** regime-conditioned FX beta.
- **Model layer 4 for Major FX:** flow and intervention scenarios.
- **Model layer 5 for Major FX:** pair-specific event study.

Validate the **Major FX** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Structural/Cyclical | In the **Major FX** research object, higher-horizon states create priors but do not time entries. |
| Tactical/Swing | In the **Major FX** research object, repricing path, catalysts, and half-life determine campaign permission. |
| Daily | In the **Major FX** research object, overnight change and current pricing produce one of four permission states. |
| Event/Intraday | In the **Major FX** research object, leader, confirmation, liquidity, and observable market-state confirmation govern execution. |

Conflicts involving **Major FX** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Major FX channel 1:** test `information gap → leader repricing`.
2. **Major FX channel 2:** test `leader → target asset`.
3. **Major FX channel 3:** test `positioning/liquidity → path shape`.
4. **Major FX channel 4:** test `observable market-state confirmation → executable risk definition`.

**Major FX asset translation:** Trading: fundamentals grant permission; the observable market-state confirmation controls instrument selection, risk budget, and exit conditions. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Major FX** posterior or activate a rival explanation.

## Fundamental decision application

- Intraday governance: [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]

## Multi-day decision application

- Multi-day governance: [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]

## Falsification and known failure modes

- **Failure test 1 for Major FX:** analyzing each currency in isolation.
- **Failure test 2 for Major FX:** using policy levels instead of changes.
- **Failure test 3 for Major FX:** ignoring basis.
- **Failure test 4 for Major FX:** assuming stable risk beta.
- **Failure test 5 for Major FX:** missing local market hours and fixings.

Score **Major FX** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required research record

- Schema: [[00 Core Standards/17 Context Object and Permission Schema Standard]]

## Preserved subject-specific foundation

This material survived consolidation because it contains subject-specific instruction for **Major FX**, not the former repeated institutional wrapper.

## Universal FX Framework

For currency A versus currency B:

\[
FX_{A/B} =
f(
\text{relative policy},
\text{relative growth},
\text{relative inflation credibility},
\text{external balance},
\text{terms of trade},
\text{funding/risk},
\text{flows},
\text{positioning}
)
\]

## EUR/USD

Primary themes:

- Fed vs ECB expected path;
- US vs euro-area growth;
- energy terms of trade;
- fiscal fragmentation/credibility;
- broad dollar funding;
- portfolio flows.

Confirmation:

- US–German front-end spread;
- broad dollar;
- European credit/periphery spreads;
- risk assets;
- energy.

## GBP/USD

Primary themes:

- Fed vs Bank of England;
- UK services/wage inflation;
- growth and housing;
- fiscal credibility;
- current account and global risk;
- EUR/GBP cross.

GBP can be rate-sensitive but vulnerable to credibility and external-financing shocks.

## USD/JPY

Primary themes:

- US–Japan yield differentials;
- Bank of Japan normalization;
- Japanese wage/inflation cycle;
- carry and global volatility;
- Ministry of Finance intervention risk;
- repatriation and hedging.

A high carry can persist until volatility or intervention changes the payoff.

## AUD/USD

Primary themes:

- China/global growth;
- commodities and terms of trade;
- Reserve Bank of Australia path;
- risk appetite;
- carry;
- housing and domestic demand.

## USD/CAD

Primary themes:

- Fed vs Bank of Canada;
- oil and terms of trade;
- US/Canada growth;
- housing and household leverage;
- risk appetite.

## USD/CHF

Primary themes:

- safe-haven demand;
- Swiss National Bank policy/intervention;
- European risk;
- inflation differential;
- global funding.

## Daily Pair Process

1. Identify today’s primary country catalyst.
2. Compare expected policy-path change on both sides.
3. Check broad-dollar direction.
4. Check risk/funding regime.
5. Check pair-specific terms of trade or intervention.
6. Observe cross-pairs.
7. Set permission.
8. Wait for implementation continuation.

## Event Logic

A US data surprise should not be traded identically across all USD pairs.

- USD/JPY may react strongly through yields.
- AUD/USD may react through both USD and global risk.
- EUR/USD may depend on ECB repricing and European data.
- USD/CAD may be offset by oil.
- USD/CHF may reflect safe-haven cross-currents.

## Common Traps

- absolute analysis of one country;
- current-rate rather than expected-path comparison;
- ignoring intervention;
- using DXY as perfect confirmation for every pair;
- assuming risk-off strengthens JPY in every yield regime;
- ignoring energy terms of trade;
- confusing carry with free return;
- using stale COT as entry timing.

---

## Primary source routes for Major FX

- [[65 Source Registry and Claim Lineage/BIS_GLI — BIS Global Liquidity Indicators]]
- [[65 Source Registry and Claim Lineage/IMF_ESR — IMF External Sector Report]]
- [[65 Source Registry and Claim Lineage/ECB — European Central Bank]]
- [[65 Source Registry and Claim Lineage/BOJ — Bank of Japan]]
- [[65 Source Registry and Claim Lineage/BOE — Bank of England]]
- [[65 Source Registry and Claim Lineage/CFTC_COT — CFTC Commitments of Traders]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Implementation Governance]]
