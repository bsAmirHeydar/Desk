# Securities Lending, Short Interest and Borrow Ecology

## Purpose
Complete the positioning/crowding layer with facts that are distinct from futures COT, options OI and modelled systematic positioning.

## Canonical distinctions
`SHORT_INTEREST != SHORT_SALE_VOLUME != SECURITIES_LOAN_ACTIVITY != BORROW_COST != NET_BEARISH_FLOW`

- **Short interest** is a lagged stock of reported short positions on a designated date.
- **Short-sale volume** is transaction activity and can reflect hedging/market-making as well as directional shorting.
- **Securities-lending activity** records loans/loan modifications; a loan is not itself a short sale.
- **Borrow fee/utilization/inventory** characterize scarcity/crowding and potential squeeze fragility; they do not prove future direction.

## Evidence hierarchy
1. identified/regulated short-position facts;
2. regulated securities-loan transaction statistics;
3. licensed borrow fee/utilization/inventory;
4. short-sale activity as contextual transaction evidence;
5. modelled squeeze/crowding inference.

## Point-in-time law
FINRA short-interest and SLATE data retain their official reporting/dissemination clocks. They cannot be backfilled into earlier intraday analysis. A stale short-interest snapshot may still be structural context but cannot be labelled current intraday positioning.

## Index use
For NASDAQ100/SP500/DJIA, constituent observations must be aggregated with current point-in-time index membership/weights and concentration-aware treatment. A squeeze in a tiny constituent is not an index-level squeeze signal.

## Decision boundary
This science may modify fragility/asymmetry only through Module 101. It never creates Fundamental Direction.
