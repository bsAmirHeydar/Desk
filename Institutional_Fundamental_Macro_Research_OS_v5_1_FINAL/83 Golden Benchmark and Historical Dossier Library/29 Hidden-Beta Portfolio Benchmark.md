---
title: "Hidden-Beta Portfolio Benchmark"
type: golden-benchmark-reference
status: internal-reference
version: 10.0.0
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [fundamental-only, benchmark, historical-dossier]
benchmark_id: "GB-29"
external_review: pending
cutoff: "2022-09-13 08:30 America/New_York"
reference_answer: executed-internal
---

# Hidden-Beta Portfolio Benchmark

## Benchmark object

- **Cutoff:** 2022-09-13 08:30 America/New_York
- **Object:** Long growth equities, long bonds, long gold and short USD portfolio
- **Primary mechanism:** Shared real-rate, dollar, liquidity and convexity exposures
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

A high-scoring answer must explain **Shared real-rate, dollar, liquidity and convexity exposures** without treating the target-market move as proof. It must distinguish accounting identities from estimated behavior, map the constrained balance sheet or physical system, and explain why the mechanism could amplify, reverse or expire.

## Mandatory evidence ledger

| ID | Claim family | Source | Locator | Limitation |
|---|---|---|---|---|
| E01 | Measurement and institutional mechanism | [[65 Source Registry and Claim Lineage/FED_FOMC — Federal Reserve — FOMC|FED_FOMC — Federal Reserve — FOMC]] | FOMC statement, minutes, SEP, transcript when available, and Implementation Note | Confirm coverage, timing, revisions and jurisdiction before inference. |
| E02 | Measurement and institutional mechanism | [[65 Source Registry and Claim Lineage/NYFED_TERM_PREMIA — New York Fed — Term Premia|NYFED_TERM_PREMIA — New York Fed — Term Premia]] | ACM Treasury term-premia estimates and methodology | Confirm coverage, timing, revisions and jurisdiction before inference. |
| E03 | Measurement and institutional mechanism | [[65 Source Registry and Claim Lineage/CBOE_VIX — Cboe VIX Methodology|CBOE_VIX — Cboe VIX Methodology]] | VIX methodology, option selection and variance calculation | Confirm coverage, timing, revisions and jurisdiction before inference. |



## Executed internal reference answer

The hidden-beta portfolio benchmark requires decomposing apparently different positions into common exposures such as lower real yields, weaker dollar, credit easing, equity duration, commodity demand or volatility selling. Correlations are conditional and can rise under stress. A correct answer reports gross and net factor exposure, nonlinear payoffs, funding, liquidity and scenarios rather than counting position names as diversification.

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

### Consolidated legacy note: 11 Portfolio Hidden-Beta Benchmark

> Decompose a portfolio into growth, inflation, rates, dollar, credit, liquidity, commodity, volatility and nonlinear exposures; identify duplicated theses and scenario concentration.

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

### Consolidated legacy note: Portfolio Fundamental Exposure and Hidden-Beta Audit Prompt

~~~text
Act as an institutional portfolio fundamental-risk, hidden-beta and catalyst-concentration audit desk. The complete Institutional Fundamental Macro Research OS Vault ZIP is uploaded. Open and use the portfolio construction, factor risk, liquidity, stress, scenario, market driver, country, options/flow and execution-handoff notes.

INPUT
PORTFOLIO: [positions, direction, size/weight/risk units, vehicle and currency]
MODE: [CURRENT | HISTORICAL]
AS_OF: [NOW | YYYY-MM-DD HH:MM:SS TIMEZONE]
HORIZON: [INTRADAY | 2-10D | WEEKS | MONTHS]
RISK_LIMITS: [optional]
KNOWN_HEDGES: [optional]
OUTPUT_LANGUAGE: [English/Persian]
SPECIAL_QUESTION: [optional]

For current mode, verify live/current facts and catalysts. For historical mode, freeze the information set.

