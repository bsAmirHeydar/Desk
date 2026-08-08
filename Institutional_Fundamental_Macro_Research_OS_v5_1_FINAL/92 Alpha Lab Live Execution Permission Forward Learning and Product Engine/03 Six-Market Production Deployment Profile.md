---
title: "Six-Market Production Deployment Profile"
type: deployment-profile
status: active
version: 14.1.0
---
# Six-Market Production Deployment Profile

## Production universe
- XAUUSD
- NASDAQ100
- SP500
- DJIA
- EURUSD
- USDJPY

WTI / crude / USOIL are excluded from this **deployment profile only**. V13 continues to support crude oil and other commodities universally.

## Per-family depth
### XAUUSD
Real/nominal yields, USD/Fed path, safe-haven/geopolitics, official-sector demand, ETF/futures/physical evidence, liquidity liquidation, inflation/credibility and reserve-diversification.

### EURUSD / USDJPY
Both currency blocks; relative policy and real-rate paths; growth/inflation/fiscal/external balance; terms of trade; carry; funding/basis; hedging; intervention; global-dollar/risk overlay.

### NASDAQ100 / SP500 / DJIA
Methodology/exposure/concentration; earnings/revisions/margins; valuation; real rates/risk premium; breadth/sector leadership; passive/foreign/systematic flows where observable; futures/options/volatility proxies; rebalance and political/regulatory risk.

## Scheduling
The active ChatGPT production contract uses one hourly workflow. A second overlapping daily schedule should not coexist in the same deployment because it can create duplicate or inconsistent states.
