---
title: "Daily and Intraday Timing Intelligence Workflow"
type: workflow
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Daily and Intraday Timing Intelligence Workflow

## Daily build — before first active session
1. Resolve date, DST and all relevant holiday calendars.
2. Compile official macro/central-bank/Treasury events.
3. Compile benchmarks/fixings and cash/futures/option clocks.
4. Check futures contract roll/expiry and index rebalance/reconstitution.
5. Check earnings/corporate events for material index constituents.
6. Determine month/quarter/year-end and fiscal/reporting states.
7. Build six-market clock graph and collisions.
8. Publish `dominant_clock`, expected transitions and preliminary validity boundaries.

## Intraday update
At each full run:
- re-fetch changed schedules/headlines;
- determine current session phase and participant centres;
- mature prior timing predictions only when their window has elapsed;
- re-rank clocks;
- update temporal forces and liquidity state;
- recompute `valid_until` and `next_review`;
- pass timing block to Module 92 Edge adjudication.

## Mandatory review triggers
next scheduled material event, session handoff, benchmark/fixing, cash open/close, expiry/settlement, rebalance implementation, material earnings release/call, temporal data failure, and unscheduled shock.

## Output discipline
Timing report must be concise enough to use operationally but deep enough to explain every veto/expiry. Full source detail remains available in the HTML/deep analysis.
