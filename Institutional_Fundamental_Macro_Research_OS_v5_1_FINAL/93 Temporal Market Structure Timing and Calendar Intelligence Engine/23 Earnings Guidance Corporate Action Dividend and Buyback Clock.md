---
title: "Earnings Guidance Corporate Action Dividend and Buyback Clock"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Earnings, Guidance, Corporate Action, Dividend and Buyback Clock

For equity indices, corporate information arrives on a clock distinct from macro data.

## Earnings object
Store exact company IR release time when available, `BMO`, `AMC`, or intraday status, conference-call time, guidance update, index weight, sector, and whether the information is available before futures/cash sessions.

## Multi-stage earnings discovery
`EARNINGS_RELEASE -> GUIDANCE_PARSE -> CALL/PREPARED_REMARKS -> Q&A -> ANALYST_REVISION -> CASH_MARKET_ADOPTION`.
A headline beat can be displaced by guidance or call commentary; V15 therefore treats the call as a second information stage when material.

## Corporate actions
Track ex-dividend dates, special dividends, splits, mergers, spin-offs, tender deadlines and index-treatment effective dates. These can change index mechanics without changing macro fundamentals.

## Buybacks
Use disclosed authorization/blackout information only when reliable. Do not assume a universal blackout rule. Corporate bid availability is a contextual temporal factor, not a directional guarantee.

## Index integration
Weight the event by current point-in-time index exposure; a large NDX constituent's after-hours release can dominate next-session Nasdaq timing while being less material to DJIA.
