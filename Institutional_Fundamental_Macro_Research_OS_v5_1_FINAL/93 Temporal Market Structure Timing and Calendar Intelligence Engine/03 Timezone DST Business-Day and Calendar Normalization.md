---
title: "Timezone DST Business-Day and Calendar Normalization"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Timezone, DST, Business-Day and Calendar Normalization

Timing fails catastrophically when clock conversion is treated as formatting. V15 makes timezone normalization a scientific prerequisite.

## Canonical representation
Store every timestamp as:
- original source timezone and local wall-clock time;
- IANA timezone identifier where available;
- UTC timestamp;
- New York, London and Tokyo renderings for cross-market work;
- report timezone (`Asia/Tehran` for the current production profile);
- source publication timezone and whether DST was active.

Never store a recurring market event using a fixed UTC offset when the local venue observes daylight saving time.

## DST mismatch weeks
The US, UK and continental Europe change clocks on different dates. Therefore London/New York overlap can temporarily shift in UTC and Tehran time. These weeks require explicit `DST_MISMATCH` state and re-computation of all cross-centre windows. Japan does not currently use DST; the system must nevertheless derive this from a timezone database rather than hard-code assumptions forever.

## Calendar classes
Maintain separate holiday calendars for venue trading, banking/payment systems, benchmark administrators, futures exchanges and central banks. A venue may be open while a relevant banking centre or benchmark is closed.

## Half days
An early equity close changes cash-futures synchronization, option cutoffs, closing-auction timing, and the available lifespan of an Edge. Half-days are not ordinary days compressed by a constant factor.

## Quality gate
If timezone, DST or holiday resolution is uncertain, temporal confidence is capped and the system must not publish an exact `valid_until` based on an unverified clock.
