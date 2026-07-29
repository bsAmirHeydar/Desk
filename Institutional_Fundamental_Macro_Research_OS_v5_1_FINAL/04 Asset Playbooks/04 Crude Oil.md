---
title: "Crude Oil"
type: field-guide
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - 04-asset-playbooks
  - crude-oil
  - institutional-fundamental
---
# Crude Oil

> [!abstract] Research mandate
> Construct a point-in-time, source-controlled, model-aware and falsifiable understanding of **Crude Oil**. Canonical doctrine is linked; this note contains the topic-specific research object.

## Definition and economic object

Oil analysis reconciles global crude supply/demand, refinery transformation, products, inventories, trade, quality/location, spare capacity, and financial positioning.

For **Crude Oil**, the relevant institutional domain is **trading**: conversion of macro information into horizon-specific permissions, scenario paths, technical handoffs, and auditable trade management. Classify every input as observation, derived measurement, model estimate, market-implied estimate, forecast, causal claim, scenario assumption, judgment, or decision rule.

## Research questions

1. What exact state or mechanism does **Crude Oil** represent, in what unit, population, instrument, and convention?
2. Which **Crude Oil** observations existed at the decision cutoff, which are estimates, and which are revised?
3. What distribution about **Crude Oil** is embedded in consensus, curves, options, valuation, positioning, or physical basis?
4. Which market or variable must lead if the proposed **Crude Oil** mechanism is active?
5. What rival model can create the same target move while **Crude Oil** is unchanged?
6. How do regime, horizon, positioning, liquidity, carry, and implementation alter the payoff?
7. Which predeclared evidence rejects, caps, or expires the **Crude Oil** decision?

## Identities and model skeleton

$$
InventoryChange=Supply+Imports-RefineryRuns-Exports-OtherDemand
$$

$$
ImpliedDemand=Supply+Imports-Exports-InventoryChange
$$

$$
Crack\approx ProductValue-CrudeInputCost
$$

For **Crude Oil**, document every variable, unit, convention, sample, parameter, regularizer, and uncertainty estimate. An identity constrains possible stories; it does not estimate an elasticity or prove a causal channel.

## Measurement architecture

- **Measurement 1 for Crude Oil:** OPEC/non-OPEC production and exports.
- **Measurement 2 for Crude Oil:** refinery runs, outages, yields, and margins.
- **Measurement 3 for Crude Oil:** crude and product inventories.
- **Measurement 4 for Crude Oil:** freight, floating storage, and quality differentials.
- **Measurement 5 for Crude Oil:** curve, spreads, options, and COT.

The **Crude Oil** dataset must satisfy [[00 Core Standards/16 Data Dictionary and Release Calendar Standard]] and preserve first releases, revisions, and admissible timestamps under [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]].

## Estimation and validation stack

- **Model layer 1 for Crude Oil:** global barrel balance.
- **Model layer 2 for Crude Oil:** regional crude/product balance.
- **Model layer 3 for Crude Oil:** refinery margin model.
- **Model layer 4 for Crude Oil:** spare-capacity/outage scenarios.
- **Model layer 5 for Crude Oil:** curve and inventory-normalization model.

Validate the **Crude Oil** stack against simple point-in-time benchmarks. Report forecast/density error, probability calibration, regime stability, vintage sensitivity, feature ablation, latency, cost, and economic value. Register implementation under [[00 Core Standards/14 Model Card Standard]].

## Multihorizon behavior

| Horizon | Topic-specific role |
|---|---|
| Structural/Cyclical | In the **Crude Oil** research object, higher-horizon states create priors but do not time entries. |
| Tactical/Swing | In the **Crude Oil** research object, repricing path, catalysts, and half-life determine campaign permission. |
| Daily | In the **Crude Oil** research object, overnight change and current pricing produce one of four permission states. |
| Event/Intraday | In the **Crude Oil** research object, leader, confirmation, liquidity, and technical structure govern execution. |

Conflicts involving **Crude Oil** must retain separate state objects and be resolved through [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]], never by an undocumented average score.

## Causal transmission

1. **Crude Oil channel 1:** test `information gap → leader repricing`.
2. **Crude Oil channel 2:** test `leader → target asset`.
3. **Crude Oil channel 3:** test `positioning/liquidity → path shape`.
4. **Crude Oil channel 4:** test `technical structure → executable risk definition`.

**Crude Oil asset translation:** Trading: fundamentals grant permission; the technical structure controls entry, stop, and target. Predeclare the leader. If the target moves without the leader or with contradictory independent evidence, reduce the **Crude Oil** posterior or activate a rival explanation.

## Day-trading decision translation

- Identify the new **Crude Oil** information since the prior close and its source timestamp.
- Reconstruct the priced **Crude Oil** baseline before reading the target move.
- Name the liquid leader closest to the **Crude Oil** mechanism and one independent confirmation.
- Compare observed transmission with the **Crude Oil** event/quiet-day historical distribution.
- Assign a permission and a confidence cap; record the **Crude Oil** cancellation condition.
- Pass only the permission, leader, invalidation, expiry, and size ceiling to technical execution.

For **Crude Oil**, fundamentals restrict the allowed trade set; they do not supply the candle trigger or authorize widening a structural stop.

## Two-to-ten-day swing translation

- Define the still-open **Crude Oil** pricing gap rather than the general narrative.
- Estimate the **Crude Oil** impulse half-life and its uncertainty by regime.
- Map catalysts capable of confirming, reversing, or exhausting the **Crude Oil** campaign.
- Compare outright and relative expressions for carry, convexity, gap, liquidity, and factor purity.
- Specify terminal realization, time expiry, and evidence-based invalidation for **Crude Oil**.

