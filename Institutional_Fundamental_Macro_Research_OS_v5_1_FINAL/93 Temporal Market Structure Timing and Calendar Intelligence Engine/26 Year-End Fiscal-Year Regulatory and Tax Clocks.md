---
title: "Year-End Fiscal-Year Regulatory and Tax Clocks"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Year-End, Fiscal-Year, Regulatory and Tax Clocks

Calendar year-end, fiscal year-end and regulatory reporting dates can create distinct market states.

## Year-end mechanisms
- bank/dealer balance-sheet compression;
- funding and collateral scarcity;
- benchmark and portfolio rebalancing;
- tax-related realization/cash needs;
- corporate treasury year-end cash management;
- holiday-thinned staffing and liquidity;
- annual index reconstitution;
- central-bank/calendar publication transitions.

## Fiscal years
Do not assume every institution uses December. Japan's fiscal year-end and corporate calendars can matter for JPY flows; other jurisdictions have different reporting dates.

## Tax dates
Tax-payment deadlines can alter Treasury cash balances and private liquidity, but timing and materiality must be sourced dynamically. V15 does not hard-code directional tax effects.

## State
`YEAR_END_NORMAL`, `BALANCE_SHEET_CONSTRAINED`, `HOLIDAY_THIN`, `FISCAL_YEAR_END`, `TAX_CASH_FLOW_WINDOW`, `POST_YEAR_END_REOPENING`.

## Rule
Year-end is a prior for altered liquidity/flows, never an unconditional directional prediction.
