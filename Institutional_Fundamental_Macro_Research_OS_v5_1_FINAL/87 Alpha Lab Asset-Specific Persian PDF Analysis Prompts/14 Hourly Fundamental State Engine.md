---
title: "Alpha Lab Hourly Fundamental State Engine"
type: hourly-analysis-standard
status: canonical
version: 10.3.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [alpha-lab, hourly-fundamental, intraday, consumption, intensity, persistence]
---
# Alpha Lab Hourly Fundamental State Engine

## Mission

This engine converts the Vault's structural, cyclical, tactical and daily knowledge into a **timestamped hour-by-hour fundamental state**. Its purpose is not to invent a new signal every hour. Its purpose is to determine, at each completed hourly cutoff and at every material event, whether the fundamental direction, intensity, remaining pressure, consumption, confidence, causal leadership, persistence and reversal risk have changed.

The engine must be practical enough to answer:

- What is the current fundamental direction?
- How strong is it?
- How much of the catalyst has already been absorbed or consumed?
- How much fundamental pressure appears to remain?
- Is the current movement information-driven, flow-amplified, liquidity-distorted or contradictory?
- What changed during the last hour?
- Which variable is controlling the next hour?
- What could strengthen, weaken or reverse the state?
- Is the impulse likely to last minutes, hours, the full session or multiple days?

## Core honesty rule

Fundamental information does not necessarily change every hour. The engine must never manufacture hourly variation merely to fill a table.

When there is no material new information, repricing, institutional constraint or cross-asset confirmation change, use:

`NO_MATERIAL_FUNDAMENTAL_UPDATE`

Carry the previous state forward, reduce freshness only when appropriate and explain why no change is warranted.

## Supported operating modes

- `HOURLY_PREMARKET_MAP` — creates a conditional map for the coming session. Future rows are scenarios, not observed states.
- `HOURLY_LIVE_MONITOR` — creates completed hourly snapshots up to the exact as-of time and conditional paths for the remaining session.
- `HOURLY_POST_EVENT` — creates event snapshots at T-60, T-15, T+5, T+15 and T+60 minutes, then resumes hourly monitoring.
- `HOURLY_END_OF_DAY_ATTRIBUTION` — reconstructs the day's completed state path and attributes every material transition.
- `HISTORICAL_HOURLY_REPLAY` — reconstructs each hourly cutoff using only information available at that cutoff. Later outcomes may appear only in a separately labeled ex-post column when explicitly requested.

## Mandatory input controls

Every hourly run must declare:

```text
HOURLY_MODE: [HOURLY_PREMARKET_MAP | HOURLY_LIVE_MONITOR | HOURLY_POST_EVENT | HOURLY_END_OF_DAY_ATTRIBUTION | HISTORICAL_HOURLY_REPLAY]
SNAPSHOT_INTERVAL_MINUTES: [30 | 60]
SNAPSHOT_START: [HH:MM timezone]
SNAPSHOT_END: [HH:MM timezone]
EVENT_DRIVEN_UPDATES: [YES | NO]
EVENT_MICRO_WINDOWS: [NONE | T-60_T-15_T+5_T+15_T+60]
COMPARE_TO_PRIOR_SNAPSHOT: [YES | NO]
```

Use 60-minute snapshots by default. Use 30-minute snapshots only when the user requests greater granularity or the session contains multiple material catalysts.

## Hourly state object

Every completed snapshot must contain all fields below.

### 1. Timestamp and information cutoff

- exact timestamp;
- timezone;
- target session;
- session stage;
- last completed market observation;
- latest source publication timestamp;
- whether the row is observed, estimated or conditional.

### 2. Fundamental direction

Select one state:

- `STRONGLY_POSITIVE`
- `POSITIVE`
- `NEUTRAL`
- `NEGATIVE`
- `STRONGLY_NEGATIVE`
- `TWO_WAY_UNRESOLVED`
- `INSUFFICIENT_EVIDENCE`

Also provide a direction score from `-100` to `+100`.

