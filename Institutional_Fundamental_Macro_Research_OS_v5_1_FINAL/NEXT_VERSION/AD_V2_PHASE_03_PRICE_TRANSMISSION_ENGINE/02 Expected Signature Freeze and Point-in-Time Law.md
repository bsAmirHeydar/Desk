---
title: "Expected Signature Freeze and Point-in-Time Law"
type: scientific-contract
status: shadow-development
---
# Expected Signature Freeze

A transmission test is invalid if the expected response is invented after the response is observed.

P03 therefore requires an **Expected Signature** frozen before the actual response window begins.

## Required ordering

`Pressure as-of <= Expected Signature declared-at <= Response Window start < Response Window end`

The Expected Signature must carry the exact P02 Pressure fingerprint from which it was formed.

## Expected target response

Where defensible, the signature declares:

- target instrument;
- response unit;
- pressure-aligned expected response range;
- minimum material response;
- earliest expected material-response time;
- latest expected-response lag;
- counterfactual method;
- method provenance;
- model/validation reference when empirical status is claimed.

If no defensible magnitude range exists, P03 allows a `DIRECTION_ONLY` expectation. In that case magnitude efficiency and numeric residuals remain unavailable.

## No post-hoc fitting

Forbidden methods include any method whose range was selected after observing the target response, including `POST_HOC_PRICE_FIT` and ex-post best-window selection.

Historical replay must use a signature frozen from the historical information set or a deterministic predeclared policy.
