# Reference Classes and Hierarchical Backoff

D4 never treats the entire history as one homogeneous sample.

Canonical cohort key:
`instrument × horizon × fundamental_direction × fundamental_force_band × d3_edge_quality × modifier_family × modifier_state × materiality × evidence_grade × regime × session/event_context × data_coverage_band × execution_profile_version`.

Exact cells often become sparse. D4 therefore uses a **predeclared hierarchical backoff**, not ad-hoc pooling:
1. exact cell;
2. drop session/event context;
3. drop regime;
4. merge evidence-grade band where policy allows;
5. market-family cohort;
6. global cohort only for descriptive context.

A broad parent cohort can stabilize an estimate; it cannot erase a materially adverse exact-market result.
