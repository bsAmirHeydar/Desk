---
title: "Market-Specific Add-On Blocks"
type: prompt-library
status: evergreen
version: 5.1.0
created: 2026-07-29
updated: 2026-07-29
language: fa
tags:
  - prompt
  - market-drivers
  - add-on
---
# Market-Specific Add-On Blocks

Append one or more blocks to a master prompt when deeper specialization is required.

## Equity index / Nasdaq / S&P

~~~text
ADD-ON — EQUITY INDEX:
Earnings and revision breadth, mega-cap concentration, equity duration, real-rate sensitivity, term premium, ERP, credit, dollar, buybacks, issuance, passive/index flows, breadth, sector leadership, vol surface, dealer gamma, expiry and cash-close mechanics را جداگانه تحلیل کن. Index direction را از index composition و leader concentration جدا نکن.
~~~

## Gold

~~~text
ADD-ON — GOLD:
Real yields را به expected policy، term premium و inflation compensation تجزیه کن. Dollar، central-bank demand، ETF/futures positioning، Asian physical demand، fiscal/monetary credibility، geopolitical hedge demand، lease/forward conditions و opportunity cost را بررسی کن. «جنگ=طلا بالا» یا «تورم=طلا بالا» را مکانیکی فرض نکن.
~~~

## Crude oil

~~~text
ADD-ON — OIL:
Global barrel balance، production/export، refinery runs، crude/product stocks، cracks، time spreads، freight، floating storage، spare capacity، OPEC compliance، sanctions/outages و demand nowcast را بررسی کن. Inventory headline را بدون composition، seasonality، adjustment و curve reaction تفسیر نکن.
~~~

## FX

~~~text
ADD-ON — FX:
Relative growth/inflation/policy distributions، OIS differentials، real-rate differentials، balance of payments، terms of trade، hedging demand، cross-currency basis، reserve/intervention flows، options/risk reversals، carry/crowding و global dollar regime را بررسی کن. هر دو سمت جفت‌ارز را مستقل تحلیل کن.
~~~

## Sovereign rates

~~~text
ADD-ON — RATES:
Expected short-rate path، term premium، inflation compensation، fiscal/issuance supply، auctions، foreign/real-money/dealer demand، repo/collateral، swap spreads، futures basis/CTD، convexity flows و rates volatility را تفکیک کن. Yield move را مستقیماً به hawkish/dovish policy نسبت نده.
~~~

## Single equity

~~~text
ADD-ON — SINGLE EQUITY:
Three statements، revenue price-volume-mix، margins، operating leverage، FCF، working capital، ROIC، balance-sheet/refinancing، accounting quality، dilution/buybacks، guidance، consensus revisions، valuation/reverse DCF، competitive position، supply chain، regulatory risk، ownership/positioning and options را تحلیل کن. Company alpha را از market/sector factor جدا کن.
~~~

## Credit

~~~text
ADD-ON — CREDIT:
Default probability، recovery، leverage، interest coverage، maturity wall، refinancing, covenant quality، downgrade/fallen-angel risk، dealer inventory، fund flows، primary calendar، basis and liquidity را بررسی کن. Spread move را به Treasury duration و credit component تجزیه کن.
~~~

## Crypto

~~~text
ADD-ON — CRYPTO:
Global dollar liquidity، real rates، stablecoin supply/redemption، ETF/fund flows، leverage/funding/basis، options، exchange/custody risk، regulatory policy، miner/validator economics، token supply schedule، on-chain evidence quality and weekend liquidity را بررسی کن. On-chain metric را بدون timestamp، entity adjustment و reflexivity مستقل فرض نکن.
~~~
