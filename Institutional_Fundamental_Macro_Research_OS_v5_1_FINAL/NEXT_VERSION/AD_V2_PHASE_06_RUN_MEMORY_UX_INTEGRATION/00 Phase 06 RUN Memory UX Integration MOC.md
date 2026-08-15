# AD-V2-P06 — RUN / Capsule / Persistence / Change Detection / UX Integration

## Mission
P06 integrates the already-defined V2 science into the run experience without reopening V1 production science.

P06 owns **composition, persistence, comparison, history, portable memory and presentation only**.

It does **not** own Directional Pressure, Price Transmission, Latent/Release science, Gold evidence science, trade permission or broker execution.

## Closed baseline
- V1 remains the closed production baseline.
- P00–P05 must already be installed exactly.
- P06 is additive and lives only under `NEXT_VERSION`.
- Deployment remains `SHADOW_ONLY`.

## One-way authority graph
`V1 RUN2 base capsule → P02 Pressure → P03 Transmission → P04 Latent/Release → P05 Gold specialization → P06 Run Overlay / Memory / UX`

P06 may render, compare and persist these states. It may not mutate them.

## Primary output
A V2 Gold Run Capsule Extension containing:
- immutable upstream fingerprints;
- full P02–P05 shadow science states;
- execution authority inherited from the V1 base capsule;
- a semantic change set versus the previous valid V2 run;
- a portable-memory summary;
- append-only persistence metadata;
- presentation model and Explorer output.

## Hard invariants
1. PRESSURE_OWNER_P02
2. TRANSMISSION_OWNER_P03
3. LATENT_RELEASE_OWNER_P04
4. GOLD_SPECIALIZATION_OWNER_P05
5. TRADE_PERMISSION_INHERITED_ONLY
6. NO_V2_BROKER_AUTHORITY
7. PRICE_ONLY_CHANGE_MUST_NOT_APPEAR_AS_PRESSURE_CHANGE
8. APPEND_ONLY_V2_HISTORY
9. IMMUTABLE_CAPSULE_EXTENSION
10. NO_REWRITE_OF_V1_CAPSULE_OR_V1_INDEX
11. CHANGE_DETECTION_IS_SEMANTIC_NOT_TEXTUAL
12. PORTABLE_MEMORY_IS_DERIVED_NOT_AUTHORITATIVE
13. UX_HAS_PRESENTATION_AUTHORITY_ONLY
14. P07_PROMOTION_REQUIRED_FOR_MAINLINE_AUTHORITY
