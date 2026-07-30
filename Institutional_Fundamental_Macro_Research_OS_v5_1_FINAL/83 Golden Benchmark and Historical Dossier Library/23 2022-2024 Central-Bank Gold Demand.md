---
title: "2022-2024 Central-Bank Gold Demand"
type: golden-benchmark-reference
status: internal-reference
version: 10.0.0
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [fundamental-only, benchmark, historical-dossier]
benchmark_id: "GB-23"
external_review: pending
cutoff: "2024-01-31 00:00 UTC"
reference_answer: executed-internal
---

# 2022-2024 Central-Bank Gold Demand

## Benchmark object

- **Cutoff:** 2024-01-31 00:00 UTC
- **Object:** Official reserve allocation and gold
- **Primary mechanism:** Reserve diversification, sanctions risk, price sensitivity and physical flows
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

A high-scoring answer must explain **Reserve diversification, sanctions risk, price sensitivity and physical flows** without treating the target-market move as proof. It must distinguish accounting identities from estimated behavior, map the constrained balance sheet or physical system, and explain why the mechanism could amplify, reverse or expire.

## Mandatory evidence ledger

| ID | Claim family | Source | Locator | Limitation |
|---|---|---|---|---|
| E01 | Measurement and institutional mechanism | [[65 Source Registry and Claim Lineage/WGC_GDT — World Gold Council Gold Demand Trends|WGC_GDT — World Gold Council Gold Demand Trends]] | Gold Demand Trends tables by sector and region | Confirm coverage, timing, revisions and jurisdiction before inference. |
| E02 | Measurement and institutional mechanism | [[65 Source Registry and Claim Lineage/IMF_BPM7 — IMF Balance of Payments and International Investment Position Manual Seventh Edition|IMF BPM7]] | BPM7 functional categories, financial account, IIP and reserve-asset chapters | Confirm coverage, timing, revisions and jurisdiction before inference. |
| E03 | Measurement and institutional mechanism | [[65 Source Registry and Claim Lineage/WGC_ETF — World Gold Council Gold ETF Data|WGC_ETF — World Gold Council Gold ETF Data]] | Use the exact table, chapter, filing item, series or methodology section relevant to the claim. | Confirm coverage, timing, revisions and jurisdiction before inference. |



## Executed internal reference answer

The central-bank-gold dossier maps reserve diversification, sanctions and geopolitical risk, currency composition, domestic production and reporting opacity. Official-sector purchases are structurally different from leveraged futures demand and may be price insensitive, but reported data can be incomplete or delayed. A correct answer avoids assigning a single motive to all central banks and separates observed purchases from inferred unreported demand.

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

### Consolidated legacy note: Gold XAU and GC Institutional Driver Book

Gold combines real-rate opportunity cost, currency, monetary/fiscal credibility, reserve demand, ETF/futures flow, physical demand, and convex risk hedging.

For **Gold XAU and GC Institutional Driver Book**, the relevant institutional domain is **equity**: equity value as expected cash flows, discount rates, risk premia, capital allocation, competitive structure, and index flow. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

$$
GoldReturn\approx \beta_r\Delta RealYield+\beta_d\Delta USD+\beta_v\Delta RiskPremium+\varepsilon
$$

For **Gold XAU and GC Institutional Driver Book**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

### Consolidated legacy note: Central-Bank Reaction Functions

This material survived consolidation because it contains subject-specific instruction for **Central-Bank Reaction Functions**, not the former repeated institutional wrapper.

A central-bank reaction function is the conditional mapping from economic and financial conditions to policy behavior.

\[
i_t^* =
r_t^*
+
\pi_t
+
a(\pi_t-\pi^*)
+
b(y_t-y_t^*)
+
c(\text{financial stability})
+
d(\text{risk balance})
\]

This is not a literal decision rule. It organizes the variables that influence the policy path.

- the next meeting outcome;
- the path over several meetings;
- the terminal rate;
- the neutral rate;
- balance-sheet policy;
- forward guidance;
- tolerance for inflation overshoot;
- tolerance for labor weakening;
- and willingness to respond to financial stress.

Examples include inflation stability, employment, growth support, exchange-rate stability, or financial stability.

- easing too early;
- tightening too long;
- allowing expectations to de-anchor;
- causing financial instability;
- or losing policy credibility.

Is existing policy restrictive enough? Has tightening reached credit, housing, labor, and demand?

Statements, projections, press conferences, minutes, speeches, and implementation notes can each shift different parts of the curve.

1. **Action shock** — current rate or balance-sheet action.
2. **Path shock** — guidance about future policy.
3. **Information shock** — what the central bank reveals about the economy.
4. **Risk-management shock** — how policymakers weight tails.
5. **Implementation shock** — reserve, liquidity, or market-operation details.

