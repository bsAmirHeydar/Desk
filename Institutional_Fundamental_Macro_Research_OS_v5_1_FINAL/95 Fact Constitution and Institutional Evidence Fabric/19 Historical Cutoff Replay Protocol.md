---
title: "Historical Cutoff Replay Protocol"
type: canonical-science-note
status: canonical
version: 17.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [v17, historical, replay, no-lookahead]
---

# Historical replay

Given a cutoff `T`, replay must reconstruct the evidence state that could actually have existed at `T`.

## Procedure

1. resolve the instrument and production profile as of the relevant methodology vintage;
2. exclude all facts whose publication/visibility time is after `T`;
3. exclude records with unresolved publication time when eligibility cannot be demonstrated;
4. group revisions by `release_family_id`;
5. select the latest eligible vintage per family at `T`;
6. retain source/proxy/inference classes exactly as they were;
7. rebuild root-cause/dependency state without future descendants;
8. create a historical Fact Coverage Receipt;
9. only then run Fundamental/Narrative/Timing science.

A modern revised database value is not a substitute for historical vintage data.
