---
title: "Open Close Auction Imbalance and Price-Discovery Clocks"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Open, Close, Auction, Imbalance and Price-Discovery Clocks

Opening and closing auctions are institutional concentration points. Nasdaq disseminates opening imbalance information beginning before the 09:30 ET Opening Cross and closing imbalance information from 15:50 ET before the Closing Cross (`SRC-NASDAQ-CROSS`). NYSE likewise defines opening/closing auctions and imbalance periods (`SRC-NYSE-HOURS`).

## Opening clock
Before the cash open, futures and premarket markets carry price discovery. The open introduces the full constituent universe, market-on-open orders and overnight inventory clearing. V15 classifies the open as an **information/participation reset**, not a bullish/bearish signal.

## Closing clock
The close concentrates benchmarked execution, index/passive orders, mutual-fund/ETF flows and auction imbalances. A directional move into the close can therefore be `FUNDAMENTAL_CONTINUATION`, `BENCHMARK_MECHANICAL`, `DE_RISKING`, or `UNDETERMINED`.

## Required fields
`auction_type`, `imbalance_publication_start`, `freeze_period`, `cross_time`, `eligible_venues`, `known_rebalance_overlap`, `expected_flow_class`, `source`.

## Rule
If mechanical closing flow is likely to dominate the remaining lifespan of a trade, Timing may shorten `valid_until` or mark `MECHANICAL_FLOW_DOMINANT`; it does not reverse the underlying thesis by itself.
