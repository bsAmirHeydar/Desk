---
title: "Settlement Payment-System Funding Cutoffs and Market Plumbing Time"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Settlement, Payment-System, Funding Cutoffs and Market-Plumbing Time

Institutional markets are constrained by the clocks of cash and collateral movement.

## Objects
- securities settlement cycle and clearing cutoffs;
- currency value dates and banking holidays;
- central securities depository/custodian cutoffs where relevant;
- payment-system availability;
- margin calls and intraday liquidity deadlines;
- collateral substitution/optimization windows;
- futures clearing and settlement cycles;
- TARGET/Japan/US banking calendar availability.

## Why it matters
As cutoffs approach, institutions may become less willing to carry unsettled exposures or may need cash/collateral in a specific currency. These pressures can appear as funding/liquidity forces rather than new macro information.

## Institutional caution
Many exact cutoff datasets are proprietary or institution-specific. The Vault stores the science and source contracts; live production must not fabricate universal deadlines.

## Output
`settlement_clock_state`, `funding_cutoff_risk`, `collateral_clock`, `currency_calendar_conflict`, `data_coverage`, `next_settlement_transition`.
