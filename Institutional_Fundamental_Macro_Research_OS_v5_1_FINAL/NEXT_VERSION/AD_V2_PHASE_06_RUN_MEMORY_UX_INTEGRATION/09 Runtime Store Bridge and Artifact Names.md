# Runtime Store Bridge

Optional run-store attachment uses only `META/OUTCOME` artifacts:
- `v2_gold_run_state`
- `v2_run_capsule_extension`
- `v2_change_set`
- `v2_portable_memory`
- `v2_report_model`

The bridge is idempotent when identical content is already registered. If the run is close-sealed, it returns a non-destructive `SKIPPED_CLOSE_SEALED` receipt.

It never writes to Decision world.
