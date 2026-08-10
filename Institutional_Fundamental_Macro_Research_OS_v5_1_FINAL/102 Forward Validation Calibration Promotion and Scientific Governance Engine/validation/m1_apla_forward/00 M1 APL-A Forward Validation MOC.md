# M1 + APL-A Forward Validation — FV1

FV1 is a D4-owned validation extension. It measures M1 method behavior and APL-A shadow perspective behavior without changing Direction, permission, Decision Seal, or broker authority.

## Truth discipline

FV1 keeps SYNTHETIC_VALIDATION, HISTORICAL_REPLAY, PSEUDO_FORWARD_WALK_FORWARD, SHADOW_LIVE, and TRUE_FORWARD_VALIDATION separate. Installation-time evidence in this repository is synthetic/component validation only. No true-forward maturity is claimed.

## Authority

- M1 remains active method governance.
- APL-A remains SHADOW_ONLY.
- APL-B is not implemented.
- No total M1/APL/Taleb/Epistemic score exists.
- Promotion is outside FV1.

## D4 integration

FV1 uses append-only hash-chained validation records and readiness matrices under D4. It is not a second promotion system and cannot mutate the D4 promotion registry.
