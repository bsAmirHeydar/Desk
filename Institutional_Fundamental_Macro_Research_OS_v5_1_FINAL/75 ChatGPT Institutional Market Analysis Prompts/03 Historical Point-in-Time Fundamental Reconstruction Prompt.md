---
title: "03 Historical Point-in-Time Fundamental Reconstruction Prompt"
type: production-prompt
status: evergreen
version: 10.4.0
created: 2026-07-29
updated: 2026-07-30
language: en
---
# 03 Historical Point-in-Time Fundamental Reconstruction Prompt

## V9 Canonical Retrieval Gate

Before external research, read [[84 Canonical Retrieval Evidence and Version Control/02 Staged Retrieval and Context-Budget Protocol]] and [[82 Canonical Institutional Fundamental Research Library/00 Canonical Institutional Fundamental Research Library MOC]]. Retrieve one direct canonical monograph and no more than six dependency monographs before using supporting legacy notes. The Reading Ledger must explain the causal role of every retrieved note.

Use [[81 Scientific QA and Certification Framework/23 Probability and Scenario Weight Taxonomy]] for every numeric or qualitative probability. Apply [[81 Scientific QA and Certification Framework/22 Weighted Review Rubric and Inter-Rater Protocol]]. The assistant may report INTERNAL QA — FULL or CONDITIONAL; it may not claim external scientific certification.


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

# V8 SCIENTIFIC CERTIFICATION GATE
Before finalizing, open and apply `81 Scientific QA and Certification Framework/00 Scientific QA and Certification Framework MOC`. Run the relevant domain scorecard and benchmark suite. The answer must begin and end with a certification verdict: CERTIFIED — FULL, CERTIFIED — CONDITIONAL, or NOT CERTIFIED. Do not label the answer FULL if any load-bearing claim lacks an exact source locator, current data are stale, historical evidence crosses the cutoff, a material domain was not retrieved, a serious rival model was ignored, or unavailable proprietary information was invented. Include the 60-point certification scorecard and failed gates.
```

> [!important] Fundamental-only boundary
> Price-pattern analysis, indicator rules and chart-trigger instructions are prohibited. Use the Vault's fundamental, macro, valuation, flow, liquidity, market-structure and portfolio methods.

## V10 specialist and evidence gate

After selecting the direct primary canonical monograph, check the specialist registry for a narrower legal, industry, instrument or physical-market dependency. Do not retrieve a broad legacy field guide when a specialist canonical note exists. Probabilities must be labelled as empirically calibrated, model-implied or judgmental scenario weights. Internal QA may be reported; external scientific certification may not be claimed.
# V10.4 hybrid density gate

For multi-day historical windows, event-only output is invalid. Apply `88 Hybrid Daily Session Event Fundamental State Engine/00 Hybrid Daily Session Event Fundamental State Engine MOC.md`. Produce daily baselines, mandatory session reassessments, event micro-windows, state-decay/no-change records, end-of-day attribution and density validation. Preserve the original cutoff discipline at every record.
