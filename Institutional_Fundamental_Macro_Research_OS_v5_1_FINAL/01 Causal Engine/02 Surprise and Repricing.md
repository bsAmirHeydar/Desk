---
title: "Surprise and Repricing"
type: field-guide
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - 01-causal-engine
  - surprise-and-repricing
  - institutional-fundamental
---
# Surprise and Repricing

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Surprise and Repricing**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

An event study measures the point-in-time surprise vector and abnormal price path around a precisely timestamped release while controlling for overlapping news and liquidity.

For **Surprise and Repricing**, the relevant institutional domain is **causal**: causal state estimation under uncertainty, competing explanations, nonlinear feedback, and regime dependence. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Surprise and Repricing** represent, in what unit, population, instrument, and convention?
2. Which **Surprise and Repricing** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Surprise and Repricing** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Surprise and Repricing** mechanism is active?
5. What rival model can create the same target move while **Surprise and Repricing** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Surprise and Repricing** decision?

## Identities and model skeleton

$$
Surprise_{i,t}=\frac{Actual_{i,t}-Consensus_{i,t}}{\sigma_i}
$$

$$
AR_{a,t}=R_{a,t}-\widehat\beta_a^\top F_t
$$

$$
CAR_{[0,h]}=\sum_{\tau=0}^{h}AR_\tau
$$

For **Surprise and Repricing**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Surprise and Repricing:** release and market timestamps.
- **Measurement 2 for Surprise and Repricing:** full consensus distribution.
- **Measurement 3 for Surprise and Repricing:** component and revision surprises.
- **Measurement 4 for Surprise and Repricing:** quotes/trades at multiple horizons.
- **Measurement 5 for Surprise and Repricing:** overlapping news and liquidity state.

The **Surprise and Repricing** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Surprise and Repricing:** high-frequency event study.
- **Model layer 2 for Surprise and Repricing:** local projection on surprise vectors.
- **Model layer 3 for Surprise and Repricing:** regime interaction.
- **Model layer 4 for Surprise and Repricing:** reversal/persistence classifier.
- **Model layer 5 for Surprise and Repricing:** transaction-cost-adjusted strategy test.

Validate the **Surprise and Repricing** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Structural | In the **Surprise and Repricing** research object, mechanisms are constrained by institutions, technology, and balance sheets. |
| Cyclical | In the **Surprise and Repricing** research object, elasticities and policy responses vary with regime and slack. |
| Tactical | In the **Surprise and Repricing** research object, the vulnerable assumption and feedback loop determine repricing. |
| Daily/Event | In the **Surprise and Repricing** research object, the leader–confirmation sequence tests the proposed mechanism in event time. |

Conflicts involving **Surprise and Repricing** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Surprise and Repricing channel 1:** test `fact → belief revision`.
2. **Surprise and Repricing channel 2:** test `belief revision → pricing distribution`.
3. **Surprise and Repricing channel 3:** test `pricing → balance-sheet and behavior response`.
4. **Surprise and Repricing channel 4:** test `feedback → new state`.

**Surprise and Repricing asset translation:** Causal trade: name the leader and rival explanation before observing the target return. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Surprise and Repricing** posterior or activate a rival explanation.

## Fundamental decision application

- Intraday governance: [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]

## Multi-day decision application

- Multi-day governance: [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]]

## Falsification and known failure modes

- **Failure test 1 for Surprise and Repricing:** using revised actuals.
- **Failure test 2 for Surprise and Repricing:** median-only consensus.
- **Failure test 3 for Surprise and Repricing:** clock misalignment.
- **Failure test 4 for Surprise and Repricing:** data-snooped event windows.
- **Failure test 5 for Surprise and Repricing:** ignoring simultaneous releases.

Score **Surprise and Repricing** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required research record

- Schema: [[00 Core Standards/17 Context Object and Permission Schema Standard]]

## Preserved subject-specific foundation

