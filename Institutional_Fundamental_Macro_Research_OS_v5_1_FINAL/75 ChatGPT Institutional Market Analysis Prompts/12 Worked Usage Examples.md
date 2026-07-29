---
title: "Worked Usage Examples"
type: guide
status: evergreen
version: 5.1.0
created: 2026-07-29
updated: 2026-07-29
language: fa
tags:
  - prompts
  - examples
---
# Worked Usage Examples

## Example 1 — Current Nasdaq

```yaml
MARKET: NQ / Nasdaq 100 futures
MODE: CURRENT
AS_OF: NOW
TRADE_VEHICLE: NQ futures
PRIMARY_HORIZON: ALL, with emphasis on INTRADAY and 2-10D
SESSION: New York
ANALYSIS_DEPTH: FULL
OUTPUT_LANGUAGE: Persian
SPECIAL_QUESTION: Is the current move rates-led, earnings-led, risk-premium-led or flow-led?
```

## Example 2 — Historical CPI day

```yaml
MARKET: NQ futures
MODE: HISTORICAL
AS_OF: 2024-04-10 08:29 America/New_York
TRADE_VEHICLE: NQ futures
PRIMARY_HORIZON: INTRADAY
EX_POST_AUDIT: YES
SPECIAL_QUESTION: What permission was defensible immediately before the CPI release?
```

## Example 3 — Current Gold swing

```yaml
MARKET: XAUUSD / Gold
MODE: CURRENT
AS_OF: NOW
PRIMARY_HORIZON: 2-10D
ANALYSIS_DEPTH: FULL
SPECIAL_QUESTION: Which component matters most now: real yields, USD, fiscal credibility, official demand or positioning?
```

## Example 4 — Historical FX reconstruction

```yaml
MARKET: USDJPY
MODE: HISTORICAL
AS_OF: 2022-09-22 16:00 Asia/Tokyo
PRIMARY_HORIZON: ALL
EX_POST_AUDIT: NO
SPECIAL_QUESTION: What could an informed analyst know about intervention risk at the cutoff?
```

## Example 5 — Current single stock

```yaml
MARKET: NVDA / Nasdaq
MODE: CURRENT
AS_OF: NOW
TRADE_VEHICLE: common equity or options comparison
PRIMARY_HORIZON: 2-10D and WEEKS
SPECIAL_QUESTION: Separate company-specific earnings/revision alpha from Nasdaq, rates and AI-capex factor exposure.
```

## Example 6 — Historical trade replay

```yaml
MARKET: WTI futures
DECISION_CUTOFF: 2020-04-20 09:30 America/New_York
TRADE_OR_DECISION: Evaluate whether long front-month crude was defensible.
HOLDING_HORIZON: intraday
EX_POST_AUDIT: YES
```
