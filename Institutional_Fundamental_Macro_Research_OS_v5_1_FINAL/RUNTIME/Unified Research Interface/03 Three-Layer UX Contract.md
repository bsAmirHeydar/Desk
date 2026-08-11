# UX3 Progressive Research Experience Contract

Alpha Desk communicates one canonical research snapshot through progressive disclosure without reducing analytical depth.

## Experience model

**Command Center → Market Workspace → Analytical Lens → Deep Dive**

### Layer 1 — نتیجه فوری / Command Center
At desktop 1440×900, the first viewport should show identity, as-of time, cross-market state, all six markets when the request is multi-market, common driver/opposition and next material review/event. Direction and action are primary. No giant desktop table.

### Layer 2 — تصویر کامل تحلیل / Market Workspace
Only one market is fully expanded at a time. The eight dimensions are compact editorial rows: زمان و موقعیت؛ بنیادی؛ انتظارات/سیاست؛ روایت/مصرف؛ موقعیت معامله‌گران؛ جریان خریدوفروش؛ نقدینگی/تأمین مالی؛ ساختار/ظرفیت/نوسان.

Preserve the signature component:
- می‌دانیم
- برداشت فعلی
- هنوز نمی‌دانیم

UNKNOWN must be visually and semantically different from neutral and not-material.

### Layer 3 — جزئیات کامل هر بخش / Deep Dive
Use one reusable accessible drawer. Every lens deep dive is section-specific: observations, why it matters, supporting/opposing evidence, unknowns, lens-specific mechanism, causal strength, rival explanation, invalidation, likely failure path and additional evidence context. Never expose raw audit JSON or internal engineering details.

## Scenario Navigator
Do not show eight large scenario cards simultaneously. Use a navigator and one active canvas. Applicable states: مسیر اصلی؛ صعودی؛ نزولی؛ برگشت؛ رنج؛ رویداد؛ عدم معامله؛ شوک نادر. Conditions/triggers must be asset-specific and observable. No artificial probabilities.

## Philosophy and method
Explain high-level research principles only; never hidden chain-of-thought. Philosophy tests fragility and dependency and does not set Direction.

## Hourly priority
`از یک ساعت قبل چه تغییر کرده؟` is a first-class view. Show only material changes from a verified comparable prior run.

## UX invariants
- very simple Persian by default;
- no technical Vault/runtime details in visible HTML;
- no color-only meaning;
- mobile navigation has full capability, not a hidden desktop sidebar with no replacement;
- one structured data payload, one market workspace, one deep drawer, one active scenario canvas;
- typography/whitespace/alignment before cards/borders;
- no scientific claim creation by the renderer.
