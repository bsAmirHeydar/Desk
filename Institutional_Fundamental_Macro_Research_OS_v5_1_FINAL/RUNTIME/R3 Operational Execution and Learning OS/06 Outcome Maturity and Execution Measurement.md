# Outcome Maturity and Execution Measurement

Outcome measurement is post-seal only. It consumes execution receipts and, when required, a declared price path. R3 computes or verifies realized R, MFE, MAE, costs and trigger timing according to the declared execution profile and D4 outcome horizon.

No-trigger and no-trade are separate states. Censored/untriggered cases are not silently treated as zero-return trades. Complex partial/multi-leg executions require a complete execution receipt; R3 returns UNSCORABLE rather than approximate.

Outcome artifacts live only in R1 OUTCOME world and cannot modify the sealed decision.
