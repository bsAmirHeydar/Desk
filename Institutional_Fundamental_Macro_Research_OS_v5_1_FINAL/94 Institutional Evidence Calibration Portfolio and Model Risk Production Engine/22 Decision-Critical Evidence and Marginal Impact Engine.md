# Decision-Critical Evidence and Marginal Impact Engine

Every load-bearing evidence node carries `decision_materiality` and `decision_role`.

`decision_role` is one of:
- `DIRECTION_ROOT`
- `TRANSMISSION_CONFIRMATION`
- `TIMING_CLEARANCE`
- `INVALIDATION`
- `CONTRADICTION`
- `CONTEXT`

## Dependency treatment
- Same-root descendants are transmission observations, never independent votes.
- `UNKNOWN_DEPENDENCY` never increases confidence.
- Decision-critical unknown dependency -> `HOLD` unless a logical/integrity failure requires `BLOCK`.
- Material-secondary unknown dependency -> `CLEAR_WITH_CONFIDENCE_CAP`.
- Contextual unknown dependency -> disclose only.

## Hard-block burden of proof
A hard evidence block requires one of:
1. lookahead or timestamp violation;
2. instrument/source identity failure that could change the claim;
3. corrupted/malformed evidence used by the decision;
4. unresolved decision-critical provenance/dependency where the alternative resolution can flip permission.

Missing premium/proprietary data is **not** a hard block by itself. Use a public proxy, cap confidence, or mark unavailable unless that data is genuinely decision-determinative.
