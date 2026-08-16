# 05 — Precision, Scores and Model Completeness

V2 explicitly labels its 0–100 pressure scale ordinal rather than probabilistic. P01 goes further for V3: user-facing numeric strength, confidence, consumption and persistence scores are forbidden until a specific estimand has true-forward/out-of-sample calibration.

Before calibration V3 uses interpretable states such as `LOW`, `MEDIUM`, `HIGH`, `CONTESTED`, `PARTIAL`, and disclosed uncertainty/coverage.

Price disagreement is also reinterpreted scientifically. It does not vote against Pressure. It is evidence that one of three things may be true:

1. a known opposing channel is dominating;
2. mechanical/funding/physical transmission is temporarily adverse;
3. the model is incomplete or a driver is missing.

Therefore V3 carries explicit `MODEL_COMPLETENESS_STATE` and `MISSING_DRIVER_RISK` objects.
