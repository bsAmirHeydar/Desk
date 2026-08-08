---
title: "AM PM Settlement Exercise and Expiration Microstructure"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, temporal-intelligence, institutional]
---
# AM/PM Settlement, Exercise and Expiration Microstructure

Product-specific settlement mechanics are mandatory. OCC explicitly warns that different indexes derive settlement values at different times (`SRC-OCC-INDEX`). SPX and DJX specifications likewise distinguish regular/weekly expiration timing (`SRC-CBOE-SPX`, `SRC-CBOE-DJX`).

## AM settlement
Settlement may be derived from opening prices/SOQ. Risk concentrates in the opening process and may persist until all constituent opens are represented.

## PM settlement
Settlement can reference closing values or defined futures fixing windows. Mechanical flow therefore concentrates near the cash close/fixing rather than the open.

## Exercise style
American versus European exercise changes assignment/exercise behavior but is separate from market direction.

## Engine rule
Never label “options expiry at 4pm” generically. Resolve the exact product, expiry series, settlement style, last trading time, underlying/fixing source and holiday rule.

## Data confidence
If the target broker trades a CFD while institutional timing is inferred from SPX/NDX/DJX/ETF/futures options, record the relationship as a proxy and state the transmission assumption.
