---
title: "Revision Vintage and First-Release Preservation"
type: canonical-science-note
status: canonical
version: 17.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [v17, vintage, revision, replay]
---

# Vintage doctrine

Revisions create new records. They never rewrite the first release.

Each release family must carry a stable `release_family_id`; every publication has its own `fact_id`/`vintage_id`, `release_sequence`, `publication_time` and optional `revision_of_fact_id`.

## Historical replay rule

At cutoff `T`, use the latest version whose publication/visibility time is `<= T`. A revision published after `T` is invisible even if it is the value a modern database displays today.

## Why this matters

Macroeconomic releases, earnings, benchmark histories, constituent files and official statistics may be revised. Replacing an old value with the latest vintage creates silent look-ahead and falsely improves historical analysis.

## Storage rule

First release, revision 1, revision 2 and later restatements are separate immutable versions. `superseded_at` governs current-state selection but never erases historical eligibility.
