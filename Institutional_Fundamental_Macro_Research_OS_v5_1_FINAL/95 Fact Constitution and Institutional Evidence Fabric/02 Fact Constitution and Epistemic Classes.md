---
title: "Fact Constitution and Epistemic Classes"
type: canonical-science-note
status: canonical
version: 17.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [v17, fact, ontology, epistemics]
---

# Canonical epistemic classes

Every load-bearing statement must expose exactly one primary class. Prose may not silently promote an inference into an observation.

## Direct factual classes

- `OBSERVED_FACT` — directly observed non-price state with identifiable observation method.
- `OBSERVED_MARKET_DATA` — directly observed market datum such as a published price, yield, spread, volume or exchange statistic.
- `OFFICIAL_REPORTED_FACT` — value formally released by an official/statutory source.
- `CONTRACTUAL_FACT` — rule, methodology, fixing convention, contract specification, index rule or published legal/operational term.
- `IDENTIFIED_FLOW_FACT` — an actual flow only when the actor/vehicle and measurement basis are identified sufficiently to justify the label.
- `IDENTIFIED_POSITIONING_FACT` — an actual positioning/ownership observation with defined participant universe and measurement basis.

## Measured or transformed factual classes

- `MARKET_IMPLIED_FACT` — a quantity implied from observable market instruments under an explicit method.
- `PUBLIC_PROXY` — a public observable used as a proxy for an unavailable target variable; never equivalent to the target.
- `DERIVED_FACT` — deterministic or reproducible transformation of parent facts with method/version lineage.

## Non-factual analytical classes

- `MODEL_INFERENCE` — analytical conclusion produced by a model or analyst.
- `NARRATIVE_INFERENCE` — statement about attention, narrative dominance, interpretation or reflexive transmission.
- `SCENARIO_ASSUMPTION` — conditional assumption used for scenario analysis.

## Epistemic availability states

- `AVAILABLE` — evidence was demonstrably available to the run.
- `UNAVAILABLE` — the target data are known to be inaccessible/not supplied for the required scope.
- `UNDETERMINED` — the system cannot determine whether the required fact is true or available.

`UNAVAILABLE` and `UNDETERMINED` are not values to be imputed. They are explicit states that route through materiality.

## Direction boundary

Only the validated Fundamental stack may own live direction. `NARRATIVE_INFERENCE`, `MODEL_INFERENCE`, `PUBLIC_PROXY`, positioning/flow labels or technical price patterns cannot masquerade as the root directional authority.
