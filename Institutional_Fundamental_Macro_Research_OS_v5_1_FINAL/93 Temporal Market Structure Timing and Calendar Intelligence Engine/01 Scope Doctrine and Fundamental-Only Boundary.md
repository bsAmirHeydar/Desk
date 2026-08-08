---
title: "Scope Doctrine and Fundamental-Only Boundary"
type: canonical-methodology
status: canonical
version: 15.1.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, boundary, no-technical-analysis]
---
# Scope Doctrine and Fundamental-Only Boundary

## What Timing is
Temporal intelligence studies **observable institutional clocks** that change the information set, participant availability, benchmark obligation, settlement/funding constraint, contract lifecycle or mechanical-flow environment. It asks only:
1. what material clock is active or approaching;
2. what real mechanism that clock can create;
3. whether the current core Edge has enough safe time to be expressed;
4. whether the next transition requires expiry, hold, veto or early review.

## What Timing is not
Timing is not a technical entry model and is not permitted to infer bullish/bearish direction from price behavior. It cannot use moving-average alignment, support/resistance, candles, RSI/MACD, chart momentum, ICT/FVG/order blocks, trend geometry, market-profile shapes or price-only day-of-week patterns to clear or reject a thesis.

## Strict separation of objects
- `CLOCK_FACT`: verifiable time/calendar/venue fact.
- `TEMPORAL_MECHANISM`: institutional mechanism linked to that clock.
- `TEMPORAL_ACTIVATION`: whether that mechanism is relevant now.
- `TEMPORAL_CLEARANCE`: whether the pre-existing core Edge is executable through the safe window.
- `TEMPORAL_FORCE`: sourced non-price mechanical/funding/benchmark flow; direction may be `UNDETERMINED`.

A clock fact never becomes a directional force merely because a market historically moved around that time.

## Permitted non-price evidence
Official calendars, rulebooks, benchmark methodologies, auction timetables, settlement specifications, exchange hours, public index implementation notices, public corporate-event schedules, government issuance calendars, clearing/holiday calendars, officially communicated policy-event timing and independently sourced institutional flow obligations.

## Price boundary
Real-time price/volume patterns are not required for V15.1 clearance. Price may be used by other Vault modules for valuation, causal-response adjudication or forward outcome review. The Timing gate remains valid without a chart.

## Directional mechanical force
A temporary timing-linked directional force may be recorded only if its sign is independently supported by a documented obligation or credible non-price flow evidence. `MONTH_END`, `FRIDAY`, `EXPIRY`, `LONDON_OPEN`, `CASH_OPEN` or `QUARTER_END` by themselves have no directional sign.

## Default
When a clock exists but its mechanism/sign/materiality is not established, classify it as `CLOCK_PRESENT_NOT_DECISIVE`, not as a veto and not as a directional force.
