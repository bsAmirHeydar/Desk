---
title: "Transmission Breadth Depth and Independence"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Transmission Breadth Depth and Independence

## Decision purpose

Measure whether the impulse transmits through economically distinct channels rather than appearing repeatedly in correlated instruments.

## Governing distinctions

- Breadth is count plus economic diversity.
- Depth is the magnitude of revision within each channel.
- Independence is conditional and must be justified.
- A causal leader can change through the session.

## Operating method

1. Construct a channel graph from the winning model.
2. Assign each observation to a channel and common-factor cluster.
3. Assess timing, sign and magnitude consistency.
4. Weight independent confirmation more than redundant confirmation.
5. Record leader changes and confirmation breaks.

## Required outputs

- `transmission_channels`
- `channel_depth`
- `confirmation_independence_matrix`
- `causal_leader`
- `leader_change`
- `confirmation_break`

## Failure modes and controls

- **Failure:** Counting related tickers as separate evidence  
  **Control:** Cluster mechanically or economically overlapping observations.
- **Failure:** Late follower treated as causal leader  
  **Control:** Use timestamp order and mechanism.
- **Failure:** Divergence automatically invalidates thesis  
  **Control:** Test lags, segmentation and rival models before downgrading.

## Independence matrix

| Pair | Default relationship | Required treatment |
|---|---|---|
| DXY and EURUSD | mechanically overlapping | do not count as two confirmations |
| Index cash and futures | same underlying | response, not independent confirmation |
| Nominal and real yield | related decomposition | partial independence with breakeven check |
| OIS and front-end yield | overlapping policy-path measure | low-to-medium independence |
| Credit spread and equity volatility | common risk factor plus distinct channels | medium, regime-dependent |
| ETF flow and price | endogenous | require timing and source-direction analysis |
| Sector breadth and index | partially distinct | higher value when concentration is material |

The matrix is a prior, not a permanent constant. Analysts must document why dependence changes in stress or liquidity regimes.

## Canonical dependencies

- [[88 Hybrid Daily Session Event Fundamental State Engine/08 Cross-Asset Confirmation and Causal-Leader Changes]]
- [[81 Scientific QA and Certification Framework/10 Cross-Asset Balance-Sheet and Flow Transmission Gate]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
