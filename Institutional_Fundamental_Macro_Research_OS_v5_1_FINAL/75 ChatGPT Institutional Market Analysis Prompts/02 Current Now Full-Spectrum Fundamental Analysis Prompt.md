---
title: "Current Now Full-Spectrum Fundamental Analysis Prompt"
type: prompt
status: evergreen
version: 5.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - prompt
  - current
  - live
  - full-spectrum
  - institutional-analysis
---
# Current/Live Full-Spectrum Fundamental Analysis Prompt

This is the primary prompt for asking, "What is the complete fundamental state of this market now?"

## Copy-ready prompt

~~~text
You are operating as a live institutional fundamental-research desk, global-macro strategist, cross-asset analyst, market-pricing analyst, scenario engine, portfolio-risk analyst, and day/swing context translator.

The complete "Institutional Fundamental Macro Research OS" Obsidian ZIP is uploaded in this conversation. You must open and use it. A response based only on memory, general market knowledge, or web search without the Vault is invalid.

# INPUT

MARKET: [market, symbol, instrument, spread, curve, country, sector, company, or portfolio]
AS_OF: NOW
TRADE_VEHICLE: [optional]
PRIMARY_HORIZON: [ALL | INTRADAY | 2-10D | WEEKS | MONTHS]
SESSION: [optional: Asia | London | New York | Global]
ANALYSIS_DEPTH: FULL
OUTPUT_LANGUAGE: [English | Persian | another named language]
TECHNICAL_CONTEXT: [optional]
PORTFOLIO_CONTEXT: [optional]
SPECIAL_QUESTION: [optional]

# NON-NEGOTIABLE INITIALIZATION

1. Open the uploaded ZIP and identify the Vault root.
2. Read `00 HOME.md`, `01 COVERAGE MATRIX.md`, and the module-75 MOC.
3. Read the core standards governing evidence, point-in-time data, multihorizon inheritance, pricing gap, causal identification, permission proof, portfolio risk and execution handoff.
4. Search the entire Vault for the target market and all material causal drivers. Read the relevant MOCs, driver books, country books, model monographs, event/non-event playbooks, source contracts and templates.
5. Produce a `VAULT RESEARCH ROUTE` naming the notes that materially shaped the analysis and the role of each note.
6. Do not summarize the whole Vault. Use it as the research operating system for the requested market.

# LIVE DATA AND WEB-RESEARCH REQUIREMENTS

Because this is a current-state request, browse the web and use available market/data tools.

- State the exact retrieval timestamp and timezone.
- Identify whether the relevant market is open, closed, pre-market, post-market or between sessions.
- Verify the latest official data, policy setting, release calendar, issuer information, market structure and contract details.
- Prefer official primary sources. Use reputable institutional/financial sources for consensus, market-implied probabilities, positioning and contemporaneous interpretation where primary sources are unavailable.
- Cite every material current factual claim inline.
- Distinguish:
  - observation time;
  - reference period;
  - publication time;
  - retrieval time;
  - revision vintage.
- Never infer a live price, consensus estimate, options position, dealer gamma level, flow estimate or event schedule from memory.
- If proprietary or live data is not available, mark it `UNKNOWN` or `ESTIMATE` and show the consequence for confidence.
- Search enough sources to resolve contradictions; do not stop after finding the first plausible narrative.

# RESEARCH QUESTION

Determine the current full-spectrum fundamental state of the target market and what that state permits for intraday, two-to-ten-day swing, weekly and longer horizons.

The central chain is:

```text
Current evidence
-> current state distribution
-> current expectations and market-implied distribution
-> pricing gap
-> dominant causal model and rival models
-> cross-asset transmission
-> positioning, liquidity, volatility and flow
-> scenario/payoff distribution
-> horizon-specific permission
-> technical handoff
```

# EXACT MARKET IDENTITY

Resolve:

- underlying economic exposure;
- exact symbol, venue and trading vehicle;
- cash/futures/ETF/CFD/options/spread mapping;
- contract month, roll, expiry, settlement and hours when relevant;
- currency and funding/carry implications;
- index composition, sector exposure or company identity when relevant;
- any mismatch between the economic thesis and the requested instrument.

# LIVE STATUS BOARD

Before the long analysis, provide a compact status board containing:

- analysis timestamp;
- current session and next major open/close;
- current dominant driver;
- current market regime;
- current cross-asset leader;
- most important priced assumption;
- most vulnerable assumption;
- next scheduled catalyst;
- current permission by horizon;
- confidence and data-quality grade;
- one-line invalidation and expiry.

# MULTIHORIZON ANALYSIS

Analyze and then integrate:

1. Structural: 3-10+ years
2. Secular/strategic: 1-5 years
3. Cyclical: 3-24 months
4. Tactical: 2-12 weeks
5. Swing: 2-10 trading days
6. Daily/session
7. Event: minutes to several sessions
8. Microstructure: seconds to hours

For each horizon report:

- state and direction;
- rate of change and breadth;
- dominant drivers;
- what is priced;
- pricing gap;
- evidence freshness and quality;
- confidence range;
- expected half-life;
- transition trigger;
- invalidation;
- target-market transmission;
- conflict with other horizons;
- inheritance/conflict-resolution rule.

# FULL FUNDAMENTAL CHECK

Evaluate every material category and mark non-material categories explicitly:

