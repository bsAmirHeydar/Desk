---
title: "Structural Liquidity and Participant Availability without Price Analysis"
type: canonical-methodology
status: canonical
version: 15.1.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, liquidity, participants, no-price-analysis]
---
# Structural Liquidity and Participant Availability without Price Analysis

V15.1 distinguishes structural time-based liquidity from technical price analysis.

## Permitted timing inputs
- venue open/closed/maintenance status;
- official holiday/half-day calendar;
- known cash/futures/options/benchmark windows;
- business/settlement-day availability;
- participant-centre overlap from official hours/timezones;
- documented auction/fixing/settlement phases.

## Not timing authority
Intraday chart volatility, candle size, support/resistance, momentum, volume profile or price trend cannot be used to label a timing window favorable/unfavorable. Execution-cost telemetry may be monitored by a separate execution-risk layer, not used here to create directional timing edge.

## Session caution
`London`, `New York`, `Tokyo`, `cash open`, `power hour` and similar labels have no intrinsic bullish/bearish sign. Session phase matters only because participant/information/benchmark obligations change.

## Participant control confidence
Participant-control claims must be marked `DIRECT`, `STRUCTURAL_INFERENCE`, or `UNAVAILABLE`. A structural inference can trigger `EARLY_REVIEW` but should not by itself create a hard veto unless the actual market/venue availability is impaired.
