---
title: "Decision Evidence Pack Contract"
type: canonical-science-note
status: canonical
version: 17.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [v17, decision-pack, evidence, runtime]
---

# Decision Evidence Pack

Before the scientific stack is allowed to emit a live permission, D1 requires a point-in-time Decision Evidence Pack.

## Minimum fields

- run/analysis ID and symbol;
- analysis cutoff UTC;
- manifest/Vault version;
- fact records or references;
- root-cause graph/dependency declarations;
- fact-family coverage summary;
- decision-critical unknowns;
- confidence/validity caps;
- source/snapshot identifiers;
- explicit statement that future vintages are excluded.

## Admission logic

The pack is not a giant archive. It is the smallest sufficient evidence set that can justify the current decision while preserving lineage to source snapshots. V16.1 retrieval firewall rules still apply.

## Immutability

Once a permission is emitted, preserve the pack or its immutable hash/reference. Later revisions generate a new pack/run; they do not rewrite the earlier decision evidence.