An unchanged rate can be highly hawkish or dovish through the path and information components.

- repeated phrases and wording changes;
- voting distribution;
- projection changes;
- forecast-error tolerance;
- which data policymakers cite;
- whether they focus on levels, momentum, or breadth;
- how they respond to prior surprises;
- and whether market pricing diverges from official guidance.

| Scenario | Action/path | Information signal | First asset | Confirmation |
|---|---|---|---|---|
| Hawkish | higher/longer path | inflation concern | front-end yields up | currency up, duration down |
| Dovish | lower/earlier path | disinflation confidence | front-end yields down | currency down, duration up |
| Hawkish information | rates/yields up with stocks up initially | stronger growth signal | curve and equities | distinguish from pure tightening |
| Dovish information | yields down with stocks down | growth concern | credit/curve | recession interpretation |

The co-movement of rates and equities helps distinguish policy tightening from information about growth, but it is not infallible.

- treating one speech as binding;
- ignoring the voting center;
- reading the dot plot as a promise;
- ignoring the distribution and uncertainty;
- assuming cuts are bullish regardless of why cuts are coming;
- focusing only on the next meeting;
- ignoring balance-sheet policy;
- or forgetting that market pricing can move before official language.

### Consolidated legacy note: Gold

This material survived consolidation because it contains subject-specific instruction for **Gold**, not the former repeated institutional wrapper.

- a monetary asset;
- a reserve asset;
- a non-yielding real asset;
- a safe-haven and uncertainty hedge;
- a physical commodity with jewelry and investment demand;
- a collateral/liquidity asset in some contexts.

- US real yields;
- broad dollar;
- policy repricing;
- event risk;
- liquidity stress;
- futures/options positioning;
- implementation flow.

- real-yield trend;
- dollar trend;
- central-bank reaction path;
- geopolitical/fiscal risk premium;
- ETF/futures flows;
- positioning and physical premiums.

- reserve diversification;
- central-bank demand;
- fiscal/monetary credibility;
- mine supply and recycling;
- long-run real rates;
- currency regime uncertainty.

Gold has no coupon. Higher real yields can raise its opportunity cost. But the relationship is not permanent or exclusive. Gold can rise with high real yields when:

- fiscal or geopolitical risk increases;
- central-bank demand is strong;
- dollar confidence changes;
- physical/ETF demand offsets;
- the market expects future easing;
- or correlations shift.

- both can rise in severe stress;
- pair-specific currency moves can differ from broad dollar;
- physical demand in local currencies can weaken when dollar gold rises.

- **Demand inflation + hawkish policy:** real yields may rise; gold can weaken.
- **Supply inflation + credibility stress:** gold can strengthen.
- **Disinflation + easing:** real yields may fall; gold can strengthen.
- **Deflationary liquidation:** gold can fall initially as cash is raised.

- central-bank purchases;
- ETF holdings;
- futures positioning;
- China/India premiums;
- jewelry demand;
- recycling;
- mine supply.

1. two-year yield;
2. ten-year real yield;
3. breakeven inflation;
4. broad dollar;
5. policy-pricing change;
6. geopolitical/fiscal developments;
7. liquidity stress;
8. ETF/futures/option context;
9. event calendar;
10. Asian physical-market clues where available.

- gold and dollar may both rise.
- confirm with bonds, oil, volatility, and funding.
- avoid assuming ordinary inverse correlations.

- gold falls with equities and even bonds;
- dollar and funding stress rise;
- macro safe-haven thesis may remain structurally valid but intraday permission is short or no-trade.

- long yields may rise;
- gold can rise if the credibility/risk channel dominates real-yield opportunity cost.
- confirmation requires more than “yields up.”

Fundamental context grants direction only. Entry still requires fundamental-state persistence, structural temporary counter-move, observable state-confirmation event trigger, predeclared risk limit, and scenario-defined realization target.

Gold is especially dangerous when the macro thesis is correct but the dollar/real-yield impulse is opposite intraday. Do not force the structural thesis into the day-trading horizon.

- Is the driver real yields, dollar, risk, reserve demand, or physical demand?
- Is the thesis priced?
- What catalyst persists for several sessions?
- Can the position survive data and weekend gaps?
- What cross-asset condition invalidates it?
- Is futures positioning crowded?
- Are local physical premiums confirming?

- “Inflation up = gold up.”
- “War = gold up.”
- “Yields up = gold down.”
- “Central-bank buying means every dip is a buy.”
- “Dollar and gold cannot rise together.”
- “Gold is purely a commodity.”
- “One COT extreme predicts reversal.”

