---
title: "Universal Dual-Mode Institutional Market Analysis Prompt"
type: prompt
status: evergreen
version: 5.1.0
created: 2026-07-29
updated: 2026-07-29
language: fa
tags:
  - prompt
  - current
  - historical
  - institutional-analysis
---
# Universal Dual-Mode Institutional Market Analysis Prompt

این پرامپت برای هر دو حالت **CURRENT** و **HISTORICAL** طراحی شده است. پس از آپلود ZIP کامل Vault، مقادیر داخل بخش ورودی را تغییر بده و کل متن را ارسال کن.

## Copy-ready prompt

~~~text
من ZIP کامل Obsidian Vault با نام Institutional Fundamental Macro Research OS را در همین گفتگو آپلود کرده‌ام. قبل از پاسخ، خود ZIP را باز کن، ریشه‌ی Vault را پیدا کن، `00 HOME.md` و `01 COVERAGE MATRIX.md` را بخوان، سپس MOCها، Core Standards، مدل‌ها، Driver Bookها، Country Bookها، Playbookها و Templateهای مرتبط با بازار درخواستی را جست‌وجو و استفاده کن. از حافظه یا یک تحلیل عمومی به‌جای Vault استفاده نکن. Vault روش‌شناسی و معماری تصمیم است؛ داده‌ی جاری یا تاریخی را باید جداگانه و با منبع معتبر به دست بیاوری.

## INPUT
MARKET: [نام بازار، نماد، دارایی، اسپرد، منحنی، کشور، صنعت یا سهم]
MODE: [CURRENT یا HISTORICAL]
AS_OF: [در حالت CURRENT بنویس NOW؛ در حالت HISTORICAL تاریخ، ساعت و منطقه زمانی دقیق]
TRADE_VEHICLE: [اختیاری: futures/CFD/cash/ETF/options/spread]
PRIMARY_HORIZON: [ALL / INTRADAY / 2-10D / WEEKS / MONTHS]
SESSION: [اختیاری: Asia / London / New York / Global]
ANALYSIS_DEPTH: [FULL]
OUTPUT_LANGUAGE: [Persian]
TECHNICAL_CONTEXT: [اختیاری]
PORTFOLIO_CONTEXT: [اختیاری]
SPECIAL_QUESTION: [اختیاری]
EX_POST_AUDIT: [در حالت تاریخی پیش‌فرض NO؛ در صورت نیاز YES]

## MODE CONTROL

اگر MODE=CURRENT است:
- حتماً وب را جست‌وجو کن و زمان دقیق تحلیل، منطقه زمانی و باز/بسته‌بودن بازار را مشخص کن.
- از آخرین داده‌های رسمی، آخرین تنظیمات سیاستی، آخرین قیمت‌گذاری نرخ‌ها، آخرین رویدادها، آخرین گزارش‌های شرکت/صنعت و داده‌های بازار در دسترس استفاده کن.
- هر واقعیت جاری را با منبع inline پشتیبانی کن.
- observation time، reference period، release time، retrieval time و revision vintage را از هم جدا کن.
- اطلاعات Vault را به‌عنوان حقیقت جاری فرض نکن؛ Vault چارچوب است، نه فید زنده.

اگر MODE=HISTORICAL است:
- خودت را دقیقاً در لحظه‌ی AS_OF قرار بده و فقط information set قابل‌دسترسی تا همان ثانیه را بازسازی کن.
- هیچ داده، اصلاحیه، تصمیم سیاستی، گزارش، قیمت نهایی، نتیجه‌ی معامله یا دانسته‌ی بعد از cutoff را وارد تحلیل point-in-time نکن.
- تا جای ممکن first release/vintage، consensus همان زمان، قیمت‌گذاری همان لحظه، ترکیب شاخص همان زمان و مشخصات قرارداد همان زمان را بازیابی کن.
- هر داده‌ی غیرقابل‌بازیابی را UNKNOWN اعلام کن و confidence را کاهش بده؛ حدس را جای واقعیت نگذار.
- اگر EX_POST_AUDIT=YES است، ابتدا تحلیل point-in-time را کامل و قفل کن؛ سپس نتیجه‌ی واقعی بعدی را در یک بخش کاملاً جدا با برچسب EX-POST بررسی کن. نتیجه‌ی آینده نباید روایت بازسازی‌شده را تغییر دهد.

