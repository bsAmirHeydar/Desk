---
title: "Source Contradiction and Timestamp Reconciliation"
type: canonical-science-note
status: canonical
version: 17.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [v17, contradiction, timestamps, reconciliation]
---

# Contradiction protocol

Conflicting evidence is preserved, not averaged away automatically.

## Sequence

1. verify instrument/series identity and units;
2. verify reference period and vintage;
3. verify source tier and publisher authority;
4. verify publication/effective timestamps;
5. determine whether the values describe different scopes rather than a true contradiction;
6. if unresolved, classify the contradiction by decision materiality.

## Timestamp tolerance

The D1 policy permits a small clock discrepancy inside a configured tolerance to pass with a cap when the underlying release identity is secure. A material conflict outside tolerance is not repaired by choosing the timestamp that helps the historical thesis. Decision-critical temporal contradiction produces `HOLD/REJECT` until reconciled.
