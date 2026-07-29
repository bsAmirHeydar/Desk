---
title: "Fast Launcher Messages"
type: prompt-index
status: evergreen
version: 5.1.0
created: 2026-07-29
updated: 2026-07-29
language: fa
tags:
  - prompt
  - launcher
  - quick-use
---
# Fast Launcher Messages

These messages assume the complete Vault ZIP is already attached in the same ChatGPT conversation.

## Current / Now launcher

~~~text
ZIP را کامل بخوان و دقیقاً طبق نوت `75 ChatGPT Institutional Market Analysis Prompts/02 Current Now Full-Spectrum Fundamental Analysis Prompt` عمل کن.

MARKET: [MARKET]
TRADE_VEHICLE: [optional]
PRIMARY_HORIZON: [ALL / INTRADAY / 2-10D]
SESSION: [optional]
TECHNICAL_CONTEXT: [optional]
SPECIAL_QUESTION: [optional]
OUTPUT_LANGUAGE: Persian
~~~

## Historical launcher

~~~text
ZIP را کامل بخوان و دقیقاً طبق نوت `75 ChatGPT Institutional Market Analysis Prompts/03 Historical Point-in-Time Fundamental Reconstruction Prompt` عمل کن.

MARKET: [MARKET]
AS_OF: [YYYY-MM-DD HH:MM TIMEZONE]
TRADE_VEHICLE: [optional]
PRIMARY_HORIZON: [ALL / INTRADAY / 2-10D]
EX_POST_AUDIT: [NO / YES]
TECHNICAL_CONTEXT: [optional]
SPECIAL_QUESTION: [optional]
OUTPUT_LANGUAGE: Persian
~~~

## Universal launcher

~~~text
ZIP را کامل بخوان و دقیقاً طبق نوت `75 ChatGPT Institutional Market Analysis Prompts/01 Universal Dual-Mode Institutional Market Analysis Prompt` عمل کن.

MARKET: [MARKET]
MODE: [CURRENT / HISTORICAL]
AS_OF: [NOW / exact historical timestamp]
PRIMARY_HORIZON: [ALL / INTRADAY / 2-10D]
EX_POST_AUDIT: [historical only: NO / YES]
OUTPUT_LANGUAGE: Persian
~~~

## Minimal examples

```text
NQ را همین الآن در همه‌ی اسکیل‌های فاندامنتال تحلیل کن؛ MODE=CURRENT؛ افق اصلی INTRADAY و 2-10D.
```

```text
Gold را در 2024-04-12 ساعت 08:25 New York به‌صورت point-in-time تحلیل کن؛ MODE=HISTORICAL؛ EX_POST_AUDIT=NO.
```
