---
title: "03 Historical Point-in-Time Fundamental Reconstruction Prompt"
type: production-prompt
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
---
# 03 Historical Point-in-Time Fundamental Reconstruction Prompt

```text
You are reconstructing an institutional fundamental decision at a historical cutoff. The attached Vault ZIP is mandatory.

# INPUT
MARKET: [required]
TRADE_VEHICLE: [optional]
ANALYSIS_CUTOFF: [required, exact timestamp and timezone]
PRIMARY_HORIZON: [ALL | STRUCTURAL | CYCLICAL | TACTICAL | 2-10D | INTRADAY | EVENT]
PORTFOLIO_CONTEXT_AT_CUTOFF: [optional]
SPECIAL_QUESTION: [optional]
EX_POST_AUDIT: [NO | YES]
OUTPUT_LANGUAGE: [Persian | English]

# STRICT INFORMATION BOUNDARY
Use only information published and operationally available by the cutoff. Do not use later revisions, later filings, future index constituents, future contract specifications, later outcomes, later commentary or knowledge of the subsequent path in the reconstructed view.

# FUNDAMENTAL-ONLY BOUNDARY
Do not use retrospective non-fundamental price-pattern methods. Historical prices may be used only as contemporaneous market-implied information, valuation, response, volatility, liquidity, basis, cost or outcome measurements.

# REQUIRED WORK
1. Read the Vault standards, historical laboratory, source registry, relevant driver and country books, model monographs and asset-engine specification.
2. Build an admissible-information ledger with publication and desk-availability timestamps.
3. Reconstruct first-release data, consensus distribution, curves, options, positioning proxies, physical balances and portfolio constraints available at the cutoff.
4. Separate unavailable evidence and state the resulting confidence cap.
5. Estimate states and pricing gaps by horizon.
6. Build primary and rival causal models.
7. Produce scenarios, expected half-life, decision state, invalidation and expiry without observing the outcome.
8. Freeze the reconstructed view.
9. Only if EX_POST_AUDIT=YES, add a separately labeled ex-post section that evaluates subsequent outcomes, revisions, attribution and counterfactuals. Never edit the frozen ex-ante record.

# OUTPUT
- Reconstruction identity and cutoff
- Vault Reading Ledger
- Admissible Information Ledger
- Vintage and survivorship audit
- Claim–Evidence Ledger
- Multihorizon fundamental state
- Historical market-implied baseline
- Pricing gap and causal models
- Scenario distribution
- Fundamental decision state by horizon
- Invalidation, expiry and unknowns
- Optional separated ex-post audit
- Machine-readable point-in-time context object
```

> [!important] Fundamental-only boundary
> Price-pattern analysis, indicator rules and chart-trigger instructions are prohibited. Use the Vault's fundamental, macro, valuation, flow, liquidity, market-structure and portfolio methods.
