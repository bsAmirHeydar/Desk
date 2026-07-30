---
title: "Market-Specific Add-On Blocks"
type: prompt-library
status: evergreen
version: 10.0.0
created: 2026-07-29
updated: 2026-07-30
language: en
tags:
  - prompt
  - market-drivers
  - add-on
---
# Market-Specific Add-On Blocks

Append the relevant block to any master prompt when deeper specialization is required. The model must also search the corresponding Vault driver books and MOCs.

## Equity index: Nasdaq, S&P, Dow, Russell, DAX, Nikkei and similar

~~~text
ADD-ON — EQUITY INDEX
Decompose index returns into expected cash-flow growth, earnings revisions, discount rates, term premium, real yields, equity risk premium and flow/microstructure effects. Analyze earnings and revision breadth, mega-cap concentration, sector leadership, breadth, equity duration, credit, USD, buybacks, issuance, passive/index flows, volatility surface, dealer gamma, expiry, rebalancing and cash-close mechanics. Separate index-level direction from constituent concentration and factor exposure.
~~~

## Single equity

~~~text
ADD-ON — SINGLE EQUITY
Build a company-specific fundamental model: three statements, revenue price-volume-mix, unit economics, margins, operating leverage, working capital, free cash flow, maintenance/growth capex, ROIC, balance sheet, maturity wall, refinancing, accounting quality, dilution, buybacks, guidance, consensus revisions, valuation/reverse DCF, competitive position, management incentives, regulation, supply chain, ownership, positioning and options. Separate company alpha from market, sector, rates, FX and thematic beta.
~~~

## Sovereign rates and curves

~~~text
ADD-ON — SOVEREIGN RATES
Decompose yields into expected short-rate path, term premium and inflation compensation. Analyze OIS/futures probabilities, central-bank reaction function, fiscal/issuance supply, auctions, foreign/real-money/dealer demand, repo/collateral, swap spreads, futures basis/CTD, convexity flows, curve shape and rates volatility. Do not label every yield rise hawkish or every yield fall dovish.
~~~

## FX

~~~text
ADD-ON — FX
Analyze both currencies independently. Compare relative growth, inflation and policy distributions; nominal and real-rate differentials; balance of payments; external balance sheets; terms of trade; hedging demand; cross-currency basis; reserve/intervention flows; options/risk reversals; carry, value, momentum and crowding; global-dollar regime and funding stress. Separate spot direction from carry, hedge cost and intervention risk.
~~~

## Gold and precious metals

~~~text
ADD-ON — GOLD/PRECIOUS METALS
Decompose nominal and real yields into expected policy, term premium and inflation compensation. Analyze USD, monetary/fiscal credibility, central-bank demand, ETF/futures flows, Asian physical demand, lease/forward conditions, mine/recycling supply, positioning, geopolitical hedge demand and opportunity cost. Do not assume mechanically that inflation or war is bullish.
~~~

## Crude oil and refined products

~~~text
ADD-ON — CRUDE OIL
Build the physical barrel balance: production, exports/imports, refinery runs, crude and product stocks, cracks, time spreads, freight, floating storage, spare capacity, OPEC policy/compliance, sanctions/outages, shale response and demand nowcast. Interpret inventory releases by composition, seasonality, adjustments and curve reaction, not headline alone.
~~~

## Natural gas and power

~~~text
ADD-ON — NATURAL GAS/POWER
Analyze production, pipeline flows, storage versus weather-normal, LNG feedgas/export capacity, regional basis, outages, maintenance, power burn, industrial demand, weather distributions, transport constraints and curve/seasonality. Distinguish local bottleneck risk from global LNG balance.
~~~

## Industrial metals

~~~text
ADD-ON — INDUSTRIAL METALS
Analyze mine supply, grades, treatment charges, smelter utilization, visible and hidden inventories, scrap, Chinese credit/property/manufacturing demand, grid/energy-transition demand, freight, curve, warehouse rules, producer hedging and FX. Separate cyclical demand from structural narratives.
~~~

## Agriculture

~~~text
ADD-ON — AGRICULTURE
Analyze acreage, yield, crop condition, weather distribution, stocks-to-use, export competition, input costs, biofuel policy, logistics, seasonality, government programs, speculative positioning and curve. Distinguish forecast uncertainty from realized crop loss.
~~~

## Credit

~~~text
ADD-ON — CREDIT
Decompose spread movement into risk-free duration, expected default, recovery, downgrade, liquidity and risk-premium components. Analyze leverage, coverage, maturity wall, refinancing, covenants, primary calendar, dealer inventory, fund flows, fallen-angel risk, basis and recovery. Compare cash bonds, CDS and equity signals.
~~~

## Crypto and digital assets

~~~text
ADD-ON — CRYPTO
Analyze global-dollar liquidity, real rates, stablecoin issuance/redemption, ETF/fund flows, leverage, funding, futures basis, options, exchange/custody risk, regulatory policy, token supply schedule, miner/validator economics, on-chain evidence quality, entity adjustment and weekend liquidity. Do not treat an on-chain metric as causal without timestamp, methodology and reflexivity controls.
~~~

## Volatility

~~~text
ADD-ON — VOLATILITY
Analyze implied versus realized volatility, term structure, skew, event premium, variance risk premium, spot-vol relationship, correlation, dealer gamma/vanna/charm estimates, supply/demand for convexity, expiry and liquidity. Distinguish direction, volatility and correlation trades.
~~~

## Country or sovereign risk

~~~text
ADD-ON — COUNTRY/SOVEREIGN RISK
Analyze growth/inflation/policy, fiscal path, debt currency and maturity, external financing need, reserves, current account, banking system, political institutions, election/policy distribution, sanctions, commodity exposure, local rates, FX regime, capital controls and default/restructuring mechanisms. Build a balance-sheet and funding map rather than a country narrative.
~~~

## Relative-value spread

~~~text
ADD-ON — RELATIVE VALUE
Model each leg independently, then the common factor and residual spread. Normalize duration, beta, currency, carry, roll, liquidity and transaction cost. Identify convergence mechanism, catalyst, structural break risk, financing/basis risk and conditions under which both legs can move against the spread thesis.
~~~

> [!important] Fundamental-only boundary
> Price-pattern analysis, indicator rules and chart-trigger instructions are prohibited. Use the Vault's fundamental, macro, valuation, flow, liquidity, market-structure and portfolio methods.

## V10 specialist and evidence gate

After selecting the direct primary canonical monograph, check the specialist registry for a narrower legal, industry, instrument or physical-market dependency. Do not retrieve a broad legacy field guide when a specialist canonical note exists. Probabilities must be labelled as empirically calibrated, model-implied or judgmental scenario weights. Internal QA may be reported; external scientific certification may not be claimed.
