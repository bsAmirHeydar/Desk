---
title: "Alpha Desk UX3 Intelligence Explorer Product Contract"
type: product-output-contract
status: production
version: 15.0.0
---
# Alpha Desk UX3 Intelligence Explorer Product Contract

Every completed Full-Vault run should create/update one standalone Persian RTL Explorer HTML as the primary human-facing artifact.

## Visible experience
Command Center → Market Workspace → Analytical Lens → Single Deep-Dive Drawer.

For six-market runs: first viewport shows all six markets, cross-market state, common driver/opposition and next review/event. Only one market is fully expanded at a time. The eight analytical dimensions are compact lens rows. Deep detail is populated into one reusable drawer. Scenarios use one navigator and one active canvas.

## Required product sections
- خلاصه فوری / six-market Command Center
- از یک ساعت قبل چه تغییر کرده؟ (verified comparable run only)
- selected Market Workspace
- می‌دانیم / برداشت فعلی / هنوز نمی‌دانیم
- eight analytical lenses
- Scenario Navigator
- optional cross-market sensitivity map / compare
- چطور این تحلیل را بخوانیم؟
- فلسفه و شکنندگی
- شواهد کلیدی
- کیفیت و محدودیت‌های تحلیل

## Separation
Direction, opportunity/action, Force, Consumption, Remaining Pressure, Persistence and Reversal Risk are separate objects. Philosophy/fragility does not determine Direction. Process quality is not market confidence.

## Product boundary
Consumer-facing, never debug-facing. Visible HTML MUST NOT expose filenames, hashes, internal module/gate/process/schema IDs, raw audit JSON, repository paths or runtime/certification engineering.

## Language
Default L1/L2 are plain Persian. Technical terms appear only when useful and after a Persian explanation.

## Performance / accessibility
No 48 preloaded dialogs. Structured data once, one reusable drawer, one active market workspace, one scenario canvas; real mobile navigation; keyboard/focus/ARIA/reduced-motion/bidi support.
