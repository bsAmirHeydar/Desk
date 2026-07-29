---
title: "Historical Point-in-Time Fundamental Reconstruction Prompt"
type: prompt
status: evergreen
version: 5.1.0
created: 2026-07-29
updated: 2026-07-29
language: fa
tags:
  - prompt
  - historical
  - point-in-time
  - no-lookahead
---
# Historical Point-in-Time Fundamental Reconstruction Prompt

## Copy-ready prompt

~~~text
ZIP کامل Obsidian Vault با نام Institutional Fundamental Macro Research OS در همین گفتگو آپلود شده است. آن را باز کن و از روش‌های Point-in-Time، Bitemporal Data، Historical Reconstruction، Event Clock، Multihorizon Inheritance، Driver Books، Country Books، Historical Case Laboratory و Permission Validation داخل Vault استفاده کن.

بازار مورد تحلیل: [MARKET]
Cutoff تاریخی دقیق: [YYYY-MM-DD HH:MM TIMEZONE]
ابزار معاملاتی: [TRADE_VEHICLE]
تمرکز: [ALL / INTRADAY / 2-10D / BOTH]
زبان خروجی: فارسی
EX_POST_AUDIT: [NO یا YES]
کانتکس تکنیکال اختیاری که در همان لحظه قابل مشاهده بوده: [TECHNICAL_CONTEXT]
سؤال ویژه: [SPECIAL_QUESTION]

این یک بازسازی تاریخی strict point-in-time است. خودت را دقیقاً در لحظه‌ی cutoff قرار بده. هدف این نیست که با دانسته‌های امروز توضیح بدهی چرا بازار بعداً حرکت کرد؛ هدف این است که مشخص کنی یک تحلیل‌گر مؤسسه‌ای در همان لحظه چه چیزهایی می‌توانست بداند، چه چیزی قیمت‌گذاری شده بود، چه سناریوهایی منطقی بودند و چه permissionی قابل دفاع بود.

قواعد قطعی ضد-lookahead:
- فقط اطلاعات منتشرشده تا cutoff مجاز است.
- later revision، benchmark revision، revised seasonal factors، تصمیم بعدی بانک مرکزی، earnings بعدی، outcome بعدی، close بعدی، تغییر ترکیب بعدی شاخص و مشخصات بعدی قرارداد ممنوع است.
- برای هر داده، reference period، first-release timestamp، vintage و availability را در نظر بگیر.
- consensus و market-implied pricing باید متعلق به همان زمان باشد؛ consensus امروزی یا بازسازی‌شده بدون مدرک را واقعیت فرض نکن.
- اگر داده‌ی دقیق تاریخی پیدا نشد، UNKNOWN اعلام کن، proxy را جداگانه برچسب بزن و confidence را کاهش بده.
- outcome آینده نباید انتخاب روایت یا وزن‌دهی متغیرها را هدایت کند.
- اگر EX_POST_AUDIT=YES است، ابتدا بخش RECONSTRUCTED POINT-IN-TIME VIEW را کامل و نهایی کن. سپس در بخش جداگانه‌ی EX-POST AUDIT نتیجه‌ی بعدی، خطاها، missed signals و counterfactual را بررسی کن. این دو بخش را مخلوط نکن.

وب را برای بازیابی آرشیو رسمی، releaseهای همان زمان، statement/minutes، filingها، historical curve/pricing، contemporaneous reporting و مشخصات قرارداد جست‌وجو کن. منبع رسمی و contemporaneous را اولویت بده و timestampها را با timezone روشن ثبت کن. فکت‌های بازیابی‌شده را inline citation کن.

تحلیل را در این افق‌ها انجام بده:
Structural 3–10y+؛ Secular 1–5y؛ Cyclical 3–24m؛ Tactical 2–12w؛ Swing 2–10d؛ Daily/Session؛ Event؛ Microstructure.

برای هر افق مشخص کن:
- information set موجود در cutoff
- state distribution
- priced baseline و consensus distribution
- causal drivers و rival models
- expected half-life
- transition triggers
- conflicts across horizons
- what was unknowable at that time

بازار هدف را با driver tree اختصاصی تحلیل کن و transmission chain را از data/policy/physical shock تا rates, FX, credit, earnings, volatility, flows و خود بازار دنبال کن. همبستگی را با علت اشتباه نگیر.

خروجی الزامی:
1) Historical Analysis Identity and Exact Cutoff
2) Information-Availability Ledger
3) Executive Point-in-Time Verdict
4) Vault Research Route Used
5) Multihorizon State at the Cutoff
6) Data Vintages and Economic/Policy State
7) Contemporaneous Expectations and Pricing
8) Asset Driver Tree
9) Causal and Rival Models
10) Cross-Asset State and Leader Sequence
11) Positioning, Flows, Funding and Liquidity Then Known
12) Historical Catalyst/Event Clock
13) Base/Bull/Bear/Tail scenario distribution as of cutoff
14) Fundamental permission: LONG_ONLY / SHORT_ONLY / TWO_WAY_REDUCED / NO_TRADE
15) Day-trading handoff available at that moment
16) Swing thesis available at that moment
17) Invalidation and expiry known at that moment
18) Unknown/unrecoverable evidence and confidence penalty
19) Claim–Evidence Ledger with FACT / ESTIMATE / INFERENCE / SCENARIO / UNKNOWN
20) Machine-readable YAML context object

اگر EX_POST_AUDIT=YES، بعد از موارد بالا اضافه کن:
21) Outcome after the cutoff — EX-POST only
22) Decision-quality versus outcome-quality
23) Which evidence truly changed and when
24) Attribution, missed signal, false signal and alternative action
25) Counterfactual permission and lessons without hindsight contamination

از نتیجه‌ی نهایی برای تحقیر تصمیم درست یا توجیه تصمیم غلط استفاده نکن. کیفیت تصمیم را بر اساس information set همان زمان بسنج.
~~~
