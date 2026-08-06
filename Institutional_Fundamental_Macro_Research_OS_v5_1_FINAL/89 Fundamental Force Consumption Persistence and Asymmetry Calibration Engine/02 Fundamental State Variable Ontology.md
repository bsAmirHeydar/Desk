---
title: "Fundamental State Variable Ontology"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Fundamental State Variable Ontology

## Decision purpose

Prevent category errors by defining the complete state object before scoring it. The ontology separates observed evidence, latent states, expectations, transmission, market response, overlays and decision-usefulness.

## Governing distinctions

- Fact is not state.
- Analyst forecast is not market expectation.
- Price response is not causal proof.
- Fundamental direction is not execution permission.
- A multi-horizon object cannot be represented by one timeless score.

## Operating method

1. Freeze the information boundary.
2. Identify the economic state variable and expectation being updated.
3. Map causal channels and rival channels.
4. Separate fundamental repricing from flow/liquidity overlays.
5. Build horizon-indexed force, consumption and residual states.

## Required outputs

- `fact_ledger`
- `expectation_state`
- `surprise_vector`
- `transmission_graph`
- `consumption_vector`
- `remaining_pressure_vector`
- `decision_state`

## Failure modes and controls

- **Failure:** One score absorbs every concept  
  **Control:** Retain component vectors and disclose aggregation logic.
- **Failure:** State is inferred from later price outcome  
  **Control:** Enforce cutoff timestamps and immutable records.
- **Failure:** Same label means different things across assets  
  **Control:** Use asset books and explicit units/applicability maps.

## Object graph

```text
Economic state
→ prior expectation distribution
→ catalyst or observation
→ surprise vector
→ expectation-path revision
→ causal transmission channels
→ market-implied and observed repricing
→ institutional/flow overlay
→ consumption vector
→ residual remaining pressure
→ persistence and reversal hazard
→ path asymmetry and edge availability
```

Each arrow is conditional. A strong observation can fail to revise expectations; an expectation revision can fail to transmit to the target instrument; a price move can occur without validating the proposed causal chain.

## Identity rules

- A **fact** is an observation with a timestamp and source.
- A **state** is a latent or measured condition inferred from facts.
- An **expectation** is the market's pre-catalyst distribution, not the analyst's forecast.
- A **surprise** is the difference between observation and recoverable expectation, adjusted for composition and relevance.
- **Force** is the directionally signed change in economically relevant state and transmission potential.
- **Consumption** describes how much of the information-to-positioning-to-price process is complete.
- **Remaining pressure** is the unresolved directional residual after opposing forces and hazards.
- **Edge availability** asks whether that residual remains usable at the selected horizon.

## Canonical dependencies

- [[00 Core Standards/05 Expectations Pricing and Distribution Gap]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/14 Hybrid Fundamental State Schema]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
