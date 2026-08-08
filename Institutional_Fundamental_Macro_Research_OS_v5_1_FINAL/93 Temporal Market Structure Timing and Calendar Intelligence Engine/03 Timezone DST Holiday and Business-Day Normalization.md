---
title: "03 Timezone DST Holiday and Business-Day Normalization"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
---
# Timezone, DST, Holiday and Business-Day Normalization

Every material timestamp must store original local time, IANA timezone, UTC, and report-timezone representation. Never represent London/New York events with a permanent UTC offset.

Explicitly detect **DST mismatch weeks** when US and Europe/UK move clocks on different dates. Recompute overlaps in UTC and Asia/Tehran.

Maintain separate calendars for venue trading, banking/payment systems, benchmark administrators, futures exchanges, central banks and index providers.

Distinguish: `calendar_date`, `trade_date`, `business_day`, `settlement_day`, `value_date`, `benchmark_day`, `policy_day`. A futures session can begin on the prior civil evening while carrying the next trade date.

Half-days are independent temporal regimes because cash close, auctions, options cutoffs and futures/cash overlap change.
