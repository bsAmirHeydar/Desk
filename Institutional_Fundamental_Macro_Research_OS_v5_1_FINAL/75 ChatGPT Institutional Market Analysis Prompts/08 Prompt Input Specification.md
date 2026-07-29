---
title: "Prompt Input Specification"
type: standard
status: evergreen
version: 5.1.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - prompts
  - input-contract
  - analysis
---
# Prompt Input Specification

Use the following fields. Only `MARKET` and `MODE` are strictly required; the model must infer reasonable defaults for omitted fields and disclose them instead of delaying the analysis.

```yaml
MARKET: "Instrument, symbol, asset, spread, curve, sector, country or theme"
MODE: "CURRENT | HISTORICAL"
AS_OF: "NOW or YYYY-MM-DD HH:MM timezone"
TRADE_VEHICLE: "Optional cash, futures, CFD, ETF, option, spread or pair"
PRIMARY_HORIZON: "ALL | INTRADAY | 2-10D | WEEKS | MONTHS"
SESSION: "Optional Asia | London | New York | full global day"
ANALYSIS_DEPTH: "FULL | STANDARD | EXECUTIVE"
OUTPUT_LANGUAGE: "Persian by default"
TECHNICAL_CONTEXT: "Optional trend, levels, setup or chart observation"
PORTFOLIO_CONTEXT: "Optional existing exposures and risk constraints"
SPECIAL_QUESTION: "Optional decision question"
EX_POST_AUDIT: "Historical mode only: NO by default | YES"
```

## Mode definitions

### CURRENT

`AS_OF` means the exact present moment. The analysis must establish the current timestamp and market-session status, use the latest available evidence, and distinguish data/reference time from publication time.

### HISTORICAL

`AS_OF` is the **information cutoff**. The model must reason as an informed analyst standing at that exact date and time. Later revisions, later releases, later policy decisions and later price outcomes are prohibited from the reconstructed decision state.

If `EX_POST_AUDIT=YES`, subsequent outcomes may appear only in a clearly separated section after the point-in-time analysis is locked.

## Recommended market identifiers

- Equity index: `NQ`, `Nasdaq 100`, `ES`, `S&P 500`, `DAX`, `Nikkei 225`
- Rates: `US 2Y`, `US 10Y`, `2s10s`, `SOFR strip`, `Bund`, `JGB`
- FX: `EURUSD`, `USDJPY`, `DXY`, `USDCAD`, `EURGBP`
- Commodities: `Gold`, `XAUUSD`, `WTI`, `Brent`, `Copper`, `Natural Gas`
- Credit: `CDX IG`, `CDX HY`, `HY spreads`, `bank CDS`
- Crypto: `BTC`, `ETH`, `BTC/Nasdaq relative value`
- Equity/security: ticker plus exchange, for example `NVDA / Nasdaq`
- Relative value: define both legs and ratio/spread convention.

## Default horizon ladder

Unless the user overrides it, the full analysis uses:

| Layer | Default horizon |
|---|---|
| Structural | 3–10+ years |
| Secular/strategic | 1–5 years |
| Cyclical | 3–24 months |
| Tactical | 2–12 weeks |
| Swing | 2–10 trading days |
| Daily/session | current trading day |
| Event | minutes to several sessions |
| Microstructure | seconds to hours |