A valid **Crude Oil** thesis with no residual pricing gap, adverse carry beyond expected payoff, or an imminent dominating catalyst is not a deployable swing.

## Falsification and known failure modes

- **Failure test 1 for Crude Oil:** using U.S. crude stocks as global balance.
- **Failure test 2 for Crude Oil:** ignoring products and refinery outages.
- **Failure test 3 for Crude Oil:** counting sanctioned barrels incorrectly.
- **Failure test 4 for Crude Oil:** mixing announced cuts with realized exports.
- **Failure test 5 for Crude Oil:** treating curve as pure inventory signal.

Score **Crude Oil** separately for state estimation, expectation measurement, causal transmission, expression, timing, sizing, execution, and residual noise. Neither a winning outcome nor a losing outcome alone establishes research quality.

## Required implementation record

Create a context object under [[00 Core Standards/17 Context Object and Permission Schema Standard]] containing the **Crude Oil** target, cutoff, data vintages, model version, state/market distributions, rival models, leader, confirmations, horizon, half-life, permission, confidence cap, size ceiling, invalidation, technical handoff, expiry, and claim IDs.

## Preserved subject-specific foundation

This material survived consolidation because it contains subject-specific instruction for **Crude Oil**, not the former repeated institutional wrapper.

## What Oil Trades

Oil is a physical market connected through storage, transport, refining, product demand, producer policy, and futures curves.

The price is influenced by:

- current and expected supply;
- current and expected demand;
- inventories;
- spare capacity;
- refinery and product balance;
- transportation constraints;
- quality/location differentials;
- geopolitical risk;
- dollar and financial conditions;
- positioning.

## Physical Balance

\[
\text{Inventory Change}
=
\text{Supply}
-
\text{Demand}
\]

Inventories are the balancing item, but reported inventories are incomplete and noisy globally.

## Supply

Track:

- OPEC+ targets and compliance;
- US production;
- rig count and productivity;
- outages;
- sanctions and exports;
- strategic reserves;
- spare capacity;
- project start-ups and decline rates.

## Demand

Track:

- global growth;
- China activity and imports;
- US and European product demand;
- aviation and mobility;
- petrochemicals;
- seasonality;
- price-induced demand destruction.

## Refining and Products

Crude can move differently from gasoline or distillates.

Track:

- refinery utilization;
- maintenance;
- crack spreads;
- product inventories;
- exports;
- regional shortages.

## Curve Structure

### Backwardation

Prompt prices above later prices. Often associated with tight immediate supply and positive convenience yield.

### Contango

Later prices above prompt. Often associated with adequate supply and storage economics.

Curve shape is informative but not a standalone signal.

## EIA Release Decomposition

Do not trade only “crude draw/build.”

Read:

- crude inventories;
- Cushing;
- gasoline;
- distillates;
- refinery utilization;
- production;
- imports;
- exports;
- implied demand;
- strategic reserve;
- seasonal expectation;
- prior revisions.

## Day-Trading Scenarios

### Bullish physical surprise

Crude draw plus product strength, strong refinery demand, supportive curve/spreads, and no offsetting production/export distortion.

### Bearish balance

Broad inventory builds, weak products, lower refinery demand, curve weakening.

### Geopolitical spike

Price rises on risk premium. Confirm physical route/supply exposure. Expect fast decay if no operational disruption.

### Growth liquidation

Oil falls with cyclicals, credit, and risk assets; curve may weaken. A later physical rebound is a separate thesis.

### Dollar shock

Stronger dollar can weigh, but physical tightness may dominate.

## Swing Framework

Maintain a rolling balance:

| Dimension | Bullish | Neutral | Bearish |
|---|---|---|---|
| Supply growth | | | |
| OPEC+ delivery | | | |
| Demand revisions | | | |
| Inventories vs season | | | |
| Curve | | | |
| Products | | | |
| Dollar/financial | | | |
| Positioning | | | |
| Geopolitical risk | | | |

## Common False Narratives

- “Inventory draw = buy.”
- “OPEC cut = guaranteed higher price.”
- “War = persistent oil rally.”
- “Backwardation means price must rise.”
- “China imports equal consumption.”
- “Rig count directly predicts next month’s output.”
- “Financial flows do not matter.”

## Execution Bridge

Use the fundamental map to choose direction. Wait for the current strategy’s structural continuation setup. Oil often gaps and overshoots around data; use event-specific slippage assumptions and do not place a structural stop inside ordinary release noise.

---

## Primary source routes for Crude Oil

- [[65 Source Registry and Claim Lineage/EIA_WPSR — EIA Weekly Petroleum Status Report]]
- [[65 Source Registry and Claim Lineage/EIA_STEO — EIA Short-Term Energy Outlook]]
- [[65 Source Registry and Claim Lineage/IEA_OMR — IEA Oil Market Report]]
- [[65 Source Registry and Claim Lineage/OPEC_MOMR — OPEC Monthly Oil Market Report]]
- [[65 Source Registry and Claim Lineage/CME_ENERGY — CME Energy Products]]
- [[65 Source Registry and Claim Lineage/CFTC_COT — CFTC Commitments of Traders]]

## Canonical controls

- [[00 Core Standards/01 Research Object and Decision Contract]]
- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[00 Core Standards/06 Causal Identification and Rival Models]]
- [[00 Core Standards/07 Permission Proof and Incremental Edge]]
- [[00 Core Standards/09 Portfolio Liquidity and Execution Handoff]]
