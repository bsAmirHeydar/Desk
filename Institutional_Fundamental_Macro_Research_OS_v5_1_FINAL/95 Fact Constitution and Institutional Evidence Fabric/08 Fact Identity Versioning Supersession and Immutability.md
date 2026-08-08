---
title: "Fact Identity Versioning Supersession and Immutability"
type: canonical-science-note
status: canonical
version: 17.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [v17, identity, versioning, immutability]
---

# Fact identity

A `fact_id` identifies one epistemic version of one proposition/value. A `release_family_id` groups revisions of the same published series/event. A `root_cause_id` groups causal descendants that should not be counted as independent evidence.

## Mutation prohibition

Do not mutate a previously emitted fact to reflect a new revision, corrected source, new method or new classification. Create a successor record with lineage.

## Supersession

`superseded_at` is a temporal selection aid, not deletion. Current analysis can prefer the newest eligible version; historical replay must select the eligible version as of the cutoff.

## Corrections

If Alpha Lab itself made a parsing/classification error, preserve the original run/output and publish a corrected fact version plus a correction record. Forward telemetry remains immutable.
