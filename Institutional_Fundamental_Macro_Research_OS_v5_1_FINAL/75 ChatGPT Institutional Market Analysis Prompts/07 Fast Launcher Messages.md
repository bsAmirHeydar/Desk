---
title: "Fast Launcher Messages"
type: prompt-library
status: evergreen
version: 5.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - prompts
  - launchers
  - current
  - historical
---
# Fast Launcher Messages

Upload the complete Vault ZIP first, then paste one launcher and replace the bracketed fields.

## Live/current full-spectrum

~~~text
Open the uploaded Institutional Fundamental Macro Research OS ZIP and execute the complete instructions in `75 ChatGPT Institutional Market Analysis Prompts/02 Current Now Full-Spectrum Fundamental Analysis Prompt`.

MARKET: [market or symbol]
TRADE_VEHICLE: [optional]
PRIMARY_HORIZON: [ALL | INTRADAY | 2-10D | WEEKS | MONTHS]
SESSION: [optional]
PORTFOLIO_CONTEXT: [optional]
SPECIAL_QUESTION: [optional]
OUTPUT_LANGUAGE: [Persian]

Use the Vault as the mandatory research method and perform current web research with inline citations. Deliver the complete analysis now.
~~~

## Historical point-in-time

~~~text
Open the uploaded Institutional Fundamental Macro Research OS ZIP and execute the complete instructions in `75 ChatGPT Institutional Market Analysis Prompts/03 Historical Point-in-Time Fundamental Reconstruction Prompt`.

MARKET: [market or symbol]
AS_OF: [YYYY-MM-DD HH:MM:SS TIMEZONE]
TRADE_VEHICLE: [optional]
PRIMARY_HORIZON: [ALL | INTRADAY | 2-10D | WEEKS | MONTHS]
DECISION_QUESTION: [optional]
EX_POST_AUDIT: [NO | YES]
OUTPUT_LANGUAGE: [Persian]

Freeze the information set at the cutoff. Do not use later prices, revisions, events or outcomes in the reconstructed section.
~~~

## Universal dual mode

~~~text
Open the uploaded Institutional Fundamental Macro Research OS ZIP and execute `75 ChatGPT Institutional Market Analysis Prompts/01 Universal Dual-Mode Institutional Market Analysis Prompt`.

MARKET: [market or symbol]
MODE: [CURRENT | HISTORICAL]
AS_OF: [NOW | YYYY-MM-DD HH:MM:SS TIMEZONE]
TRADE_VEHICLE: [optional]
PRIMARY_HORIZON: [ALL | INTRADAY | 2-10D | WEEKS | MONTHS]
SESSION: [optional]
PORTFOLIO_CONTEXT: [optional]
SPECIAL_QUESTION: [optional]
EX_POST_AUDIT: [NO | YES for historical]
OUTPUT_LANGUAGE: [Persian]
~~~

## Live intraday

~~~text
Open the uploaded Vault and execute `75 ChatGPT Institutional Market Analysis Prompts/04 Current Day-Trading Context Prompt`.

MARKET: [market or symbol]
TRADE_VEHICLE: [optional]
SESSION: [Asia | London | New York | Global]
SPECIAL_QUESTION: [optional]
OUTPUT_LANGUAGE: [Persian]
~~~

## Live swing

~~~text
Open the uploaded Vault and execute `75 ChatGPT Institutional Market Analysis Prompts/05 Current Swing-Trading Context Prompt`.

MARKET: [market or symbol]
TRADE_VEHICLE: [optional]
HOLDING_HORIZON: [2-10 trading days]
PORTFOLIO_CONTEXT: [optional]
SPECIAL_QUESTION: [optional]
OUTPUT_LANGUAGE: [Persian]
~~~

## Live event/catalyst

~~~text
Open the uploaded Vault and execute `75 ChatGPT Institutional Market Analysis Prompts/13 Current Event and Catalyst Analysis Prompt`.

MARKET: [market or symbol]
EVENT: [event or catalyst]
EVENT_TIME: [YYYY-MM-DD HH:MM TIMEZONE]
TRADE_VEHICLE: [optional]
PRIMARY_HORIZON: [INTRADAY | 2-10D]
OUTPUT_LANGUAGE: [Persian]
~~~

## Relative-value comparison

~~~text
Open the uploaded Vault and execute `75 ChatGPT Institutional Market Analysis Prompts/14 Cross-Market Relative-Value Analysis Prompt`.

LEG_A: [market/instrument]
LEG_B: [market/instrument]
MODE: [CURRENT | HISTORICAL]
AS_OF: [NOW | YYYY-MM-DD HH:MM:SS TIMEZONE]
HORIZON: [INTRADAY | 2-10D | WEEKS | MONTHS]
OUTPUT_LANGUAGE: [Persian]
~~~

## Portfolio exposure audit

~~~text
Open the uploaded Vault and execute `75 ChatGPT Institutional Market Analysis Prompts/15 Portfolio Fundamental Exposure and Hidden-Beta Audit Prompt`.

MODE: [CURRENT | HISTORICAL]
AS_OF: [NOW | YYYY-MM-DD HH:MM:SS TIMEZONE]
PORTFOLIO: [positions, direction, size or weights]
HORIZON: [INTRADAY | 2-10D | WEEKS | MONTHS]
OUTPUT_LANGUAGE: [Persian]
~~~

> [!important] Fundamental-only boundary
> Price-pattern analysis, indicator rules and chart-trigger instructions are prohibited. Use the Vault's fundamental, macro, valuation, flow, liquidity, market-structure and portfolio methods.
