---
title: "USDJPY Timing Operating Book"
type: asset-specific-operating-book
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# USDJPY Timing Operating Book

## Core clocks
- Tokyo/Asia participation and Japanese banking calendar;
- London and New York handoffs;
- BoJ MPM/release sequence (`SRC-BOJ-CALENDAR`, `SRC-BOJ-MPM`);
- Fed/US macro calendar;
- WMR 4pm London benchmark (`SRC-LSEG-WMR`);
- quarter/year-end funding and cross-currency basis;
- CME JPY futures expiry/roll proxy (`SRC-CME-FX`);
- Japanese fiscal-year-end and corporate repatriation/hedging windows when supported by evidence.

## BoJ timing
Official decision release times can be listed as undecided. Preserve uncertainty instead of inventing a fixed clock. The Governor's press conference and later Summary of Opinions/minutes are separate stages.

## Intervention
Potential FX intervention is unscheduled unless officially communicated. If intervention risk is elevated, V15 tracks local liquidity/session state and official-source monitoring, but does not fabricate an intervention timestamp.

## Cross-centre issue
JPY liquidity and information leadership can shift materially between Tokyo and London/NY. Session handoff is therefore a first-class review trigger for USDJPY.
