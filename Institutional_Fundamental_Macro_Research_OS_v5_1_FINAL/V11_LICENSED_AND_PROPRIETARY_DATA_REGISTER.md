---
title: "V11 Licensed and Proprietary Data Register"
type: data-register
status: canonical
version: 11.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v11, fundamental-force, consumption, calibration]
---
# V11 Licensed and Proprietary Data Register

# V11 Licensed and Proprietary Data Register

| Data object | Preferred tier | Public alternative | Mandatory label when absent | Maximum default confidence |
|---|---|---|---|---:|
| Dealer inventory/gamma book | proprietary/licensed | public options open interest and model proxy | `PUBLIC_PROXY` | 65 |
| Prime-broker positioning | proprietary | CFTC, ETF, public positioning proxies | `PUBLIC_PROXY` | 60 |
| CTA/vol-control notionals | licensed/proprietary | public model proxy | `MODEL_IMPLIED` | 65 |
| Real-money flow | proprietary/licensed | ETF/fund flow proxies | `PUBLIC_PROXY` | 60 |
| Exact intraday consensus vintage | licensed | archived public reports where timestamped | `UNAVAILABLE` if not frozen | 55 |
| Historical option surface snapshots | licensed | exchange/public delayed data | `PUBLIC_PROXY` | 65 |
| Central-bank/physical gold flows | official plus specialist data | official lagged releases and public premiums | label by source | frequency-dependent |

A data subscription never grants causal certainty. Incremental value requires ablation and out-of-sample validation.
