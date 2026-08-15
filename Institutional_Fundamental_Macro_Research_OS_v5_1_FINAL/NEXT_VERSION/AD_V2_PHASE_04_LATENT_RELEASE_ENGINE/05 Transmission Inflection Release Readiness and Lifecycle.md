---
title: "Transmission Inflection, Release Readiness and Lifecycle"
type: scientific-contract
status: shadow-development
---
# Transmission Inflection

P04 compares the current P03 state with prior valid P03 snapshots from the same pressure/horizon regime.

Possible states:

`IMPROVING_FAST`, `IMPROVING`, `STABLE`, `DETERIORATING`, `UNKNOWN`.

A move from `NEGATIVE_TRANSMISSION` toward `COMPRESSION`, `ALIGNED_INCOMPLETE` or `ALIGNED` can be an improving transmission inflection. It is not by itself a Release.

# Release Readiness

Vocabulary:

`BLOCKED_UNRESOLVED`, `NOT_READY`, `WATCH`, `PRE_RELEASE`, `HIGH_READINESS`.

High readiness requires high unreleased pressure, a mature/exhausting opposing move, improving transmission and at least one independent release-support group. Event-reset risk or unresolved causal-model error can cap readiness.

# Release lifecycle

P04 may emit:

- `PRESSURE_BUILDING`
- `DIVERGENCE`
- `OPPOSING_MOVE_ACTIVE`
- `PRE_RELEASE`
- `RELEASE_CANDIDATE`
- `RELEASE`
- `EXPANSION`
- `CONSUMPTION`
- `EXHAUSTION`
- `UNDETERMINED`

## Release proof rule

A target-price flip is necessary for some release states but **never sufficient**.

`RELEASE` requires independent non-price release support from at least two independence groups, maturity at `EXHAUSTING/EXHAUSTED`, no fresh replacement opposing driver, and a valid P03 aligned transition after prior disagreement.
