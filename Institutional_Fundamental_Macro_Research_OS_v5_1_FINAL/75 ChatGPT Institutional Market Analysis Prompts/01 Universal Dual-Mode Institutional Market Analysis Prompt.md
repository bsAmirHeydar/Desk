---
title: "01 Universal Dual-Mode Institutional Market Analysis Prompt"
type: production-prompt
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
---
# 01 Universal Dual-Mode Institutional Market Analysis Prompt

```text
Open the attached Institutional Fundamental Macro Research OS Vault ZIP and use it as the governing knowledge and research architecture.

MODE: [LIVE | HISTORICAL]
MARKET: [required]
TRADE_VEHICLE: [optional]
ANALYSIS_CUTOFF: [required for HISTORICAL; ISO timestamp with timezone]
PRIMARY_HORIZON: [ALL | STRUCTURAL | CYCLICAL | TACTICAL | 2-10D | INTRADAY | EVENT]
SESSION: [optional]
PORTFOLIO_CONTEXT: [optional]
SPECIAL_QUESTION: [optional]
EX_POST_AUDIT: [NO | YES; historical only]
OUTPUT_LANGUAGE: [Persian | English]

If MODE=LIVE, execute `02 Current Now Full-Spectrum Fundamental Analysis Prompt`.
If MODE=HISTORICAL, execute `03 Historical Point-in-Time Fundamental Reconstruction Prompt`.

The Vault is mandatory. Price-pattern analysis is prohibited. Use source-controlled fundamental, macro, valuation, institutional-flow, physical-market, market-structure, liquidity and portfolio methods only.

# V8 SCIENTIFIC CERTIFICATION GATE
Before finalizing, open and apply `81 Final Scientific Red-Team and Analysis Certification/00 Final Scientific Red-Team and Analysis Certification MOC`. Run the relevant domain scorecard and benchmark suite. The answer must begin and end with a certification verdict: CERTIFIED — FULL, CERTIFIED — CONDITIONAL, or NOT CERTIFIED. Do not label the answer FULL if any load-bearing claim lacks an exact source locator, current data are stale, historical evidence crosses the cutoff, a material domain was not retrieved, a serious rival model was ignored, or unavailable proprietary information was invented. Include the 60-point certification scorecard and failed gates.
```