- World Gold Council data and research;
- official TIPS/real-yield data;
- central-bank reserve statistics;
- CFTC positioning;
- LBMA/physical market data where available.

### Consolidated legacy note: Commodity, Energy, and Gold Sources

This material survived consolidation because it contains subject-specific instruction for **Commodity, Energy, and Gold Sources**, not the former repeated institutional wrapper.

### U.S. Energy Information Administration
- Petroleum overview: https://www.eia.gov/petroleum/
- Weekly Petroleum Status Report: https://www.eia.gov/petroleum/supply/weekly/
- Short-Term Energy Outlook: https://www.eia.gov/outlooks/steo/
- Crude price drivers: https://www.eia.gov/finance/markets/crudeoil/

### International and Producer Sources
- IEA Oil Market Report: https://www.iea.org/topics/oil-market-report
- OPEC Monthly Oil Market Report: https://www.opec.org/opec_web/en/publications/338.htm
- OPEC production communications: https://www.opec.org/
- National energy ministries and pipeline/shipping authorities.

### Market Data
- CME/NYMEX contract data: https://www.cmegroup.com/markets/energy.html
- Futures curve, spreads, open interest, options, and settlement data.
- Physical differentials and shipping data generally require specialized vendors.

### World Gold Council
- Gold research and market structure: https://www.gold.org/goldhub/research
- Demand trends: https://www.gold.org/goldhub/research/gold-demand-trends

### Official/Market Sources
- Central-bank reserve data via IMF and national sources.
- COMEX futures/options via CME: https://www.cmegroup.com/markets/metals/precious/gold.html
- ETF holdings from official fund sponsors.
- Real yields and USD from official/market sources.

- World Bank commodity data: https://www.worldbank.org/en/research/commodity-markets
- IMF commodity data: https://www.imf.org/en/Research/commodity-prices
- USDA for agricultural balances: https://www.usda.gov/topics/data
- LME for base metals: https://www.lme.com/

- flat price;
- curve shape;
- calendar spreads;
- inventory;
- physical differentials;
- producer hedging;
- speculative positioning;
- FX;
- global growth;
- policy/geopolitical premium.

Weekly inventory and production estimates can be noisy and revised. A durable thesis should triangulate multiple physical and market signals.

### Consolidated legacy note: Central-Bank Intervention and Reserve Management

**Central-Bank Intervention and Reserve Management** is a research object inside relative monetary, external-balance, funding, hedging, valuation, and capital-flow forces across currencies. The analyst must isolate the measurable state, the expectation already embedded in prices, the mechanism connecting them, and the horizon on which that inference can survive.

For **Central-Bank Intervention and Reserve Management**, the relevant institutional domain is **fx**: relative monetary, external-balance, funding, hedging, valuation, and capital-flow forces across currencies. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

$$
F_{t,T}^{CIP}=S_t\frac{1+r_d\tau}{1+r_f\tau}
$$

For **Central-Bank Intervention and Reserve Management**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

### Consolidated legacy note: Gold Monetary and Physical Demand System

For **Gold Monetary and Physical Demand System**, the relevant institutional domain is **commodities**: physical supply, demand, inventories, transformation capacity, logistics, seasonality, substitution, and financial overlay. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

For **Gold Monetary and Physical Demand System**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

### Consolidated legacy note: Central-Bank Session Intelligence Playbook

**Central-Bank Session Intelligence Playbook** is a research object inside conversion of macro information into horizon-specific permissions, scenario paths, implementation handoffs, and auditable trade management. The analyst must isolate the measurable state, the expectation already embedded in prices, the mechanism connecting them, and the horizon on which that inference can survive.

For **Central-Bank Session Intelligence Playbook**, the relevant institutional domain is **trading**: conversion of macro information into horizon-specific permissions, scenario paths, implementation handoffs, and auditable trade management. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

$$
Edge(a,h)=\sum_s[P_{desk}(s)-P_{mkt}(s)]Payoff(a,s,h)-Cost(a,h)
$$

For **Central-Bank Session Intelligence Playbook**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

### Consolidated legacy note: Dollar Real-Yield and Gold Playbook

For **Dollar Real-Yield and Gold Playbook**, the relevant institutional domain is **trading**: conversion of macro information into horizon-specific permissions, scenario paths, implementation handoffs, and auditable trade management. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

For **Dollar Real-Yield and Gold Playbook**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Scoring status

This packet is an **internal golden reference**, not an external scientific certification. External review remains pending. A report is compared against the mechanism key, admissible evidence set and failure deductions; prose similarity is irrelevant.
