# Failure, Degradation and Recovery Semantics

R1 does not turn missing data into zero and does not turn runtime failure into a synthetic complete run.

## Core failure classes

- `INPUT_INVALID`
- `TIME_AMBIGUOUS`
- `SOURCE_MISSING`
- `VINTAGE_UNPROVEN`
- `ARTIFACT_HASH_MISMATCH`
- `ILLEGAL_STATE_TRANSITION`
- `OUTCOME_FIREWALL_VIOLATION`
- `DECISION_WORLD_MUTATION`
- `CATALOG_CONFLICT`
- `REPLAY_INCOMPLETE`
- `SCHEMA_INVALID`

## Flexible degradation

Scientific materiality remains external to R1. R1 reports exact evidence status so later reasoning can distinguish:

```text
PRESENT
UNAVAILABLE
UNDETERMINED
NOT_APPLICABLE
INVISIBLE_FUTURE
FORBIDDEN_VINTAGE
```

Runtime infrastructure is strict; interpretation of how a non-critical gap affects a trade remains context-sensitive in the scientific stack.

## Recovery

- Object writes are atomic.
- Catalog writes are transactional.
- Per-run writes use locks.
- Failed runs retain events and failure receipts.
- Recovery never rewrites a valid Decision Seal.
