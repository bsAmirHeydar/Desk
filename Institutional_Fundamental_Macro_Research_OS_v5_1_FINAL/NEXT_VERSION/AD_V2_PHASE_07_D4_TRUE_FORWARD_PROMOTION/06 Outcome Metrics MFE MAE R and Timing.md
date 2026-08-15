# Outcome metrics

P07 uses existing D4-compatible outcome concepts:
- `MFE_R`
- `MAE_R`
- `realized_R` when a trade exists;
- `time_to_trigger_seconds`;
- `time_to_mfe_seconds`;
- expiry/no-trigger state.

For shadow states with no trade, MFE/MAE may still be measured against a predeclared reference execution profile or counterfactual profile. Such records must be labeled counterfactual and cannot be presented as realized trading P&L.

Core research questions include:
- does HIGH_READINESS precede larger favorable excursion than WATCH?
- does MATURE/EXHAUSTING opposing movement improve MFE/MAE asymmetry?
- does RELEASE occur before expansion rather than after it?
- is incremental value present beyond Pressure alone?
