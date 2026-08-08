---
title: "USDJPY Force Consumption and Persistence Book"
type: asset-operating-book
status: canonical-operational
version: 16.1.0
production_retrieval: allowed
---
# USDJPY Force, Consumption and Persistence Book

USDJPY is bilateral and policy-sensitive. Never analyze it as an equity-style generic asset.

## Mandatory routing graph
### US block
Fed reaction function; US inflation/growth/labor; 2Y/5Y and relevant real-rate path; Treasury/funding stress; broad USD funding.

### Japan block
BoJ reaction function and implementation; wages and services inflation; JGB curve and policy operations; domestic growth; fiscal/liquidity conditions.

### Relative block
US-Japan nominal and real-rate differential, carry and expected policy convergence/divergence. Do not assume the differential is causal unless transmission is observed and rival channels are weaker.

### Intervention block
Separate: confirmed official intervention, official verbal intervention, credible public reporting/proxy, rumor, and model inference. Only confirmed/official evidence may be labeled intervention fact.

### Flow/risk block
Repatriation, importer/exporter hedging, Japanese institutional hedging, global risk/funding and year/fiscal/settlement effects where observable. Missing proprietary flow data is a confidence limitation, not automatic NO_TRADE.

## Consumption
Track US-rate fact, BoJ/Japan-policy fact, intervention fact and risk/funding fact separately. One can be consumed while another remains active.

## Rival models
At minimum tournament policy differential, intervention, Japan domestic macro, global USD funding/risk, and hedging/repatriation when material.
