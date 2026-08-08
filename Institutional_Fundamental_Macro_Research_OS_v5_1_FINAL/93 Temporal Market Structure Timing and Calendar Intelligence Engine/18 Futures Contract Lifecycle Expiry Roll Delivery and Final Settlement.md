---
title: "Futures Contract Lifecycle Expiry Roll Delivery and Final Settlement"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# Futures Contract Lifecycle, Expiry, Roll, Delivery and Final Settlement

Every futures contract has a lifecycle that can change liquidity and basis before the nominal expiry date.

## Lifecycle states
`NEWLY_LISTED`, `BACK_MONTH`, `ACTIVE_FRONT`, `ROLL_BUILDUP`, `LIQUIDITY_MIGRATION`, `EXPIRY_APPROACH`, `LAST_TRADE`, `FINAL_SETTLEMENT`, and for deliverables `NOTICE/DELIVERY` states.

## Calendar versus realized roll
Calendar conventions define when expiry occurs; **actual liquidity migration** must be observed in volume/open interest or official market data. V15 never assumes the front month switches solely because a calendar date arrived.

## Risks
- split liquidity between contracts;
- basis/roll distortion mistaken for directional market move;
- final-settlement-specific price formation;
- delivery/notice mechanics for commodities;
- proxy mismatch when a CFD/spot broker references a different futures month.

## Required output
`reference_contract`, `next_contract`, `roll_state`, `roll_confidence`, `last_trade`, `final_settlement`, `delivery_risk`, `proxy_mapping`, `next_roll_review`.
