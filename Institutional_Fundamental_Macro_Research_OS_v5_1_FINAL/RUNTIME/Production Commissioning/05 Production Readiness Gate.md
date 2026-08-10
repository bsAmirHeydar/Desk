# Production Readiness Gate

`PRODUCTION_READY` is never granted merely because C1 is installed.

The gate requires: R4 full offline certification PASS, C1 environment receipt PASS, C1 shadow receipt PASS across all six production instruments, intact prompt/context/source policies, no unresolved decision-critical source insufficiency in the certification basket, and an explicit operator signoff.

Even after signoff, Alpha Lab remains permission-only. Broker write/order creation is outside C1 authority.

## Live-launch immutability gate

A `LIVE` launcher run is blocked unless the readiness receipt is `PRODUCTION_READY_PERMISSION_ONLY`, its R4/C1 certification-surface fingerprint equals the current surface, the current tracked working tree is clean, and the current Git HEAD equals the signed Git commit stored in the readiness receipt. Any governed code/prompt/context change therefore forces re-certification and a new operator signoff before live permission delivery resumes.
