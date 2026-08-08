---
title: "Source Hierarchy and Load-Bearing Eligibility"
type: canonical-science-note
status: canonical
version: 17.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [v17, sources, provenance, evidence]
---

# Source hierarchy

D1 distinguishes *source usefulness* from *load-bearing eligibility*. A source can be useful context without being strong enough to support a decisive claim.

## Canonical source tiers

1. `OFFICIAL_PRIMARY` — issuing statistical agency, central bank, regulator, issuer, treasury/ministry or other first-party statutory source.
2. `OFFICIAL_SECONDARY` — official republication or official analytical layer that is not the original release.
3. `EXCHANGE_ADMINISTRATOR` — exchange, benchmark administrator, index provider or market infrastructure operator for its own data/rules.
4. `REGULATED_FILING` — legally filed disclosure.
5. `INSTITUTIONAL_PUBLIC` — high-quality public institutional research or published dataset with transparent methodology.
6. `LICENSED` — licensed/proprietary source with valid access and identifiable dataset/version.
7. `PUBLIC_PROXY` — public data intentionally used as a proxy for a less observable target.
8. `MEDIA_CONFIRMATION` — reputable media used for confirmation/context when primary material is delayed or unavailable.
9. `UNVERIFIED` — unattributed, unverifiable, social or otherwise non-auditable claim.

## Load-bearing contract

- Tiers 1–6 may be load-bearing if timestamp, identity and claim fit are adequate.
- `PUBLIC_PROXY` may support a decision only with an explicit proxy label, confidence cap and no claim of equivalence to the target variable.
- `MEDIA_CONFIRMATION` is normally supporting, not sole decision-critical evidence.
- `UNVERIFIED` may never be load-bearing.

Source quality cannot repair temporal invalidity. A perfect official source published after the historical cutoff is still unavailable to that cutoff.
