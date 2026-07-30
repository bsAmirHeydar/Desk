---
title: "March 2020 Treasury Dysfunction"
type: golden-benchmark-reference
status: internal-reference
version: 10.0.0
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [fundamental-only, benchmark, historical-dossier]
benchmark_id: "GB-14"
external_review: pending
cutoff: "2020-03-12 08:00 America/New_York"
reference_answer: executed-internal
---

# March 2020 Treasury Dysfunction

## Benchmark object

- **Cutoff:** 2020-03-12 08:00 America/New_York
- **Object:** Treasury, repo and leveraged basis
- **Primary mechanism:** Safe-asset liquidation, dealer capacity, margin and policy facilities
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

A high-scoring answer must explain **Safe-asset liquidation, dealer capacity, margin and policy facilities** without treating the target-market move as proof. It must distinguish accounting identities from estimated behavior, map the constrained balance sheet or physical system, and explain why the mechanism could amplify, reverse or expire.

## Mandatory evidence ledger

| ID | Claim family | Source | Locator | Limitation |
|---|---|---|---|---|
| E01 | Measurement and institutional mechanism | [[65 Source Registry and Claim Lineage/NYFED_SOFR — New York Fed — SOFR|NYFED_SOFR — New York Fed — SOFR]] | SOFR methodology, rate publication and repo reference-rate documentation | Confirm coverage, timing, revisions and jurisdiction before inference. |
| E02 | Measurement and institutional mechanism | [[65 Source Registry and Claim Lineage/NYFED_DEALERS — New York Fed — Primary Dealer Statistics|NYFED_DEALERS — New York Fed — Primary Dealer Statistics]] | Use the exact table, chapter, filing item, series or methodology section relevant to the claim. | Confirm coverage, timing, revisions and jurisdiction before inference. |
| E03 | Measurement and institutional mechanism | [[65 Source Registry and Claim Lineage/FED_H41 — Federal Reserve — H.4.1|FED_H41 — Federal Reserve — H.4.1]] | H.4.1 factors affecting reserve balances | Confirm coverage, timing, revisions and jurisdiction before inference. |



## Executed internal reference answer

The March 2020 Treasury dossier identifies a dash for cash, leveraged relative-value unwinds, foreign and domestic liquidity needs and limited dealer balance-sheet capacity. Even the safest securities can become difficult to intermediate when many holders seek cash simultaneously. The reference answer distinguishes credit safety from market liquidity and maps official purchases and facilities to functioning rather than a change in Treasury creditworthiness.

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

### Consolidated legacy note: March 2020 Treasury Dysfunction and Basis Unwind

Sovereign-bond analysis combines expected policy, inflation compensation, term premium, fiscal supply, investor base, collateral value, and market liquidity.

For **March 2020 Treasury Dysfunction and Basis Unwind**, the relevant institutional domain is **orientation**: the institutional research process, its roles, information boundaries, controls, and decision handoffs. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

For **March 2020 Treasury Dysfunction and Basis Unwind**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

### Consolidated legacy note: US Treasury Futures Institutional Driver Book

For **US Treasury Futures Institutional Driver Book**, the relevant institutional domain is **equity**: equity value as expected cash flows, discount rates, risk premia, capital allocation, competitive structure, and index flow. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

For **US Treasury Futures Institutional Driver Book**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

### Consolidated legacy note: 17 Treasury Futures CTD Implied Repo Net Basis and Delivery Options

Treasury futures delivery economics compare eligible cash bonds after conversion factors, financing, coupon cash flows, delivery options, and hedge ratios. Secured funding prices cash, collateral scarcity, counterparty balance sheet, settlement demand, and regulatory capacity.

For **17 Treasury Futures CTD Implied Repo Net Basis and Delivery Options**, the relevant institutional domain is **nowcast**: point-in-time measurement, forecasting, causal inference, model validation, data lineage, and research deployment. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

For **17 Treasury Futures CTD Implied Repo Net Basis and Delivery Options**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

### Monograph implementation requirements for 17 Treasury Futures CTD Implied Repo Net Basis and Delivery Options

Provide a formal variable table, derivation or pseudocode, synthetic tests, point-in-time reconstruction, benchmarks and ablation, parameter uncertainty, regime stability, computational profile, cost/capacity translation, and a monitored model card. A second researcher must reproduce **17 Treasury Futures CTD Implied Repo Net Basis and Delivery Options** from hash-addressed artifacts.

