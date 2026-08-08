---
title: "Clock Dependency Graph and Double-Counting Firewall"
type: canonical-methodology
status: canonical
version: 15.1.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, clock-graph, double-counting]
---
# Clock Dependency Graph and Double-Counting Firewall

Multiple timestamps can be stages of one institutional mechanism. Counting them independently creates false timing conviction and over-veto.

## Relationship classes
- `INDEPENDENT`;
- `PARENT_CHILD`;
- `SAME_ROOT_MECHANISM`;
- `SEQUENTIAL_STAGE`;
- `MECHANICALLY_LINKED`;
- `AMPLIFIER`;
- `CORRELATED_ONLY`;
- `UNKNOWN_RELATION`.

## Examples
- Equity-index quarterly expiry, SOQ, cash opening prints and futures final settlement are related stages of one expiration/settlement mechanism; they are not four independent vetoes.
- Month-end WMR benchmark and asset-manager hedge implementation can share a root mechanism.
- A Treasury auction and an unrelated earnings release may be independent clocks even when timestamps are close.

## Dominance
Rank **root mechanisms**, then clocks within each mechanism. Materiality is based on direct target linkage, institutional obligation, participant breadth, reset severity, proximity, persistence, evidence quality and independence.

## Gate consequence
One strong root mechanism can create HOLD/VETO. Five weak child clocks cannot be added together mechanically to imitate one strong independent mechanism.
