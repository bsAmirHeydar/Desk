# Immutable Forward Telemetry and Outcome Contract — V20 bridge

Every live run creates a frozen record before outcome is known. Later outcome records append; they never rewrite the original state.

V20 keeps Module 94 identifiers (`run_id`, `analysis_id`, `permission_id`, `model_run_id`, `vault_commit`, `prompt_sha256`, `state_sha256`) and extends them through Module 102 with D3 modifier IDs, promotion-registry version/hash, actual/counterfactual branches and hash-chained append-only records.

Execution telemetry still includes permission publish time, bridge receipt time, EA read time, first Donchian trigger, entry, initial stop distance, spread/slippage, MFE, MAE, exit, realized R, expiry-without-trigger and incidents when available.

Outcome maturity remains horizon-specific. Canonical D4 contract: [[102 Forward Validation Calibration Promotion and Scientific Governance Engine/03 Immutable Forward Observation Ledger]].
