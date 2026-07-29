---
title: "Prompt Input Specification"
type: specification
status: evergreen
version: 5.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - prompts
  - input-contract
  - specification
---
# Prompt Input Specification

## Required fields

| Field | Requirement | Meaning |
|---|---|---|
| `MARKET` | required | The economic exposure, symbol, instrument, spread, curve, company, country, sector or portfolio to analyze. |
| `MODE` | universal prompt only | `CURRENT` or `HISTORICAL`. |
| `AS_OF` | required | `NOW` for live analysis or an exact timestamp plus timezone for historical work. |
| `OUTPUT_LANGUAGE` | recommended | Language of the final report; prompt instructions remain English. |

## Instrument fields

| Field | Default | Notes |
|---|---|---|
| `TRADE_VEHICLE` | infer conservatively | Cash, futures, CFD, ETF, option, swap, spread or other expression. Exact contract month matters for futures. |
| `SESSION` | infer from market | Asia, London, New York or Global. |
| `PRIMARY_HORIZON` | `ALL` | `INTRADAY`, `2-10D`, `WEEKS`, `MONTHS`, `STRUCTURAL`, or `ALL`. |
| `HOLDING_HORIZON` | prompt-specific | Actual intended holding window. |

## Context fields

| Field | Use |
|---|---|
| `TECHNICAL_CONTEXT` | User-supplied chart state, trigger, stop or market structure. The model must not invent missing technical data. |
| `PORTFOLIO_CONTEXT` | Existing positions, weights, risk limits, hedges, funding or correlation constraints. |
| `SPECIAL_QUESTION` | The exact ambiguity to resolve: driver, regime, event, expression or risk. |
| `DECISION_QUESTION` | Historical decision to reconstruct. |
| `EX_POST_AUDIT` | `NO` by default. `YES` permits a separate hindsight-labeled audit after the blind reconstruction is locked. |

## Historical timestamp standard

Preferred form:

```text
YYYY-MM-DD HH:MM:SS IANA_TIMEZONE
```

Examples:

```text
2024-04-10 08:29:00 America/New_York
2022-09-22 16:00:00 Asia/Tokyo
2020-04-20 13:30:00 UTC
```

A date without time is insufficient for intraday or event reconstruction. If the user supplies only a date, the model may use the relevant official close only after clearly stating the assumption.

## Market identity examples

```yaml
MARKET: NQ / Nasdaq-100 futures
TRADE_VEHICLE: CME E-mini Nasdaq-100 front contract
```

```yaml
MARKET: XAUUSD / Gold
TRADE_VEHICLE: spot proxy, with COMEX futures used for positioning and curve evidence
```

```yaml
MARKET: US 2s10s curve
TRADE_VEHICLE: DV01-neutral Treasury futures spread
```

```yaml
MARKET: NVDA common equity
TRADE_VEHICLE: common shares versus defined-risk options comparison
```

## Missing inputs

The model should make a conservative explicit assumption for minor omissions and continue. It should ask a clarifying question only when:

- the symbol maps to materially different markets;
- the historical cutoff cannot be resolved;
- the requested decision depends on a missing trade vehicle with materially different payoff;
- the portfolio cannot be audited because positions or direction are absent.

Missing proprietary data must become `UNKNOWN`, not a user question unless it prevents any meaningful result.
