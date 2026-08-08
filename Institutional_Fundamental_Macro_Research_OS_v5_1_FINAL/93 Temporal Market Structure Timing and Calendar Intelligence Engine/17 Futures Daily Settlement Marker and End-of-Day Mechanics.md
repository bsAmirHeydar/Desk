---
title: "Futures Daily Settlement Marker and End-of-Day Mechanics"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Futures Daily Settlement Marker and End-of-Day Mechanics

Daily settlement is an accounting/risk-transfer clock, not necessarily the same as the cash close or final contract expiry.

CME equity-index products use defined settlement/fixing windows; Micro E-mini daily settlement references the E-mini counterpart and CME publishes product-specific procedures (`SRC-CME-EQ-HOURS`). TMAC also references the US market close (`SRC-CME-TMAC`).

## Engine duties
For each futures proxy used in Alpha Lab store:
- venue and contract;
- maintenance breaks;
- daily settlement calculation window;
- cash close relationship;
- trade date rollover;
- last trade/final settlement distinction;
- holiday modifications.

## Why it matters
Margin, P&L recognition, benchmark orders and risk books may reference settlement marks. Activity around a settlement marker can temporarily increase mechanical trading. V15 labels this `SETTLEMENT_MARKER_FLOW` and estimates whether it matters for the target spot/CFD/index expression.

## No universal clock
CME product families differ. Never copy ES settlement logic to gold or FX futures without product-specific verification.
