# Continuous-forward operational state machine

Each P08 cycle is intentionally ordered:

1. `DISCOVER_P06_RUNS`
2. `FREEZE_ELIGIBLE_COMMITMENTS`
3. `SEAL_P08_OPERATING_BINDINGS`
4. **only after all freeze decisions are complete:** `READ_FUTURE_OBSERVATIONS`
5. `MATURE_ELIGIBLE_OUTCOMES`
6. `CALIBRATE`
7. `EVALUATE_PROMOTION_ELIGIBILITY`
8. `WRITE_CYCLE_RECEIPT`

The freeze phase is prohibited from reading the observation store. This prevents future market information from influencing whether a run is admitted as TRUE_FORWARD.
