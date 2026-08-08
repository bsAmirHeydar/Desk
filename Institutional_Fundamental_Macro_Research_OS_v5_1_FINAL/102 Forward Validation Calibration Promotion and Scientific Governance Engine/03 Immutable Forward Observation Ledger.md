# Immutable Forward Observation Ledger

D4 uses a hash-chained JSONL ledger. Each record contains `previous_record_hash` and `record_hash`. The canonical hash is computed over the record payload excluding `record_hash` itself.

## Record classes
- `FORWARD_OBSERVATION`
- `OUTCOME`
- `COUNTERFACTUAL_OUTCOME`
- `CALIBRATION_REPORT`
- `PROMOTION_PROPOSAL`
- `VALIDATOR_DECISION`
- `REGISTRY_CHANGE`
- `DRIFT_ALERT`
- `RETIREMENT_RECORD`

The ledger is append-only. Correction is represented by a new record that references the superseded record; deletion/rewrite is forbidden.

Runtime ledgers should live outside the Git-controlled Vault or in a deliberately excluded runtime store. The Vault contains schemas, policies and tools—not mutable production outcomes.
