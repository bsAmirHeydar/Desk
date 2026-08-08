---
title: "Treasury Auction Fiscal and Government-Funding Clock"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Treasury Auction, Fiscal and Government-Funding Clock

US Treasury supply can alter rates, term premium, dealer balance-sheet usage and therefore transmit to USD, gold and equity valuations.

## Auction lifecycle
`TENTATIVE_SCHEDULE -> ANNOUNCEMENT -> WHEN_ISSUED_TRADING -> AUCTION -> RESULTS -> SETTLEMENT/ISSUE -> POST_AUCTION_POSITIONING`.

Use TreasuryDirect official schedules and announcements (`SRC-TREASURY-AUCTIONS`). Holidays, funding needs and debt-limit developments can alter patterns; do not hard-code a static auction calendar.

## Required fields
security type, tenor, new issue/reopening, announcement time, auction time, issue/settlement date, size, indirect/direct/dealer metrics when officially released, contemporaneous rate-market context, and affected V11 force channels.

## Timing relevance
The same auction is not equally important to every asset. Large duration supply is more relevant to real/nominal yields and rate-sensitive indices; bill supply can matter through liquidity/funding channels. The engine never labels an auction bullish or bearish before analyzing its actual causal setup.

## Fiscal clock
Track refunding announcements, debt-limit deadlines, major tax-payment dates and government cash-balance dynamics as separate temporal mechanisms when they are materially active and supported by official data.
