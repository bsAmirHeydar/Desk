---
title: "37 Daily Intraday and Specialized Timing Workflows"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
---
# Daily, Intraday and Specialized Timing Workflows

Daily build: resolve date/DST/holidays; compile macro/central-bank/Treasury; compile benchmarks/fixings and cash/futures/options clocks; check roll/expiry and index maintenance; material earnings; month/quarter/year-end; construct global clock graph; publish preliminary validity boundaries.

Intraday run: refresh changed schedules/headlines; determine session phase; mature prior timing predictions only when elapsed; rerank clocks; update temporal forces/liquidity; recompute `valid_until` and `next_review`; pass to Edge engine.

Specialized workflows: high-impact event micro-grid, month-end WMR, quarter-end funding, futures roll/expiry, options AM/PM expiry, index rebalance, earnings multi-stage discovery.
