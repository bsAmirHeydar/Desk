---
title: "Root Cause Dependency and Same-Root Deduplication"
type: canonical-science-note
status: canonical
version: 17.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [v17, root-cause, dependency, deduplication]
---

# Independence is causal, not numerical

Four market reactions to one release are not four independent confirmations of the release.

Example:

`Fed decision → Treasury yield move → USD move → equity move`

All may be useful transmission evidence, but treating them as four independent root facts would overstate confidence.

## Root-cause contract

Every load-bearing fact/claim should carry a `root_cause_id` when known. When root cause is unresolved and independence is decision-critical, the system must not fabricate independence. It may `HOLD` or cap confidence according to materiality.

## Deduplication rule

Evidence from the same root can strengthen understanding of transmission and consistency, but confidence aggregation must count the root once unless genuinely distinct causal information is demonstrated.

## Cross-layer rule

The same fact used by Fundamental, Narrative and Timing does not become three votes. Layer boundaries govern function, not evidence independence.
