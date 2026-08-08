---
title: "First-Seen Retrieval Ingestion and Snapshot Integrity"
type: canonical-science-note
status: canonical
version: 17.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [v17, snapshot, retrieval, audit]
---

# Snapshot integrity

A URL is not evidence by itself. D1 treats a source snapshot as an auditable object.

A snapshot should record, where available: canonical source locator, publisher, dataset/document identifier, publication time, retrieval time, local first-seen time, content hash, version/edition, query parameters, and any transformation required to parse the content.

## First-seen is conservative

`first_seen_time` is not a substitute for publication time. If Alpha Lab first fetched an official release 30 minutes after it was published, the release may still be historically available from publication time if the publisher timestamp is reliable. If the publication time is unresolved, the later first-seen clock cannot be backdated.

## Snapshot immutability

When source content changes, store a new snapshot/version. Do not silently replace the prior snapshot. Any derived fact must retain the source snapshot IDs that made the derivation reproducible.
