---
title: "Incomplete-Data Certification Benchmark"
type: golden-benchmark-reference
status: internal-reference
version: 10.0.0
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [fundamental-only, benchmark, historical-dossier]
benchmark_id: "GB-30"
external_review: pending
cutoff: "2026-07-30 09:00 Europe/Amsterdam"
reference_answer: executed-internal
---

# Incomplete-Data Certification Benchmark

## Benchmark object

- **Cutoff:** 2026-07-30 09:00 Europe/Amsterdam
- **Object:** Hypothetical live market with unavailable proprietary positioning
- **Primary mechanism:** Unknown handling, proxy labeling, confidence caps and certification vetoes
- **Permitted mode:** strict point-in-time reconstruction followed by a separately labelled ex-post audit.

## Reference analytical sequence

1. Resolve the exact institution, security, contract, geography and legal regime.
2. Freeze all evidence at the cutoff and exclude later revisions, retrospective labels and outcomes.
3. Reconstruct observed state, expectations, market pricing, financing constraints and positioning proxies.
4. State the primary causal chain and at least two rivals.
5. Identify the variables or markets expected to lead if the mechanism is correct.
6. Report conclusions separately for event, day, multi-day, tactical, cyclical and structural horizons.
7. Run the claim-evidence, contradiction, unknowns and false-precision gates.

## Golden mechanism key

A high-scoring answer must explain **Unknown handling, proxy labeling, confidence caps and certification vetoes** without treating the target-market move as proof. It must distinguish accounting identities from estimated behavior, map the constrained balance sheet or physical system, and explain why the mechanism could amplify, reverse or expire.

## Mandatory evidence ledger

| ID | Claim family | Source | Locator | Limitation |
|---|---|---|---|---|
| E01 | Measurement and institutional mechanism | [[65 Source Registry and Claim Lineage/FED_MRM_2026 — Federal Reserve Revised Model Risk Management Guidance|Federal Reserve Revised Guidance on Model Risk Management (SR 26-2)]] | SR 26-2 attachment sections on governance, development, validation and controls | Confirm coverage, timing, revisions and jurisdiction before inference. |
| E02 | Measurement and institutional mechanism | [[65 Source Registry and Claim Lineage/BIS — Bank for International Settlements|BIS — Bank for International Settlements]] | Use the exact table, chapter, filing item, series or methodology section relevant to the claim. | Confirm coverage, timing, revisions and jurisdiction before inference. |
| E03 | Measurement and institutional mechanism | [[65 Source Registry and Claim Lineage/SEC_MARKETS — SEC Division of Trading and Markets|SEC_MARKETS — SEC Division of Trading and Markets]] | Use the exact table, chapter, filing item, series or methodology section relevant to the claim. | Confirm coverage, timing, revisions and jurisdiction before inference. |



## Executed internal reference answer

The incomplete-data benchmark is passed by refusing false completeness. The answer must identify which claims cannot be measured, distinguish unavailable from stale or proprietary data, use bounded scenarios, cap confidence and return CONDITIONAL or NOT CERTIFIED where load-bearing evidence is absent. Invented dealer positioning, consensus or precise probabilities are automatic failures.

### Horizon and inference controls

- **Event/day:** identify the immediate information shock, constrained market or balance sheet and the first admissible confirming evidence.
- **Multi-day/tactical:** explain persistence, policy response, funding, positioning and the information expected next.
- **Cyclical/structural:** state whether the event changes the underlying regime or only reveals an existing fragility.
- **Rival model:** preserve at least one mechanism that can explain the same observed move.
- **Ex-post boundary:** later outcomes are used only to evaluate the prior process, not to rewrite the ex-ante information set.

### Reference verdict

This dossier is an internally authored golden mechanism key. It is sufficiently specific for retrieval and scoring, but it is not independently peer reviewed. A benchmark run must record the generated answer, prompt version, retrieved notes, reviewer identities, category scores and adjudicated errors.

## Common failure deductions

