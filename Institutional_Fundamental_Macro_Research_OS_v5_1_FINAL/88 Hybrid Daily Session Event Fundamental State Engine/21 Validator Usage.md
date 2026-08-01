---
title: "Validator Usage"
type: operational-note
status: canonical
version: 10.4.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [validator, density, csv]
---
# Validator Usage

Run:

```bash
python tools/validate_hybrid_reconstruction.py MASTER_HYBRID_STATE_TIMELINE.csv --report DENSITY_VALIDATION_REPORT.json
```

The utility checks minimum daily records, baseline/end-of-day coverage, maximum gaps and event micro-window completion. Human review must still audit session correctness, source timestamps and no-lookahead integrity.
