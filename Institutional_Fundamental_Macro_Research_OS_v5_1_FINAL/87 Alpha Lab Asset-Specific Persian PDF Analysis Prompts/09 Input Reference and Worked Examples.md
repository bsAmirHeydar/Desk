---
title: "Alpha Lab Prompt Input Reference and Worked Examples"
type: usage-reference
status: canonical
version: 10.2.0
created: 2026-07-30
updated: 2026-07-31
language: en
tags: [alpha-lab, prompt-input, examples]
---
# Alpha Lab Prompt Input Reference and Worked Examples

## Input fields

| Field | Required | Meaning |
|---|---:|---|
| `MODE` | yes | `LIVE` or `HISTORICAL` |
| `AS_OF` | yes | `NOW` or exact timestamp plus timezone |
| `ANALYSIS_PROFILE` | yes | `FULL_SPECTRUM`, `DAILY_PREMARKET`, `LIVE_SESSION_UPDATE`, `POST_EVENT_UPDATE` or `END_OF_DAY` |
| `TARGET_DATE` | daily | `TODAY` or exact trading date |
| `REFERENCE_TIMEZONE` | daily | Timezone used for all catalysts and session references |
| `SESSION_STAGE` | daily | Current stage from pre-Asia through post-close |
| `DAILY_LOOKBACK` | daily | `1D`, `3D` or `5D` |
| `CATALYST_WINDOW` | daily | `TODAY`, `24H` or `48H` |
| `PRIMARY_HORIZON` | yes | `ALL`, `STRUCTURAL`, `CYCLICAL`, `TACTICAL`, `2-10D`, `INTRADAY` or `EVENT` |
| `SESSION` | yes | `Global`, `Asia`, `London` or `New York` |
| `REPORT_DEPTH` | yes | `STANDARD` for a concise report or `DEEP` for full institutional depth |
| `PORTFOLIO_CONTEXT` | no | Existing exposures, constraints or `NONE` |
| `SPECIAL_QUESTION` | no | A precise question or `NONE` |
| `EX_POST_AUDIT` | historical | `YES` only when a separate outcome audit is desired |

## Recommended default

```text
MODE: LIVE
AS_OF: NOW
PRIMARY_HORIZON: ALL
SESSION: Global
REPORT_DEPTH: DEEP
PORTFOLIO_CONTEXT: NONE
SPECIAL_QUESTION: Produce the complete current full-spectrum fundamental state.
EX_POST_AUDIT: NO
```

## Intraday example

```text
MODE: LIVE
AS_OF: NOW
PRIMARY_HORIZON: INTRADAY
SESSION: New York
REPORT_DEPTH: STANDARD
PORTFOLIO_CONTEXT: NONE
SPECIAL_QUESTION: Explain the current session's causal leader, whether the move is fundamentally persistent, and which evidence would invalidate the state.
EX_POST_AUDIT: NO
```

## Multi-day example

```text
MODE: LIVE
AS_OF: NOW
PRIMARY_HORIZON: 2-10D
SESSION: Global
REPORT_DEPTH: DEEP
PORTFOLIO_CONTEXT: NONE
SPECIAL_QUESTION: Determine whether the dominant repricing has a multi-day fundamental half-life and identify the next catalyst sequence.
EX_POST_AUDIT: NO
```

## Historical example

```text
MODE: HISTORICAL
AS_OF: 2024-11-07 08:25 America/New_York
PRIMARY_HORIZON: ALL
SESSION: New York
REPORT_DEPTH: DEEP
PORTFOLIO_CONTEXT: NONE
SPECIAL_QUESTION: Reconstruct the full point-in-time state without future leakage.
EX_POST_AUDIT: YES
```


## Recommended daily pre-market default

```text
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
SPECIAL_QUESTION: Produce today's complete day-horizon fundamental context, causal leader, catalyst map, persistence classification and invalidation evidence.
EX_POST_AUDIT: NO
```
