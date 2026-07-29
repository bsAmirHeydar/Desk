---
title: "Current Day-Trading Context Prompt"
type: prompt
status: evergreen
version: 5.1.0
created: 2026-07-29
updated: 2026-07-29
language: fa
tags:
  - prompt
  - current
  - day-trading
---
# Current Day-Trading Context Prompt

## Copy-ready prompt

~~~text
ZIP کامل Institutional Fundamental Macro Research OS را بخوان و برای بازار زیر یک CURRENT institutional day-trading context بساز:

MARKET: [MARKET]
SESSION: [Asia / London / New York]
TRADE_VEHICLE: [اختیاری]
TECHNICAL_CONTEXT: [اختیاری: trend/levels/setup]
OUTPUT_LANGUAGE: Persian

وب را برای وضعیت دقیق همین لحظه جست‌وجو کن. timestamp، timezone، session status، تقویم باقی‌مانده، آخرین نرخ‌ها/real yields/curve، FX، credit، volatility، breadth، commodity/physical data، positioning/flow و خبرهای رسمی مرتبط را بررسی و cite کن.

از Vault این مسیر را اجرا کن:
Inherited structural/cyclical/tactical state → overnight repricing → current priced baseline → today’s causal leader → cross-asset confirmations → flow/liquidity regime → event/non-event playbook → permission → technical handoff.

تمرکز اصلی روی معامله‌پذیری امروز باشد، اما context بزرگ‌تر را فقط به‌اندازه‌ای وارد کن که direction، persistence، veto یا no-trade را تغییر دهد.

خروجی:
1. Exact session clock and market status
2. Overnight/global handoff
3. Higher-horizon inherited state
4. What changed since prior close
5. What is already priced
6. Today’s causal leader hierarchy
7. Cross-asset confirmation matrix
8. Event clock and non-event flow clock
9. Liquidity, volatility, dealer/systematic flow and likely path shape
10. Base continuation, reversal, chop and tail scenarios
11. Permission: LONG_ONLY / SHORT_ONLY / TWO_WAY_REDUCED / NO_TRADE
12. Minimum confirmations before entry
13. Vetoes and immediate invalidation
14. When permission expires
15. Conditions for converting an intraday trade into a 2–10D swing
16. Facts that matter versus noise
17. Claim-evidence ledger and citations
18. Compact YAML context object

ورود، استاپ و تارگت را تعیین نکن مگر اینکه من technical context داده باشم؛ در آن صورت فقط fundamental compatibility و veto را بگو. فاندامنتال حق جابه‌جایی استاپ یا averaging را ندارد.
~~~
