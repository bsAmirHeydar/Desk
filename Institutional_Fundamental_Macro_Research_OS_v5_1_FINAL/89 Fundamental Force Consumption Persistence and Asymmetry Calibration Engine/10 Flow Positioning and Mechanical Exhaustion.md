---
title: "Flow Positioning and Mechanical Exhaustion"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Flow Positioning and Mechanical Exhaustion

## Decision purpose

Assess whether the positioning and mechanical-flow leg is forming, active, saturating or exhausted while preserving the distinction between observed and inferred flow.

## Governing distinctions

- Positioning level is not flow.
- Flow magnitude is not price impact.
- Exhaustion is mechanism-specific.
- A flow can restart after a threshold, volatility change or new catalyst.

## Operating method

1. Name the mechanism and party potentially forced to act.
2. Classify evidence as direct, licensed, public proxy or inferred.
3. Map trigger, direction, capacity, timing and saturation.
4. Compare marginal flow and marginal impact through time.
5. Publish exhaustion band, uncertainty and restart conditions.

## Required outputs

- `flow_mechanism`
- `positioning_state`
- `flow_state`
- `exhaustion_band`
- `restart_trigger`
- `observability_tier`
- `proxy_limitations`

## Failure modes and controls

- **Failure:** Inferring exact dealer inventory from public price action  
  **Control:** Use proxy labels and a hard confidence cap.
- **Failure:** High volume treated as forced flow  
  **Control:** Require mechanism and directional evidence.
- **Failure:** Exhaustion inferred from one pause  
  **Control:** Check liquidity, event waiting and replacement flows.

## Observability ladder

Direct position books and prime-broker data are not assumed. Public implementation may use exchange volume/open interest, options-implied measures, ETF creation/redemption where available, futures positioning, basis, breadth, auction/close data and time-aligned price-impact decay. Each is a proxy for a narrower construct and must be labelled accordingly.

Flow exhaustion is high only when the relevant forced mechanism has substantially completed, marginal impact is decaying, replacement demand is absent and no new trigger is likely to restart the mechanism. Low marginal price impact alone is insufficient; liquidity can temporarily absorb an active flow.

## Canonical dependencies

- [[48 Systematic Strategies Positioning and Flow Ecology/00 48 Systematic Strategies Positioning and Flow Ecology MOC]]
- [[74 Non-Event Fundamental Context and Flow-Led Session Playbooks/08 Options Expiry Strike and Dealer-Hedge Day]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
