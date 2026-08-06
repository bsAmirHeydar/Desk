---
title: "Global Multi-Asset Coverage and Instrument Intelligence Engine"
type: moc
status: canonical
version: 13.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v13, universal-multi-asset]
---
# Global Multi-Asset Coverage and Instrument Intelligence Engine

## Mission

Module 91 is the canonical V13 routing and asset-adaptation layer. It extends validated V11 and V12 science to any resolvable FX instrument, materially tradable commodity or global index family without pretending that every market has complete live data.

## Architecture

```text
request → instrument resolution → metadata freeze → coverage state → V11/V12 shared state → family adapter → specialist evidence → report router → V13 record
```

## Coverage states

- `FULLY_SUPPORTED`
- `TEMPLATE_SUPPORTED`
- `LIMITED_DATA`
- `UNRESOLVED_OR_UNSUPPORTED`

## Navigation
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/01 Scope Honest Universality and Coverage Tiers]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/02 Universal Instrument Identity and Resolution]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/03 Asset Family Taxonomy]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/04 Symbol Alias Venue Benchmark and Contract Resolution]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/05 Point-in-Time Instrument Metadata]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/06 Universal Shared State and Asset Adapter Architecture]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/07 Report Router and Retrieval Planner]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/08 Global Calendar Timezone Session and Holiday Engine]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/09 Data Observability Licensing and Confidence Caps]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/10 Cross-Asset Driver Graph and Dependency Control]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/11 Universal Daily Reporting Workflow]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/12 Custom Watchlist and Batch Reporting]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/13 Cross-Sectional Ranking and Relative-Value Analysis]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/14 Universal Event Shock Propagation]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/15 Global Regime Classification and Regional Divergence]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/16 Country and Currency Block Architecture]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/17 Bilateral FX Pair Synthesis]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/18 G10 FX Operating Science]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/19 Emerging and Frontier FX Operating Science]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/20 Pegs Managed Floats Bands and Intervention]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/21 NDF Deliverability Capital Controls and Onshore Offshore Splits]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/22 FX Carry Funding Hedging and Cross-Currency Basis]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/23 External Balance Terms of Trade and Reserve Adequacy]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/24 Commodity Currency and Political-Risk Transmission]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/25 FX Fixings Month-End Quarter-End and Institutional Flows]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/26 Commodity Universe and Contract Identity]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/27 Physical Balance Supply Demand and Inventory Science]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/28 Futures Curves Basis Carry and Roll Yield]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/29 Commodity Location Grade Quality and Substitution]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/30 Commodity Seasonality Weather and Biological Cycles]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/31 Commodity Logistics Storage Freight and Bottlenecks]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/32 Energy and Crude Oil Operating Science]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/33 Refined Products and Refining Margin Science]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/34 Natural Gas LNG Power and Emissions Science]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/35 Precious Metals Operating Science]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/36 Base Metals Ferrous and Battery Materials Science]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/37 Grains Oilseeds and Agricultural Inputs Science]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/38 Soft Commodities Science]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/39 Livestock Forestry Rubber and Other Commodity Science]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/40 Commodity Producer Consumer and Policy Response]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/41 Global Index Universe and Methodology Resolution]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/42 Equity Index Fundamental Decomposition]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/43 Country Regional and Global Equity Index Science]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/44 Sector Factor Style and Thematic Index Science]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/45 Small Mid and Large-Cap Index Science]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/46 Index Constituents Weights Concentration and Rebalancing]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/47 Index Earnings Margins Valuation and Breadth]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/48 Currency Translation and Foreign Investor Transmission]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/49 Passive Flows Futures Options and Index Arbitrage]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/50 Volatility Index Science]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/51 Rates Bond and Duration Index Science]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/52 Credit Index Science]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/53 FX Dollar and Currency-Basket Index Science]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/54 Commodity Index Science]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/55 Universal Narrative and Attention Adaptation]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/56 Universal Fact Persistence and Consumption Adaptation]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/57 Universal Asymmetry and Ignored-Fact Detection]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/58 Single-Instrument Full Report Standard]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/59 Multi-Instrument Dashboard Standard]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/60 FX Daily Report Standard]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/61 Commodity Daily Report Standard]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/62 Global Index Daily Report Standard]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/63 Universal Full Analysis Production Prompt]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/64 Universal Short Launcher]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/65 FX Launcher]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/66 Commodity Launcher]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/67 Global Index Launcher]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/68 Custom Watchlist Launcher]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/69 Cross-Sectional Ranking Launcher]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/70 Relative-Value Pair Trade Research Launcher]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/71 Intraday and Event Update Launcher]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/72 End-of-Day Global Review Launcher]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/73 Machine-Readable V13 Universal State Schema]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/74 Instrument Registry and Adapter Contract]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/75 Benchmark Scenarios and Acceptance Tests]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/76 V11 and V12 Regression Preservation]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/77 Migration Precedence and Backward Compatibility]]
- [[91 Global Multi-Asset Coverage and Instrument Intelligence Engine/78 Residual Frontiers and Research Agenda]]

## Authority

Module 89 governs force/consumption/persistence/asymmetry. Module 90 governs attention/narratives/reflexivity. Module 91 governs identity, family adaptation, universal coverage, watchlists, rankings and relative value.
