---
title: "Alpha Lab Persian PDF Design System"
type: report-design-standard
status: canonical
version: 10.1.0
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [alpha-lab, pdf, rtl, persian, design-system]
---
# Alpha Lab Persian PDF Design System

## Design objective

Create a Persian institutional research report that looks disciplined, expensive and calm rather than decorative. The report should feel like a high-end hedge-fund research memo translated into a visually clear executive document.

## Mandatory format

- Output an actual `.pdf` file. Do not return only Markdown, HTML, a design description or a simulated report.
- A4 portrait pages.
- Full right-to-left layout for Persian text.
- Correct Persian glyph shaping and punctuation.
- One Persian font family throughout the report. Prefer `Vazirmatn` when installed; otherwise use `Noto Sans Arabic`. Do not mix Persian font families.
- Use the same family in regular, medium and bold weights for body, captions, tables and headings.
- Latin tickers, formulas and source identifiers may remain left-to-right inside controlled inline spans.

## Alpha Lab visual identity

### Cover

- Deep obsidian/navy background: `#0B0F14`.
- Muted institutional gold accent: `#C6A15B`.
- Warm ivory text: `#F7F3EA`.
- Title at top: `Alpha Lab`.
- Main Persian title: `گزارش جامع فاندامنتال`.
- Market name, mode, as-of timestamp and data cutoff.
- Small label: `Institutional Fundamental Research`.
- No stock photographs, decorative candlesticks, neon effects or generic finance imagery.

### Interior pages

- White or warm-ivory background.
- Dark navy headings.
- Muted gold only for separators, section markers and key highlights.
- Green, red, amber, gray and blue may be used sparingly for fundamental state labels, with text labels so meaning is not color-dependent.
- Thin rules, generous white space, consistent table grid and restrained iconography.

## Typography and density

- Main body: approximately 10.5–11.5 pt.
- Section headings: 16–20 pt.
- Main report title: 26–34 pt.
- Line height: approximately 1.7–1.9 for Persian text.
- Avoid paragraphs longer than six visual lines.
- Use short subsections, compact tables and clear callout boxes.
- Do not reduce font size to fit excessive text. Move technical detail to appendices.

## Required report architecture

1. Cover
2. `خلاصه مدیریتی در یک نگاه`
3. `نتیجه بسیار ساده و واضح`
4. Multihorizon fundamental-state matrix
5. Primary drivers and causal chain
6. Market pricing and vulnerable assumptions
7. Asset-specific fundamental engine
8. Cross-asset confirmation and contradiction
9. Positioning, liquidity and institutional constraints
10. Scenario table
11. Catalysts, invalidation and expiry
12. Unknowns and unavailable data
13. Evidence appendix
14. Vault Reading Ledger and methodology appendix

## Executive page standard

Page two must be understandable in under two minutes and contain five compact cards:

- `وضعیت کلی`
- `جهت بنیادی به تفکیک افق`
- `محرک اصلی`
- `بزرگ‌ترین ریسک`
- `رویداد یا داده بعدی`

Then provide a Persian plain-language conclusion of no more than 180 words.

## Clarity rule

Every technical section must begin with a box titled `معنای ساده` that explains the conclusion without jargon. Technical terms may follow, but the simple explanation must come first.

## Chart and table rule

- Include only charts that add decision value.
- Every chart must identify source, timestamp, units and cutoff.
- Never fabricate a chart from unavailable data.
- Prefer clean line, spread, contribution or scenario charts over decorative graphics.
- Tables must repeat header rows when they continue to another page.
- Do not allow tables or charts to overflow page margins.

## Footer and header

- Header: `Alpha Lab | [Market] | Fundamental Research`.
- Footer: page number, mode and as-of date.
- Add `Research Use Only` in small text.

## File naming

Use:

```text
Alpha_Lab_[MARKET]_[LIVE_or_HISTORICAL]_Fundamental_Report_[YYYY-MM-DD].pdf
```

## Prohibited design choices

- Mixed Persian fonts.
- Tiny body text.
- Dense wall-of-text pages.
- Low-contrast gray text.
- Decorative market charts with no source.
- English left-to-right page layout with Persian text forced into isolated boxes.
- Excessive gradients, shadows, glass effects or dashboard-style clutter.
