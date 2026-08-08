# Forward Calibration and Reference-Class Engine

V16 calibrates **frozen outputs**, not hindsight narratives.

## Unit of calibration
A cohort key is composed from fields that existed at decision time: symbol/family, horizon, core direction, edge class, timing gate, dominant driver family, narrative family, regime label, evidence-quality band and execution profile version.

## Runtime states
- `COLD_START`: insufficient independent matured observations; no numeric probability is legal.
- `DEVELOPING`: descriptive outcome statistics may be shown with uncertainty; no automatic capital scaling.
- `ELIGIBLE_FOR_CALIBRATION`: configurable minimum independent sample, regime diversity and holdout requirements passed.
- `CALIBRATED_SHADOW`: probabilities/reference-class metrics produced but not yet allowed to change permission.
- `CALIBRATED_ENFORCED`: only after documented promotion and independent validation.

Default sample thresholds in config are conservative governance defaults, not universal scientific constants and may be changed only through a versioned policy update.

Metrics: net R, positive-R rate, MFE/MAE, time-to-trigger, time-to-MFE, state survival, expiry-without-trigger, realized cost and calibration interval. No performance metric may use unmatured horizons.

Use `tools/alphalab_calibrate.py`.
