# UX3 World-Class Research Experience Contract

## Status
CANONICAL HUMAN PRESENTATION CONTRACT

## Mission
Reduce cognitive work without reducing analytical depth. The product must feel like a private institutional research publication/operating surface, not a generic dashboard.

## Core experience
Command Center → Market Workspace → Analytical Lens → Single Deep-Dive Drawer.

## First viewport
At 1440×900 without scrolling, show: Alpha Desk identity; New York as-of time (Tehran secondary); compact cross-market briefing; all six markets for six-market runs; main common driver; strongest common opposition; next material review/event.

The six-market strip shows symbol, Direction, action/permission, Force, Remaining Pressure, Reversal Risk and meaningful prior-run delta. Mobile uses compact rows or swipeable tiles; never a shrunk 1000px desktop table.

## Market workspace
Only one market is fully expanded at a time. Direction and action have highest hierarchy. Force, Consumption, Remaining Pressure, Persistence and Reversal Risk form a restrained information strip rather than equal dashboard cards.

Immediately show:
- الان مهم‌ترین چیز چیست؟
- نیروی اصلی
- نیروی دوم
- قوی‌ترین نیروی مخالف
- می‌دانیم / برداشت فعلی / هنوز نمی‌دانیم
- از یک ساعت قبل چه تغییر کرده؟ (verified comparable run only)

## Analytical Lens Index
Render all eight dimensions as compact editorial rows. Each shows title, effect state, one concise result sentence and a disclosure action. All eight should scan in under 20 seconds.

## Deep Dive
One reusable accessible drawer. Never preload 48 deep-dive bodies. Every lens must have its own mechanism and specific evidence context. Required user-facing fields: result; observations; why it matters; supporting evidence; opposing evidence; unknowns; mechanism; causal-strength wording; rival explanation; invalidation/change trigger; likely failure mode; additional evidence context.

## Scenario Navigator
Tabs/chips: مسیر اصلی، صعودی، نزولی، برگشت، رنج، رویداد، عدم معامله، شوک نادر. One active scenario canvas. Each applicable scenario names actual variables, current supporting evidence, missing evidence, trigger, invalidation, qualitative path and horizon. No fake probabilities. Mark immaterial scenarios quietly rather than manufacturing content.

## Global multi-market views
When six markets are present, support:
- تصویر مشترک شش بازار
- نقشه انتقال نیروها
- تناقض‌های مهم
- فرضیه اصلی و توضیح‌های رقیب
- ماتریس سناریو/حساسیت
- ریسک‌های مشترک
- چه چیزی می‌تواند همه‌چیز را عوض کند؟
- optional compare of 2–3 markets (Direction, Force, Remaining Pressure, drivers, opposition, reversal, key contradiction only)

## Thinking Guide
High-level method only, never private reasoning trace: separate observed facts; evaluate plausible causes; argue against the current thesis; keep multiple scenarios open; decide only with sufficient evidence; every conclusion expires. Preserve evidence-before-story, fact≠interpretation≠hypothesis≠decision, price≠proof of cause, root-source independence, UNKNOWN valid, proxy≠reality, correlation≠causation, rival explanations, simplest sufficient explanation, Direction≠opportunity and process quality≠random outcome.

## Philosophy / Fragility
Editorial chapter under four themes: واقعیت قبل از داستان؛ شک و فرضیه رقیب؛ شکنندگی و چیزهایی که نمی‌دانیم؛ تصمیم بدون اجبار به پیش‌بینی. Cover source/story/model removal, hidden unknowns, nonlinear/rare severe risk, common-mode dependence, optionality, forced actors, incentives, fragility transfer, intervention risk and invariant conclusions when material. This perspective NEVER determines Direction.

## Evidence UX
Group human-readable evidence by اقتصاد و سیاست پولی؛ قیمت و بازار؛ جریان و موقعیت معامله‌گران؛ رویداد و ژئوپولیتیک. Show what it says, why it matters, type (داده مستقیم / گزارش معتبر / نشانه غیرمستقیم / نامشخص), freshness/time where useful and limitation. No internal IDs/hashes.

## Quality / limitations
Show only: what we know well; where data are incomplete; how much the gap affects the result; whether the result is usable / usable-with-limitations / partial / not reliable enough. Process quality is not market confidence.

## Persian language
L1 ≈95% plain Persian; L2 ≈90% plain Persian. Prefer: سود شرکت‌ها، ضعف داده‌های اشتغال، بازدهی اوراق، گستردگی مشارکت بازار، هیجان جا نماندن از رشد، رشد بیش‌ازحد کوتاه‌مدت، جریان خرید و فروش، نحوه قرار گرفتن معامله‌گران، مداخله ارزی، مزیت اختلاف نرخ بهره، ریسک کم‌تکرار اما شدید. Technical term may appear quietly in parentheses in deep dive only.

## Visual / UX discipline
Warm ivory/off-white, deep charcoal/black, restrained muted gold. Typography, whitespace, alignment and hairlines before cards. Reduce visible cards/borders/radius. Gold is identity/hierarchy, not bullishness. No red/green-only state meaning. Motion 100–180ms; respect reduced motion.

Desktop sidebar 220–240px. Mobile gets a real sticky bar + market selector + menu drawer. Search is non-destructive command-palette navigation. Keyboard: `/` search, `Esc` close drawer/menu, arrows may navigate scenario tabs. Use semantic headings, skip-link, focus-visible, ARIA, logical tab order, bdi for mixed RTL/LTR.

## Performance
Standalone HTML, no external JS framework, no display-time network requirement, structured data separated from view, no 48 dialogs, one market workspace, one drawer, one active scenario canvas.

## Acceptance
The interface passes only if: first viewport answers the six-market state within 10 seconds; one selected market is understood within 60 seconds; any lens can be audited deeply; hourly deltas are prominent; mobile is designed rather than adapted; no analytical depth is lost; visible HTML exposes no internal Vault/runtime engineering.
