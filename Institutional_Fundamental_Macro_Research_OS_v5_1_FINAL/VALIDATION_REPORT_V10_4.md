---
title: "Validation Report V10.4 Hybrid Daily Session Event State"
type: validation-report
status: final
version: 10.4.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [validation, hybrid-state, no-lookahead, density]
---
# Validation Report V10.4

## Build identity

- **Release:** V10.4 Hybrid Daily Session Event Fundamental State Engine
- **Base:** V10.3 cumulative Vault payload
- **Mission:** replace sparse event-only historical reconstruction with mandatory daily/session/event/decay coverage

## Final scale

| Metric | Result |
|---|---:|
| Markdown notes | **1,457** |
| Approximate words | **1,324,747** |
| Obsidian links | **15,920** |
| Display equation blocks | **3,706** |
| New hybrid module notes | **22** |
| Supported record types | **25** |
| Asset fast/medium/slow stacks | **4** |
| New production prompts/contracts | **3** |

## Hard validation gates

| Gate | Result |
|---|---|
| Broken wikilinks | PASS — 0 |
| Ambiguous wikilinks | PASS — 0 |
| Trailing whitespace | PASS — 0 |
| Unbalanced code fences | PASS — 0 |
| Canonical/specialist/benchmark counts | PASS |
| Required daily/session/event record types | PASS — 25/25 |
| Lower adaptive thresholds | PASS |
| Daily/session density rules | PASS |
| Event T+30 and full micro-window rules | PASS |
| State-decay and no-change records | PASS |
| Four-market driver stacks | PASS |
| Four-market 100-day hybrid prompt | PASS |
| Machine-readable schema | PASS |
| Density validator syntax and sample run | PASS |
| Fundamental-only boundary | PASS |
| No-lookahead immutable-state controls | PASS |

## Methodological changes

- Daily baseline and end-of-day state are mandatory on every open day.
- Session handoffs and post-open/midday/afternoon reassessments are mandatory.
- Event micro-windows include T-60, T-15, T0, T+5, T+15, T+30 and T+60.
- State decay is reassessed without requiring a new headline.
- `NO_MATERIAL_DIRECTION_CHANGE` records subordinate state changes.
- Default materiality thresholds are 5 points for direction/intensity/confidence and 10 for consumption/confirmation/reversal variables.
- Direction is separated from edge availability.
- Density validators measure daily coverage, session coverage, maximum gaps and event-window completeness.

## Known limitations

- Public historical intraday archives can be incomplete. Missing evidence must be documented rather than invented.
- Flow, dealer and systematic-position estimates may remain proxy-based without proprietary data.
- Ordinal scores are not calibrated probabilities unless explicitly labelled otherwise.
- The included density validator performs structural checks; human review remains necessary for causal and timestamp integrity.

**Status: PASS**
