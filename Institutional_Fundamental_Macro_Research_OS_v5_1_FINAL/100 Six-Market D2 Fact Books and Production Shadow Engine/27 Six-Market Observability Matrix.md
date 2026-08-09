# Six-Market Observability Matrix

V21.3 adds a 6 × 16 machine-readable matrix in `config/six_market_observability_map.json`.

## XAUUSD
Highest residual value: physical/OTC/location state, ETF flows, COMEX stocks/deliveries, London vault/clearing/trade activity, USD funding, options/convexity and execution capacity. Comprehensive OTC client flow remains private/licensed.

## NASDAQ100
Highest residual value: options/0DTE/convexity, Treasury auction/dealer balance sheet, TRACE credit, QQQ/passive/auction flow, mega-cap earnings/revision breadth, securities-lending crowding and NQ depth/cost-to-trade.

## SP500
Highest residual value: SPX options/0DTE, credit, buybacks/issuance, SPY/passive and closing-auction flow, dealer/funding capacity, breadth/earnings and ES capacity.

## DJIA
Highest residual value: constituent/cyclical earnings, price-weighted concentration, NYSE auction imbalances, corporate capital allocation, dealer/funding state and YM/DIA execution capacity.

## EURUSD
Highest residual value: bilateral policy/funding, public FX/rates SDR transactions, cross-currency funding/basis, options path and explicit private-spot-flow gap. Futures/TIC/SDR subsets are never labelled global spot flow.

## USDJPY
Same FX discipline plus BoJ/MOF intervention/operation clocks, carry/funding differential and official-intervention facts. Private spot client/dealer flow remains an explicit gap.


## Flexible runtime materiality

The six-market map is the **baseline materiality prior**, not an inflexible verdict. A run may raise or lower a family's runtime materiality when context warrants it, but the receipt must preserve `baseline_materiality`, state `runtime_materiality`, and give a `materiality_reason`. A downgrade never permits a family to disappear silently; the item remains receipted as `NOT_MATERIAL`. This keeps the system flexible without making coverage discretionary or unauditable.
