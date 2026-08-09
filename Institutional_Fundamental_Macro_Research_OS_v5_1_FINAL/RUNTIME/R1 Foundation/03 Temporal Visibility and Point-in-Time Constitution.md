# Temporal Visibility and Point-in-Time Constitution

## Canonical clock

All runtime comparison clocks are stored in UTC RFC3339. Source-local timestamps may be retained as metadata, but they never replace the canonical UTC clock.

## Required temporal fields where applicable

- `event_time`
- `reference_time`
- `effective_time`
- `publication_time`
- `first_available_time`
- `retrieved_at`
- `ingested_at`
- `superseded_at`

## Visibility test

The minimum visibility condition is:

```text
first_available_time <= analysis_cutoff
```

A later retrieval does not automatically make a historical record valid. Historical replay also requires acceptable **vintage integrity**.

## Vintage-integrity classes

- `ORIGINAL_CAPTURE` — snapshot captured contemporaneously.
- `OFFICIAL_VINTAGE_ARCHIVE` — official archived vintage with point-in-time identity.
- `RECONSTRUCTED_WITH_PROVENANCE` — reconstructable historical content with explicit limitations.
- `CURRENT_ONLY` — current/latest representation; not admissible for strict historical claims about earlier vintages.
- `UNDETERMINED` — vintage integrity cannot be established.

## Replay admissibility

- `STRICT_ADMISSIBLE`
- `LIMITED_ADMISSIBLE`
- `FORBIDDEN`
- `UNDETERMINED`

`DECISION_CRITICAL` historical evidence must be strictly admissible under `STRICT_POINT_IN_TIME`. Limited evidence may be retained for context only when explicitly governed later by scientific materiality rules.

## Revision selection

For a requirement with multiple vintages, the selected vintage is the latest admissible vintage whose `first_available_time` is not later than the analysis cutoff and whose supersession state is valid at that cutoff.

Future revisions are never projected backward.

## DST and ambiguous local time

Runtime contracts require explicit timezone-aware timestamps. When a local wall-clock time is ambiguous because of DST, the caller must specify an explicit offset or `fold`. Silent DST guessing is forbidden.
