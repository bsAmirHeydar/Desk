# Public Swap SDR Transaction Intelligence

## Object
CFTC Part 43 public dissemination makes many reportable swap transactions observable through registered SDRs. V21.3 treats these as **direct transaction facts with partial market coverage**.

## What may be observed
Depending on repository/asset class and the public fields: timestamp, product/asset class, economic terms, price/rate, notional subject to caps/masking, action/correction/cancellation and other disseminated fields.

## What is not observed by default
- complete counterparty/client identity;
- full dealer inventory;
- the entire OTC market in one repository;
- a clean signed buy/sell direction equivalent to an exchange aggressor side.

## Required normalization
1. preserve SDR identity and transaction/correction lifecycle;
2. deduplicate corrections/cancellations;
3. normalize product/tenor/currency/index;
4. preserve block/large-notional dissemination treatment;
5. classify direct transaction fact separately from any flow-sign inference;
6. group same-root event bursts without pretending every print is independent macro evidence.

## Six-market relevance
- **EURUSD/USDJPY:** FX/rates derivative repricing and hedging context; not a substitute for spot client flow.
- **NASDAQ/SP500/DJIA:** rates/equity/credit swap activity may diagnose transmission and hedging.
- **XAUUSD:** rates/commodity swap subsets can inform derivatives transmission but not physical/OTC gold completeness.