This material survived consolidation because it contains subject-specific instruction for **Surprise and Repricing**, not the former repeated institutional wrapper.

## Surprise Is Multidimensional

The simplest definition is:

\[
\text{Headline Surprise} = \text{Actual} - \text{Consensus}
\]

This is insufficient.

A complete surprise vector includes:

- headline surprise;
- core/component surprise;
- revision surprise;
- breadth and diffusion;
- composition quality;
- persistence signal;
- policy relevance;
- market-positioning surprise;
- and narrative surprise.

## Consensus Is a Distribution

The published median hides:

- dispersion among forecasts;
- skew;
- late forecast changes;
- whisper estimates;
- option-implied event risk;
- and one-sided positioning.

A print at consensus can still be surprising when the market was positioned for a softer or stronger outcome.

## First-Order and Second-Order Surprise

### First-order

What changed in the measured variable?

Example: CPI was above consensus.

### Second-order

What does that change imply for policy, growth, earnings, risk premia, and future data?

Example:

- Was the inflation surprise broad?
- Was shelter lagging?
- Did services excluding housing accelerate?
- Did wages or productivity alter persistence?
- Does the central bank react?
- Does the surprise damage real income and growth?

The second-order interpretation usually determines persistence.

## Repricing Channels

A macro surprise can reprice:

1. **Current policy rate**
2. **Future policy path**
3. **Terminal or neutral rate**
4. **Inflation compensation**
5. **Real yields**
6. **Term premium**
7. **Growth and earnings**
8. **Credit risk**
9. **Volatility and tail probability**
10. **Currency risk premium**

## Event Reaction Sequence

### Phase 1 — Algorithmic parsing

Milliseconds to seconds. Headline and key components hit.

### Phase 2 — Cross-asset repricing

Seconds to minutes. Rates, FX, index futures, gold, and volatility respond.

### Phase 3 — Human decomposition

Minutes to roughly one hour. Revisions, details, and policy implications are assessed.

### Phase 4 — Position adjustment

One hour to several sessions. Real-money, macro, systematic, and hedging flows react.

### Phase 5 — Narrative stabilization

The market settles on a dominant interpretation until contradicted.

For day trading, the best opportunity is often not the first spike. It can be the continuation after Phase 2 or the reversal when Phase 3 invalidates the headline reaction.

## State Dependence

A positive growth surprise can:

- raise equities in a recession-fear regime;
- lower equities in an inflation-fear regime;
- raise the currency if policy divergence dominates;
- lower bonds through higher expected rates;
- or produce little movement if fully priced.

## Surprise Quality Checklist

- Was the release reliable or noisy?
- Were prior months revised?
- Did the market care about the headline or a component?
- Did the release alter the central-bank reaction function?
- Did the front end confirm the interpretation?
- Did real yields or breakevens drive nominal yields?
- Did credit spreads confirm or reject the growth story?
- Did the dollar confirm relative policy?
- Was the move accepted after the first temporary counter-move?
- Is the move large relative to the actual repricing?

## Repricing Exhaustion

A correct surprise can still be a poor trade when:

- the expected move occurs instantly;
- positioning is already extreme;
- the instrument overshoots relative to rates;
- liquidity is thin;
- the next catalyst can reverse the interpretation;
- or cross-asset follow-through fails.

The tradeable edge is not “being right about the number.” It is estimating whether the repricing is incomplete.

---

## Primary source routes for Surprise and Repricing

- [[65 Source Registry and Claim Lineage/ALFRED — Federal Reserve Bank of St. Louis ALFRED]]
- [[65 Source Registry and Claim Lineage/BLS_CPI — US BLS — CPI]]
- [[65 Source Registry and Claim Lineage/BLS_EMP — US BLS — Employment Situation]]
- [[65 Source Registry and Claim Lineage/CME_FEDWATCH — CME FedWatch]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Implementation Governance]]
