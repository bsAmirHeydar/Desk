# TF2 — True-Forward Evidence Review & Calibration Gate

TF2 reviews only chronology-valid, seal-valid forward evidence and never promotes M1 or APL-A. Historical replay, synthetic validation, and walk-forward evidence remain useful but cannot be counted as `VALID_TRUE_FORWARD`.

A TF2 review freezes a UTC cutoff and creates an immutable review snapshot under the mutable scientific evidence store. Records after the cutoff are excluded. Outcomes linked after the cutoff are not credited to that review. The review preserves component versions and does not rewrite source commitments, outcomes, or human reviews.

TF1.0.1 adds a forward-commitment repair: new commitments carry immutable M1 findings plus APL-A telemetry and lens output payload snapshots. Existing TF1.0.0 commitments remain valid when their seals and chronology pass, but their detailed M1/APL reviewability is explicitly limited rather than retrospectively enriched.

Readiness is decomposed by capability/lens, market, research class, horizon, version, and review labels. No Taleb score, M1 score, APL score, or combined confidence score is created. APL-A remains `SHADOW_ONLY`; broker authority remains `NONE`; APL-B is not implemented.
