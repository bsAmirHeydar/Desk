---
title: "Alpha Lab Hourly Fundamental Fast Launcher Messages"
type: launcher-library
status: canonical
version: 10.3.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [alpha-lab, hourly, launcher, pdf, direction, consumption]
---
# Alpha Lab Hourly Fundamental Fast Launcher Messages

Attach the complete Vault ZIP and send one launcher.

## Nasdaq 100 — hourly live monitor

```text
Open the attached Vault and execute `87 Alpha Lab Asset-Specific Persian PDF Analysis Prompts/04 Nasdaq 100 Alpha Lab Persian PDF Prompt.md`.

MODE: LIVE
AS_OF: NOW
ANALYSIS_PROFILE: LIVE_SESSION_UPDATE
HOURLY_MODE: HOURLY_LIVE_MONITOR
SNAPSHOT_INTERVAL_MINUTES: 60
SNAPSHOT_START: 04:00 America/New_York
SNAPSHOT_END: 20:00 America/New_York
EVENT_DRIVEN_UPDATES: YES
EVENT_MICRO_WINDOWS: T-60_T-15_T+5_T+15_T+60
COMPARE_TO_PRIOR_SNAPSHOT: YES
TARGET_DATE: TODAY
REFERENCE_TIMEZONE: America/New_York
SESSION: New York
SESSION_STAGE: NEW_YORK
DAILY_LOOKBACK: 3D
CATALYST_WINDOW: TODAY
PRIMARY_HORIZON: INTRADAY
REPORT_DEPTH: DEEP
PORTFOLIO_CONTEXT: NONE
SPECIAL_QUESTION: Produce the complete hour-by-hour fundamental state for Nasdaq 100, including direction, intensity, confidence, information absorption, repricing completion, flow exhaustion, remaining fundamental pressure, persistence, reversal risk, causal leadership and all material state changes.
EX_POST_AUDIT: NO

Create and deliver the required Alpha Lab Persian RTL hourly PDF. Do not return only text.
```

## S&P 500 — hourly live monitor

```text
Open the attached Vault and execute `87 Alpha Lab Asset-Specific Persian PDF Analysis Prompts/05 S&P 500 Alpha Lab Persian PDF Prompt.md`.

MODE: LIVE
AS_OF: NOW
ANALYSIS_PROFILE: LIVE_SESSION_UPDATE
HOURLY_MODE: HOURLY_LIVE_MONITOR
SNAPSHOT_INTERVAL_MINUTES: 60
SNAPSHOT_START: 04:00 America/New_York
SNAPSHOT_END: 20:00 America/New_York
EVENT_DRIVEN_UPDATES: YES
EVENT_MICRO_WINDOWS: T-60_T-15_T+5_T+15_T+60
COMPARE_TO_PRIOR_SNAPSHOT: YES
TARGET_DATE: TODAY
REFERENCE_TIMEZONE: America/New_York
SESSION: New York
SESSION_STAGE: NEW_YORK
DAILY_LOOKBACK: 3D
CATALYST_WINDOW: TODAY
PRIMARY_HORIZON: INTRADAY
REPORT_DEPTH: DEEP
PORTFOLIO_CONTEXT: NONE
SPECIAL_QUESTION: Produce the complete hour-by-hour fundamental state for S&P 500, including direction, intensity, consumption, remaining pressure, sector confirmation, credit and rates leadership, persistence and reversal risk.
EX_POST_AUDIT: NO

Create and deliver the required Alpha Lab Persian RTL hourly PDF. Do not return only text.
```

## Gold — hourly live monitor

```text
Open the attached Vault and execute `87 Alpha Lab Asset-Specific Persian PDF Analysis Prompts/06 Gold Alpha Lab Persian PDF Prompt.md`.

MODE: LIVE
AS_OF: NOW
ANALYSIS_PROFILE: LIVE_SESSION_UPDATE
HOURLY_MODE: HOURLY_LIVE_MONITOR
SNAPSHOT_INTERVAL_MINUTES: 60
SNAPSHOT_START: 00:00 UTC
SNAPSHOT_END: 23:00 UTC
EVENT_DRIVEN_UPDATES: YES
EVENT_MICRO_WINDOWS: T-60_T-15_T+5_T+15_T+60
COMPARE_TO_PRIOR_SNAPSHOT: YES
TARGET_DATE: TODAY
REFERENCE_TIMEZONE: UTC
SESSION: Global
SESSION_STAGE: NEW_YORK
DAILY_LOOKBACK: 3D
CATALYST_WINDOW: TODAY
PRIMARY_HORIZON: INTRADAY
REPORT_DEPTH: DEEP
PORTFOLIO_CONTEXT: NONE
SPECIAL_QUESTION: Produce the complete hour-by-hour fundamental state for Gold and XAUUSD, including direction, intensity, real-yield and dollar leadership, information absorption, repricing completion, flow exhaustion, remaining pressure, session handoff, persistence and reversal risk.
EX_POST_AUDIT: NO

Create and deliver the required Alpha Lab Persian RTL hourly PDF. Do not return only text.
```

## EURUSD — hourly live monitor

```text
Open the attached Vault and execute `87 Alpha Lab Asset-Specific Persian PDF Analysis Prompts/07 EURUSD Alpha Lab Persian PDF Prompt.md`.

MODE: LIVE
AS_OF: NOW
ANALYSIS_PROFILE: LIVE_SESSION_UPDATE
HOURLY_MODE: HOURLY_LIVE_MONITOR
SNAPSHOT_INTERVAL_MINUTES: 60
SNAPSHOT_START: 06:00 Europe/London
SNAPSHOT_END: 17:00 America/New_York
EVENT_DRIVEN_UPDATES: YES
EVENT_MICRO_WINDOWS: T-60_T-15_T+5_T+15_T+60
COMPARE_TO_PRIOR_SNAPSHOT: YES
TARGET_DATE: TODAY
REFERENCE_TIMEZONE: America/New_York
SESSION: Global
SESSION_STAGE: NEW_YORK
DAILY_LOOKBACK: 3D
CATALYST_WINDOW: TODAY
PRIMARY_HORIZON: INTRADAY
REPORT_DEPTH: DEEP
PORTFOLIO_CONTEXT: NONE
SPECIAL_QUESTION: Produce the complete hour-by-hour fundamental state for EURUSD, including direction, intensity, Fed-ECB repricing, rate-differential leadership, consumption, remaining pressure, fixing and flow effects, persistence and reversal risk.
EX_POST_AUDIT: NO

Create and deliver the required Alpha Lab Persian RTL hourly PDF. Do not return only text.
```

## Historical hourly replay conversion

Change:

```text
MODE: HISTORICAL
AS_OF: [exact end-of-replay timestamp]
ANALYSIS_PROFILE: END_OF_DAY
HOURLY_MODE: HISTORICAL_HOURLY_REPLAY
EX_POST_AUDIT: NO
SPECIAL_QUESTION: Reconstruct every hourly fundamental state using only information available at each hourly cutoff. Do not use the final outcome to assign earlier states.
```

## Post-event hourly conversion

Change:

```text
ANALYSIS_PROFILE: POST_EVENT_UPDATE
HOURLY_MODE: HOURLY_POST_EVENT
EVENT_MICRO_WINDOWS: T-60_T-15_T+5_T+15_T+60
SPECIAL_QUESTION: Decompose the event and show how direction, intensity, consumption, remaining pressure and persistence changed from before the event through T+60 minutes.
```
