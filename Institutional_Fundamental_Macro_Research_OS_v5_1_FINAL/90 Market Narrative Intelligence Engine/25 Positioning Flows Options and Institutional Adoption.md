---
title: "Positioning Flows Options and Institutional Adoption"
type: canonical-method
status: canonical
version: 12.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v12, market-narrative, daily-intelligence]
---
# Positioning Flows Options and Institutional Adoption

## Adoption versus mechanics

Positioning and flow can express a narrative, amplify it, or temporarily override it. Dealer hedging, CTA behavior, volatility-control, passive flows, real-money allocation and options demand have different mechanisms and data availability.

## Evidence discipline

Direct proprietary observations receive their declared provenance. Public options or price proxies cannot be relabeled as dealer books or institutional adoption. When data are unavailable, use `UNAVAILABLE` and apply a confidence cap.

## Control states

Distinguish `NARRATIVE_EXPRESSED_BY_FLOW`, `FLOW_AMPLIFIES_NARRATIVE`, `FLOW_HIJACKS_PRICE`, `POSITIONING_COMPLETE`, `POSITIONING_REVERSING` and `UNDETERMINED`. A flow hijack can change the tactical price controller without changing the fundamental or narrative leader.
