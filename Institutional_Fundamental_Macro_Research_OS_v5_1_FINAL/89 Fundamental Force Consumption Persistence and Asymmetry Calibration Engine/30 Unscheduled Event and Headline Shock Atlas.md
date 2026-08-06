---
title: "Unscheduled Event and Headline Shock Atlas"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Unscheduled Event and Headline Shock Atlas

## Decision purpose

Control timestamp ambiguity, source quality, rumor risk, policy optionality and rapid reversal in tariffs, sanctions, wars, political statements, corporate disclosures, outages and financial stress.

## Governing distinctions

- Earliest rumor time differs from verified public time.
- A statement can be policy signal, negotiation tactic or noise.
- Binary headlines can create price gaps without durable state change.
- Official clarification can reverse information content before flow exhaustion ends.
- Geopolitical severity and market transmission are separate vectors.

## Operating method

1. Build a source chronology with message hashes or stable locators where possible.
2. Tag each item as rumor, primary statement, official action, implementation or clarification.
3. Score credibility, authority, implementation probability and economic incidence separately.
4. Map first-order and second-order transmission plus rival interpretations.
5. Use bounded scenario branches until implementation evidence resolves uncertainty.
6. Reassess consumption and reversal hazard after every authoritative update.

## Required outputs

- `event_chronology`
- `source_authority`
- `implementation_state`
- `scenario_branches`
- `causal_channels`
- `reversal_hazard`
- `timestamp_confidence`

## Failure modes and controls

- **Failure:** Backfilling the cleanest later timestamp  
  **Control:** Preserve the contemporaneous chronology.
- **Failure:** Treating rhetoric as implemented policy  
  **Control:** Separate signal from action.
- **Failure:** Ignoring legal/operational lag  
  **Control:** Model implementation path.
- **Failure:** High confidence from one social post  
  **Control:** Apply authority and corroboration caps.

## Shock-state ladder

`RUMOR → ATTRIBUTED_REPORT → PRIMARY_STATEMENT → FORMAL_ACTION → IMPLEMENTATION → ECONOMIC_INCIDENCE → REVISION/REVERSAL`

Direction may change at any stage, but confidence and persistence cannot outrun the evidence stage without an explicit model-implied label.

## Canonical dependencies

- [[20 Observability Data Tiers and Confidence Caps]]
- [[15 Exhaustion Reversal Hazard and Thesis Failure]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
