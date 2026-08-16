# 04 — Unknown, Freshness, Persistence and Consumption

## Unknown is decomposed
V3 distinguishes current observation, delayed observation, latest-valid release, release-not-due, stale, model-derived, public proxy, paid-only, private-unobservable, fetch failure, parse failure, not-material, not-applicable and true unknown.

This prevents two common errors:

- calling lagged structural data "live" just because it was fetched now;
- calling missing data neutral.

## Freshness != economic persistence
A central-bank purchase series may be low-frequency but economically persistent. A geopolitical headline can be freshly observed but have a short half-life. P02/P03 therefore cannot use one TTL as a substitute for economic persistence.

## Consumption
V3 consumption is defined as a vector: information absorption, expectations repricing, flow propagation, position adjustment, narrative saturation, time decay, reinforcement and contradiction. A human summary (`LOW/PARTIAL/HIGH/EXHAUSTED/...`) may be shown, but an uncalibrated percentage may not.
