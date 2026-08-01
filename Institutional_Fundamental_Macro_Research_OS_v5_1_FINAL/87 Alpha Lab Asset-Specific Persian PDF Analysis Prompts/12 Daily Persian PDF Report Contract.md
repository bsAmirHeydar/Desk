---
title: "Alpha Lab Daily Persian PDF Report Contract"
type: daily-pdf-standard
status: canonical
version: 10.3.0
created: 2026-07-31
updated: 2026-08-01
language: en
tags: [alpha-lab, daily-report, pdf, persian, rtl]
---
# Alpha Lab Daily Persian PDF Report Contract

## Purpose

The daily PDF must be materially shorter and more decision-oriented than the full-spectrum report. It must explain today's fundamental context in simple Persian while preserving institutional evidence in appendices.

## Page and density target

- Recommended length: **8–14 A4 pages** for `DAILY_PREMARKET`, `LIVE_SESSION_UPDATE` or `POST_EVENT_UPDATE`.
- Recommended length: **8–16 pages** for `END_OF_DAY`.
- Structural and cyclical background: normally no more than one page.
- Evidence and methodology may extend the appendix when necessary.
- Do not fill pages merely to appear comprehensive.

## Mandatory daily PDF structure

### Cover

- `Alpha Lab`
- market name in Persian
- `گزارش روزانه فاندامنتال`
- analysis profile
- target date and session
- exact as-of timestamp and timezone
- `Institutional Daily Fundamental Research`

### Page two — امروز در یک نگاه

Five compact cards:

- `وضعیت بنیادی امروز`
- `محرک غالب امروز`
- `نوع روز`
- `ماندگاری احتمالی حرکت`
- `مهم‌ترین زمان یا رویداد بعدی`

Then provide `نتیجه خیلی ساده امروز` in no more than 120 Persian words.

### Core pages

1. `چه چیزی از کلوز قبلی تغییر کرده است؟`
2. `نقشه اتفاقات شبانه و انتقال بین سشن‌ها`
3. `تقویم و نقاط تصمیم امروز`
4. `بازار قبل از رویدادها چه چیزی را قیمت‌گذاری کرده است؟`
5. `رهبر علّی امروز و بازارهای تأییدکننده`
6. `موتور روزانه اختصاصی بازار`
7. `سناریوهای سشن و وزن آن‌ها`
8. `روز بی‌خبر، جریان پول و محدودیت نقدشوندگی`
9. `چه چیزی تحلیل امروز را باطل می‌کند؟`
10. `زمان آپدیت بعدی و چیزهایی که باید دوباره بررسی شوند`
11. `پل امروز به افق ۲ تا ۱۰ روزه`

### End-of-day additions

For `END_OF_DAY`, add:

- `واقعاً چه چیزی بازار را حرکت داد؟`
- `مقایسه با گزارش قبل از بازار`
- `چه چیزی به فردا منتقل می‌شود؟`
- `خطاها، تناقض‌ها و درس روز`

### Appendices

- timestamped change ledger;
- catalyst calendar with timezones;
- Claim–Evidence Ledger;
- Vault Reading Ledger;
- market and instrument definition;
- unavailable data and confidence caps;
- internal QA state.

## Daily state translation

Translate the codes as follows while retaining the English code in smaller text:

- `DAILY_FUNDAMENTAL_LONG_BIAS` → `تمایل بنیادی امروز به سمت صعود`
- `DAILY_FUNDAMENTAL_SHORT_BIAS` → `تمایل بنیادی امروز به سمت نزول`
- `DAILY_TWO_WAY_EVENT_DEPENDENT` → `روز دوطرفه و وابسته به رویداد`
- `DAILY_NO_FUNDAMENTAL_EDGE` → `امروز مزیت بنیادی روشنی وجود ندارد`
- `DAILY_INSUFFICIENT_EVIDENCE` → `شواهد کافی برای نتیجه‌گیری وجود ندارد`

## Simplicity requirement

The executive pages must answer these questions without jargon:

1. امروز چه چیزی بازار را کنترل می‌کند؟
2. آیا حرکت شبانه از نظر بنیادی تأیید شده است؟
3. مهم‌ترین رویداد امروز چیست؟
4. اثر غالب احتمالاً چند ساعت یا چند روز دوام دارد؟
5. چه چیزی نظر امروز را تغییر می‌دهد؟

Detailed macro history belongs in the appendix unless it directly controls the day.

## Visual standard

Use [[87 Alpha Lab Asset-Specific Persian PDF Analysis Prompts/01 Alpha Lab Persian PDF Design System]]. Preserve the same Alpha Lab brand, RTL layout and single Persian font family. The daily report should feel like a concise morning note from a hedge-fund research desk, not a long academic paper or a crowded dashboard.

## File naming

Use:

```text
Alpha_Lab_[MARKET]_[PROFILE]_[SESSION]_Daily_Fundamental_Report_[YYYY-MM-DD].pdf
```

Examples:

- `Alpha_Lab_NASDAQ_100_DAILY_PREMARKET_NEW_YORK_Daily_Fundamental_Report_2026-07-31.pdf`
- `Alpha_Lab_GOLD_POST_EVENT_UPDATE_NEW_YORK_Daily_Fundamental_Report_2026-07-31.pdf`


## Hourly extension

For hourly profiles, the dedicated hourly PDF contract overrides the daily page-two cards and timeline structure. See [[87 Alpha Lab Asset-Specific Persian PDF Analysis Prompts/16 Hourly Persian PDF Report Contract]].
