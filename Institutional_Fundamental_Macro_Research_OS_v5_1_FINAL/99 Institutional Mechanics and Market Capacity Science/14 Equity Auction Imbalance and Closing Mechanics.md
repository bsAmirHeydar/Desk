# Equity Auction Imbalance and Closing Mechanics

## Observable mechanics
Nasdaq NOII and NYSE-group imbalance feeds can expose paired quantity, imbalance direction/size and indicative-clearing information before opening/closing auctions.

## Core distinction
`INDICATIVE IMBALANCE != REALIZED CROSS FLOW`.

Before the auction, imbalance is an executable-mechanics state. After the cross, realized volume/price is a transaction fact. For index-level inference, constituent values must be aggregated using point-in-time membership/weights and venue coverage.

## High-value windows
Open, close, month/quarter end, index rebalance/reconstitution and large passive events. Outside these windows this family may be `NOT_MATERIAL`.
