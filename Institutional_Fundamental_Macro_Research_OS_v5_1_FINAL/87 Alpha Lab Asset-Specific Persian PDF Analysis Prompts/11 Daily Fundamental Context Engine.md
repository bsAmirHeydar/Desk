---
title: "Alpha Lab Daily Fundamental Context Engine"
type: daily-analysis-standard
status: canonical
version: 10.2.0
created: 2026-07-31
updated: 2026-07-31
language: en
tags: [alpha-lab, daily-fundamental, intraday, session, event, flow]
---
# Alpha Lab Daily Fundamental Context Engine

## Mission

This standard converts the Vault's structural and macro knowledge into a repeatable **day-horizon fundamental analysis**. It is not a chart-entry system. Its job is to determine what is economically and institutionally driving the market today, how the overnight and session repricing relates to the priced baseline, whether the move has independent confirmation, how long the impulse is likely to persist, and what evidence would invalidate the daily state.

The daily engine must prevent two opposite errors:

1. **Macro overreach** — repeating long-cycle material that does not change today's decision state.
2. **Intraday myopia** — treating every price move or headline as a new regime without reference to the inherited state.

## Daily analysis profiles

Every run must declare one profile:

- `DAILY_PREMARKET` — completed before the target session opens. Builds the day's initial state and scenario map.
- `LIVE_SESSION_UPDATE` — completed during the session. Explains what has changed since the pre-market state.
- `POST_EVENT_UPDATE` — completed immediately after a scheduled or unscheduled catalyst. Decomposes the surprise and repricing.
- `END_OF_DAY` — completed after the primary session. Attributes the day and records what carries forward.
- `FULL_SPECTRUM` — retains the longer structural report and includes the daily layer as one horizon.

## Time anchoring

A daily report is invalid unless it states:

- exact `AS_OF` timestamp;
- reference timezone;
- target trading date;
- target session and current session stage;
- previous official close used for comparison;
- current data cutoff;
- next scheduled update time.

In historical mode, the engine must reconstruct the information set available at the exact cutoff. Later prices, later revisions, subsequent speeches, later constituent changes and future outcomes are forbidden in the reconstructed section.

## Anti-macro-dominance allocation

For a daily report, allocate research attention approximately as follows:

- **60–70%**: current day, overnight repricing, today's catalysts, session transmission, flow and liquidity.
- **20–30%**: tactical and 2–10-day inherited state that can persist into today.
- **0–15%**: structural and cyclical background, limited to facts that materially constrain today's interpretation.

A longer-cycle section may exceed 15% only when a genuine regime change, policy break, systemic shock or major earnings/physical-balance transition is occurring. The report must explain why the exception is necessary.

## Required comparison windows

Use the smallest windows that answer the daily question:

1. previous official close to current time;
2. prior 24 hours;
3. prior three trading days;
4. prior five trading days when needed to distinguish continuation from reversal;
5. the next 24–48 hours of scheduled catalysts.

Do not produce a long historical review unless it changes today's state.

## The daily state stack

### 1. Inherited state

Summarize in no more than one page:

- structural prior;
- cyclical state;
- tactical state;
- current 2–10-day campaign or repricing;
- unresolved contradiction carried from the previous session.

The inherited state is a prior, not today's conclusion.

### 2. What changed since the previous close?

Build a change ledger. For every material change, state:

- variable or market;
- previous-close value or state;
- current value or state;
- direction and magnitude;
- timestamp;
- source;
- causal relevance;
- whether it confirms or contradicts the inherited state.

Focus on changes in expectations and constraints, not on price movement alone.

### 3. Overnight repricing map

Separate:

- Asia session developments;
- Europe/London developments;
- pre-New-York developments;
- cross-session handoff;
- whether the move was led by macro information, policy, earnings, physical-market news, risk, positioning or liquidity.

State which market moved first and which markets confirmed later. Do not infer causality from simultaneous movement without evidence.

### 4. Today's catalyst calendar

List every material scheduled and unscheduled catalyst with:

- exact local time and timezone;
- source/release institution;
- expected information content;
- priced baseline or known market expectation;
- vulnerable component rather than headline only;
- first market expected to react;
- likely transmission path;
- whether the event can alter only the session, the full day, or the multi-day state.

Include speeches, auctions, refunding, major earnings, index events, options expiries, fixings, policy deadlines and physical-market releases when relevant.

### 5. Priced baseline and surprise map

Before interpreting a release or headline, reconstruct what the market was expecting through available evidence:

- policy pricing;
- yield curves and real rates;
- forward or futures pricing;
- options-implied distribution;
- consensus only when genuinely available;
- earnings or physical-balance expectations;
- relative pricing across connected markets.

