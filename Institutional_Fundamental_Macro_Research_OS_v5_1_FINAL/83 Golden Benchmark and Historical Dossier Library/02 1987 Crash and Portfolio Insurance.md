---
title: "1987 Crash and Portfolio Insurance"
type: golden-benchmark-reference
status: internal-reference
version: 10.0.0
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [fundamental-only, benchmark, historical-dossier]
benchmark_id: "GB-02"
external_review: pending
cutoff: "1987-10-19 09:30 America/New_York"
reference_answer: executed-internal
---

# 1987 Crash and Portfolio Insurance

## Benchmark object

- **Cutoff:** 1987-10-19 09:30 America/New_York
- **Object:** U.S. equity liquidity and dynamic hedging
- **Primary mechanism:** Valuation, liquidity, portfolio insurance feedback, market making and policy response
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

A high-scoring answer must explain **Valuation, liquidity, portfolio insurance feedback, market making and policy response** without treating the target-market move as proof. It must distinguish accounting identities from estimated behavior, map the constrained balance sheet or physical system, and explain why the mechanism could amplify, reverse or expire.

## Mandatory evidence ledger

| ID | Claim family | Source | Locator | Limitation |
|---|---|---|---|---|
| E01 | Measurement and institutional mechanism | [[65 Source Registry and Claim Lineage/FED_FOMC — Federal Reserve — FOMC|FED_FOMC — Federal Reserve — FOMC]] | FOMC statement, minutes, SEP, transcript when available, and Implementation Note | Confirm coverage, timing, revisions and jurisdiction before inference. |
| E02 | Measurement and institutional mechanism | [[65 Source Registry and Claim Lineage/SEC_MARKETS — SEC Division of Trading and Markets|SEC_MARKETS — SEC Division of Trading and Markets]] | Use the exact table, chapter, filing item, series or methodology section relevant to the claim. | Confirm coverage, timing, revisions and jurisdiction before inference. |
| E03 | Measurement and institutional mechanism | [[65 Source Registry and Claim Lineage/CBOE_VIX — Cboe VIX Methodology|CBOE_VIX — Cboe VIX Methodology]] | VIX methodology, option selection and variance calculation | Confirm coverage, timing, revisions and jurisdiction before inference. |



## Executed internal reference answer

The reference answer distinguishes stretched equity valuation from the crash mechanism. Portfolio-insurance strategies and index-futures arbitrage translated declining prices into additional selling, while limited market-making capacity and order-routing stress reduced liquidity. The Federal Reserve response addressed financial functioning rather than proving a prior macro recession. A correct account treats dynamic hedging as an amplifier, not the sole cause, and distinguishes the one-day market event from the subsequent economic path.

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

### Consolidated legacy note: 1987 Crash Portfolio Insurance and Liquidity

**1987 Crash Portfolio Insurance and Liquidity** is a research object inside the institutional research process, its roles, information boundaries, controls, and decision handoffs. The analyst must isolate the measurable state, the expectation already embedded in prices, the mechanism connecting them, and the horizon on which that inference can survive.

For **1987 Crash Portfolio Insurance and Liquidity**, the relevant institutional domain is **orientation**: the institutional research process, its roles, information boundaries, controls, and decision handoffs. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

For **1987 Crash Portfolio Insurance and Liquidity**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

### Consolidated legacy note: Gold XAU and GC Institutional Driver Book

Gold combines real-rate opportunity cost, currency, monetary/fiscal credibility, reserve demand, ETF/futures flow, physical demand, and convex risk hedging.

For **Gold XAU and GC Institutional Driver Book**, the relevant institutional domain is **equity**: equity value as expected cash flows, discount rates, risk premia, capital allocation, competitive structure, and index flow. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

$$
GoldReturn\approx \beta_r\Delta RealYield+\beta_d\Delta USD+\beta_v\Delta RiskPremium+\varepsilon
$$

For **Gold XAU and GC Institutional Driver Book**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

### Consolidated legacy note: Bitcoin and Crypto Liquidity Driver Book

Crypto fundamentals combine network security and usage, monetary supply, stablecoin and ETF flows, collateral leverage, venue fragmentation, and global liquidity.

For **Bitcoin and Crypto Liquidity Driver Book**, the relevant institutional domain is **equity**: equity value as expected cash flows, discount rates, risk premia, capital allocation, competitive structure, and index flow. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

For **Bitcoin and Crypto Liquidity Driver Book**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

### Consolidated legacy note: 1970s Inflation Regime and Policy Credibility

Inflation analysis separates level, momentum, breadth, persistence, relative-price shocks, margins, wages, rents, and policy-relevant underlying pressure. A reaction function maps the policymaker information set, mandate, risk asymmetry, financial conditions, and institutional constraints into a policy distribution.

For **1970s Inflation Regime and Policy Credibility**, the relevant institutional domain is **orientation**: the institutional research process, its roles, information boundaries, controls, and decision handoffs. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

$$
P(i_{t+1}|I_t)=\sum_s P(i_{t+1}|s,I_t)P(s|I_t)
$$

For **1970s Inflation Regime and Policy Credibility**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

### Consolidated legacy note: 1994 Bond Massacre and Convexity

Fixed-income risk must be represented as price sensitivity to localized curve shocks rather than by notional or maturity alone.

For **1994 Bond Massacre and Convexity**, the relevant institutional domain is **orientation**: the institutional research process, its roles, information boundaries, controls, and decision handoffs. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

For **1994 Bond Massacre and Convexity**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

### Consolidated legacy note: 1997 1998 Asia Russia LTCM and Dollar Funding

Secured funding prices cash, collateral scarcity, counterparty balance sheet, settlement demand, and regulatory capacity.

For **1997 1998 Asia Russia LTCM and Dollar Funding**, the relevant institutional domain is **orientation**: the institutional research process, its roles, information boundaries, controls, and decision handoffs. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

For **1997 1998 Asia Russia LTCM and Dollar Funding**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

### Consolidated legacy note: 2000 Technology Bubble Earnings and Valuation

Equity valuation separates cash-flow expectations, discount-rate path, terminal assumptions, risk premia, capital structure, and per-share dilution. Earnings intelligence reconstructs operational drivers, accounting quality, guidance, consensus dispersion, and the path of revisions rather than trading headline EPS.

For **2000 Technology Bubble Earnings and Valuation**, the relevant institutional domain is **orientation**: the institutional research process, its roles, information boundaries, controls, and decision handoffs. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

$$
EV=\sum_{t=1}^{T}\frac{FCFF_t}{(1+WACC_t)^t}+\frac{TV_T}{(1+WACC_T)^T}
$$

For **2000 Technology Bubble Earnings and Valuation**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

### Consolidated legacy note: 2008 Global Financial Crisis Balance Sheets and Collateral

Secured funding prices cash, collateral scarcity, counterparty balance sheet, settlement demand, and regulatory capacity. Balance-sheet analysis maps operating assets and liabilities, financing, liquidity, duration, contingent claims, and working-capital behavior.

For **2008 Global Financial Crisis Balance Sheets and Collateral**, the relevant institutional domain is **orientation**: the institutional research process, its roles, information boundaries, controls, and decision handoffs. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

For **2008 Global Financial Crisis Balance Sheets and Collateral**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Scoring status

This packet is an **internal golden reference**, not an external scientific certification. External review remains pending. A report is compared against the mechanism key, admissible evidence set and failure deductions; prose similarity is irrelevant.
