# Flow Ontology and Identification Standard

Canonical flow types include:
- `CASH_SECURITY_FLOW`
- `FUTURES_TRANSACTION_FLOW`
- `OPTION_TRANSACTION_FLOW`
- `ETF_CREATION_REDEMPTION`
- `FUND_SUBSCRIPTION_REDEMPTION`
- `DEALER_HEDGE_FLOW`
- `SYSTEMATIC_REBALANCE_FLOW`
- `PASSIVE_INDEX_FLOW`
- `CORPORATE_BUYBACK_FLOW`
- `CORPORATE_ISSUANCE_FLOW`
- `FX_HEDGE_FLOW`
- `OFFICIAL_SECTOR_FLOW`
- `PHYSICAL_COMMODITY_FLOW`

Every flow record states `identified_actor`, `actor_confidence`, `signed_direction_method`, interval, instrument, units, notional, evidence class and root cause.
