---
title: "Temporal Ontology and Multi-Clock Stack"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Temporal Ontology and Multi-Clock Stack

A market is simultaneously governed by multiple clocks. V15 forbids reducing time to “London session” or “news time.”

## Clock hierarchy
### Micro clock — seconds to minutes
Auction freezes, imbalance publications, benchmark fixing windows, settlement markers, economic-release timestamps, option-expiry calculations, maintenance halts and abrupt information shocks.

### Session clock — minutes to hours
Asia/Tokyo, London/Europe and New York participation; futures-to-cash handoff; cash open discovery; midday participation decay; closing-auction concentration; after-hours earnings.

### Daily clock
Business-day conventions, value dates, same-day expiration, Treasury announcements/auctions, central-bank communication sequence, daily settlements and benchmark publication.

### Weekly clock
Weekly option expiries, recurring macro release days, Treasury bill cycles, weekend risk, long weekends and holiday-adjacent liquidity.

### Monthly clock
Month-end benchmark rebalancing, asset-manager hedge activity, month-end futures/options, index maintenance, economic-data clusters and accounting/portfolio reporting.

### Quarterly clock
Equity-index futures quarterly expiry, quarterly options, index reviews, earnings season, regulatory reporting, dealer/bank balance-sheet window dressing and funding-basis stress.

### Annual / fiscal clock
Year-end balance-sheet constraints, tax/fiscal year boundaries, annual index reconstitution, central-bank calendar reset and holiday clusters.

### Contract-lifecycle clock
Listing -> liquidity migration -> first/last trade -> notice/delivery -> final settlement. This clock can differ materially by instrument.

## Dominance
The engine must rank clocks by **causal relevance now**, not by proximity alone. A close benchmark in 20 minutes can dominate a low-impact release in five minutes. A quarter-end funding constraint can dominate an otherwise normal session clock. The output therefore includes a `dominant_clock`, runner-up clocks, collision score and transition sequence.
