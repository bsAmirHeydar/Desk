---
title: "Fundamental Force and Intensity Decomposition"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Fundamental Force and Intensity Decomposition

## Decision purpose

Upgrade intensity from a broad expert judgment into an auditable force vector. The objective is to identify magnitude, sign, transmission capacity and durability without confusing any of them with confidence.

## Governing distinctions

- Intensity is magnitude; confidence is reliability.
- Economic importance is not the same as surprise.
- Breadth counts independent channels, not repeated measurements of one factor.
- Durability belongs in persistence, although it conditions the force horizon.

## Operating method

1. Select applicable force components from the event/asset map.
2. Score or band each component with evidence and provenance.
3. Apply asset-, regime- and horizon-specific weights only when disclosed.
4. Subtract contradiction and measurement-quality penalties.
5. Report an aggregate range plus the full component ledger.

## Required outputs

- `force_component_ledger`
- `force_sign`
- `force_range_0_100`
- `force_class`
- `aggregation_method`
- `contradiction_penalty`
- `confidence_cap`

## Failure modes and controls

- **Failure:** Large price move creates high intensity  
  **Control:** Score the fundamental state before using price as response evidence.
- **Failure:** Double counting nominal and real rates  
  **Control:** Apply confirmation-independence controls.
- **Failure:** Unavailable data omitted from denominator  
  **Control:** Mark unavailable-but-applicable components and impose a confidence cap.

## Force component ledger

| Component | Question | Typical evidence | Treatment |
|---|---|---|---|
| Economic-state change | Did the underlying system change materially? | first release, filing, official action | signed, asset-specific |
| Expectation surprise | Was the observation different from recoverable consensus? | consensus vintage, market-implied path | signed surprise |
| Policy-path revision | Did expected reaction-function output change? | OIS/SOFR, yield curve, guidance | signed, asset-specific |
| Cash-flow/earnings revision | Did expected cash generation change? | guidance, revisions, margins | signed |
| Valuation/risk-premium revision | Did discount rate or compensation change? | real rates, spreads, volatility distribution | signed |
| Physical-balance revision | Did scarcity, inventory or official demand change? | inventory, physical flow evidence | signed |
| Funding/liquidity revision | Did financing or collateral capacity change? | repo, basis, funding spreads | signed |
| Transmission breadth | How many independent channels are active? | rates, FX, credit, sectors | amplifier |
| Institutional amplification | Are constraints forcing continuation or suppression? | direct or proxy flow data | amplifier/dampener |
| Contradiction load | How much high-quality evidence points the other way? | rival-model ledger | penalty |

The default aggregate is a disclosed weighted ordinal range, not an arithmetic truth. Weights are selected by asset, event family, regime and horizon. `NOT_APPLICABLE` components leave the denominator; `UNAVAILABLE` but applicable components remain economically relevant and impose a confidence penalty.

## Canonical dependencies

- [[87 Alpha Lab Asset-Specific Persian PDF Analysis Prompts/15 Hourly Direction Intensity Consumption and Remaining Pressure Standard]]
- [[82 Canonical Institutional Fundamental Research Library/34 Econometrics Causal Identification and Model Risk/00 Econometrics Causal Identification and Model Risk]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
