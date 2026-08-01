---
title: "15 Historical Reconstruction and Event Clock Standard"
type: standard
status: canonical
version: 10.4.0
created: 2026-07-29
updated: 2026-08-01
language: en
tags: [institutional-standard, historical-reconstruction, event-clock, session-state]
---
# 15 Historical Reconstruction and Event Clock Standard

## Governing architecture

Historical reconstruction uses the hybrid architecture in [[88 Hybrid Daily Session Event Fundamental State Engine/00 Hybrid Daily Session Event Fundamental State Engine MOC]]. Event-only reconstruction is deprecated.

## Required clocks

Store reference period, scheduled release time, actual publication time, desk-availability time, observation time, revision time, local timezone, UTC and daylight-saving convention.

## Mandatory state sequence

For every open trading day, reconstruct:

- daily baseline;
- overnight change;
- relevant session handoffs;
- pre-event baselines and event micro-windows;
- post-open, midday and afternoon reassessments;
- state decay and no-change records;
- end-of-day attribution and carry-forward.

## Reconstruction packet

Store official documents and contemporaneous vintages, available consensus or priced distribution, market curves/options/positioning/liquidity evidence, scenario tree, surprise vector, causal leader, confirmation sequence, state-decay ledger, missing archives and what a rational desk could not have known.

## Immutability

Never rewrite an earlier state using a later reaction. Every update is a new linked record. Ex-post audit is separate and cannot alter the reconstructed state.

## Counterfactual boundary

Counterfactuals and realized outcomes belong only in an explicitly requested ex-post audit. The primary historical state engine must remain outcome-blind.
