---
title: "01 Research Object and Decision Contract"
type: core-standard
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [research-object, decision-contract, institutional-governance]
---
# 01 Research Object and Decision Contract

## Institutional purpose

A research object is the smallest auditable unit that can support a fundamental decision. It is not a topic heading, a narrative or a collection of links. It is a versioned package that connects a defined target to admissible data, transformations, models, assumptions, evidence, uncertainty, decision consequences and retirement rules.

## Required identity

Every research object must declare:

| Field | Requirement |
|---|---|
| Object ID | Stable, unique and immutable identifier |
| Target | Exact variable, market, institution, company, country or mechanism |
| Decision horizon | Structural, cyclical, tactical, multi-day, intraday or event |
| Cutoff | Timestamp and timezone of the admissible information set |
| Observation time | When the underlying phenomenon occurred |
| Publication time | When the observation became public or licensed to the desk |
| Ingestion time | When the platform received the observation |
| Version | Research, data and model versions |
| Owner | Accountable analyst or research team |
| Independent reviewer | Reviewer with veto authority |
| Expiry | Time or information condition after which the object is stale |

## Mandatory separation of layers

The object must distinguish:

1. **Observation:** source-reported value or document.
2. **Transformation:** seasonal adjustment, normalization, aggregation, curve construction or accounting reconciliation.
3. **Estimate:** latent state, forecast, valuation, market-implied quantity or uncertainty interval.
4. **Claim:** descriptive, predictive, causal or normative statement.
5. **Scenario:** internally coherent conditional world.
6. **Decision state:** research conclusion after expected payoff, risk and portfolio constraints.
7. **Implementation constraints:** instrument, liquidity, cost, financing, capacity and expiry.
8. **Outcome attribution:** what happened and why, without rewriting the ex-ante record.

## Minimum decision contract

A deployable decision contract contains:

- a state distribution rather than a single adjective;
- a market-implied or consensus distribution;
- the residual pricing gap;
- at least one causal model and one serious rival model;
- the variable or market that should lead if the mechanism is active;
- independent confirmations and contradiction signals;
- scenario probabilities, payoffs and losses;
- risk budget, liquidity and cost limits;
- information invalidation and time expiry;
- claim-level evidence IDs;
- an explicit statement of what is unknown.

## Decision-state vocabulary

Use [[00 Core Standards/19 Fundamental-Only Research Boundary and Implementation Standard]]. The output is a fundamental deployment state, not an order or a price-pattern instruction.

## Non-negotiable controls

- No information after the cutoff may enter a historical object.
- No revised observation may overwrite its first-release vintage.
- No market move is evidence of its own cause.
- No model may be promoted without a simple benchmark.
- No scenario probability may be presented as calibrated unless calibration has been measured.
- No winning outcome validates a process by itself.
- No losing outcome invalidates a probabilistic process by itself.
- No narrative may override a predeclared risk or expiry condition.

## Definition of done

The object is complete only when a second researcher can reconstruct the admissible information set, reproduce the derived variables, understand the assumptions, rerun the model, trace every material claim to evidence, reproduce the decision table and audit subsequent changes.
