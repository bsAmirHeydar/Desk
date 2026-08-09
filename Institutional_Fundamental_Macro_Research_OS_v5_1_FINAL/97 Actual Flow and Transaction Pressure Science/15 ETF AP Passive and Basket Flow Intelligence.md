# ETF, Authorized Participant, Passive and Basket Flow Intelligence

## Core law
`AUM CHANGE != NET SUBSCRIPTION/REDEMPTION != AP ACTIVITY != UNDERLYING BASKET EXECUTION`

## Observable layers
- sponsor-published shares outstanding/holdings/creation-redemption information where available;
- regulatory fund holdings with filing lag;
- index rebalance/reconstitution announcements;
- opening/closing auction imbalance and realized cross data where available;
- ETF premium/discount and basket composition as mechanics/context.

## Decomposition
AUM change should be decomposed into market-price effect, FX effect, distributions/corporate actions, net shares/creations-redemptions and residual. Actual AP identity and internal execution are often private.

## Index application
QQQ/SPY/DIA/passive pressure is translated through point-in-time constituent weights. Expected rebalance demand remains `MODEL_INFERENCE` until an observed flow/auction transaction confirms it.
