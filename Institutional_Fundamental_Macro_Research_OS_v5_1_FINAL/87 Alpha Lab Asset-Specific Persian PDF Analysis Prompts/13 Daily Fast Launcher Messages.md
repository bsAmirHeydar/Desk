---
title: "Alpha Lab Daily Fundamental Fast Launcher Messages"
type: launcher-library
status: canonical
version: 10.3.0
created: 2026-07-31
updated: 2026-08-01
language: en
tags: [alpha-lab, daily, launcher, pdf]
---
# Alpha Lab Daily Fundamental Fast Launcher Messages

Attach the complete Vault ZIP, then send one launcher.

## Nasdaq 100 — Daily pre-market

```text
Open the attached Vault and execute `87 Alpha Lab Asset-Specific Persian PDF Analysis Prompts/04 Nasdaq 100 Alpha Lab Persian PDF Prompt.md`.

MODE: LIVE
AS_OF: NOW
ANALYSIS_PROFILE: DAILY_PREMARKET
TARGET_DATE: TODAY
REFERENCE_TIMEZONE: America/New_York
SESSION: New York
SESSION_STAGE: PRE_NEW_YORK
DAILY_LOOKBACK: 3D
CATALYST_WINDOW: TODAY
PRIMARY_HORIZON: INTRADAY
REPORT_DEPTH: DEEP
PORTFOLIO_CONTEXT: NONE
SPECIAL_QUESTION: Determine the complete day-horizon fundamental context, causal leader, overnight confirmation, event risks, expected persistence and invalidation conditions for Nasdaq 100 today.
EX_POST_AUDIT: NO

Create and deliver the required Alpha Lab Persian RTL daily PDF. Do not return only text.
```

## S&P 500 — Daily pre-market

```text
Open the attached Vault and execute `87 Alpha Lab Asset-Specific Persian PDF Analysis Prompts/05 S&P 500 Alpha Lab Persian PDF Prompt.md`.

MODE: LIVE
AS_OF: NOW
ANALYSIS_PROFILE: DAILY_PREMARKET
TARGET_DATE: TODAY
REFERENCE_TIMEZONE: America/New_York
SESSION: New York
SESSION_STAGE: PRE_NEW_YORK
DAILY_LOOKBACK: 3D
CATALYST_WINDOW: TODAY
PRIMARY_HORIZON: INTRADAY
REPORT_DEPTH: DEEP
PORTFOLIO_CONTEXT: NONE
SPECIAL_QUESTION: Determine the complete day-horizon fundamental context, sector confirmation, credit and rates leadership, event risks, persistence and invalidation conditions for S&P 500 today.
EX_POST_AUDIT: NO

Create and deliver the required Alpha Lab Persian RTL daily PDF. Do not return only text.
```

## Gold — Daily pre-market

```text
Open the attached Vault and execute `87 Alpha Lab Asset-Specific Persian PDF Analysis Prompts/06 Gold Alpha Lab Persian PDF Prompt.md`.

MODE: LIVE
AS_OF: NOW
ANALYSIS_PROFILE: DAILY_PREMARKET
TARGET_DATE: TODAY
REFERENCE_TIMEZONE: America/New_York
SESSION: New York
SESSION_STAGE: PRE_NEW_YORK
DAILY_LOOKBACK: 3D
CATALYST_WINDOW: TODAY
PRIMARY_HORIZON: INTRADAY
REPORT_DEPTH: DEEP
PORTFOLIO_CONTEXT: NONE
SPECIAL_QUESTION: Determine the complete day-horizon fundamental context for Gold and XAUUSD, including real yields, USD, policy pricing, geopolitical risk, session handoff, flows, persistence and invalidation conditions.
EX_POST_AUDIT: NO

Create and deliver the required Alpha Lab Persian RTL daily PDF. Do not return only text.
```

## EURUSD — Daily pre-market

```text
Open the attached Vault and execute `87 Alpha Lab Asset-Specific Persian PDF Analysis Prompts/07 EURUSD Alpha Lab Persian PDF Prompt.md`.

MODE: LIVE
AS_OF: NOW
ANALYSIS_PROFILE: DAILY_PREMARKET
TARGET_DATE: TODAY
REFERENCE_TIMEZONE: America/New_York
SESSION: New York
SESSION_STAGE: PRE_NEW_YORK
DAILY_LOOKBACK: 3D
CATALYST_WINDOW: TODAY
PRIMARY_HORIZON: INTRADAY
REPORT_DEPTH: DEEP
PORTFOLIO_CONTEXT: NONE
SPECIAL_QUESTION: Determine the complete day-horizon fundamental context for EURUSD, including Fed-ECB repricing, rate differentials, European and U.S. data, dollar funding, session flows, persistence and invalidation conditions.
EX_POST_AUDIT: NO

Create and deliver the required Alpha Lab Persian RTL daily PDF. Do not return only text.
```

## Live session update conversion

Change:

```text
ANALYSIS_PROFILE: LIVE_SESSION_UPDATE
SESSION_STAGE: NEW_YORK
SPECIAL_QUESTION: Explain what changed since the pre-market state, which causal model is winning, whether the current move is fundamentally persistent and what would invalidate it.
```

## Post-event update conversion

Change:

```text
ANALYSIS_PROFILE: POST_EVENT_UPDATE
SESSION_STAGE: NEW_YORK
SPECIAL_QUESTION: Decompose the event surprise, compare it with the priced baseline, identify the causal leader and determine whether the repricing is transient, session-persistent or a multi-day bridge.
```

## End-of-day conversion

Change:

```text
ANALYSIS_PROFILE: END_OF_DAY
SESSION_STAGE: POST_CLOSE
SPECIAL_QUESTION: Attribute the day, compare the outcome with the pre-market state and identify what carries into the next session.
```


## Hourly monitoring

For direction, intensity, consumption and remaining-pressure monitoring, use [[87 Alpha Lab Asset-Specific Persian PDF Analysis Prompts/17 Hourly Fast Launcher Messages]].
