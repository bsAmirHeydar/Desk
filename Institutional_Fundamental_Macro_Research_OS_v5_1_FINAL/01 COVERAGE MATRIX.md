---
title: "Coverage Matrix — Horizons Markets Methods and Decisions"
type: map
status: evergreen
version: 5.1.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - coverage
  - moc
  - audit
---
# Coverage Matrix — Horizons Markets Methods and Decisions

> [!map] Coverage objective
> This matrix verifies that the Vault covers the chain from structural economic capacity to event-time execution and from official observations to auditable portfolio decisions.

## Horizon coverage

| Horizon | State object | Principal modules | Decision role |
|---|---|---|---|
| Structural | demographics, institutions, technology, resources, productive capacity, fiscal/monetary regime | [[44 Demographics Housing and Long-Horizon Structural Forces/00 MOC]], [[41 Energy Transition Climate and Resource Security/00 MOC]], [[43 Technology AI Productivity and Capital Cycle/00 MOC]] | priors, strategic valuation, stress boundaries |
| Cyclical | growth, inflation, labor, credit, liquidity, policy, profits | [[02 Macro State/00 Macro State MOC]], [[14 Macro Accounting and Stock-Flow Systems/00 MOC]], [[27 Macro Regime Ontology and State Machines/00 MOC]] | regime probability and medium-horizon risk |
| Tactical | pricing gap, policy path, revisions, supply, positioning | [[03 Market Pricing/00 Market Pricing MOC]], [[16 Rates Fixed Income and Policy Pricing/00 MOC]], [[48 Systematic Strategies Positioning and Flow Ecology/00 MOC]] | multi-week expression |
| Swing | incomplete repricing, catalysts, half-life, carry, gap | [[58 Institutional Swing Trading Campaign Playbooks/00 MOC]], [[70 Expanded Asset and Market Driver Books/00 Expanded Asset and Market Driver Books MOC]] | two-to-ten-day permission |
| Daily | overnight change, current pricing, leader, liquidity | [[23 Institutional Day and Swing Trading OS/00 MOC]], [[57 Institutional Day Trading Playbooks/00 MOC]], [[74 Non-Event Fundamental Context and Flow-Led Session Playbooks/00 Non-Event Fundamental Context and Flow-Led Session Playbooks MOC]] | session permission |
| Event | surprise vector, revisions, policy information effect, event path | [[08 Event Playbooks/00 Event Playbooks MOC]], [[69 Historical Point-in-Time Case Laboratory/00 Historical Point-in-Time Case Laboratory MOC]] | state update and persistence/reversal |
| Microstructure | spread, depth, inventory, options hedging, auction and impact | [[46 Market Microstructure and Execution Intelligence/00 MOC]], [[47 Derivatives Volatility Convexity and Tail Risk/00 MOC]] | execution, path, cost and kill conditions |

## Market coverage

| Market | Fundamental engine |
|---|---|
| Sovereign rates | policy path, inflation compensation, term premium, fiscal supply, investor base, collateral and funding |
| FX | relative policy, external balance, hedging/basis, valuation, intervention, risk and flow |
| Equities/indexes | revenue, margins, revisions, discount rates, risk premium, concentration, corporate/index flow |
| Single companies | three statements, unit economics, cash conversion, ROIC, valuation, governance and event surprise |
| Credit | default/recovery, migration, liquidity, issuance, covenants, maturity wall and fund flow |
| Banks/NBFI | liability stability, duration, capital, liquidity, leverage, margin, redemption and contagion |
| Oil/products/gas | physical balances, transformation capacity, stocks, logistics, curve and hedging |
| Metals/agriculture | production, inventories, end use, weather, cost curve, trade and location basis |
| Gold/silver | real rates, dollar, reserve demand, ETF/futures flow, physical premiums and tail demand |
| Crypto | network/custody, stablecoins, ETF flow, basis/funding, leverage, liquidations and dollar liquidity |
| Volatility/options | surface, term/skew, variance risk premium, event variance, Greeks and dealer-side scenarios |
| Real estate/REITs | rents, occupancy, cap rates, credit, supply pipeline, refinancing and local demand |
| Shipping/supply chains | fleet/capacity, routes, congestion, insurance, trade volumes and fuel |
| Cross-asset RV | common-driver neutrality, carry/roll, basis, hedge ratios, liquidity and scenario payoff |

## Research-method coverage

- national accounting and stock-flow consistency;
- point-in-time and bitemporal databases;
- dynamic factor/state-space and mixed-frequency nowcasting;
- BVAR/SVAR, local projections and regime models;
- panel, IV, DiD and synthetic controls;
- event studies and surprise vectors;
- curve, basis, repo and derivatives models;
- corporate financial statement and valuation models;
- portfolio construction, stress, capacity and transaction cost;
- probability calibration, multiple testing, drift and retirement;
- adversarial economic schools and rival-model synthesis;
- historical decision replay and rejected-trade counterfactuals.


## ChatGPT operationalization coverage

| Mode | Prompt route | Control objective |
|---|---|---|
| Universal dual mode | [[75 ChatGPT Institutional Market Analysis Prompts/01 Universal Dual-Mode Institutional Market Analysis Prompt]] | select CURRENT or HISTORICAL from one input contract |
| Current full spectrum | [[75 ChatGPT Institutional Market Analysis Prompts/02 Current Now Full-Spectrum Fundamental Analysis Prompt]] | combine live evidence with the complete multihorizon Vault method |
| Historical point in time | [[75 ChatGPT Institutional Market Analysis Prompts/03 Historical Point-in-Time Fundamental Reconstruction Prompt]] | reconstruct the information set without later revisions or outcome leakage |
| Current day trading | [[75 ChatGPT Institutional Market Analysis Prompts/04 Current Day-Trading Context Prompt]] | produce session permission, causal leaders, confirmations, vetoes and expiry |
| Current swing trading | [[75 ChatGPT Institutional Market Analysis Prompts/05 Current Swing-Trading Context Prompt]] | build a two-to-ten-day campaign with carry, catalysts, path and invalidation |
| Historical replay | [[75 ChatGPT Institutional Market Analysis Prompts/06 Historical Replay Counterfactual and Attribution Prompt]] | separate blind reconstruction, locked decision, outcome and counterfactual audit |
| Current event/catalyst | [[75 ChatGPT Institutional Market Analysis Prompts/13 Current Event and Catalyst Analysis Prompt]] | decompose priced baseline, surprise vector, reaction sequence and persistence |
| Cross-market relative value | [[75 ChatGPT Institutional Market Analysis Prompts/14 Cross-Market Relative-Value Analysis Prompt]] | compare legs, normalize risk and isolate the residual convergence mechanism |
| Portfolio hidden-beta audit | [[75 ChatGPT Institutional Market Analysis Prompts/15 Portfolio Fundamental Exposure and Hidden-Beta Audit Prompt]] | detect duplicated drivers, false diversification and catalyst concentration |

The prompt suite is governed by [[75 ChatGPT Institutional Market Analysis Prompts/09 Output Contract and Quality Gates]] and [[75 ChatGPT Institutional Market Analysis Prompts/10 Vault Reading and Evidence Protocol]].

## Completion boundary

No static Vault can contain future information, licensed real-time data, every proprietary dataset, or empirically proven alpha for every market. The completeness target is therefore **conceptual, methodological, operational and architectural coverage**. Production completeness is measured by data availability, replayability, model validation, execution integration and monitored live evidence.
