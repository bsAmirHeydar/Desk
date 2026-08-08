---
title: "Temporal Conflict Resolution and Multi-Clock Dominance"
type: canonical-methodology
status: canonical
version: 15.1.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Temporal Conflict Resolution and Multi-Clock Dominance

V15.1 resolves **root mechanisms**, not timestamp counts.

## Procedure
1. enumerate material clocks inside the execution horizon and safety buffer;
2. build evidence objects with source/freshness/status;
3. map dependency relations using [[93 Temporal Market Structure Timing and Calendar Intelligence Engine/51 Clock Dependency Graph and Double-Counting Firewall]];
4. group clocks by root mechanism;
5. rank root mechanisms by direct target linkage, obligation strength, participant breadth, reset severity, proximity, persistence, evidence quality and independence;
6. resolve sequential transitions and earliest hard hazard;
7. output one dominant root mechanism or explicitly unresolved co-dominance.

## Resolution states
`CLEAR_DOMINANT_ROOT`, `CO_DOMINANT_REINFORCING`, `CO_DOMINANT_OFFSETTING`, `SEQUENTIAL_ROOTS`, `TEMPORALLY_FRAGMENTED`, `CLOCK_UNRESOLVED`.

## Edge rule
Unresolved material conflict blocks Temporal CLEAR. It does not automatically mean permanent NO_TRADE: use `HOLD` when a known near transition can resolve the conflict, `VETO` only when no safe new-entry window exists.
