---
title: "Regime Dependence"
type: field-guide
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - 01-causal-engine
  - regime-dependence
  - institutional-fundamental
---
# Regime Dependence

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Regime Dependence**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

Regime models represent persistent but uncertain state differences in means, variances, correlations, elasticities, and policy responses.

For **Regime Dependence**, the relevant institutional domain is **causal**: causal state estimation under uncertainty, competing explanations, nonlinear feedback, and regime dependence. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Regime Dependence** represent, in what unit, population, instrument, and convention?
2. Which **Regime Dependence** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Regime Dependence** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Regime Dependence** mechanism is active?
5. What rival model can create the same target move while **Regime Dependence** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Regime Dependence** decision?

## Identities and model skeleton

$$
P(S_t=j|S_{t-1}=i)=p_{ij}
$$

$$
y_t|\{S_t=s\}\sim f(\theta_s)
$$

$$
P(S_t|I_t)\propto P(y_t|S_t)\sum_i p_{is}P(S_{t-1}=i|I_{t-1})
$$

For **Regime Dependence**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Regime Dependence:** state probabilities.
- **Measurement 2 for Regime Dependence:** transition matrix and expected duration.
- **Measurement 3 for Regime Dependence:** regime-conditioned betas.
- **Measurement 4 for Regime Dependence:** change-point scores.
- **Measurement 5 for Regime Dependence:** out-of-sample classification stability.

The **Regime Dependence** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Regime Dependence:** Markov switching.
- **Model layer 2 for Regime Dependence:** hidden Markov models.
- **Model layer 3 for Regime Dependence:** Bayesian change-point detection.
- **Model layer 4 for Regime Dependence:** threshold models.
- **Model layer 5 for Regime Dependence:** ensemble state classifier.

Validate the **Regime Dependence** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Structural | In the **Regime Dependence** research object, mechanisms are constrained by institutions, technology, and balance sheets. |
| Cyclical | In the **Regime Dependence** research object, elasticities and policy responses vary with regime and slack. |
| Tactical | In the **Regime Dependence** research object, the vulnerable assumption and feedback loop determine repricing. |
| Daily/Event | In the **Regime Dependence** research object, the leader–confirmation sequence tests the proposed mechanism in event time. |

Conflicts involving **Regime Dependence** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Regime Dependence channel 1:** test `fact → belief revision`.
2. **Regime Dependence channel 2:** test `belief revision → pricing distribution`.
3. **Regime Dependence channel 3:** test `pricing → balance-sheet and behavior response`.
4. **Regime Dependence channel 4:** test `feedback → new state`.

**Regime Dependence asset translation:** Causal trade: name the leader and rival explanation before observing the target return. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Regime Dependence** posterior or activate a rival explanation.

## Fundamental decision application

- Intraday governance: [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]

## Multi-day decision application

- Multi-day governance: [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]

## Falsification and known failure modes

- **Failure test 1 for Regime Dependence:** hard labels without uncertainty.
- **Failure test 2 for Regime Dependence:** too many regimes.
- **Failure test 3 for Regime Dependence:** lookahead state labeling.
- **Failure test 4 for Regime Dependence:** unstable economic interpretation.
- **Failure test 5 for Regime Dependence:** using regime model as causal proof.

Score **Regime Dependence** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required research record

- Schema: [[00 Core Standards/17 Context Object and Permission Schema Standard]]

## Preserved subject-specific foundation

This material survived consolidation because it contains subject-specific instruction for **Regime Dependence**, not the former repeated institutional wrapper.

## Definition

A regime is a persistent configuration of dominant economic constraints, policy behavior, market sensitivity, volatility, and correlation structure.

A regime is not merely “bull” or “bear.”

## Fundamental Regime Axes

### Growth

- accelerating;
- positive but decelerating;
- below trend;
- contracting.

### Inflation

- accelerating;
- sticky;
- disinflating;
- deflationary.

### Policy

- easing;
- neutral;
- tightening;
- constrained by credibility or stability.

### Liquidity

- expanding;
- stable;
- contracting;
- stressed.

### Credit

- benign;
- deteriorating;
- distressed.

### Fiscal

- supportive;
- neutral;
- restrictive;
- credibility-challenged.

## Growth–Inflation Quadrants

| Growth | Inflation | Typical policy tension | Common asset tendency |
|---|---|---|---|
| Up | Down | benign expansion | risk assets supported, bonds mixed |
| Up | Up | overheating | yields/currency up, duration challenged |
| Down | Up | stagflation | difficult for both bonds and equities |
| Down | Down | disinflation/recession | bonds supported; equities depend on credit and earnings |

These are starting priors, not automatic trades.

## Market Sensitivity Regime

The same macro regime can produce different market behavior depending on what prices are sensitive to.

Track rolling sensitivity of:

- Nasdaq to real yields;
- S&P to growth surprises;
- gold to real yields and dollar;
- oil to inventory and risk;
- FX to rate differentials;
- equities to credit spreads;
- volatility to data surprises.

Sensitivity changes are evidence of regime transition.

## Regime Transition Signals

- cross-asset correlation changes;
- bad news begins producing a different response;
- yield-curve dynamics change;
- credit stops confirming equities;
- market reaction to similar releases changes;
- central-bank language shifts;
- inflation breadth changes;
- liquidity indicators deteriorate;
- positioning becomes unstable.

## Dominant Concern Test

After a major release, ask which interpretation wins:

- inflation concern;
- growth concern;
- policy relief;
- earnings relief;
- liquidity concern;
- fiscal concern;
- positioning squeeze.

The winning interpretation is the one that best explains the cross-asset cluster and persists after the first reversal.

## Day-Trading Use

Regime is a filter, not a forecast.

Example:

- In an inflation-dominant regime, hot data makes long-duration equity shorts more permissible.
- In a growth-scare regime, soft data may support bond longs but not equity longs.
- In a liquidity-stress regime, usual safe-haven correlations can temporarily fail because participants sell what they can.
- In a squeeze regime, correct fundamentals can be delayed by positioning.

## Regime Confidence

Use three levels:

- **Established:** multiple data waves, policy alignment, persistent cross-asset behavior.
- **Emerging:** several transition signals but incomplete confirmation.
- **Uncertain:** conflicting state and market sensitivity.

When uncertain, reduce directional restrictions and increase no-trade frequency.

---

## Primary source routes for Regime Dependence

- [[65 Source Registry and Claim Lineage/ALFRED — Federal Reserve Bank of St. Louis ALFRED]]
- [[65 Source Registry and Claim Lineage/OFR_FSI — Office of Financial Research Financial Stress Index]]
- [[65 Source Registry and Claim Lineage/CHI_NFCI — Chicago Fed — NFCI]]
- [[65 Source Registry and Claim Lineage/IMF_GFSR — IMF Global Financial Stability Report]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Implementation Governance]]
