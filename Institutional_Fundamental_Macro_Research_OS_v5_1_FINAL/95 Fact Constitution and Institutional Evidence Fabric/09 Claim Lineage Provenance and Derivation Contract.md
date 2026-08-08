---
title: "Claim Lineage Provenance and Derivation Contract"
type: canonical-science-note
status: canonical
version: 17.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [v17, lineage, derivation, provenance]
---

# Claim lineage

Every decision-relevant claim must be traceable to either direct fact IDs or a declared derivation/inference method.

## Derived fact requirements

A `DERIVED_FACT` requires:

- one or more `parent_fact_ids`;
- `derivation_method_id`;
- method version or code hash when applicable;
- transformation parameters;
- output units and semantics;
- no use of parent facts that were invisible at the run cutoff.

A derived value missing parent/method lineage is invalid for load-bearing use.

## Inference requirements

`MODEL_INFERENCE` and `NARRATIVE_INFERENCE` must declare supporting fact IDs, model/prompt/analyst identity when available, horizon, and uncertainty. They may inform the validated layer that owns that inference, but they may not be relabeled as factual observations.

## Claim graph

The system should be able to traverse:

`final permission ← Edge decision ← layer claims ← fact/derived records ← source snapshots`

This makes an analysis reproducible and exposes where uncertainty actually enters.
