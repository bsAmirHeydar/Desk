# Treasury Auction, Refunding and Settlement Microstructure

## Event clocks
`announcement -> when-issued trading -> auction -> result -> settlement -> investor-class allotment publication`.

Each clock has different information content and must remain point-in-time clean.

## Auction fact set
Security/tenor, new issue/reopening, amount, CUSIP, auction time, stop yield/rate, accepted bids, bid-to-cover and published bidder categories. Where a defensible when-issued reference exists, derive tail/stop-through explicitly with timestamp/source.

## Supply context
Quarterly refunding, bill-vs-coupon mix, maturity profile, buyback plans and settlement clusters matter to dealer/funding capacity. Gross issuance is not a universal liquidity-drain scalar.

## Investor-class allotments
Useful structural confirmation, but lagged. They must not rewrite the live auction interpretation retroactively.