Interpretation:

- `+70 to +100` — strongly positive fundamental pressure;
- `+25 to +69` — positive;
- `-24 to +24` — neutral, balanced or unresolved;
- `-25 to -69` — negative;
- `-70 to -100` — strongly negative.

The score is an ordinal synthesis, not a calibrated return forecast. Round to the nearest five and label its evidence type.

### 3. Intensity

`INTENSITY_0_100` measures the current strength of the active fundamental impulse, not confidence and not expected return.

Intensity rises when:

- the surprise is economically large;
- multiple transmission channels agree;
- the causal leader moves decisively;
- independent markets confirm;
- institutional constraints amplify the impulse;
- the state affects cash flows, policy path, risk premium, funding or a physical balance.

Intensity falls when:

- the impulse is narrow;
- the information is stale;
- confirmation is weak;
- the move is dominated by temporary liquidity;
- the next catalyst can easily reverse the state.

### 4. Confidence

`CONFIDENCE_0_100` measures evidence quality and model reliability.

It is separate from intensity. A high-intensity move may have low confidence when data are incomplete or flow explanations dominate.

Confidence must reflect:

- source quality;
- data freshness;
- priced-baseline quality;
- causal identification;
- independent confirmation;
- model agreement;
- absence of unresolved contradictions;
- availability of required market data.

When critical inputs are unavailable, cap confidence explicitly.

### 5. Consumption vector

Do not use one vague consumption number. Report the full vector:

- `INFORMATION_ABSORPTION_0_100` — how much of the new information appears incorporated into expectations;
- `REPRICING_COMPLETION_0_100` — how far the observable market repricing appears to have progressed relative to the plausible fundamental adjustment;
- `FLOW_EXHAUSTION_0_100` — how much of identifiable forced, passive, hedging or positioning flow appears completed;
- `NARRATIVE_SATURATION_0_100` — how broadly the information has become consensus and repeatedly expressed;
- `CATALYST_FRESHNESS_0_100` — how fresh and decision-relevant the catalyst remains;
- `REMAINING_FUNDAMENTAL_PRESSURE_0_100` — residual directional pressure after absorption, contradictions, upcoming catalysts and flow exhaustion.

These values are normally judgmental or model-implied ordinal scores. They must not be presented as empirically calibrated probabilities unless a validated model exists.

Consumption cannot be inferred from price distance alone. It must incorporate:

- the expected magnitude of the information shock;
- policy-path or cash-flow revision;
- breadth of cross-asset transmission;
- elapsed time;
- positioning and flow evidence;
- liquidity quality;
- upcoming catalysts;
- whether new reinforcing evidence has arrived.

Consumption may decline and remaining pressure may rise when a second catalyst reinforces the first.

### 6. State phase

Select one:

- `FORMING`
- `STRENGTHENING`
- `MATURE`
- `CONSUMING`
- `EXHAUSTED`
- `REVERSING`
- `UNRESOLVED`

### 7. Move-quality classification

Select one primary classification:

- `FUNDAMENTALLY_CONFIRMED`
- `FUNDAMENTAL_UNDERREACTION`
- `PROPORTIONATE_REPRICING`
- `OVERREACTION_OR_SATURATION`
- `FLOW_AMPLIFIED`
- `LIQUIDITY_DISTORTED`
- `CONTRADICTORY_TO_FUNDAMENTALS`
- `INSUFFICIENT_EVIDENCE`

### 8. Causal leader and driver stack

Record:

- primary causal driver;
- secondary reinforcing driver;
- strongest opposing driver;
- first market or variable that moved;
- independent confirmation;
- contradiction;
- driver concentration score from 0 to 100.

A high concentration score means the state depends on one fragile driver and should receive a confidence cap.

### 9. Surprise and expectation revision

Report separately:

- headline surprise;
- composition surprise;
- revision surprise;
- policy-reaction surprise;
- market-positioning surprise;
- change in the priced baseline since the previous snapshot.

### 10. Cross-asset coherence

