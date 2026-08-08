# Calibration Uncertainty Stability and Promotion

Calibration remains SHADOW until evidence matures. V16.1 makes the reference class executable and aligned with the telemetry schema.

## Cohort key
`symbol × horizon × core_direction × edge_class × timing_gate × driver_family × narrative_family × regime_label × evidence_quality_band × execution_profile_version`

## Separate development and holdout
Training/development observations and pre-designated holdout observations are reported separately. Holdout may never be silently merged into training metrics.

## Required descriptive outputs
- N and independent root-event N;
- train/holdout mean and median R;
- train/holdout positive-R rate **descriptive only**;
- approximate descriptive interval for mean R;
- MFE/MAE;
- time-to-trigger and time-to-MFE;
- expiry-without-trigger rate;
- state-survival rate;
- cost R;
- per-regime metrics and sign consistency.

## Promotion logic
Sample floors in config are governance floors, not proof. Crossing a floor only makes a cohort eligible for calibration review. Promotion additionally requires documented stability review, holdout review, regime review, multiple-testing control where relevant, and independent validation. No numeric predictive probability is authorized by sample count alone.
