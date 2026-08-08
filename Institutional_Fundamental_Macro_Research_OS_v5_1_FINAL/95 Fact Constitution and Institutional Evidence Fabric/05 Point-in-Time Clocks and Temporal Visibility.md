---
title: "Point-in-Time Clocks and Temporal Visibility"
type: canonical-science-note
status: canonical
version: 17.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [v17, point-in-time, clocks, no-lookahead]
---

# The nine-clock model

Each clock answers a different question and must not be collapsed into one timestamp.

- `event_time` — when the underlying event occurred.
- `reference_time` — period/date the observation describes.
- `effective_time` — when a rule/state became economically or legally effective.
- `publication_time` — when the publisher released the information.
- `first_seen_time` — earliest time Alpha Lab can demonstrate it observed the released item.
- `retrieval_time` — when the current run fetched/accessed it.
- `ingestion_time` — when it entered the local evidence store or run pack.
- `valid_from` — earliest time this fact version is allowed to be used by the model.
- `superseded_at` — time a later version replaced it for current-state work.

## Historical visibility

A fact is eligible for a cutoff only when the system can demonstrate that the relevant version was public/available by the cutoff. `publication_time` is the primary visibility clock for public releases. `first_seen_time` is a conservative local audit clock and can be later than publication.

Unknown publication time is not backfilled from later knowledge. A decision-critical record with unresolved visibility routes to `HOLD`; a material but noncritical record may permit analysis with a confidence cap if the remaining evidence is sufficient.

## Clock conflicts

Small discrepancies inside the configured tolerance may be admitted with a timestamp confidence cap. Material contradictions in a decision-critical release time are rejected/held until reconciled. The policy file defines the mechanical tolerance; event-specific science may impose stricter clocks.
