---
title: "Observability Data Tiers and Confidence Caps"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Observability Data Tiers and Confidence Caps

## Decision purpose

Bind every important state claim to an observability tier and enforce confidence caps when ideal inputs are licensed, proprietary or unknowable.

## Governing distinctions

- Observation quality and causal confidence are separate.
- A proxy inherits mapping risk.
- Missing data remain in the applicability set.
- `UNDETERMINED` is a valid high-quality output.

## Operating method

1. Create the input observability matrix.
2. Record preferred source, public alternative and proxy.
3. Assign timestamp, revision and point-in-time risks.
4. Apply default or justified confidence caps.
5. Store missing-input penalties at field level.

## Required outputs

- `observability_matrix`
- `data_tier`
- `preferred_source`
- `proxy_mapping`
- `confidence_cap`
- `missing_input_penalty`
- `unavailable_inputs`

## Failure modes and controls

- **Failure:** Proprietary construct silently proxied  
  **Control:** Label target, proxy and mapping risk.
- **Failure:** Confidence exceeds data ceiling  
  **Control:** Validator blocks the record.
- **Failure:** Unavailable input dropped  
  **Control:** Retain it as applicable and unresolved.

## Data tiers

| Tier | Meaning | Permitted claim |
|---|---|---|
| `TIER_0_OFFICIAL_PUBLIC` | official release, filing or methodology | high factual confidence subject to revision/timestamp risk |
| `TIER_1_PUBLIC_MARKET` | observable curve, price, volume, OI or exchange data | high observation confidence; causal inference remains conditional |
| `TIER_2_REPUTABLE_INSTITUTIONAL_PUBLIC` | public institutional research/aggregation | source-method dependent |
| `TIER_3_LICENSED` | licensed institutional dataset | according to history and methodology |
| `TIER_4_PROPRIETARY_INTERNAL` | direct internal book or flow | high for the observed field, not automatically generalizable |
| `TIER_5_UNOBSERVABLE_OR_UNKNOWN` | unavailable construct | no point claim; proxy or unknown only |

## Default confidence caps

- Exact dealer positioning from public price/options proxies: maximum 55.
- Flow exhaustion without directional flow or position evidence: maximum 50.
- Historical intraday consumption without consensus and contemporaneous curve: maximum 45.
- Repricing completion without defensible counterfactual range: maximum 50.
- Unscheduled headline with unresolved earliest timestamp: maximum 60.
- Causal leader inferred only from simultaneous daily closes: maximum 45.

These are governance defaults, not empirical constants. Override requires evidence and a methodology version.

## Canonical dependencies

- [[81 Scientific QA and Certification Framework/13 Contradiction Unknowns and Missing-Data Gate]]
- [[65 Source Registry and Claim Lineage/00 Source Registry MOC]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.