## REQUIRED RESEARCH METHOD

تحلیل را با زنجیره‌ی زیر انجام بده:
Point-in-time evidence → state distribution → expectations/pricing distribution → pricing gap → causal and rival models → transmission → cross-asset confirmation → positioning/flows/liquidity → scenario/payoff distribution → portfolio-aware permission → technical handoff → invalidation/expiry.

فقط فکت‌های عملی را نگه دار. هر داده، روایت یا متغیر باید روشن کند چگونه probability، path، timing، payoff، risk یا trade permission را تغییر می‌دهد. مطالب تزئینی و غیرقابل‌بهره‌برداری را حذف کن.

## MULTIHORIZON ANALYSIS

بازار را مستقل و سپس یکپارچه در این مقیاس‌ها تحلیل کن:
1. Structural: سه تا ده سال و بیشتر
2. Secular/Strategic: یک تا پنج سال
3. Cyclical: سه تا بیست‌وچهار ماه
4. Tactical: دو تا دوازده هفته
5. Swing: دو تا ده روز معاملاتی
6. Daily/Session: روز و سشن جاری یا تاریخی
7. Event: دقیقه تا چند سشن
8. Microstructure: ثانیه تا ساعت

برای هر لایه بنویس:
- state و direction
- causal drivers
- expectations و آنچه از قبل قیمت‌گذاری شده
- confidence و quality of evidence
- expected half-life
- triggerهای transition
- invalidation
- اثر بر بازار هدف
- تعارض با سایر horizonها
- قانون inheritance/conflict resolution

یک روایت تایم‌فریم بالا نباید بدون قاعده، سیگنال تایم‌فریم پایین را خنثی کند و برعکس.

## COMPLETE FUNDAMENTAL COVERAGE

در حد ارتباط با بازار هدف بررسی کن:
- growth, inflation, labor, productivity
- monetary policy, reaction function, OIS/futures pricing, real yields, term premium and curve
- fiscal impulse, issuance, auctions, debt sustainability and sovereign plumbing
- liquidity, reserves, repo, collateral, dealer balance sheet and financial conditions
- banks, credit, defaults, private credit, NBFI and hidden leverage
- external balance, capital flows, global dollar funding, FX basis and hedging demand
- corporate earnings, revisions, margins, valuation, cash flow, balance sheet and index mechanics
- commodity physical balances, inventories, curves, freight, refining and producer behavior
- geopolitics, sanctions, tariffs, elections, policy probabilities and supply-chain transmission
- volatility surface, skew, gamma/vanna/charm, positioning, crowding and systematic flows
- market microstructure, cash-futures basis, settlement, expiry, rebalancing, liquidity and execution
- alternative data and OSINT only when source quality and timestamp are defensible
- competing economic schools and rival causal explanations

## MARKET PRICING AND DRIVER TREE

برای بازار هدف یک Driver Tree اختصاصی بساز و هر driver را در یکی از این دسته‌ها قرار بده:
- direct causal driver
- conditional/regime-dependent driver
- transmission variable
- confirmation variable
- flow/microstructure driver
- misleading correlation
- rival explanation

اقتصاد خوب/بد را مستقیماً bullish/bearish فرض نکن. ابتدا بگو چه چیزی قیمت‌گذاری شده، چه assumptionی آسیب‌پذیر است، شوک چگونه distribution را تغییر می‌دهد و کدام بازار باید اول واکنش نشان دهد.

## SCENARIOS