REQUIRED METHOD
1. Open the Vault and list the material notes used.
2. Resolve every position's true economic exposure and vehicle-specific basis/carry/convexity.
3. Map each position to common fundamental drivers:
   - growth;
   - inflation;
   - policy path;
   - real yields;
   - term premium;
   - USD/global liquidity;
   - credit/risk premium;
   - commodity physical balance;
   - volatility/correlation;
   - country/political risk;
   - positioning/systematic flow;
   - liquidity and funding.
4. Identify false diversification, duplicated thesis, nonlinear exposure and hidden short-vol or short-liquidity risk.
5. Build the catalyst calendar and identify simultaneous event concentration.
6. Stress Base, growth shock, inflation shock, policy shock, fiscal/term-premium shock, USD funding shock, credit shock, volatility/liquidity shock and market-specific tails.
7. Evaluate hedges for basis risk, timing mismatch, convexity, carry and failure under stress.
8. Recommend keep, reduce, rebalance, hedge, replace or no action. Do not optimize using false precision when position data are incomplete.

OUTPUT
1. Portfolio verdict
2. Timestamp/cutoff and data-quality statement
3. Vault research route
4. Position-by-position driver map
5. Aggregate factor and hidden-beta map
6. Correlation versus causal concentration
7. Catalyst concentration calendar
8. Liquidity, financing, convexity and gap-risk audit
9. Scenario stress table
10. Hedge effectiveness and basis-risk table
11. Recommended risk actions with priorities
12. Portfolio-level permission and kill-switches
13. Claim-evidence ledger and unknowns
14. YAML portfolio context object

> [!important] Fundamental-only boundary
> Price-pattern analysis, indicator rules and chart-trigger instructions are prohibited. Use the Vault's fundamental, macro, valuation, flow, liquidity, market-structure and portfolio methods.

### Consolidated legacy note: 1987 Crash Portfolio Insurance and Liquidity

**1987 Crash Portfolio Insurance and Liquidity** is a research object inside the institutional research process, its roles, information boundaries, controls, and decision handoffs. The analyst must isolate the measurable state, the expectation already embedded in prices, the mechanism connecting them, and the horizon on which that inference can survive.

For **1987 Crash Portfolio Insurance and Liquidity**, the relevant institutional domain is **orientation**: the institutional research process, its roles, information boundaries, controls, and decision handoffs. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

For **1987 Crash Portfolio Insurance and Liquidity**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

### Consolidated legacy note: 23 Portfolio Optimization Robust Risk Budgets and Scenario P&L

**23 Portfolio Optimization Robust Risk Budgets and Scenario P&L** is a research object inside point-in-time measurement, forecasting, causal inference, model validation, data lineage, and research deployment. The analyst must isolate the measurable state, the expectation already embedded in prices, the mechanism connecting them, and the horizon on which that inference can survive.

For **23 Portfolio Optimization Robust Risk Budgets and Scenario P&L**, the relevant institutional domain is **nowcast**: point-in-time measurement, forecasting, causal inference, model validation, data lineage, and research deployment. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

For **23 Portfolio Optimization Robust Risk Budgets and Scenario P&L**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

### Monograph implementation requirements for 23 Portfolio Optimization Robust Risk Budgets and Scenario P&L

Provide a formal variable table, derivation or pseudocode, synthetic tests, point-in-time reconstruction, benchmarks and ablation, parameter uncertainty, regime stability, computational profile, cost/capacity translation, and a monitored model card. A second researcher must reproduce **23 Portfolio Optimization Robust Risk Budgets and Scenario P&L** from hash-addressed artifacts.

$$
\max_w\; E[R_p]-\frac{\lambda}{2}w^\top\Sigma w-C(w)-L(w)
$$

subject to leverage, liquidity, concentration, legal, funding and scenario-loss constraints. \(C(w)\) represents transaction and financing costs; \(L(w)\) can penalize illiquidity or model uncertainty.

Expected returns and covariance matrices are unstable. Use shrinkage, factor structures, Bayesian estimates, robust optimization or resampled sensitivity. Report how allocations change under plausible input perturbations.

Volatility contributions are not sufficient when payoffs are nonlinear or correlations change. Combine factor, scenario, expected-shortfall, liquidity and convexity budgets. Hidden exposures are aggregated by causal driver, not ticker count.

