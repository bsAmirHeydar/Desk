# Operational Risk Kill Switch

This layer is not Fundamental invalidation and does not reinterpret a thesis.

Hard incidents include:
- broker/API/feed disconnected or stale beyond policy;
- symbol/reference mapping unresolved;
- impossible/negative/non-finite prices or ATR inputs;
- spread/cost outside configured hard limit;
- market halt/closure inconsistent with execution state;
- permission expired or clock drift beyond tolerance;
- state/JSON checksum mismatch;
- duplicate order/position-state desynchronization;
- corrupted or unknown permission.

Actions: `CLEAR`, `BLOCK_NEW_ENTRY`, `FREEZE_AUTOMATION`, `SAFE_CLOSE_IF_EXECUTION_POLICY_REQUIRES`, `MANUAL_ESCALATION`.

Default is fail-closed for new entries. Open positions remain under their mechanical exit policy unless an explicitly configured operational emergency requires safe close.

Use `schemas/AlphaLab_Operational_Gate.schema.json` and `tools/alphalab_operational_gate.py`.
