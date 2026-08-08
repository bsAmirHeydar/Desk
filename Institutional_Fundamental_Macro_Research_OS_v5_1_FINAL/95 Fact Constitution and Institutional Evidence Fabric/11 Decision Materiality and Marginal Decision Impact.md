---
title: "Decision Materiality and Marginal Decision Impact"
type: canonical-science-note
status: canonical
version: 17.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [v17, materiality, decision, fuzzy]
---

# Materiality routing

D1 preserves V16.1's fuzzy decision doctrine but normalizes evidence language to four tiers:

- `DECISION_CRITICAL` — unresolved state can plausibly flip direction/permission, invalidate Edge, or destroy temporal validity.
- `MATERIAL` — meaningful to confidence, validity window or Edge quality, but not independently expected to reverse the decision.
- `SUPPORTING` — useful corroboration or explanation.
- `CONTEXTUAL` — recorded for completeness; not load-bearing.

For compatibility, D1 `MATERIAL` maps to the V16.1 `MATERIAL_SECONDARY` behavior.

## Marginal-decision test

Ask: **If this item were resolved the other plausible way, could the current permission or active Edge change?**

- yes, and no substitute evidence resolves it → `HOLD/BLOCK`;
- no, but it could materially change conviction or validity → confidence/validity cap;
- no meaningful marginal effect → disclose, do not veto.

This avoids both extremes: unsafe permissiveness and a system that becomes permanently `NO_TRADE` because some secondary data are missing.
