---
title: "V15 Temporal Market Structure Timing and Calendar Intelligence Release Notes"
type: release-notes
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# V15.0 Temporal Market Structure, Timing and Calendar Intelligence

## Baseline
Requires V14.1 Module 92 installed. Preserves Modules 89-92 and the fundamental-only boundary.

## New authority
Module 93 becomes canonical authority for temporal market structure: sessions, handoffs, macro/central-bank clocks, benchmark/fixing clocks, Treasury auctions, futures/options lifecycle, index rebalance/reconstitution, earnings/corporate clocks, month/quarter/year-end, holidays/DST, settlement/funding clocks, temporal forces and Edge validity/veto interaction.

## Scientific boundary
V15 does not add technical direction analysis. Timing is causal/institutional/calendar science. It may constrain validity or add a sourced temporary mechanical force, but it cannot derive direction from chart patterns.

## Production integration
Module 92 production prompts and launchers are upgraded to call V15 before Edge adjudication. The six-market email contract and M1 Donchian/4ATR/trailing execution profile are preserved.

## Primary-source research
The patch includes 33 baseline source entries from exchanges, clearinghouses, index providers, benchmark administrators, central banks, statistical agencies, U.S. Treasury and BIS/Basel institutional research. Live production must dynamically re-fetch current calendars/methodologies.


## Superseded by V15.1
V15.0 temporal coverage is preserved, but final Active gating and production integration are superseded by [[V15_1_RELEASE_NOTES]].
