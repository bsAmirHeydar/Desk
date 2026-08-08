---
title: "16 Equity Index Futures Quarterly Expiry SOQ and Roll"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
---
# Equity Index Futures Quarterly Expiry, SOQ and Roll

For ES/NQ/YM families distinguish: liquidity roll, last trade/expiry and Special Opening Quotation/final settlement. They are different temporal objects.

During roll, basis/spread activity can be large without changing outright index fundamentals. Settlement morning creates a special opening-price mechanism. If quarterly options/index rebalance overlap, create a `QUARTERLY_EXPIRY_COLLISION` state.