Scenarios reprice curves, spreads, FX, commodities, options, funding and correlations consistently. Include first-order and nonlinear effects, margin, haircut, basis and exit-cost changes.

Estimate participation, impact, liquidation horizon and stressed depth by instrument. Concentration limits use the worse of normal and stressed capacity. Hedge liquidity is evaluated jointly with the asset.

Separate research expected return, portfolio construction and independent risk approval. Overrides require a reason, owner, expiry and later attribution. Optimizer outputs are proposals, not authority.

Compare with equal risk, simple factor-balanced and policy portfolios. Evaluate turnover, cost, drawdown, tail loss, stability, capacity and performance under input error.

### Consolidated legacy note: 09 Portfolio Liquidity and Implementation Governance

A correct fundamental view can be an unacceptable portfolio decision. Research must be translated through portfolio exposure, liquidity, financing, convexity, correlation, basis and scenario loss.

- duration and key-rate exposure;
- real-yield and inflation exposure;
- dollar and cross-currency exposure;
- growth, earnings and credit beta;
- commodity and physical-balance exposure;
- volatility, skew and convexity exposure;
- liquidity and funding dependence;
- country, legal and sanctions exposure;
- crowded-flow and deleveraging exposure;
- catalyst and gap concentration.

- purity of the intended factor;
- carry and financing;
- convexity and gap behavior;
- liquidity and market depth;
- basis and hedge risk;
- transaction cost and impact;
- legal, operational and tax constraints;
- capacity and crowdedness;
- exit feasibility under stress.

- research-confidence budget;
- scenario-loss limit;
- liquidity-adjusted capacity;
- concentration limit;
- funding and margin headroom;
- model-risk cap;
- governance approval level.

Confidence is not leverage. A highly confident but negatively convex or illiquid expression may deserve smaller size than a lower-confidence, liquid and bounded-loss expression.

Stress bid-ask spreads, depth, market impact, financing, haircuts, basis, correlation and execution delay. Include the possibility that the hedge becomes less liquid or more correlated precisely when needed.

- information invalidation;
- scenario-loss limit;
- liquidity contingency;
- time expiry;
- catalyst completion rule;
- financing or carry limit;
- escalation path if exit is impaired.

### Consolidated legacy note: Portfolio Manager Decision Rights

**Portfolio Manager Decision Rights** is a research object inside the institutional research process, its roles, information boundaries, controls, and decision handoffs. The analyst must isolate the measurable state, the expectation already embedded in prices, the mechanism connecting them, and the horizon on which that inference can survive.

For **Portfolio Manager Decision Rights**, the relevant institutional domain is **orientation**: the institutional research process, its roles, information boundaries, controls, and decision handoffs. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

For **Portfolio Manager Decision Rights**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

### Consolidated legacy note: Regime-Conditional Portfolio Construction

Regime models represent persistent but uncertain state differences in means, variances, correlations, elasticities, and policy responses.

For **Regime-Conditional Portfolio Construction**, the relevant institutional domain is **portfolio**: capital allocation across uncertain scenarios, correlated drivers, liquidity constraints, convex payoffs, and institutional survival limits. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

$$
P(S_t|I_t)\propto P(y_t|S_t)\sum_i p_{is}P(S_{t-1}=i|I_{t-1})
$$

For **Regime-Conditional Portfolio Construction**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

### Consolidated legacy note: Portfolio-Level Catalyst Map

**Portfolio-Level Catalyst Map** is a research object inside capital allocation across uncertain scenarios, correlated drivers, liquidity constraints, convex payoffs, and institutional survival limits. The analyst must isolate the measurable state, the expectation already embedded in prices, the mechanism connecting them, and the horizon on which that inference can survive.

For **Portfolio-Level Catalyst Map**, the relevant institutional domain is **portfolio**: capital allocation across uncertain scenarios, correlated drivers, liquidity constraints, convex payoffs, and institutional survival limits. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

For **Portfolio-Level Catalyst Map**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Scoring status

This packet is an **internal golden reference**, not an external scientific certification. External review remains pending. A report is compared against the mechanism key, admissible evidence set and failure deductions; prose similarity is irrelevant.
