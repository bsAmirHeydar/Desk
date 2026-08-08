# Instrument and Economic Exposure Normalization

A position must identify both **legal instrument** and **economic exposure**.

Required dimensions:
- underlying / benchmark
- venue and contract
- cash/future/option/swap/fund/share/physical
- gross and net units when available
- delta-equivalent only when derivation is explicit
- notional currency
- maturity/expiry/tenor
- participant taxonomy
- reference time and publication time

Never add raw contracts, shares and OTC notionals as if they were homogeneous. Cross-instrument aggregation is a `DERIVED_FACT` and must preserve parent lineage and normalization method.
