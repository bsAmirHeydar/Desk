# Immutable Forward Telemetry and Outcome Contract

Every live run creates a run record before outcome is known. Later outcome records append; they never rewrite the original state.

Required IDs: `run_id`, `analysis_id`, `permission_id`, `model_run_id`, `vault_commit`, `prompt_sha256`, `state_sha256`.

Execution telemetry, when available: permission publish time, bridge receipt time, EA read time, first Donchian trigger, entry, initial stop distance, spread/slippage, MFE, MAE, exit, realized R, expiry-without-trigger and data/broker incidents.

Outcome maturity is horizon-specific. A 2–5 day call cannot be scored after one hour.

Use `schemas/AlphaLab_Run_Record.schema.json`, `schemas/AlphaLab_Outcome_Record.schema.json`, and `tools/alphalab_append_ledger.py`.