Treasury futures allow delivery of an eligible basket. The short selects the security and timing subject to exchange rules. Each bond has a conversion factor \(CF_i\).

Net basis adjusts for financing carry, coupon cash flows and delivery timing. Sign conventions must be documented because dealer systems differ.

The implied repo rate equates buying the bond, financing it, receiving interim coupons and delivering into futures. The production engine must use actual settlement dates, accrued interest, coupon reinvestment assumptions, day-count conventions and delivery dates.

The cheapest-to-deliver security maximizes implied repo or minimizes net basis under the declared convention.

Value arises from quality, timing, end-of-month and wildcard options. A static CTD calculation may fail when yield levels or curve slopes shift. Compute switch boundaries and scenario CTD across rate shocks.

Use DV01 or key-rate duration rather than face value. Conversion-factor hedges are approximate. Residual curve, convexity and funding risks remain.

Observed basis reflects repo rates, haircuts, specialness, capital and leverage constraints, dealer balance sheets, futures margin and asset-manager demand. A wide basis is not a free arbitrage when financing and balance-sheet costs are binding.

Store historical contract specifications, baskets, conversion factors, first notice and delivery dates. Reconcile cash prices, accrued interest and futures settlement. Unit-test the engine against exchange examples and independent dealer calculations.

### Consolidated legacy note: Fiscal Policy, Treasury Supply, and Fiscal Impulse

This material survived consolidation because it contains subject-specific instruction for **Fiscal Policy, Treasury Supply, and Fiscal Impulse**, not the former repeated institutional wrapper.

Fiscal policy changes aggregate demand through spending, taxes, transfers, subsidies, and public investment. Debt management changes the quantity, maturity, and ownership of sovereign securities supplied to markets.

The market does not trade the variable in isolation. It trades how the variable changes expected policy, cash flows, default risk, risk premia, and relative returns.

- Budget balance and cyclically adjusted fiscal stance.
- Composition and timing of spending and taxes.
- Automatic stabilizers.
- Debt issuance and maturity mix.
- Treasury cash balance.
- Central-bank holdings and quantitative tightening.
- Domestic and foreign investor demand.
- Interest expense and fiscal credibility.
- Political deadlines, shutdowns, and debt-limit constraints.

- Budget announcements and legislation.
- Treasury borrowing estimates and quarterly refunding.
- Auction calendar and issuance composition.
- Tax dates and large spending dates.
- Debt-limit and shutdown timelines.

- Daily Treasury Statement cash flows.
- Auction results.
- Government consumption and transfers.
- Fiscal impulse estimates.

- Long-end yields and term premium.
- Swap spreads and auction performance.
- Dollar response to growth versus credibility.
- Banks and duration-sensitive equities.

1. **Level** — where the variable stands.
2. **Momentum** — whether it is improving or deteriorating.
3. **Breadth** — how widely the change is distributed.
4. **Quality** — whether the composition is durable.
5. **Revision risk** — how much history may change.
6. **Expectation gap** — what was already priced.
7. **Policy relevance** — whether the reaction function changes.
8. **Horizon** — when the impact should appear.

- Fiscal expansion can support growth and earnings while raising inflation and yields.
- Large duration supply can raise term premium and tighten financial conditions.
- Fiscal credibility concerns can weaken bonds and sometimes the currency.
- Tax and spending flows can alter near-term liquidity.
- Debt-limit episodes can distort bills, cash balances, and money markets.

For day trading, distinguish macro fiscal news from Treasury-market supply events. Auction weakness or a refunding shift may hit long-end yields without changing near-term policy. That can pressure Nasdaq and gold through real yields even if growth data are unchanged. Watch the long end, curve shape, dollar, and equity duration.

The daily objective is not to forecast the next data print from scratch. It is to know which outcome would force the largest repricing and which cross-asset market should confirm first.

For swings, estimate fiscal impulse, financing needs, issuance composition, and interaction with quantitative tightening. A supply-driven yield thesis differs from a growth-driven one and may favor curve or duration expressions.

A swing thesis should survive normal intraday noise. It needs a multi-session pricing gap, a catalyst sequence, and a clearly separate overnight invalidation.

