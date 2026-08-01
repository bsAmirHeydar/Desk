---
title: "Density Coverage and Gap Validation Standard"
type: validation-standard
status: canonical
version: 10.4.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [density, coverage, validator, gap]
---
# Density Coverage and Gap Validation Standard

## Required metrics

Validate per market and trading day:

- daily baseline coverage;
- overnight update coverage;
- session-handoff coverage;
- post-open, midday and afternoon reassessment coverage;
- end-of-day coverage;
- maximum gap between completed observations;
- event micro-window completion;
- state-decay update completion;
- no-change reassessment count;
- record count by market, day, session and type;
- percentage of proxy, unavailable and insufficient-evidence fields.

## Default density gates

### Nasdaq 100 and S&P 500

- minimum six records per regular U.S. trading day before event additions;
- maximum 120-minute gap during 09:30–16:00 New York;
- required pre-open, post-open, midday, afternoon and close records.

### Gold

- minimum six global-session records per active weekday;
- Asia, London and New York handoffs required;
- maximum 180-minute gap during London/New York active windows.

### EURUSD

- minimum six records per active weekday;
- Asia, London, pre-New-York, overlap/fixing and end-of-day coverage;
- maximum 180-minute gap during London/New York active windows.

## Event gates

For every high-impact scheduled event with reliable data, require T-60, T-15, T0, T+5, T+15, T+30 and T+60 or an explicit missing-window reason.

## Valid no-change coverage

A day with unchanged direction still requires reassessment records. The validator should flag long sequences containing only repeated identical records with no updated freshness, absorption, confirmation, remaining pressure or next-catalyst fields.

## Pass classes

- `PASS_STRICT`: all required records present and no unexplained gap;
- `PASS_WITH_DOCUMENTED_DATA_GAPS`: missing items have explicit point-in-time data limitations;
- `FAIL_DENSITY`: insufficient daily/session coverage;
- `FAIL_MICRO_WINDOWS`: event windows incomplete;
- `FAIL_LOOKAHEAD`: any temporal contamination;
- `FAIL_STATE_DECAY`: stale states carried without reassessment.
