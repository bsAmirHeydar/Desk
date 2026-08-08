---
title: "DJIA Force Consumption and Persistence Book"
type: asset-operating-book
status: canonical-operational
version: 16.1.0
production_retrieval: allowed
---
# DJIA Force, Consumption and Persistence Book

DJIA is a **price-weighted** index. Never inherit Nasdaq or S&P factor sensitivity by default.

## Mandatory routing graph
1. **Identity / weights:** resolve current point-in-time constituents, divisor/methodology and price weights from S&P Dow Jones methodology/current constituent data.
2. **US macro root:** Fed path, nominal/real rates, growth, inflation, credit/funding and USD effects.
3. **Price-weighted constituent root:** identify whether one/few high-price constituents dominate the index move or earnings shock.
4. **Cyclical/industrial root:** industrial demand, capex, trade/industrial policy, transport/manufacturing where relevant.
5. **Financial/rates root:** curve, credit, lending/financial conditions for financial constituents.
6. **Health/regulatory root:** reimbursement/regulation/drug/health policy where material.
7. **Earnings/revision root:** constituent guidance, revision breadth and margins.
8. **Flow/mechanics root:** index rebalance, futures/options/passive flows only as separate mechanical evidence.

## Direction
Direction is produced only after ranking the active causal roots by materiality and horizon. A broad US-equity move is corroboration, not DJIA causality, unless the same root transmits through current price-weighted constituents.

## Consumption / pressure
Track macro-root and constituent-root consumption separately. A macro rates repricing can be consumed while an idiosyncratic high-weight earnings revision remains fresh, or vice versa.

## Rival models
Always consider: broad beta, cyclical growth, financial-rate sensitivity, health/regulatory shock, one/few constituent shock, and passive/rebalance mechanics.
