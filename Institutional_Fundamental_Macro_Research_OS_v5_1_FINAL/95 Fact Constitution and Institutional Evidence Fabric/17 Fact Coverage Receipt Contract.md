---
title: "Fact Coverage Receipt Contract"
type: canonical-science-note
status: canonical
version: 17.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [v17, coverage-receipt, audit, runtime]
---

# Fact Coverage Receipt

The receipt is the honesty layer between retrieval and decision output.

For each registered fact family, record:

- requested/required status;
- retrieved status;
- source tier(s);
- direct/proxy/derived/inference class distribution;
- latest eligible vintage at the cutoff;
- missing/undetermined items;
- D2-pending status where applicable;
- materiality of the residual gap;
- decision effect: `NONE | CONFIDENCE_CAP | VALIDITY_CAP | HOLD | BLOCK`.

A run with excellent macro coverage but unavailable institutional flow must say so explicitly. It may still proceed if that flow is not decision-critical under current validated science; it may not imply the unavailable flow was observed.
