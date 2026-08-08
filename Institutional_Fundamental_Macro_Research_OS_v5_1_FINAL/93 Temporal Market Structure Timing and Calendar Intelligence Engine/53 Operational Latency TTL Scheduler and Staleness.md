---
title: "Operational Latency TTL Scheduler and Staleness"
type: canonical-operational-standard
status: canonical
version: 15.1.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, latency, ttl, scheduler]
---
# Operational Latency, TTL, Scheduler and Staleness

A temporally valid analysis can become unusable while it travels to execution. Operational time is part of V15.1.

## Required timestamps
- market/source cutoff;
- analysis start/completion;
- permission publication;
- transport receipt when available;
- MT5/bridge ingestion when available;
- `valid_until`;
- next required review.

## Rule
Transport/processing latency can consume the validity window but can never extend it. If a state expires before execution reads it, downstream permission is `NO_TRADE`.

## Scheduler feasibility
If `next_required_review` occurs before the platform can reliably run again, do not pretend monitoring is continuous. Choose one:
- expire permission before the review boundary and fail closed;
- external event trigger if actually available;
- `HOLD` if a safe interval cannot be maintained.

## Clock drift
Store UTC and source-local time, and detect material local clock/timezone conversion mismatch. Machine clock uncertainty around a critical event is a material data-quality failure.

## TTL
`valid_until` is an analytical expiry, not merely a JSON field. Missing, malformed, stale or expired permission remains `NO_TRADE` downstream.
