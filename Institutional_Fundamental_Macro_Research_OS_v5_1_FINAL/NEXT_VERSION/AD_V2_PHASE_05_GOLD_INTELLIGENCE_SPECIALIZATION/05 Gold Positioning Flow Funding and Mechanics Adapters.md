# Gold Positioning, Flow, Funding and Mechanics Adapters

## Positioning

- CFTC precious-metals categories: public regulated positioning subset; weekly and lagged.
- ETF holdings: product/vehicle ownership subset.
- options-derived positioning: inference unless counterparty mapping is direct.
- official-sector holdings: structural state, not a live trading tape.

## Actual flow

- CME trades/MBO/depth: listed futures/options transaction and liquidity evidence where subscribed.
- ETF creations/redemptions or holdings change: investment-flow subset with product-specific decomposition.
- LBMA trade data: London OTC aggregate subset, access-dependent.
- physical/official flow: only when directly reported.

`Volume != Flow`; `OI != directional Flow`; `price change != Flow`.

## Funding

USD funding, repo/dealer balance sheet, futures margin/collateral and sourced gold lease/basis/physical financing may change transmission. Public coverage is incomplete.

## Mechanics

- CME expiry/roll/settlement and listed-market depth;
- benchmark/fixing windows;
- ETF basket/creation mechanics;
- Treasury auction and macro-event clocks;
- options expiry/convexity when directly or defensibly modeled.

Expected mechanical demand is not realized flow.
