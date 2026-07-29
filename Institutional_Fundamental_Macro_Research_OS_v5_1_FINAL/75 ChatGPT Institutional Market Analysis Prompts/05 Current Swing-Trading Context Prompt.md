---
title: "Current Swing-Trading Context Prompt"
type: prompt
status: evergreen
version: 5.1.0
created: 2026-07-29
updated: 2026-07-29
language: fa
tags:
  - prompt
  - current
  - swing-trading
---
# Current Swing-Trading Context Prompt

## Copy-ready prompt

~~~text
ZIP کامل Institutional Fundamental Macro Research OS را باز کن و برای بازار زیر یک CURRENT institutional swing campaign analysis با افق دو تا ده روز معاملاتی بساز:

MARKET: [MARKET]
TRADE_VEHICLE: [اختیاری]
HOLDING_WINDOW: [2-10D یا مقدار دیگر]
TECHNICAL_CONTEXT: [اختیاری]
PORTFOLIO_CONTEXT: [اختیاری]
OUTPUT_LANGUAGE: Persian

حتماً وضعیت جاری را از وب و منابع معتبر به‌روز کن. تحلیل فقط رویدادمحور نباشد؛ continuation of repricing، earnings revisions، Treasury/funding calendar، physical balances، index/option expiry، positioning unwind، systematic flow، carry، seasonality و non-event information decay را هم بررسی کن.

از Vault برای تفکیک Structural، Cyclical، Tactical، Swing و Daily استفاده کن. تعیین کن کدام لایه برای افق 2–10D غالب است و کدام لایه فقط prior یا veto می‌سازد.

خروجی:
1. Exact as-of and evidence cutoff
2. Swing executive thesis
3. Multihorizon inheritance/conflict table
4. State versus priced expectations
5. Main repricing gap
6. Driver tree and causal transmission
7. Cross-asset confirmation and best expression comparison
8. Positioning/crowding/carry/roll/financing
9. Catalyst path for every day in holding window
10. Base/Bull/Bear/Tail scenarios with probability ranges
11. Expected thesis half-life and decay curve
12. Overnight/weekend/gap risks
13. Fundamental permission and size ceiling
14. Entry compatibility conditions, without overriding technical execution
15. Add/hold/reduce/exit conditions
16. Fundamental, market-implied and time invalidation
17. Conditions that convert the setup into no-trade
18. Alternative relative-value or hedged expression
19. Claim-evidence ledger
20. YAML swing context object

بین «جهت درست» و «trade expression درست» فرق بگذار. هزینه، carry، volatility، liquidity، convexity و hidden factor concentration را وارد تصمیم کن.
~~~
