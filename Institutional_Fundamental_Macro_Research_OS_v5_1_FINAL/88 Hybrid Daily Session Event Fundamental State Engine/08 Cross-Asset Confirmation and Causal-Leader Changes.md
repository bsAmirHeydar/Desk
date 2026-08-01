---
title: "Cross-Asset Confirmation and Causal-Leader Changes"
type: canonical-standard
status: canonical
version: 10.4.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [cross-asset, causal-leader, confirmation]
---
# Cross-Asset Confirmation and Causal-Leader Changes

## Causal-leader record

At every mandatory checkpoint rank candidate leaders and identify:

- first mover;
- economic reason it should lead;
- observation timestamp;
- independent confirmations;
- contradictions;
- confidence cap;
- whether leadership changed since prior checkpoint.

## Confirmation independence

Do not count multiple instruments driven by the same underlying observation as independent. Examples:

- 2-year yield and Fed-funds futures are related policy-path evidence, not two fully independent confirmations;
- NQ and QQQ are the same complex;
- DXY and EURUSD are mechanically related.

Seek confirmation from a separate causal channel: credit, real yields, earnings, physical balance, funding, volatility or another region.

## Record triggers

Use `CAUSAL_LEADER_CHANGE` when the primary driver changes. Use `CONFIRMATION_BREAK` when the main state remains but an independent confirmation falls below the required level or becomes contradictory.

## Confirmation score

`CROSS_ASSET_CONFIRMATION_0_100` is an ordinal evidence score unless a documented model calibration exists. State which markets contributed and apply a duplication penalty.
