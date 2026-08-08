---
title: "V17 D1 Manual and Scheduled Launcher Contract"
type: canonical-science-note
status: canonical
version: 17.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [v17, launcher, runtime]
---

# Launcher contract

Manual and scheduled runs call only the V17 D1 production entrypoint after D1 runtime preflight passes.

## Short launcher

`Run Alpha Lab V17 D1 for <SYMBOL> at NOW or the supplied historical cutoff. Resolve the instrument, build a point-in-time Decision Evidence Pack and Fact Coverage Receipt under Module 95, then delegate scientific synthesis to the validated V16.1 stack. Use Fundamental as sole direction authority, Narrative/Timing only as clearance layers, preserve D2-pending boundaries, and return Persian BUY/SELL/NO_TRADE with validity, next-review time, evidence gaps and exact source/vintage lineage. No look-ahead and no invented unavailable data.`

## Scheduler rule

A scheduled run must create a new immutable run ID and evidence pack. It must not reuse a stale permission merely because the previous run had the same direction.
