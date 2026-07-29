---
title: "Historical Replay Counterfactual and Attribution Prompt"
type: prompt
status: evergreen
version: 5.1.0
created: 2026-07-29
updated: 2026-07-29
language: fa
tags:
  - prompt
  - historical
  - replay
  - counterfactual
---
# Historical Replay, Counterfactual and Attribution Prompt

## Copy-ready prompt

~~~text
ZIP کامل Institutional Fundamental Macro Research OS را بخوان و این معامله/روز تاریخی را با پروتکل strict point-in-time بازسازی و سپس ممیزی کن:

MARKET: [MARKET]
DECISION_CUTOFF: [YYYY-MM-DD HH:MM TIMEZONE]
TRADE_OR_DECISION: [شرح ورود، عدم ورود، جهت، زمان، یا تصمیم مورد بررسی]
TECHNICAL_INFORMATION_AVAILABLE_THEN: [اختیاری]
HOLDING_HORIZON: [intraday / 2-10D / other]
OUTPUT_LANGUAGE: Persian

مرحله ۱ — BLIND RECONSTRUCTION:
فقط اطلاعات موجود تا cutoff را بازیابی کن و بدون نگاه به نتیجه، state، pricing، scenarios، permission، confidence، invalidation و بهترین تصمیم قابل دفاع را بساز. later revisions و outcome ممنوع‌اند.

مرحله ۲ — LOCKED DECISION:
قبل از دیدن نتیجه، تصمیم پیشنهادی، rejected alternatives، size ceiling، veto و expiry را به‌طور شفاف قفل کن.

مرحله ۳ — EX-POST AUDIT:
فقط بعد از قفل مرحله ۲، داده‌ها و مسیر بعدی قیمت را بررسی کن. decision quality را از outcome quality جدا کن.

مرحله ۴ — ATTRIBUTION:
حرکت را به economic news، policy repricing، term premium، earnings/cash-flow، risk premium، credit، positioning، forced flow، volatility، liquidity و noise نسبت بده. سهم‌ها را range و با uncertainty بیان کن، نه دقت ساختگی.

مرحله ۵ — COUNTERFACTUAL:
بررسی کن اگر permission متفاوت، no-trade، timing متفاوت، expression جایگزین یا size کمتر استفاده می‌شد، چه چیز تغییر می‌کرد. فقط counterfactualهای قابل دفاع را نگه دار.

خروجی:
1. Point-in-time evidence ledger
2. Blind multihorizon reconstruction
3. Locked permission and decision
4. Ex-post outcome path
5. Decision quality versus luck
6. Causal attribution
7. Missed evidence and unavailable evidence
8. False positives and false negatives
9. Counterfactual alternatives
10. Lesson that can be encoded without overfitting
11. Proposed update to rule/model/template
12. Whether the case should change confidence, remain anecdotal, or enter a validation sample
13. Claim-evidence ledger and sources
14. Historical decision-record YAML

از hindsight narrative، cherry-picking و outcome-based condemnation جلوگیری کن.
~~~
