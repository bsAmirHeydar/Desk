---
title: "Session Clocks and Handoff Protocol"
type: canonical-standard
status: canonical
version: 10.4.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [session, handoff, clocks, dst]
---
# Session Clocks and Handoff Protocol

## General clock requirements

Every checkpoint stores UTC, local market time, timezone identifier and daylight-saving status. Fixed UTC assumptions are prohibited where the venue or release uses local daylight-saving rules.

## U.S. equity index checkpoints

For Nasdaq 100 and S&P 500, default checkpoints in `America/New_York` are:

- 04:00–06:00 pre-market inherited-state check;
- 07:45–08:15 daily baseline before major 08:30 data;
- 09:00–09:25 pre-cash-open state;
- 10:00–10:30 post-open reassessment;
- 12:00–13:00 midday reassessment;
- 14:00–15:00 afternoon reassessment, adjusted for policy and Treasury events;
- 15:45–16:15 end-of-day state;
- post-market earnings update when a systemically important constituent reports.

## Gold checkpoints

Gold is global. Default checkpoints are:

- Asia baseline and Asia-session state;
- Asia-to-London handoff;
- London open and morning physical/rates state;
- pre-New-York/COMEX reassessment;
- post-U.S.-data or post-COMEX-open reassessment;
- London fixing-related check when material;
- New York afternoon and end-of-day state.

## EURUSD checkpoints

Default checkpoints are:

- Asia baseline;
- pre-London and London-open handoff;
- European data/ECB window reassessment;
- pre-New-York handoff;
- U.S. data and overlap-session reassessment;
- options-cut/fixing window when relevant;
- London close and New York end-of-day state.

## Handoff content

Every `SESSION_HANDOFF` reports:

- inherited direction and score;
- information added in the outgoing session;
- which driver led;
- which evidence confirmed or contradicted;
- what remains unresolved;
- degree of catalyst consumption;
- expected persistence into the incoming session;
- next mandatory checkpoint.

A handoff is mandatory even if direction is unchanged.
