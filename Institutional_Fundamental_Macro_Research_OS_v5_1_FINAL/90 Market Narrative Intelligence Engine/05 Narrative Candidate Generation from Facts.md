---
title: "Narrative Candidate Generation from Facts"
type: canonical-method
status: canonical
version: 12.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v12, market-narrative, daily-intelligence]
---
# Narrative Candidate Generation from Facts

## Candidate-generation procedure

Start with the frozen fact ledger, not price charts. Cluster facts by common state variable or transmission channel. For each cluster, state the most direct interpretation, then generate at least one plausible rival interpretation and one flow-only explanation where relevant.

For every candidate document:

- the facts it selects;
- the expectation it claims has changed;
- the causal sequence;
- the first variable that should move;
- the target asset and horizon;
- confirming and contradicting observations;
- what evidence is still missing;
- and the predeclared rejection condition.

## Candidate classes

Use `FACT_LED`, `POLICY_LED`, `EARNINGS_LED`, `FLOW_LED`, `POSITIONING_LED`, `MEDIA_LED`, `REFLEXIVE`, or `MIXED`. Classification describes the current mechanism, not the topic.

## Anti-story rule

A candidate that cannot name its fact basis, expectation revision and causal discriminator is a story, not an admissible narrative. Price action may reveal sensitivity or control, but candidates must not be retrofitted solely to explain a completed move.