After the event, decompose the surprise into components. Distinguish headline surprise, composition surprise, revision surprise, policy-reaction surprise and positioning/liquidity amplification.

### 6. Causal leader scoreboard

Rank the markets or variables controlling the day. A useful scoreboard contains:

- candidate leader;
- current direction;
- evidence strength;
- causal role;
- confirming markets;
- contradicting markets;
- confidence cap.

Possible leaders include policy-path pricing, real yields, term premium, dollar funding, credit, earnings revisions, energy terms of trade, physical balances, geopolitical risk or forced-flow mechanics.

### 7. Cross-asset confirmation matrix

For each daily conclusion, seek at least one independent confirmation and one contradiction check across:

- rates and real rates;
- FX and dollar conditions;
- credit;
- equities and sector leadership;
- volatility and options;
- commodities or physical markets;
- funding and liquidity.

Do not count two instruments driven by the same underlying data as independent confirmations.

### 8. Day-type classification

Select one primary day type and, if necessary, one secondary type:

- `DATA_LED`
- `POLICY_LED`
- `RATES_LED`
- `EARNINGS_LED`
- `PHYSICAL_MARKET_LED`
- `GEOPOLITICAL_LED`
- `CREDIT_LED`
- `FLOW_LED`
- `POSITIONING_UNWIND`
- `QUIET_DIGESTION`
- `EVENT_BINARY`
- `MIXED_OR_UNCLEAR`

Explain the classification in plain language.

### 9. Persistence classification

Classify the likely half-life of the dominant impulse:

- `TRANSIENT_0_2H`
- `SESSION_PERSISTENT`
- `FULL_DAY`
- `MULTI_DAY_BRIDGE`
- `UNKNOWN`

The classification must be based on information persistence, cross-asset confirmation, the next catalyst and whether the move changes expected cash flows, policy path, risk premium, physical balance or institutional constraints.

### 10. No-event and flow-led days

A quiet calendar is not an analytical void. On no-event days, test:

- continuation of the previous repricing;
- delayed digestion of a prior release;
- Treasury settlement, issuance or funding effects;
- options expiry and dealer hedging;
- month-end or quarter-end rebalance;
- index rebalance or passive flow;
- CTA, volatility-control or risk-parity adjustment;
- buyback blackout or corporate flow;
- fixing and benchmark flow;
- short-covering, liquidation or crowded unwind;
- thin-liquidity and holiday effects.

Label inferred flows as proxies. Never claim unavailable dealer or prime-broker data.

### 11. Session map

For the chosen target session, define:

- inherited state at session open;
- unresolved overnight question;
- scheduled catalysts during the session;
- first causal market to monitor;
- independent confirmation required;
- contradiction that would reduce confidence;
- state-change trigger;
- next mandatory update time.

This is a fundamental monitoring map, not a technical entry plan.

### 12. Daily fundamental state

Issue exactly one primary daily state:

- `DAILY_FUNDAMENTAL_LONG_BIAS`
- `DAILY_FUNDAMENTAL_SHORT_BIAS`
- `DAILY_TWO_WAY_EVENT_DEPENDENT`
- `DAILY_NO_FUNDAMENTAL_EDGE`
- `DAILY_INSUFFICIENT_EVIDENCE`

Also issue separate states for the selected session and for the 2–10-day bridge when relevant. A long or short bias is not a personalized order and does not replace risk management.

### 13. Invalidation and update triggers

State explicit evidence that would:

- invalidate the daily view;
- downgrade confidence;
- upgrade confidence;
- convert a transient impulse into a multi-day bridge;
- force a new report.

Avoid arbitrary price thresholds unless they represent a valuation, market-implied expectation, financing, liquidity or policy-reaction threshold.

### 14. End-of-day attribution

For `END_OF_DAY`, answer:

- what actually drove the day;
- what the pre-market report got right or wrong;
- which model won;
- whether the move was information, valuation, risk-premium, positioning or liquidity driven;
- what carries into the next session;
- what should be retired from the thesis;
- what evidence is still missing.

## Daily research states are not technical signals

The daily engine may describe direction, persistence, event dependence, causal leaders and invalidation evidence. It must not prescribe a chart pattern, indicator, candlestick entry, support/resistance rule, stop placement or target construction.

## Daily evidence minimum

A `DAILY_FUNDAMENTAL_LONG_BIAS` or `DAILY_FUNDAMENTAL_SHORT_BIAS` requires:

1. a clear priced baseline;
2. a plausible causal leader;
3. one independent confirmation;
4. no unresolved contradiction severe enough to reverse the sign;
5. an explicit invalidation condition;
6. a defined expected half-life;
7. a timestamped evidence ledger.

If those conditions are absent, use a conditional, no-edge or insufficient-evidence state.
