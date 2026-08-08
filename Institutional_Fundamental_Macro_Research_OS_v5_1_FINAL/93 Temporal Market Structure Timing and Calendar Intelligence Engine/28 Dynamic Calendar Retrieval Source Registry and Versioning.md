---
title: "28 Dynamic Calendar Retrieval Source Registry and Versioning"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
---
# Dynamic Calendar Retrieval, Source Registry and Versioning

The Vault stores timing science, **not a frozen calendar**. Live runs must re-fetch current exchange hours, central-bank/statistical calendars, benchmark schedules, index methodology/calendars, derivatives lifecycle and holidays from authoritative sources.

Source hierarchy: exchange/clearing/index/benchmark provider > central bank/statistical/government > regulated market association > licensed institutional calendar > reputable secondary source.

Store source URL/ID, retrieval time, effective/version date and current-vs-historical status.