حداقل Base، Bullish، Bearish و Tail scenario بساز. برای هرکدام:
- probability range، نه دقت کاذب
- required evidence
- trigger
- causal sequence
- leader and confirmations
- expected magnitude/path where defensible
- expected half-life
- invalidation
- best and worst trade expression

احتمال‌ها باید با شواهد، market-implied distribution، base rates و uncertainty توضیح داده شوند و مجموع آن‌ها تقریباً 100% باشد.

## CROSS-ASSET AND FLOW TEST

در صورت ارتباط، این بازارها را به‌عنوان causal leader یا confirmation بررسی کن:
- front-end and long-end rates, real yields, breakevens and curve
- USD and major FX crosses
- equity index, breadth, sectors and earnings revisions
- IG/HY credit and bank risk
- commodities and physical curves
- implied/realized volatility and skew
- repo/funding/collateral
- positioning, COT, dealer/systematic flows, issuance, buybacks, expiry and rebalancing

Divergenceها را توضیح بده و فقط با همبستگی سطحی نتیجه نگیر.

## REQUIRED OUTPUT

پاسخ را دقیقاً با این معماری بده:
1. Analysis Identity and Data Cutoff
2. Executive Verdict
3. Vault Research Route Used
4. Multihorizon Fundamental Dashboard
5. Economic and Policy State
6. Expectations, Pricing and Vulnerable Assumptions
7. Asset-Specific Driver Tree
8. Causal Transmission Map
9. Cross-Asset Confirmation and Divergence
10. Positioning, Flows, Liquidity and Market Plumbing
11. Catalyst and Event Clock
12. Scenario Distribution
13. Fundamental Permission
14. Day-Trading Handoff
15. Swing-Trading Handoff
16. Fundamental, Market and Time Invalidation
17. Unknowns, Missing Data and Confidence Limits
18. Claim–Evidence Ledger with FACT / ESTIMATE / INFERENCE / SCENARIO / UNKNOWN
19. Machine-Readable YAML Context Object
20. Bottom-Line Decision Memo

## PERMISSION CONTRACT

فقط یکی از این خروجی‌ها را انتخاب کن:
- LONG_ONLY
- SHORT_ONLY
- TWO_WAY_REDUCED
- NO_TRADE

Permission جهت ورود نیست؛ فقط مجموعه‌ی معاملات مجاز را محدود می‌کند. ورود، استاپ ساختاری و تارگت همچنان باید از ساختار تکنیکال بیایند. تحلیل فاندامنتال هرگز اجازه‌ی جابه‌جایی استاپ، averaging into loss یا توجیه معامله‌ی خراب را نمی‌دهد.

برای permission مشخص کن:
- confidence ceiling
- causal leader
- minimum confirmations
- vetoes
- fundamental invalidation
- market-implied invalidation
- time expiry
- next catalyst
- conditions for intraday-to-swing conversion

## EVIDENCE DISCIPLINE

هر ادعا را با یکی از این برچسب‌ها مشخص کن:
FACT / ESTIMATE / INFERENCE / SCENARIO / UNKNOWN / EX-POST

منابع رسمی و اولیه اولویت دارند. اگر وب را جست‌وجو کردی، تمام فکت‌های اینترنتی مهم و جاری را inline citation بده. چیزی را جعل نکن، از نبود دیتا نتیجه‌ی قطعی نگیر و اختلاف منابع را پنهان نکن.

هیچ سؤال توضیحی نپرس اگر MARKET و MODE مشخص هستند. برای فیلدهای خالی default منطقی انتخاب کن، آن را در ابتدای پاسخ اعلام کن و تحلیل را کامل انجام بده.
~~~

## Related controls

- [[75 ChatGPT Institutional Market Analysis Prompts/08 Prompt Input Specification]]
- [[75 ChatGPT Institutional Market Analysis Prompts/09 Output Contract and Quality Gates]]
- [[75 ChatGPT Institutional Market Analysis Prompts/10 Vault Reading and Evidence Protocol]]
