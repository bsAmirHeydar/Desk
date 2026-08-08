---
title: "Immutable Forward State Archive"
type: research-data-governance
status: canonical-operational
version: 14.1.0
---
# Immutable Forward State Archive

The primary validation dataset for the live brain is the sequence of decisions actually made before outcomes were known.

Every Full-Vault run must append, never rewrite:
- timestamps and source cutoff;
- six-market full state;
- all six horizons;
- direction/confidence;
- active and opposing drivers;
- narrative state;
- consumption and remaining pressure;
- persistence and reversal risk;
- Edge class and reason;
- permission and `valid_until`;
- invalidations, upgrade/downgrade triggers and next review;
- missing evidence and confidence caps.

The archive included in this release is a seed snapshot of the existing live forward states and must remain immutable. New states should be appended chronologically.
