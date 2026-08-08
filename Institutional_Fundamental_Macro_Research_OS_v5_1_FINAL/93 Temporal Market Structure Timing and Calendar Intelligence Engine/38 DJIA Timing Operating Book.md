---
title: "DJIA Timing Operating Book"
type: asset-specific-operating-book
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# DJIA Timing Operating Book

## Core clocks
- YM/MYM futures session, daily settlement and quarterly expiry (`SRC-CME-EQ-HOURS` family);
- US cash opening/closing auctions;
- DJX/DIA option expiry and product-specific cutoff (`SRC-CBOE-DJX`, `SRC-OCC-INDEX`);
- DJIA constituent change announcements under S&P DJI governance (`SRC-DJIA`, `SRC-SPDJI-METHOD`);
- earnings of high-price constituents;
- US macro/Fed/Treasury clocks;
- month/quarter-end benchmark flows.

## Price-weighted timing consequence
DJIA is price weighted. A corporate event in a high-priced constituent can have disproportionate index impact. Timing therefore combines event time with **point-in-time price-weight influence**, while direction remains a fundamental/corporate analysis question.

## Constituent changes
DJIA has no simple periodic rebalancing frequency comparable with cap-weighted quarterly processes. Use official announcements and effective dates dynamically.

## Relative use
On rotation days, DJIA can diverge from NDX/SPX. Timing must identify whether divergence is caused by constituent earnings/price-weight mechanics, close flows, or genuine macro rotation before Module 92 classifies any relative Edge.
