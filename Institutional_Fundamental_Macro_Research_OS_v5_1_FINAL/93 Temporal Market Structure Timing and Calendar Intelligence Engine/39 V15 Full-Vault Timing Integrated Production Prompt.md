---
title: "39 V15 Full-Vault Timing Integrated Production Prompt"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
---
# V15 Full-Vault Timing-Integrated Production Prompt

For every six-market Full-Vault run, execute V11 force science, V12 narrative science, V13 asset routing and **V15 temporal intelligence before Module 92 Edge adjudication**.

Mandatory timing pass: resolve current timezone/DST/business-day state; sessions and participant handoffs; macro/central-bank/Treasury clocks; benchmark/fixing windows; cash auctions; futures settlement/roll/expiry; options exact series/AM-PM/0DTE state; index rebalance/reconstitution; earnings/corporate clocks; month/quarter/year-end; holidays/half-days; settlement/funding constraints; temporal-force collisions.

Return `temporal_state`, dominant/competing clocks, timing action (`NO_CHANGE`, `SHORTEN_VALIDITY`, `EARLY_REVIEW`, `VETO_NEW_ENTRY`, `TEMPORAL_FORCE_OVERLAY`, `FRAGMENTED`), true-veto flag, `valid_until`, `next_review`, missing data and sources.

Timing cannot derive direction from technical price analysis.

If timing causes EDGE_CONDITIONAL, the HTML must explicitly say why it is not Active, exact clock/mechanism, veto vs constraint, expiry and upgrade/downgrade conditions.

Permission remains BUY/SELL/NO_TRADE. Entry remains M1 Donchian-20; initial stop 4 ATR; exit candle-close trailing. Timing governs new-entry validity, not discretionary chart location or open-position exit.
