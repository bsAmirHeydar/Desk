---
title: "Surprise Materiality and Expectation Revision"
type: canonical-method
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# Surprise Materiality and Expectation Revision

## Decision purpose

Separate raw surprise from economic materiality and expectation-path revision. This prevents headline arithmetic from substituting for a causal update.

## Governing distinctions

- Observation-minus-consensus is only the first layer.
- Composition and revisions can reverse the headline interpretation.
- Materiality is conditional on regime and reaction function.
- The same release can affect an asset through opposing discount-rate and cash-flow channels.

## Operating method

1. Freeze consensus and market-implied state at T-minus.
2. Build a multidimensional surprise vector.
3. Translate components into state-path revisions.
4. Test reaction-function and rival-model implications.
5. Map the revision to asset-specific channels and horizons.

## Required outputs

- `pre_catalyst_expectation`
- `surprise_vector`
- `materiality_class`
- `expectation_revision_vector`
- `reaction_function_update`
- `revision_uncertainty`

## Failure modes and controls

- **Failure:** Using final revised data as the release  
  **Control:** Store first-release and revision chains separately.
- **Failure:** Z-score interpreted as economic importance  
  **Control:** Add regime and transmission relevance.
- **Failure:** Consensus unavailable but numeric surprise reported  
  **Control:** Use unknown state and confidence cap.

## Surprise vector

A release is decomposed into headline, core, composition, revisions, breadth, trend, level, rate-of-change and reaction-function relevance. The expectation must be recovered at the cutoff; a later survey revision is inadmissible. When consensus is unavailable, use `EXPECTATION_UNRECOVERABLE`.

Materiality asks how strongly the observation changes the state path. A statistically large miss can be economically small when volatile, offsetting or outside the reaction function. A small headline miss can be powerful when composition changes persistence or terminal outcomes.

## Canonical dependencies

- [[00 Core Standards/05 Expectations Pricing and Distribution Gap]]
- [[88 Hybrid Daily Session Event Fundamental State Engine/04 Scheduled and Unscheduled Event Micro-Windows]]

## V11 authority

This note governs its stated object for methodology version `11.0.0`. Earlier notes remain valid where they do not conflict. Scores remain ordinal unless the record explicitly declares an empirically calibrated estimand and validation evidence.

## V21 market-surprise extension
V21 requires two separate objects: **economic surprise** and **market surprise**. The point-in-time expectation stack may include official consensus, survey dispersion, market-implied pricing, alternative/whisper expectations, positioning expectation, option-implied event distribution, prior trend and revision expectation. Economic surprise can differ in sign from market surprise. When the expectation baseline is not recoverable, numeric surprise is prohibited.
