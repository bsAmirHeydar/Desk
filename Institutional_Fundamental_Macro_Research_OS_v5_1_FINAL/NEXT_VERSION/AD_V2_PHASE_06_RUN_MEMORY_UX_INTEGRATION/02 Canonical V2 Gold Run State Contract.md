# Canonical V2 Gold Run State

The state is deliberately layered.

## BASE
Identity, cutoff, horizon, mode, V1 run id and immutable V1 permission.

## PRESSURE
Exact P02 state. Price is never reinterpreted here.

## TRANSMISSION
Exact P03 state. Price response, efficiency and counterfactual residual live here.

## LATENT
Exact P04 state. Unreleased Pressure, opposing-move maturity, reserve, readiness and lifecycle live here.

## GOLD INTELLIGENCE
Exact P05 state. Gold observability, venue boundaries, event reset and missing-driver search live here.

## EXECUTION
Read-only inheritance of V1 permission. `v2_override_allowed=false`.

## CHANGE SET
Semantic transitions since the last compatible P06 capsule.

## PORTABLE MEMORY
A concise derived summary for cross-chat / operator continuity. It has no scientific authority.
