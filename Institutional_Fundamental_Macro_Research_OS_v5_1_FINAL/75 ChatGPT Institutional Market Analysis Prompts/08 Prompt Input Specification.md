---
title: "08 Prompt Input Specification"
type: prompt-contract
status: evergreen
version: 10.0.0
created: 2026-07-29
updated: 2026-07-30
language: en
---
# 08 Prompt Input Specification

| Field | Required | Definition |
|---|---|---|
| MODE | Universal prompt | LIVE or HISTORICAL |
| MARKET | Yes | Exact market, asset, security, country, curve or portfolio |
| TRADE_VEHICLE | Recommended | Exact instrument or instrument universe |
| AS_OF | Live | NOW |
| ANALYSIS_CUTOFF | Historical | ISO timestamp and timezone |
| PRIMARY_HORIZON | Yes | ALL, STRUCTURAL, CYCLICAL, TACTICAL, 2-10D, INTRADAY or EVENT |
| SESSION | Optional | Global, Asia, London or New York |
| PORTFOLIO_CONTEXT | Optional | Existing positions, exposures, limits and funding constraints |
| SPECIAL_QUESTION | Optional | Concrete decision or mechanism question |
| EX_POST_AUDIT | Historical | NO or YES |
| OUTPUT_LANGUAGE | Yes | Persian or English |

No chart or indicator context is accepted. Relevant current or historical market data are independently researched as part of the fundamental information set.

## V10 specialist and evidence gate

After selecting the direct primary canonical monograph, check the specialist registry for a narrower legal, industry, instrument or physical-market dependency. Do not retrieve a broad legacy field guide when a specialist canonical note exists. Probabilities must be labelled as empirically calibrated, model-implied or judgmental scenario weights. Internal QA may be reported; external scientific certification may not be claimed.
