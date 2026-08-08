---
title: "Fact Inference Proxy and Assumption Separation"
type: canonical-science-note
status: canonical
version: 17.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [v17, fact, proxy, inference]
---

# Separation rules

D1 prohibits epistemic laundering: the process by which a weakly observed or inferred idea becomes phrased as a hard fact after several layers of analysis.

## Required language discipline

A claim must retain its class through summaries, PDFs, dashboards and downstream prompts. If a statement begins as `PUBLIC_PROXY`, it remains a proxy unless new direct evidence justifies reclassification. A `MODEL_INFERENCE` can become a hypothesis supported by facts, but it does not become an observed fact merely because multiple model outputs agree.

## Examples

- CFTC reported category net position: `OFFICIAL_REPORTED_FACT` or `IDENTIFIED_POSITIONING_FACT`, with the category definition and report vintage attached.
- Estimated CTA demand from a trend model: `MODEL_INFERENCE`, not identified flow.
- ETF published shares outstanding and NAV: direct/official or administrator-reported facts; inferred primary-market creation pressure from them may be a `DERIVED_FACT` if method is reproducible.
- Social/media attention score built by a model: `DERIVED_FACT` or `NARRATIVE_INFERENCE` depending on whether it is a deterministic metric or interpretive conclusion.

## Promotion rule

Reclassification requires new evidence and a new fact version. Never overwrite the original epistemic class. Historical replay must still be able to recover what the system believed the record was at the earlier cutoff.
