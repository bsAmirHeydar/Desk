# Run Lifecycle and State Machine

Canonical states:

```text
REQUESTED
→ INPUTS_RESOLVED
→ SNAPSHOT_FROZEN
→ EVIDENCE_FROZEN
→ COGNITION_FROZEN
→ DECISION_FROZEN
→ PERMISSION_ISSUED
→ EXECUTION_PENDING
→ EXECUTED | NO_TRIGGER | NO_TRADE
→ OUTCOME_MATURED
→ COUNTERFACTUALS_ATTACHED
→ D4_CALIBRATED
→ CLOSED
```

Exceptional terminal/intermediate states:

- `FAILED`
- `ABORTED`

R1 enforces legal transitions and records every transition as an append-only run event. Later runtimes may skip execution-specific states for research-only runs, but they may not bypass `DECISION_FROZEN` before accessing Outcome World.

## Manifest history

The current run manifest is a convenience pointer. Each mutation creates an immutable manifest-history record with monotonic revision number. The scientific freeze is represented by seals, not by trusting a mutable current manifest.
