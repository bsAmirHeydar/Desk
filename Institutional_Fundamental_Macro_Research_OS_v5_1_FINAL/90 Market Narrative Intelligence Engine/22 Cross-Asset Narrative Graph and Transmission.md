---
title: "Cross-Asset Narrative Graph and Transmission"
type: canonical-method
status: canonical
version: 12.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v12, market-narrative, daily-intelligence]
---
# Cross-Asset Narrative Graph and Transmission

## Graph ontology

The graph links facts, expectations, narratives, yields, currencies, credit, volatility, liquidity, sectors and target assets. Every edge is typed as `CAUSAL`, `CONFIRMATION`, `MECHANICAL`, `CORRELATED`, `ATTENTION`, `FLOW` or `UNCERTAIN`.

## Independence control

DXY and EURUSD, cash index and futures, or front-end yields and policy-implied rates may overlap mechanically. Do not count dependent edges as independent confirmation. Store an independence class and rationale.

## Leader sequence

For each narrative predeclare the expected sequence. Example: Fed-path revision → front-end rates → real yields → Nasdaq duration valuation. If the target moves without the leader, downgrade causal confidence or activate a flow/rival model.

The graph can show different narratives controlling different nodes. It must not force one global market story.

## V21 dynamic causal graph
V21 distinguishes the canonical possibility graph from the run-specific graph. Every material edge receives an active/dormant/weakening/broken/uncertain state and a horizon. Same-root independence is deduplicated while distinct channels are retained.
