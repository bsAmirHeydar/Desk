# Gold Source Freshness, Cadence and Observability

Gold contains mixed-frequency evidence. P05 forbids cadence laundering.

Examples:

- real-time market feed / CME MBO: seconds to minutes when licensed/available;
- exchange transaction/depth: intraday listed-market evidence only;
- CME volume/OI: product-specific/daily unless a real-time product explicitly supplies more;
- ETF sponsor/WGC ETF: product-specific daily/periodic investment subset;
- CFTC COT: weekly/lagged positioning;
- COMEX stocks/deliveries: daily listed/physical subset;
- LBMA clearing/vault: delayed/lagged, often monthly structural/location context;
- WGC Gold Demand Trends: structural/cyclical, not intraday;
- OTC/client/dealer flow: `LICENSED_REQUIRED`/`UNAVAILABLE` unless a named direct source exists.

A slow source may support structural persistence but cannot be promoted to a live release trigger.
