---
title: "17 Certification Verdict and Scorecard"
type: canonical-standard
status: canonical
version: 8.0.0
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [fundamental-only, scientific-certification]
---

# Certification Verdict and Scorecard

## Scorecard

Score each category from 0 to 5:

| Category | 0 | 3 | 5 |
|---|---|---|---|
| Object definition | unresolved | mostly defined | exact instrument, scope and cutoff |
| Vault retrieval | absent | core domains used | all material domains logged |
| Evidence lineage | unsourced | mixed | load-bearing claims fully located |
| Freshness/vintage | invalid | partial | exact and auditable |
| Measurement | unclear | mostly consistent | transformations and breaks explicit |
| Causality | narrative | primary model | rivals, falsifiers and reflexivity |
| Multihorizon | mixed | partly separated | full conflict-aware stack |
| Cross-asset transmission | correlation list | partial map | balance-sheet and flow map |
| Pricing/payoff | omitted | rough baseline | expectations, valuation, carry and payoff |
| Scenario/tail | single case | alternatives | signposted distribution and tails |
| Contradictions/unknowns | hidden | noted | explicit ledgers and confidence cap |
| Output usefulness | generic | informative | decision-complete and auditable |

Maximum raw score: 60.

## Verdict thresholds

- **FULL**: at least 55, no category below 4 and no veto.
- **CONDITIONAL**: at least 46, no integrity failure, limitations explicit.
- **NOT CERTIFIED**: below 46 or any integrity veto.

## Integrity vetoes

Regardless of score, reject the report for:

- fabricated or misrepresented evidence;
- historical lookahead contamination;
- unresolved object identity;
- hidden use of unavailable licensed data;
- material source conflict suppressed;
- fundamental-only boundary violation;
- citations that do not support the claims.

## Final certification block

```yaml
certification:
  verdict: FULL | CONDITIONAL | NOT_CERTIFIED
  raw_score: 0-60
  failed_gates: []
  confidence_cap:
  material_unknowns: []
  re_certification_triggers: []
```
