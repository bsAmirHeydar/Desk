---
title: "Benchmark Scenarios and Acceptance Tests"
type: benchmark-standard
status: canonical
version: 10.4.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [benchmark, acceptance, historical]
---
# Benchmark Scenarios and Acceptance Tests

## Required tests

1. Quiet U.S. equity day with no major data: baseline, session reassessments and state decay must still exist.
2. CPI day: complete T-60 through T+60 windows without T0 contamination.
3. FOMC statement plus press conference: separate statement and press-conference state changes.
4. Trump or official social-media tariff headline: earliest verified timestamp, source uncertainty and unscheduled micro-windows.
5. Treasury auction/funding day: distinguish rates-led fundamental repricing from equity flow.
6. Mega-cap post-market earnings: post-market update and next-day carry-forward.
7. Gold safe-haven shock followed by liquidation: fundamental-to-flow transition.
8. EURUSD fixing/month-end day: proxy-labelled flow effect without inventing proprietary data.
9. Direction unchanged but catalyst consumed: mandatory no-change record.
10. Cross-asset confirmation break: confidence and edge downgrade without automatic sign change.
11. Missing intraday archive: explicit data-gap record and density pass-with-gap, not invented observation.
12. Weekend geopolitical event: conditional state until relevant market opens.

## Acceptance

A benchmark passes only if it satisfies point-in-time boundaries, mandatory coverage, score-reason documentation, micro-window completeness, state-decay tracking and honest data-availability labels.
