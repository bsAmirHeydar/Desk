---
title: "Alpha Lab Hourly Persian PDF Report Contract"
type: hourly-pdf-standard
status: canonical
version: 10.3.0
created: 2026-08-01
updated: 2026-08-01
language: en
tags: [alpha-lab, hourly-report, pdf, persian, rtl, practical]
---
# Alpha Lab Hourly Persian PDF Report Contract

## Purpose

The hourly report must convert institutional fundamental analysis into a practical Persian monitoring document. It must show the current direction, intensity, confidence, catalyst consumption, remaining pressure, persistence and state-change risks in a form that can be understood quickly without sacrificing evidence quality.

## Recommended length

- `HOURLY_PREMARKET_MAP`: 10–16 A4 pages;
- `HOURLY_LIVE_MONITOR`: 10–18 pages;
- `HOURLY_POST_EVENT`: 10–18 pages;
- `HOURLY_END_OF_DAY_ATTRIBUTION`: 12–20 pages;
- `HISTORICAL_HOURLY_REPLAY`: 14–24 pages.

Use appendices when evidence requires more space. Do not compress the hourly table until it becomes unreadable.

## Page two — practical state dashboard

Display seven compact cards:

1. `جهت بنیادی فعلی`
2. `شدت فشار بنیادی`
3. `میزان مصرف محرک`
4. `فشار بنیادی باقی‌مانده`
5. `اعتماد به تحلیل`
6. `ماندگاری احتمالی`
7. `زمان یا رویداد تغییر بعدی`

Then add a box titled `نتیجه بسیار ساده اکنون` in no more than 120 Persian words.

## Mandatory hourly pages

1. `وضعیت فعلی در یک نگاه`
2. `تغییر نسبت به ساعت قبل`
3. `جدول ساعت‌به‌ساعت وضعیت بنیادی`
4. `محرک اصلی، محرک تقویت‌کننده و نیروی مخالف`
5. `میزان مصرف و ظرفیت باقی‌مانده`
6. `کیفیت حرکت فعلی`
7. `تأیید و تناقض در بازارهای مرتبط`
8. `تقویم رویدادها و پنجره‌های تغییر حالت`
9. `سناریوی ساعات باقی‌مانده‌ی سشن`
10. `ریسک چرخش، ابطال و زمان بررسی بعدی`
11. `پل به افق باقی روز و ۲ تا ۱۰ روز`

## Mandatory hourly table

Use RTL column order suitable for Persian. Include:

- time;
- fundamental direction;
- direction score;
- intensity;
- confidence;
- information absorption;
- repricing completion;
- flow exhaustion;
- remaining pressure;
- state phase;
- primary driver;
- independent confirmation;
- expected persistence;
- reversal risk;
- change from prior snapshot.

Use color sparingly:

- muted green for positive states;
- muted red for negative states;
- amber for unresolved/event-dependent states;
- gray for no material update or insufficient evidence;
- navy and matte gold for structure and branding.

## Consumption panel

Show the full vector, not just one number:

- absorption;
- repricing completion;
- flow exhaustion;
- narrative saturation;
- freshness;
- remaining pressure.

Below it, show one plain-Persian summary such as:

- `محرک هنوز تازه است و بخش زیادی از فشار باقی مانده است.`
- `حرکت قوی بوده، اما بخش عمده‌ی بازقیمت‌گذاری انجام شده است.`
- `جهت هنوز مثبت است ولی فشار باقی‌مانده ضعیف شده است.`
- `اطلاعات جدید ظرفیت حرکت را دوباره افزایش داده است.`

## Future-hour rule

Completed hours belong in the observed timeline. Future hours must appear only under:

`سناریوی مشروط ساعات آینده`

Never present future conditional scores as observed facts.

## No-update rule

If an hour contains no material new information, display:

`بدون تغییر بنیادی معنادار`

Keep the prior direction, update freshness and next-catalyst proximity only when justified.

## Event micro-window panel

For major events, display:

- T-60 minutes;
- T-15 minutes;
- T+5 minutes;
- T+15 minutes;
- T+60 minutes.

At each point show priced baseline, surprise decomposition, direction, intensity, absorption and remaining pressure.

## PDF visual standard

Use [[87 Alpha Lab Asset-Specific Persian PDF Analysis Prompts/01 Alpha Lab Persian PDF Design System]]. Preserve one Persian font family, full RTL flow, A4 portrait, clear tables and simple Persian executive language. The report should resemble a hedge-fund intraday fundamental monitor, not a technical dashboard.

## File naming

```text
Alpha_Lab_[MARKET]_[HOURLY_MODE]_[SESSION]_Hourly_Fundamental_State_[YYYY-MM-DD]_[HHMM].pdf
```