- Treating deficits as immediate bearish signals.
- Ignoring spending composition.
- Confusing gross issuance with net duration supply.
- Reading bid-to-cover without historical and issue context.
- Assuming fiscal expansion is unambiguously bullish.
- Ignoring the Treasury cash balance and settlement timing.
- Using political headlines without operational timelines.

- Is fiscal policy adding to or subtracting from demand?
- Who receives the spending and with what multiplier?
- How much duration supply must the market absorb?
- Is the yield move term-premium-led?
- Are auctions clearing with concession or stress?
- Does the fiscal path threaten credibility or merely support growth?
- What is the interaction with central-bank balance-sheet policy?

### Consolidated legacy note: Treasury Auctions and Refunding

This material survived consolidation because it contains subject-specific instruction for **Treasury Auctions and Refunding**, not the former repeated institutional wrapper.

Treasury supply can move rates independently of immediate economic data. For equity day trading, this matters through real yields, term premium, liquidity, and risk appetite.

- auction size and maturity;
- issue versus reopening;
- when-issued yield;
- stop-through or tail;
- bid-to-cover;
- indirect, direct, and dealer participation;
- concession before auction;
- post-auction price behavior;
- refunding composition;
- expected future net issuance;
- bill versus coupon supply;
- cash-balance and money-market interactions.

```text
More duration supply / weaker demand
→ higher term premium or yields
→ tighter financial conditions
→ pressure on duration equities and sometimes gold
```

- large concession can make an auction look strong;
- bid-to-cover is not directly comparable across all auctions;
- dealer share may reflect mechanics;
- a tail can reverse if macro demand dominates;
- bill issuance can interact differently with liquidity than coupon issuance.

- maturity and size;
- recent comparable auctions;
- current volatility;
- concession;
- foreign/real-money demand context;
- dealer balance-sheet conditions;
- data or central-bank events nearby;
- equity sensitivity to the current yield regime.

1. Compare stop with when-issued level.
2. Examine participation composition.
3. Observe immediate and 15–30 minute rate behavior.
4. Check real yields and curve.
5. Check USD and NQ/ES response.
6. Determine whether the result changes the daily driver or is absorbed.

Quarterly refunding can affect the expected maturity composition of supply and therefore term premium. The relevant question is not only total borrowing, but **who must absorb which duration and when**.

- U.S. Treasury auctions: https://home.treasury.gov/resource-center/data-chart-center/quarterly-refunding
- Treasury auction data: https://treasurydirect.gov/auctions/announcements-data-results/
- Daily Treasury Statement: https://fiscaldata.treasury.gov/datasets/daily-treasury-statement/

### Consolidated legacy note: Treasury Futures Basis and Cheapest-to-Deliver

Treasury futures delivery economics compare eligible cash bonds after conversion factors, financing, coupon cash flows, delivery options, and hedge ratios. Sovereign-bond analysis combines expected policy, inflation compensation, term premium, fiscal supply, investor base, collateral value, and market liquidity.

For **Treasury Futures Basis and Cheapest-to-Deliver**, the relevant institutional domain is **rates**: the path of policy rates, sovereign cash flows, duration supply, inflation compensation, collateral, funding, and term risk. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

For **Treasury Futures Basis and Cheapest-to-Deliver**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

### Consolidated legacy note: Treasury Auctions Refunding and Issuance Composition

Secured funding prices cash, collateral scarcity, counterparty balance sheet, settlement demand, and regulatory capacity. Fiscal analysis links primary balances, interest expense, maturity structure, Treasury cash management, issuance composition, and private-sector absorption.

For **Treasury Auctions Refunding and Issuance Composition**, the relevant institutional domain is **rates**: the path of policy rates, sovereign cash flows, duration supply, inflation compensation, collateral, funding, and term risk. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

For **Treasury Auctions Refunding and Issuance Composition**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

### Consolidated legacy note: Treasury Market Depth and Liquidity

For **Treasury Market Depth and Liquidity**, the relevant institutional domain is **microstructure**: how information and forced demand meet liquidity, dealer balance sheets, order books, derivatives hedging, and execution constraints. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

For **Treasury Market Depth and Liquidity**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Scoring status

This packet is an **internal golden reference**, not an external scientific certification. External review remains pending. A report is compared against the mechanism key, admissible evidence set and failure deductions; prose similarity is irrelevant.
