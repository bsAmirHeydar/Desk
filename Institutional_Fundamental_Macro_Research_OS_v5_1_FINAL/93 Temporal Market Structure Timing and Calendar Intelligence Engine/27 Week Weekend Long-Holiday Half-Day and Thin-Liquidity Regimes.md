---
title: "Week Weekend Long-Holiday Half-Day and Thin-Liquidity Regimes"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Week, Weekend, Long-Holiday, Half-Day and Thin-Liquidity Regimes

## Weekly structure
Track weekend information accumulation, Monday re-opening, scheduled weekly expiries, recurring release calendars and Friday/weekend risk. Day-of-week price effects remain `CANDIDATE` unless empirically validated point-in-time.

## Weekend
A position opened late Friday faces a different catalyst horizon from one opened Tuesday. For a day-trading executor, the main effect is shrinking time-to-close and reduced tolerance for new risk near market shutdowns.

## Holidays
Use venue-specific holiday calendars (`SRC-NASDAQ-CALENDAR`, `SRC-NYSE-HOURS`) plus London/TARGET/Japan calendars for FX/gold. A US holiday does not imply the global FX market is closed, but it can reduce US participation and alter rates/index transmission.

## Half days
Early closes alter auction timing, options expiration, futures/cash overlap and liquidity. Classify them as their own regime.

## Thin liquidity
Time-of-day or holiday thinness can increase vulnerability to order imbalances; BIS's sterling flash-event review found time of day was an important vulnerability amplifier (`SRC-BIS-FLASH`). Timing may veto execution for liquidity risk without changing direction.
