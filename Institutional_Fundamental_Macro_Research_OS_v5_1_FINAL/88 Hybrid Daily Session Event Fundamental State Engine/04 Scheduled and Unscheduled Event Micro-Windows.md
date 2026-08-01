---
title: "Scheduled and Unscheduled Event Micro-Windows"
type: canonical-standard
status: canonical
version: 10.4.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [event, micro-window, no-lookahead]
---
# Scheduled and Unscheduled Event Micro-Windows

## Scheduled events

For material scheduled events create:

- `PRE_EVENT_BASELINE` at T-60 when data permit;
- updated `PRE_EVENT_BASELINE` at T-15;
- `SCHEDULED_EVENT_T0` using only the release available at T0;
- `EVENT_T_PLUS_5`;
- `EVENT_T_PLUS_15`;
- `EVENT_T_PLUS_30`;
- `EVENT_T_PLUS_60`;
- later session reassessment if the causal interpretation changes.

Each window is an immutable record. Do not backfill T0 with T+5 reaction data.

## Unscheduled events

For statements, social-media posts, policy headlines, geopolitical shocks, emergency actions or surprise corporate information:

1. establish the earliest verifiable publication time;
2. state timestamp confidence;
3. create `UNSCHEDULED_EVENT_T0`;
4. create the same +5/+15/+30/+60 windows when markets are liquid and evidence exists;
5. separate source verification from market reaction;
6. preserve conflicting reports rather than selecting the later-correct version retroactively.

## Event content

Every event window decomposes:

- headline information;
- composition information;
- revisions;
- policy-reaction implications;
- cash-flow/earnings/physical-balance implications;
- positioning and liquidity amplification;
- causal leader;
- independent confirmation;
- rival model;
- expected half-life;
- score changes and evidence for them.

## Micro-window completion

Missing a required micro-window is allowed only with an explicit reason: market closed, data unavailable, timestamp uncertain or no reliable observation. The density validator treats an unexplained missing window as a failure.