- **-20:** uses information, revisions or outcomes unavailable at the cutoff.
- **-15:** fails to resolve the correct instrument, contract, issuer or legal regime.
- **-15:** substitutes a single narrative for rival models.
- **-10:** counts mechanically related market moves as independent evidence.
- **-10:** invents consensus, dealer inventory, positioning or proprietary data.
- **-10:** mixes judgmental scenario weights with empirical probabilities.
- **-10:** omits the strongest contradictory evidence or unknown.
- **-5:** fails to separate horizons, invalidation and expiry.

## Internal reference material

### Consolidated legacy note: 12 Adversarial Incomplete-Data Benchmark

> Answer a question where dealer positions, consensus history or physical stocks are unavailable. The correct output must narrow the conclusion, label proxies and refuse fabricated precision.

- object, cutoff, mode and source freshness;
- Vault Reading Ledger;
- claim-level evidence ledger;
- state and expectations separated;
- at least one primary and two rival causal models when material;
- cross-asset, balance-sheet and institutional transmission;
- horizon-specific conclusions;
- scenarios, tails, contradictions, unknowns and confidence cap;
- certification score and verdict.

The answer fails if it invents unavailable information, omits obvious domains, collapses all horizons, uses secondary summaries instead of primary evidence, or provides a confident direction without reconstructing what was priced.

1. Which conclusion-changing claim has the weakest source?
2. What rival model best explains the same observations?
3. Which variable is being proxied rather than observed?
4. What evidence would reverse the conclusion?
5. What did the report omit because it was inconvenient or inaccessible?

### Consolidated legacy note: Benchmark Query Suites

These suites test whether Vault-based analysis is genuinely complete rather than merely verbose.

- [[01 Live Macro and Equity Index Benchmark]]
- [[02 Live Gold Benchmark]]
- [[03 Live Rates Treasury and Repo Benchmark]]
- [[04 Live FX and Global Dollar Benchmark]]
- [[05 Live Oil Power and Commodities Benchmark]]
- [[06 Corporate Equity and Accounting Benchmark]]
- [[07 Credit Banking Insurance and NBFI Benchmark]]
- [[08 Country Sovereign and Municipal Benchmark]]
- [[09 Event and Policy Benchmark]]
- [[10 Historical Point-in-Time Benchmark]]
- [[11 Portfolio Hidden-Beta Benchmark]]
- [[12 Adversarial Incomplete-Data Benchmark]]
- [[13 Benchmark Scoring Rubric and Regression Standard]]

### Consolidated legacy note: 01 Live Macro and Equity Index Benchmark

> Analyze Nasdaq 100 now across structural, cyclical, multi-day and session horizons. Separate earnings, real yields, policy path, credit, dollar, concentration, volatility and flows. Identify the priced baseline and rival explanations.

### Consolidated legacy note: 02 Live Gold Benchmark

> Analyze gold now. Distinguish real yields, dollar, inflation compensation, central-bank and ETF demand, futures positioning, physical demand, fiscal credibility and geopolitical hedging. Explain horizon conflicts.

### Consolidated legacy note: 03 Live Rates Treasury and Repo Benchmark

> Analyze the U.S. Treasury curve and repo system. Decompose expected policy, term premium, inflation compensation, issuance, investor absorption, dealer balance sheets, collateral and convexity.

### Consolidated legacy note: 04 Live FX and Global Dollar Benchmark

> Analyze EURUSD or a selected pair using both country systems, policy paths, external accounts, valuation, carry, global dollar funding, basis, reserve flows and intervention risk.

### Consolidated legacy note: 05 Live Oil Power and Commodities Benchmark

> Analyze WTI or power using physical balances, inventories, refinery or grid constraints, curves, location/quality basis, weather, logistics, producer/consumer hedging and policy.

### Consolidated legacy note: 06 Corporate Equity and Accounting Benchmark

> Analyze a public company using filings, segment economics, accounting quality, cash flow, ROIC, capital allocation, debt, valuation, industry structure and macro sensitivities.

## Scoring status

This packet is an **internal golden reference**, not an external scientific certification. External review remains pending. A report is compared against the mechanism key, admissible evidence set and failure deductions; prose similarity is irrelevant.
