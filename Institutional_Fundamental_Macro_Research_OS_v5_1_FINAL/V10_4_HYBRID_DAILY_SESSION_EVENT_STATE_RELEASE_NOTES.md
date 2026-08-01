---
title: "V10.4 Hybrid Daily Session Event State Release Notes"
type: release-notes
status: final
version: 10.4.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [release, hybrid-state, historical-reconstruction]
---
# V10.4 Hybrid Daily Session Event State Release Notes

V10.4 replaces sparse event-only historical recording with mandatory daily baselines, session handoffs, event micro-windows, state-decay/no-change reassessments, cross-asset confirmation, end-of-day attribution and density validation.

## Main changes

- 25 record types;
- adaptive lower materiality thresholds;
- fast/medium/slow driver stacks for Nasdaq 100, S&P 500, Gold and EURUSD;
- four-market 100-day production prompt;
- machine-readable schema;
- output package contract;
- daily/session density validator;
- no-lookahead immutable-state audit;
- canonical precedence over prior event-only behavior.