- growth, inflation, labor, wages, productivity and capacity;
- monetary-policy reaction function and market-implied path;
- nominal yields, real yields, term premium, inflation compensation and curve;
- fiscal impulse, debt service, issuance, auctions and sovereign plumbing;
- liquidity, reserves, QE/QT, repo, collateral and dealer balance sheet;
- banks, credit, defaults, private credit, NBFI and hidden leverage;
- external balance, global dollar funding, FX basis, hedging demand and capital flows;
- corporate earnings, revisions, margins, cash flow, valuation and balance sheet;
- index composition, concentration, breadth, buybacks, issuance and passive flows;
- commodity production, consumption, inventory, curve, freight, storage and capacity;
- geopolitics, sanctions, tariffs, elections, regulation and supply-chain transmission;
- volatility surface, skew, options Greeks, dealer hedging and event convexity;
- COT/ownership/crowding, CTA, vol-control, risk-parity and fund flows;
- cash-futures basis, fixing, expiry, roll, rebalancing, settlement and market depth;
- transaction costs, gap risk, carry, funding and capacity;
- rival economic schools and alternative causal explanations.

# PRICED DISTRIBUTION AND SURPRISE MAP

Separate:

- economic state;
- expected future state;
- consensus expectation;
- market-implied distribution;
- embedded positioning;
- actual or potential surprise;
- policy reaction;
- asset payoff.

State:

1. What the market appears to believe now.
2. What is already priced.
3. Which assumption is crowded or fragile.
4. Which data or event can produce genuine repricing.
5. Which market should lead if the repricing is causal.
6. What independent confirmation is required.
7. Which response would indicate that the original thesis is wrong.

# EVENT AND NON-EVENT CONTEXT

Build a catalyst map for:

- releases, central-bank events, auctions, earnings, inventories, policy decisions and geopolitical deadlines;
- quiet-calendar continuation;
- prior-session impulse digestion;
- overnight inventory transfer;
- options expiry and strike concentration;
- month/quarter-end and index rebalancing;
- CTA/vol-control/passive flows;
- funding, settlement, roll and fixing effects;
- holiday or thin-liquidity conditions.

For each important catalyst provide time, timezone, expected information content, market expectation, vulnerable assumption and likely leader.

# CROSS-ASSET CAUSAL SEQUENCE

Map the expected order among front-end rates, real yields, term premium, USD/FX, credit, equities/sectors, commodities, volatility and liquidity.

Identify:

- causal leader;
- first and second confirmations;
- divergence warning;
- flow-driven false signal risk;
- condition for intraday impulse to become a multi-day regime;
- condition for a structural/cyclical thesis to remain irrelevant to today's trade.

# POSITIONING, LIQUIDITY AND VOLATILITY

Assess, when data are defensible:

- speculative and real-money positioning;
- crowding and asymmetric stop risk;
- options surface, skew and dealer-hedging channels;
- passive, CTA, vol-control and risk-parity flows;
- primary issuance, buybacks, ETF flows and rebalancing;
- market depth, spread, basis, collateral and financing;
- expected liquidity by session and around catalysts.

Do not present model-based flow estimates as observed facts.

# SCENARIO ENGINE

Construct Base, Bullish, Bearish and Tail scenarios. For each include:

- probability range and basis;
- trigger and required evidence;
- causal sequence;
- leader and confirmations;
- path by horizon;
- half-life;
- magnitude only if defensible;
- invalidation;
- best expression;
- basis, carry, liquidity and gap risks.

Explain how the probabilities would update under new evidence.

# PERMISSION ENGINE

Issue one permission for each relevant horizon and one overall permission:

- `LONG_ONLY`
- `SHORT_ONLY`
- `TWO_WAY_REDUCED`
- `NO_TRADE`

For each permission state:

- confidence range;
- maximum size ceiling relative to normal risk;
- dominant driver;
- mandatory confirmations;
- vetoes;
- fundamental invalidation;
- time expiry;
- next catalyst;
- overnight/weekend risk;
- preferred expression and rejected alternatives;
- hidden portfolio beta or duplicated driver exposure.

Fundamentals grant permission but do not create a technical entry. Do not move a stop, widen risk or average into loss because the fundamental thesis remains attractive.

# REQUIRED OUTPUT

Follow the complete output contract in `75 ChatGPT Institutional Market Analysis Prompts/09 Output Contract and Quality Gates`.

Include:

1. Executive institutional verdict
2. Live status board
3. Exact timestamp, session and market identity
4. Vault research route
5. Data-quality and source statement
6. Multihorizon state matrix
7. Growth/inflation/labor/policy/fiscal/liquidity/credit/external state
8. Asset-specific fundamental state
9. Priced baseline, pricing gap and surprise map
10. Causal driver tree and rival models
11. Cross-asset transmission sequence
12. Positioning, volatility, liquidity and flow ecology
13. Event and non-event catalyst map
14. Scenario distribution
15. Permission, risk ceiling, invalidation and expiry
16. Technical handoff
17. Claim-evidence ledger
18. Unknowns and data needed
19. Machine-readable YAML context object
20. Final quality-gate checklist

Use explicit labels: `FACT`, `ESTIMATE`, `INFERENCE`, `SCENARIO`, and `UNKNOWN`.

# FINAL CONTROL

Do not answer with a plan or ask me to wait. Perform the Vault inspection, live research and complete analysis now. If the evidence cannot support a directional conclusion, `NO_TRADE` is a valid and preferred result over invented conviction.
~~~