`CROSS_ASSET_CONFIRMATION_0_100` measures whether rates, FX, credit, volatility, equities, commodities and funding markets tell a coherent causal story.

Do not double-count instruments sharing the same underlying driver as independent confirmation.

### 11. Persistence and half-life

Select one:

- `MINUTES_0_30`
- `INTRAHOUR_30_90`
- `MULTI_HOUR_2_4H`
- `SESSION_PERSISTENT`
- `FULL_DAY`
- `MULTI_DAY_BRIDGE`
- `UNKNOWN`

Also state the mechanism supporting persistence and the next catalyst that could shorten or extend the half-life.

### 12. Reversal and state-change risk

Report:

- `REVERSAL_RISK_0_100`;
- the most likely reversal mechanism;
- the exact evidence that would trigger a state downgrade;
- the exact evidence that would trigger a sign change;
- the next mandatory reassessment time.

### 13. Path asymmetry

Select one:

- `UPSIDE_DOMINANT`
- `DOWNSIDE_DOMINANT`
- `SYMMETRIC`
- `BINARY_EVENT`
- `UNKNOWN`

Explain whether the asymmetry comes from valuation, policy path, positioning, liquidity, physical balance, earnings or event risk.

### 14. Edge availability

Select one:

- `STRONG_FUNDAMENTAL_EDGE`
- `MODERATE_FUNDAMENTAL_EDGE`
- `WEAK_FUNDAMENTAL_EDGE`
- `NO_CLEAR_FUNDAMENTAL_EDGE`
- `INSUFFICIENT_EVIDENCE`

This is a research state, not a personalized order.

### 15. Change from prior snapshot

State explicitly:

- what changed;
- what did not change;
- why the direction score changed or remained stable;
- why intensity changed or remained stable;
- why consumption changed;
- whether confidence rose or fell;
- the timestamp and cause of the last material state transition.

## Mandatory hourly timeline

For every completed hour, produce one row with:

| Time | Direction | Score | Intensity | Confidence | Absorption | Repricing completion | Flow exhaustion | Remaining pressure | Phase | Primary driver | Confirmation | Persistence | Reversal risk | Change from prior hour |

Future hours must not be displayed as observed rows. Present them in a separate conditional scenario map.

## Event-driven update rule

A material event overrides the fixed hourly schedule. Create an immediate state update when any of these occurs:

- material macro data release;
- central-bank decision, speech or communication surprise;
- Treasury auction, refunding or funding shock;
- major earnings or guidance surprise;
- material geopolitical escalation or de-escalation;
- physical-market supply or demand shock;
- credit or funding stress;
- abnormal liquidation, expiry, rebalance or institutional-flow event;
- decisive cross-asset contradiction that invalidates the previous model.

## Historical hourly replay rule

For each reconstructed hour:

1. freeze the information set at that hour;
2. use only releases, prices, statements and filings available by that cutoff;
3. do not use the day's final outcome to assign the state;
4. do not let later revisions alter earlier rows;
5. store later knowledge only in a clearly separated ex-post audit column;
6. mark unreconstructable data as unavailable rather than estimating it from the outcome.

## No-false-precision rules

- Round ordinal scores to the nearest five.
- Never report decimal precision.
- Label every score as `EMPIRICALLY_CALIBRATED`, `MODEL_IMPLIED` or `JUDGMENTAL_ORDINAL`.
- Do not convert a judgmental score into a probability.
- Do not infer consumption solely from price movement.
- Do not claim dealer inventory, prime-broker flows or licensed consensus without access.
- When data are inadequate, use `INSUFFICIENT_EVIDENCE`.

## Minimum evidence for a directional hourly state

A positive or negative hourly state requires:

1. a reconstructed priced baseline;
2. a named causal leader;
3. one independent confirmation;
4. a contradiction check;
5. an explicit consumption vector;
6. an expected half-life;
7. an invalidation condition;
8. a timestamped source ledger.

If any core condition is missing, cap the state at weak edge, no edge or insufficient evidence.
