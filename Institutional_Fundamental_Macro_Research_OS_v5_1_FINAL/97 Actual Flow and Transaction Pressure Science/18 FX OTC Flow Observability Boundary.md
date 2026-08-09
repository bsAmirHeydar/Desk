# FX OTC Flow Observability Boundary

## Reality
Comprehensive live spot-FX dealer/client flow is not public. V21.3 therefore maximizes public partial observability without pretending that futures, TIC, SDR derivatives or price action are the global EURUSD/USDJPY flow book.

## Public/direct subsets
- public SDR derivatives transactions;
- official intervention disclosures;
- official cross-border/statistical flows with their publication lag;
- regulated futures activity/positioning as a listed subset.

## Private/licensed layer
Dealer/client spot flow, corporate hedging, real-money execution, internalization and some options/LP liquidity require admissible licensed data.

## Production rule
If private spot flow is unavailable, output `PARTIAL_DIRECT`/`LICENSED_REQUIRED` in the observability receipt. Never fill the missing layer with a proxy and label it direct.
