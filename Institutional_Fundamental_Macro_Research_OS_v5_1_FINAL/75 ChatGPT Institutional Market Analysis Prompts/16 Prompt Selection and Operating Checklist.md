---
title: "Prompt Selection and Operating Checklist"
type: guide
status: evergreen
version: 10.0.0
created: 2026-07-29
updated: 2026-07-30
language: en
tags:
  - prompts
  - selection-guide
  - checklist
---
# Prompt Selection and Operating Checklist

## Select the prompt

| Question | Use |
|---|---|
| What is the complete state of this market now? | [[75 ChatGPT Institutional Market Analysis Prompts/02 Current Now Full-Spectrum Fundamental Analysis Prompt]] |
| What could be known at this exact historical moment? | [[75 ChatGPT Institutional Market Analysis Prompts/03 Historical Point-in-Time Fundamental Reconstruction Prompt]] |
| What is permitted in the current session? | [[75 ChatGPT Institutional Market Analysis Prompts/04 Current Day-Trading Context Prompt]] |
| Does the current impulse support a 2-10 day hold? | [[75 ChatGPT Institutional Market Analysis Prompts/05 Current Swing-Trading Context Prompt]] |
| Was a historical decision defensible and why did it work/fail? | [[75 ChatGPT Institutional Market Analysis Prompts/06 Historical Replay Counterfactual and Attribution Prompt]] |
| How should a scheduled or unscheduled catalyst be interpreted? | [[75 ChatGPT Institutional Market Analysis Prompts/13 Current Event and Catalyst Analysis Prompt]] |
| Which market/leg is fundamentally superior? | [[75 ChatGPT Institutional Market Analysis Prompts/14 Cross-Market Relative-Value Analysis Prompt]] |
| Is a portfolio truly diversified or one hidden macro bet? | [[75 ChatGPT Institutional Market Analysis Prompts/15 Portfolio Fundamental Exposure and Hidden-Beta Audit Prompt]] |
| One prompt for both current and historical | [[75 ChatGPT Institutional Market Analysis Prompts/01 Universal Dual-Mode Institutional Market Analysis Prompt]] |

## Before sending

- Upload the complete Vault ZIP in the same conversation.
- Use an exact market/symbol and vehicle when possible.
- Give a timezone for historical analysis.
- State the intended holding horizon.
- Add implementation context only if actually observed.
- Add portfolio context when position interaction matters.
- Choose `EX_POST_AUDIT=NO` for a clean blind reconstruction.

## After receiving the analysis

Reject or ask for correction if:

- no Vault research route is shown;
- current facts lack citations;
- historical data are not vintage/cutoff controlled;
- the analysis does not say what is priced;
- scenario probabilities lack evidence;
- a rival model or cross-asset contradiction is missing;
- permission lacks invalidation or expiry;
- implementation stops are subordinated to the fundamental narrative;
- unknowns are hidden.

## Minimum reusable launcher

```text
Open the uploaded Vault ZIP, execute the selected prompt note exactly, use the Vault as the mandatory methodology, obtain the required current or historical evidence, and deliver the complete output contract now.
```

> [!important] Fundamental-only boundary
> Price-pattern analysis, indicator rules and chart-trigger instructions are prohibited. Use the Vault's fundamental, macro, valuation, flow, liquidity, market-structure and portfolio methods.

## V10 specialist and evidence gate

After selecting the direct primary canonical monograph, check the specialist registry for a narrower legal, industry, instrument or physical-market dependency. Do not retrieve a broad legacy field guide when a specialist canonical note exists. Probabilities must be labelled as empirically calibrated, model-implied or judgmental scenario weights. Internal QA may be reported; external scientific certification may not be claimed.
