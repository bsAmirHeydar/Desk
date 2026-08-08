---
title: "Six-Market Fact Coverage Foundation"
type: canonical-science-note
status: canonical
version: 17.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [v17, coverage, six-market, production]
---

# Production universe

D1 coverage governance is exact for:

`XAUUSD, NASDAQ100, SP500, DJIA, EURUSD, USDJPY`

Crude oil remains outside the current production profile.

## Coverage states

Each market × fact-family cell declares one of:

- `ACTIVE_CANONICAL` — existing validated science uses this family now;
- `ACTIVE_LIMITED` — usable but known to have public/licensing/proxy limitations;
- `REGISTERED_D2_PENDING` — explicitly registered but not a new D1 decision authority;
- `NOT_APPLICABLE` — only where structurally inapplicable;
- `UNAVAILABLE` — required target exists but is not available in the current evidence route.

## Coverage receipt rule

A live run may not merely say “data checked.” It must state which family was requested, source tier actually used, cutoff, direct/proxy status, unresolved gaps, and whether the gap was decision-critical.
