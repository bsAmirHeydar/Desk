# Gold Missing Driver Search and Escalation

When P03 reports material/decision-critical disagreement, P05 opens a Gold-specific search sequence rather than weakening Pressure from price.

Priority families:

1. **data / timestamp / instrument mismatch** — spot vs futures basis, stale quote, contract roll, FX/unit issue;
2. **rates / USD pathway** — 2Y, real yield, curve, policy repricing, autonomous USD shock;
3. **listed liquidation / flow** — CME trade/MBO/depth, volume/OI with correct non-equivalence;
4. **positioning** — CFTC/ETF/options/systematic unwind where observable;
5. **funding / collateral** — repo/dealer/margin/lease/basis stress;
6. **options/mechanics** — expiry, convexity, settlement, roll, benchmark effects;
7. **physical / ETF / official** — actual allocation, redemption, delivery/location imbalance;
8. **new macro/geopolitical event** — recompute P02 if causal;
9. **private/OTC gap** — preserve as unavailable rather than inventing a public proxy.

If a new causal driver is found, P05 requests `P02_RECOMPUTE_REQUIRED`. It never patches the frozen Pressure state locally.
