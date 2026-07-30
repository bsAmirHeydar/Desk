---
title: "Calendar and Timestamp Discipline"
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
  - 10-data-sources
  - calendar-and-timestamp-discipline
  - institutional-fundamental
---
# Calendar and Timestamp Discipline

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Calendar and Timestamp Discipline**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

Cross-currency basis measures the cost of obtaining one currency through FX swaps relative to cash-market borrowing after accounting for conventions and balance-sheet frictions.

For **Calendar and Timestamp Discipline**, the relevant institutional domain is **data_reference**: source-controlled data, definitions, metadata, transformations, lineage, schemas, and reproducible research interfaces. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Calendar and Timestamp Discipline** represent, in what unit, population, instrument, and convention?
2. Which **Calendar and Timestamp Discipline** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Calendar and Timestamp Discipline** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Calendar and Timestamp Discipline** mechanism is active?
5. What rival model can create the same target move while **Calendar and Timestamp Discipline** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Calendar and Timestamp Discipline** decision?

## Identities and model skeleton

$$
F_{t,T}^{CIP}=S_t\frac{1+r_d\tau}{1+r_f\tau}
$$

$$
Basis\approx \frac{1}{\tau}\ln\left(\frac{F}{S}\right)-(r_d-r_f)
$$

$$
HedgedReturn_f\approx r_f+\frac{F-S}{S\tau}
$$

For **Calendar and Timestamp Discipline**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Calendar and Timestamp Discipline:** spot, forwards, OIS, and FX swaps.
- **Measurement 2 for Calendar and Timestamp Discipline:** tenor basis curve.
- **Measurement 3 for Calendar and Timestamp Discipline:** bank and institutional hedging demand.
- **Measurement 4 for Calendar and Timestamp Discipline:** quarter/year-end balance-sheet pressure.
- **Measurement 5 for Calendar and Timestamp Discipline:** cross-border credit and collateral.

The **Calendar and Timestamp Discipline** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Calendar and Timestamp Discipline:** CIP-consistent curve.
- **Model layer 2 for Calendar and Timestamp Discipline:** basis decomposition by funding/hedging.
- **Model layer 3 for Calendar and Timestamp Discipline:** tenor and turn analysis.
- **Model layer 4 for Calendar and Timestamp Discipline:** hedged-yield comparison.
- **Model layer 5 for Calendar and Timestamp Discipline:** stress and normalization scenarios.

Validate the **Calendar and Timestamp Discipline** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Design | In the **Calendar and Timestamp Discipline** research object, definitions, identifiers, and ownership must be stable. |
| Historical | In the **Calendar and Timestamp Discipline** research object, vintages and methodology changes preserve the information set. |
| Production | In the **Calendar and Timestamp Discipline** research object, latency, missingness, and source continuity are monitored. |
| Decision | In the **Calendar and Timestamp Discipline** research object, every feature and claim is traceable to the admissible source timestamp. |

Conflicts involving **Calendar and Timestamp Discipline** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Calendar and Timestamp Discipline channel 1:** test `publisher → raw immutable observation`.
2. **Calendar and Timestamp Discipline channel 2:** test `raw → curated point-in-time feature`.
3. **Calendar and Timestamp Discipline channel 3:** test `feature → model and decision object`.
4. **Calendar and Timestamp Discipline channel 4:** test `decision → audit and reproducibility record`.

**Calendar and Timestamp Discipline asset translation:** Data: no field enters a decision without units, vintage, lineage, and quality status. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Calendar and Timestamp Discipline** posterior or activate a rival explanation.

## Fundamental decision application

- Intraday governance: [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]

## Multi-day decision application

- Multi-day governance: [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]

## Falsification and known failure modes

- **Failure test 1 for Calendar and Timestamp Discipline:** sign-convention errors.
- **Failure test 2 for Calendar and Timestamp Discipline:** mixing unsecured rates with OIS.
- **Failure test 3 for Calendar and Timestamp Discipline:** ignoring settlement and collateral.
- **Failure test 4 for Calendar and Timestamp Discipline:** calling all basis dollar shortage.
- **Failure test 5 for Calendar and Timestamp Discipline:** using indicative quotes without executable depth.

Score **Calendar and Timestamp Discipline** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required research record

- Schema: [[00 Core Standards/17 Context Object and Permission Schema Standard]]

## Preserved subject-specific foundation

This material survived consolidation because it contains subject-specific instruction for **Calendar and Timestamp Discipline**, not the former repeated institutional wrapper.

Fundamental research fails when the model uses information before it was publicly available.

## Required Timestamps

Store:

- reference period;
- scheduled release timestamp;
- actual publication timestamp;
- first reliable receipt timestamp;
- market venue timestamp;
- timezone and daylight-saving status;
- revision timestamp;
- source URL/archive.

## Timezones

Use a canonical storage timezone, preferably UTC, while preserving source timezone.

```yaml
release_time_source: 08:30 America/New_York
release_time_utc:
dst_rule:
first_market_bar_after_release:
```

Europe/Amsterdam and New York daylight-saving transitions do not always change on the same date. Never hard-code a constant offset for session studies.

## Calendar Sources

- BLS release calendar: https://www.bls.gov/schedule/
- BEA release schedule: https://www.bea.gov/news/schedule
- Federal Reserve calendar: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
- Treasury auctions: https://treasurydirect.gov/auctions/upcoming/
- EIA release schedule: https://www.eia.gov/todayinenergy/schedule.php
- Company investor-relations calendars and SEC filings.

## Unscheduled Events

Store:

- first verified timestamp;
- source hierarchy;
- original statement/document;
- later corrections;
- whether markets were open;
- liquidity conditions.

## Research Alignment

For bar data:

- a release at 08:30:00 cannot be used to predict the 08:30 bar open if the bar includes post-release trading;
- define whether features are available at bar open, close, or after a delay;
- include data/vendor latency;
- avoid using revised calendar timestamps.

## Event Window Labels

```text
PRE_EVENT
RELEASE_IMPULSE
PRICE_DISCOVERY
POST_EVENT_ACCEPTANCE
LATE_SESSION_DIGESTION
```

These labels should be empirically defined by asset and event type.

## Audit Rule

Every backtest observation should answer: **What exact information set was available at the decision timestamp?**

---

## Primary source routes for Calendar and Timestamp Discipline

- [[65 Source Registry and Claim Lineage/BIS_GLI — BIS Global Liquidity Indicators]]
- [[65 Source Registry and Claim Lineage/BIS — Bank for International Settlements]]
- [[65 Source Registry and Claim Lineage/NYFED_SOFR — New York Fed — SOFR]]
- [[65 Source Registry and Claim Lineage/UST_TIC — U.S. Treasury International Capital System]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Implementation Governance]]
