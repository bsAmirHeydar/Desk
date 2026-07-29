---
title: "ChatGPT Institutional Market Analysis Prompts MOC"
type: moc
status: evergreen
version: 5.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - moc
  - prompts
  - chatgpt
  - institutional-research
  - live-analysis
  - historical-reconstruction
---
# ChatGPT Institutional Market Analysis Prompts

This module turns the complete **Institutional Fundamental Macro Research OS** Vault into an operational research protocol for ChatGPT. The prompts are written in English so the model receives an unambiguous, production-grade instruction set. The final analysis may be returned in any language selected by the user.

The Vault must be uploaded with the prompt. The model is required to open the archive, discover the Vault root, read the governing notes, search the relevant market and model modules, and use the Vault's methodology throughout the analysis. A generic answer produced from memory is a failed execution.

## Primary prompts

| Use case | Prompt |
|---|---|
| One master prompt for either live or historical work | [[75 ChatGPT Institutional Market Analysis Prompts/01 Universal Dual-Mode Institutional Market Analysis Prompt]] |
| Deep live/current market-state analysis | [[75 ChatGPT Institutional Market Analysis Prompts/02 Current Now Full-Spectrum Fundamental Analysis Prompt]] |
| Strict historical point-in-time reconstruction | [[75 ChatGPT Institutional Market Analysis Prompts/03 Historical Point-in-Time Fundamental Reconstruction Prompt]] |
| Live intraday/day-trading context | [[75 ChatGPT Institutional Market Analysis Prompts/04 Current Day-Trading Context Prompt]] |
| Live two-to-ten-day swing campaign | [[75 ChatGPT Institutional Market Analysis Prompts/05 Current Swing-Trading Context Prompt]] |
| Historical decision replay and counterfactual audit | [[75 ChatGPT Institutional Market Analysis Prompts/06 Historical Replay Counterfactual and Attribution Prompt]] |
| Live event and catalyst analysis | [[75 ChatGPT Institutional Market Analysis Prompts/13 Current Event and Catalyst Analysis Prompt]] |
| Cross-market or relative-value comparison | [[75 ChatGPT Institutional Market Analysis Prompts/14 Cross-Market Relative-Value Analysis Prompt]] |
| Portfolio fundamental exposure and hidden-beta audit | [[75 ChatGPT Institutional Market Analysis Prompts/15 Portfolio Fundamental Exposure and Hidden-Beta Audit Prompt]] |

## Operating documents

- [[75 ChatGPT Institutional Market Analysis Prompts/07 Fast Launcher Messages]]
- [[75 ChatGPT Institutional Market Analysis Prompts/08 Prompt Input Specification]]
- [[75 ChatGPT Institutional Market Analysis Prompts/09 Output Contract and Quality Gates]]
- [[75 ChatGPT Institutional Market Analysis Prompts/10 Vault Reading and Evidence Protocol]]
- [[75 ChatGPT Institutional Market Analysis Prompts/11 Market-Specific Add-On Blocks]]
- [[75 ChatGPT Institutional Market Analysis Prompts/12 Worked Usage Examples]]
- [[75 ChatGPT Institutional Market Analysis Prompts/16 Prompt Selection and Operating Checklist]]

## Mandatory operating doctrine

Every valid execution must follow this chain:

```text
Vault inspection and research-route construction
-> exact market and instrument identity
-> point-in-time evidence set
-> economic and market state distributions
-> expectations and what is already priced
-> pricing gap and vulnerable assumptions
-> causal model plus rival models
-> cross-asset transmission and independent confirmation
-> positioning, liquidity, volatility and flow ecology
-> multihorizon scenarios and payoff distributions
-> portfolio-aware permission
-> technical execution handoff
-> invalidation, expiry, attribution and calibration
```

## What the Vault is and is not

The Vault is the authoritative **methodology, ontology, model library, market-driver map, source protocol, decision architecture and quality-control system** for the analysis. It is not a live data feed and must never be treated as one.

- In **CURRENT/LIVE** mode, the model must obtain and verify current evidence through web research and available data tools.
- In **HISTORICAL** mode, the model must reconstruct only the information that was available at or before the exact cutoff and must prevent all outcome and revision leakage.

## Required status outputs

Every primary analysis must provide:

1. exact analysis timestamp or historical cutoff;
2. market identity and contract/vehicle mapping;
3. Vault research route and notes materially used;
4. structural, cyclical, tactical, swing, daily, event and microstructure states;
5. current or reconstructed expectations and priced distribution;
6. dominant causal driver, rival explanations and cross-asset leader;
7. base, bullish, bearish and tail scenarios;
8. directional permission: `LONG_ONLY`, `SHORT_ONLY`, `TWO_WAY_REDUCED`, or `NO_TRADE`;
9. confidence, size ceiling, invalidation, expiry and next catalyst;
10. technical handoff without moving stops or averaging losses for fundamental reasons;
11. claim-evidence ledger and unresolved data gaps;
12. machine-readable context object.

The output is an institutional research state, not a promise of profit and not a substitute for execution controls.
