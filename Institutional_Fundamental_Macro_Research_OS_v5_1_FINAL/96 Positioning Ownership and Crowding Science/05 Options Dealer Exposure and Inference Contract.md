# Options / Dealer Exposure Contract

Separate layers:
1. observed option chain / trades / OI where sourced;
2. contract greeks calculated from declared model and inputs;
3. assumed customer/dealer side assignment;
4. derived aggregate gamma/vanna/charm exposure;
5. behavioral inference about hedging pressure.

Only layer 1 can be direct market data. Layers 2–5 are derived/inferred unless a source directly identifies the relevant inventory/counterparty.

A dealer-gamma estimate therefore carries model lineage, sign-assumption lineage, timestamp, expiry scope and sensitivity to alternative assumptions.
