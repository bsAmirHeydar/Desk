---
title: "Adaptive Materiality and Change Thresholds"
type: canonical-standard
status: canonical
version: 10.4.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [thresholds, materiality, scoring]
---
# Adaptive Materiality and Change Thresholds

## Mandatory versus threshold-triggered records

Daily baselines, session handoffs, scheduled checkpoint reassessments, end-of-day records and event micro-windows are mandatory regardless of numerical change. Thresholds govern additional records, not minimum coverage.

## Default lower thresholds

Create an additional material-change record when any of the following occurs:

- Direction Score: 5 points;
- Intensity: 5 points;
- Confidence: 5 points;
- Catalyst Freshness: 10 points;
- Information Absorption: 10 points;
- Repricing Completion: 10 points;
- Flow Exhaustion: 10 points;
- Narrative Saturation: 10 points;
- Remaining Fundamental Pressure: 10 points;
- Reversal Risk: 10 points;
- Cross-Asset Confirmation: 10 points.

## Always-material categorical changes

Record regardless of score:

- directional sign or label change;
- causal leader change;
- winning model change;
- persistence-class change;
- move-quality change;
- edge-availability change;
- confirmation break;
- thesis reinforcement, exhaustion or invalidation;
- fundamental-to-flow or flow-to-fundamental transition;
- material new catalyst or catalyst expiry.

## Micro-event sensitivity

For high-impact events, rapid policy repricing, thin liquidity or a known binary window, use 5-point thresholds for consumption and confirmation sub-scores when the change alters practical interpretation.

## Anti-noise control

Do not create records for numerical noise without a causal explanation. Every score change requires a written reason and an evidence label: observed, derived, model-implied, proxy, structured judgment or unavailable.
