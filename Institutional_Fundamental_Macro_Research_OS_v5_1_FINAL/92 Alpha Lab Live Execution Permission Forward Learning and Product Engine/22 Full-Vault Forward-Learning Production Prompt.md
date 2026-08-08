---
title: "Alpha Lab V14.1 — Full-Vault Forward-Learning Six-Market Production Prompt"
type: production-live-analysis-prompt
status: execution-ready
version: 14.1.0
language: en
output_language: fa
---
# Alpha Lab V14.1 — Full-Vault Forward-Learning Production Prompt

Execute Alpha Lab in **FULL-VAULT, ZERO-SHORTCUT, FORWARD-LEARNING** mode for XAUUSD, NASDAQ100, SP500, DJIA, EURUSD and USDJPY. WTI/crude/USOIL is excluded from this deployment profile only.

## 1. Fresh six-market adjudication
Freshly re-research and independently adjudicate all six markets from the current point-in-time evidence set. Never replace a full run with a quick refresh, headline scan, partial-symbol update or copied prior state.

Apply all relevant canonical science:
- V11 / Module 89 for force, consumption, remaining pressure, fact persistence, reversal risk and fundamental asymmetry;
- V12 / Module 90 for attention, narratives, dominance, validity, persistence, saturation, reflexivity, ignored facts and transitions;
- V13 / Module 91 for instrument resolution and family adapters;
- V14 live rules for point-in-time, six horizons, scenarios, invalidation and next review;
- V14.1 / Module 92 for Edge, permission, forward learning and product output.

Use dynamic retrieval: retrieve all relevant specialist notes and source/data contracts, but do not load irrelevant parts of the Vault merely for file-count optics. Record the important Vault paths used.

For every market analyze independently:
- instrument identity/session/current reliable price context;
- MICRO 0–15m, SHORT 15–60m, SESSION 1–6h, DAILY, NEXT_24H, MULTI_DAY_2_5D;
- fact universe, expectations, surprise, materiality;
- force and strongest opposing force;
- available vs ACTIVE driver;
- activation, conditional sensitivity and transmission integrity;
- causal/independent/mechanical/correlated/lagging/contradictory/unavailable confirmations;
- cross-asset causal leaders and confirmation breaks;
- market attention and ignored facts;
- dominant/challenger/opposing narratives, validity, dominance, price control, persistence, saturation, fragility, transition;
- fact persistence separately from narrative persistence;
- consumption/repricing with anti-trap checks;
- remaining pressure independently from consumption;
- reversal hazard/exhaustion;
- horizon conflict;
- observable flow/positioning/liquidity/volatility with explicit limits;
- scheduled/unscheduled event risk;
- base, bullish expansion, bearish expansion, failed-break/reversal, range/no-edge and event-binary paths when applicable;
- factual, narrative, causal-leader, price-control, cross-asset, event, time and data-confidence invalidations;
- exact next review and early triggers;
- source quality and confidence caps.

## 2. Asset-specific depth
### EURUSD / USDJPY
Full bilateral synthesis of both currency blocks, relative policy/real rates/growth/inflation/fiscal/external balance/terms of trade/carry/funding-basis/hedging/intervention/global-dollar-risk overlay.

### NASDAQ100 / SP500 / DJIA
Methodology/exposure/concentration, earnings/revisions/margins, valuation, real rates/risk premium, breadth/sector leadership, passive/foreign/systematic flows where observable, futures/options/volatility proxies, rebalance and political/regulatory risk.

### XAUUSD
Real/nominal yields, USD/Fed path, safe-haven/geopolitics, official-sector demand, ETF/futures/physical demand where observable, liquidity liquidation, inflation/credibility and reserve-diversification.

## 3. Prior-call learning before the new verdict
Load the immutable state archive and learning ledger. For each symbol, compare the previous call with the realized path only for horizons that have matured. Use reliable MFE/MAE or path proxies when available; otherwise state `UNAVAILABLE`.

Audit prior direction, timing, driver, narrative, consumption, remaining pressure, persistence, reversal risk, Edge, permission, invalidations, transition triggers and next-review timing. Classify using the Module 92 learning taxonomy.

### Hindsight firewall
Future price may identify a failure but may never be used as if it were evidence at the previous timestamp. Ask whether a better decision was justified using only information available then. A move after NO_TRADE is not automatically a missed opportunity.

## 4. Learning generation and governance
Create operationally specific, falsifiable observations/candidates. Promotion path: OBSERVATION → CANDIDATE → VALIDATED → CANONICAL. Never promote one anecdote directly to canonical methodology. Preserve rival explanations and contradictory evidence.

Apply already VALIDATED/CANONICAL learnings. Provisional CANDIDATE rules may influence working hypotheses only when explicitly labelled and must not silently rewrite core science.

## 5. Event-proximity candidate
A future high-impact event must not automatically veto an otherwise currently tradable Edge. Distinguish:
- `EVENT_AS_EXPIRY_CONSTRAINT`: Active may remain valid with `valid_until` safely before the risk window;
- `EVENT_AS_VETO`: use when event proximity already creates fragmentation, unstable price control, transmission failure, liquidity deterioration, unfavorable asymmetry or insufficient execution time.

This remains a CANDIDATE until forward validation promotes it.

## 6. Edge adjudication
Treat Direction, Confidence, Edge and Permission separately. Assign one class:
`EDGE_ACTIVE`, `EDGE_CONDITIONAL`, `EDGE_RELATIVE`, `BIAS_ONLY`, `NO_EDGE`, `EVENT_OR_FRAGMENTED`, `INSUFFICIENT_EVIDENCE`.

### Conditional disclosure
For every `EDGE_CONDITIONAL`, include a complete `Why Not Active?` block: reason, ranked decisive blockers, caution factors, missing evidence, exact upgrade triggers, downgrade triggers, event veto-vs-expiry classification, usable time window/valid_until, blocker-removal evidence and whether a pre-event opportunity exists but is withheld for insufficient evidence.

### Permission
- EDGE_ACTIVE + bullish approved direction → BUY
- EDGE_ACTIVE + bearish approved direction → SELL
- everything else → NO_TRADE

## 7. Execution handoff
Entry timing is external and mechanical: M1 Donchian-20 using prior 20 completed bars; BUY allows upper break only; SELL lower break only. Initial stop = 4 ATR. Exit = candle-by-candle trailing. Permission affects new entries only; open trades remain under mechanical exit logic.

## 8. Persistence
Append all six new full states to the immutable archive. Append run-level learning observations/candidates to the learning ledger. On final Tehran run of the trading day, create the Daily Learning Commit. Do not claim persistence if the write fails.

## 9. Human output
Create/update `AlphaLab_Intelligence_Explorer.html` as a polished Persian RTL complete report. Required views: Overview, Markets, Compare, per-market Summary, Full Analysis, Sources, Learning/Prior-Call Review, and `Why Not Active?` for every conditional Edge. Preserve the Module 92 visual/product contract.

Create/update `AlphaLab_Execution_Permissions.json` with only generated_at_utc and the six permission + valid_until fields. Missing/malformed/stale/expired → NO_TRADE.

Do not produce routine PDFs, ZIPs, Markdown reports or CSV product outputs.

## 10. Email
Send a simple no-attachment email: Tehran timestamp, optional one-line cross-market note, and six rows `Symbol | Edge Level | Permission`. Do not put full analysis or learning details into email.

## 11. Quality gate
Never call a run Full-Vault unless all six markets were freshly adjudicated at the required depth. Never fabricate unavailable data. Never claim a learning was persisted or the core Vault changed unless the write/update was actually completed and verified.
