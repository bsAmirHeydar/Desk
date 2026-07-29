---
title: "Worked Usage Examples"
type: guide
status: evergreen
version: 5.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - prompts
  - examples
---
# Worked Usage Examples

## Current Nasdaq full spectrum

```yaml
MARKET: NQ / Nasdaq-100 futures
AS_OF: NOW
TRADE_VEHICLE: CME E-mini Nasdaq-100 front contract
PRIMARY_HORIZON: ALL, emphasis on INTRADAY and 2-10D
SESSION: New York
OUTPUT_LANGUAGE: Persian
SPECIAL_QUESTION: Is the present move rates-led, earnings-led, risk-premium-led or flow-led, and what must confirm?
```

## Historical CPI pre-release reconstruction

```yaml
MARKET: NQ futures
AS_OF: 2024-04-10 08:29:00 America/New_York
TRADE_VEHICLE: NQ front contract known at the cutoff
PRIMARY_HORIZON: INTRADAY
DECISION_QUESTION: What permission was defensible immediately before CPI?
EX_POST_AUDIT: YES
OUTPUT_LANGUAGE: Persian
```

## Current gold swing

```yaml
MARKET: XAUUSD / Gold
AS_OF: NOW
TRADE_VEHICLE: spot proxy with COMEX futures for curve and positioning
PRIMARY_HORIZON: 2-10D
OUTPUT_LANGUAGE: Persian
SPECIAL_QUESTION: Rank real yields, USD, fiscal credibility, official demand, physical demand and positioning by current causal importance.
```

## Historical FX intervention risk

```yaml
MARKET: USDJPY
AS_OF: 2022-09-22 16:00:00 Asia/Tokyo
PRIMARY_HORIZON: ALL
DECISION_QUESTION: What could a disciplined analyst know about intervention probability at the cutoff?
EX_POST_AUDIT: NO
OUTPUT_LANGUAGE: Persian
```

## Current single-stock swing

```yaml
MARKET: NVDA common equity
AS_OF: NOW
TRADE_VEHICLE: common shares versus defined-risk options
PRIMARY_HORIZON: 2-10D and WEEKS
OUTPUT_LANGUAGE: Persian
SPECIAL_QUESTION: Separate company-specific earnings/revision alpha from Nasdaq, rates and AI-capex factor exposure.
```

## Current oil event

```yaml
MARKET: WTI futures
EVENT: EIA Weekly Petroleum Status Report
EVENT_TIME: [exact release time and timezone]
TRADE_VEHICLE: active WTI futures contract
PRIMARY_HORIZON: INTRADAY and 2-10D
OUTPUT_LANGUAGE: Persian
```

## Current relative value

```yaml
LEG_A: Nasdaq-100 futures
LEG_B: S&P 500 futures
MODE: CURRENT
AS_OF: NOW
HORIZON: 2-10D
SPECIAL_QUESTION: Is the spread driven by real-rate duration, earnings revisions, concentration or flow?
OUTPUT_LANGUAGE: Persian
```

## Portfolio hidden-beta audit

```yaml
MODE: CURRENT
AS_OF: NOW
PORTFOLIO:
  - Long NQ: 1.0 risk unit
  - Long Gold: 0.8 risk unit
  - Short DXY: 0.7 risk unit
HORIZON: 2-10D
SPECIAL_QUESTION: Quantify the shared real-yield, USD and liquidity exposures and identify false diversification.
OUTPUT_LANGUAGE: Persian
```
