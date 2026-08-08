---
title: "Simple Email Output Contract"
type: production-output-contract
status: active
version: 14.1.0
---
# Simple Email Output Contract

Email remains intentionally simple regardless of analytical depth.

## Body only
1. Tehran analysis/update timestamp.
2. At most one short cross-market sentence when materially useful.
3. Exactly six rows with columns: `Symbol | Edge Level | Permission`.

Product-facing Persian Edge labels:
- Edge فعال
- Edge مشروط
- Edge نسبی
- فقط Bias
- بدون Edge
- رویدادی/Fragmented
- شواهد ناکافی

Permission may only be `BUY`, `SELL`, `NO_TRADE`.

## No attachments
Do not attach HTML, JSON, PDF, ZIP, Markdown, CSV or technical reports. Do not mention attachment-transfer errors, debug state or internal implementation details.

Current deployment recipients are stored in `production_profiles/alpha_lab_six_market_profile.yaml`.
