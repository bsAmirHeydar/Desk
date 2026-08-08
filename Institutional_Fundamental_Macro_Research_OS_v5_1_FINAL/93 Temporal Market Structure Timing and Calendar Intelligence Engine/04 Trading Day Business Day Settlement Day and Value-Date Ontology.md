---
title: "Trading Day Business Day Settlement Day and Value-Date Ontology"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Trading Day, Business Day, Settlement Day and Value-Date Ontology

“Today” is not one object in global markets.

- `TRADING_DAY`: the exchange/venue trade date; futures often begin the prior civil evening.
- `BUSINESS_DAY`: day on which the relevant jurisdiction/banking system operates.
- `SETTLEMENT_DAY`: day on which cash/securities obligations can settle.
- `VALUE_DATE`: FX/OTC contractual value date, requiring both currency calendars.
- `BENCHMARK_DAY`: day a benchmark is calculated/published.
- `POLICY_DAY`: day a central-bank or government event occurs.

## Why this matters
A futures session opening Sunday evening can carry Monday’s trade date. A US equity holiday can coexist with open foreign markets. FX value dates move around holidays in either currency. Benchmark and settlement calendars can diverge from trading calendars.

## Engine rule
Every event object must specify which calendar it belongs to. Do not infer settlement availability from venue-open status. For bilateral FX, resolve both currency business calendars before computing value-date or roll-related effects. For futures, distinguish trade date from civil date. For index products, distinguish last trading date from final settlement calculation date.

## State fields
`trade_date`, `calendar_date`, `business_day_flags`, `settlement_eligible`, `benchmark_eligible`, `value_date`, `next_rollover_boundary`, and `calendar_conflicts[]`.
