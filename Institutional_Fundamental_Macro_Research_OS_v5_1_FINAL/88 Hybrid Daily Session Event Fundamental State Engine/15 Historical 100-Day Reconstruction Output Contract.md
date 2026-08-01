---
title: "Historical 100-Day Reconstruction Output Contract"
type: output-contract
status: canonical
version: 10.4.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [historical, csv, output, backtest]
---
# Historical 100-Day Reconstruction Output Contract

## Required package

Create one folder and ZIP containing:

- `MASTER_HYBRID_STATE_TIMELINE.csv`
- `NASDAQ100_HYBRID_STATE.csv`
- `SP500_HYBRID_STATE.csv`
- `GOLD_HYBRID_STATE.csv`
- `EURUSD_HYBRID_STATE.csv`
- `CROSS_ASSET_CONFIRMATION_MATRIX.csv`
- `EVENT_MICRO_WINDOWS.csv`
- `DAILY_COVERAGE_LEDGER.csv`
- `SESSION_COVERAGE_LEDGER.csv`
- `STATE_DECAY_LEDGER.csv`
- `EVIDENCE_LEDGER.csv`
- `NO_LOOKAHEAD_AUDIT.md`
- `METHODOLOGY_AND_SCORING.md`
- `DENSITY_VALIDATION_REPORT.md`
- `PERSIAN_INSTITUTIONAL_SUMMARY.md`
- `RUN_MANIFEST.json`

## Timeline rule

The master timeline contains mandatory baseline and session records plus event-driven records. It is not a fixed hourly bar dataset and it is not event-only. Fixed checkpoints guarantee observability; additional events capture meaningful changes.

## Initial and terminal states

The window begins with `INITIAL_WINDOW_STATE` for all four markets. Every open day contains `DAILY_BASELINE` and `END_OF_DAY_STATE`. The final record states whether a catalyst or thesis remains active beyond the window without using future information.

## Practical fields

Every market file includes direction, intensity, confidence, freshness, absorption, repricing completion, flow exhaustion, narrative saturation, remaining pressure, confirmation, persistence, reversal risk, edge availability, dominant driver, rival model and next update trigger.
