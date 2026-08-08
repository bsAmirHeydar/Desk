---
title: "Alpha Lab Live Learning Ledger"
type: live-forward-learning-ledger
status: active
version: 1.0.0
created: 2026-08-07
language: en-fa
scope: XAUUSD,NASDAQ100,SP500,DJIA,EURUSD,USDJPY
---

# Alpha Lab Live Learning Ledger

## Purpose
This note is the persistent forward-learning layer for Alpha Lab live analysis. It records what the model believed before outcomes were known, how price and causal drivers subsequently evolved, what was learned, and which learnings are provisional versus validated. It must never rewrite prior calls with hindsight.

## Scientific rules
- Evaluate only horizons that have matured.
- Preserve the exact prior timestamp, evidence set, direction, Edge class, permission, invalidations and next-review triggers.
- Separate forecast error from randomness, timing error, data limitation, and legitimate no-trade decisions.
- Never infer causality from price outcome alone.
- Do not optimize a rule from a single observation.
- New findings are appended first as `OBSERVATION` or `CANDIDATE`.
- Promotion path: `OBSERVATION -> CANDIDATE -> VALIDATED -> CANONICAL`.
- A core Vault rule may be changed only after repeated point-in-time evidence across enough independent cases/regimes to justify it, with rival explanations and failure cases documented.
- Contradictory evidence must be preserved, not deleted.

## Per-run learning protocol
For every completed Alpha Lab run and every symbol:
1. Load the previous immutable state.
2. Reconstruct realized price path from the previous cutoff to the current cutoff.
3. Evaluate only matured horizons: MICRO 0-15m, SHORT 15-60m, SESSION 1-6h, DAILY, NEXT_24H, 2-5D.
4. Compare realized path with prior direction, driver, narrative, consumption, remaining pressure, persistence, reversal risk, Edge class, permission, invalidations and expected transition triggers.
5. Record MFE/MAE or robust path proxies when available; do not fabricate unavailable data.
6. Classify the outcome:
   - CORRECT_STATE
   - CORRECT_DIRECTION_WRONG_TIMING
   - WRONG_DIRECTION
   - DRIVER_MISIDENTIFIED
   - NARRATIVE_MISREAD
   - CONSUMPTION_MISESTIMATED
   - REMAINING_PRESSURE_MISESTIMATED
   - REVERSAL_RISK_MISESTIMATED
   - TRANSMISSION_BREAK_MISSED
   - EVENT_RISK_MISREAD
   - OVER_VETO / MISSED_OPPORTUNITY
   - UNDER_VETO / FALSE_PERMISSION
   - DATA_LIMITATION
   - UNRESOLVED / HORIZON_NOT_MATURED
7. Explain what evidence at the original timestamp should have been weighted differently, without using future information as if it were available then.
8. Create a learning candidate only when it is operationally specific and falsifiable.

## Daily learning commit
At the end of each Tehran trading day, consolidate all new run-level learnings. Deduplicate them and append a dated section below. Every learning must contain:
- affected market(s), horizon(s), and regime;
- prior call and realized path;
- error/validation classification;
- causal post-mortem;
- evidence that was available at the time;
- evidence that was missing/unavailable;
- proposed analytical adjustment;
- rival explanation;
- confidence in the learning;
- status: OBSERVATION / CANDIDATE / VALIDATED / CANONICAL;
- validation requirement before promotion;
- whether the core Vault should change now: YES/NO.

## Canonical-change gate
Daily learning is mandatory; daily mutation of core science is not. Most new items should remain OBSERVATION or CANDIDATE until repeated evidence justifies promotion. When a learning becomes VALIDATED, update the relevant Vault methodology note and record the exact change, rationale, date, affected modules, and rollback condition here.

## Learning entries

_No entries yet. New entries must be appended chronologically and prior entries must remain immutable except for an explicit status-promotion record._

### 2026-08-07 12:12 Tehran — CANDIDATE — Scheduled-event proximity and conditional-edge transparency
- **Markets:** all six; initially surfaced from XAUUSD pre-NFP review.
- **Affected horizons:** MICRO, SHORT, SESSION; event-adjacent intraday states.
- **Observation:** A scheduled high-impact event several hours ahead must not automatically downgrade an otherwise currently tradable directional state from `EDGE_ACTIVE` to `EDGE_CONDITIONAL`. Event proximity should first shorten the state's usable validity window unless the event is already degrading price control, transmission, liquidity, asymmetry, or leaves insufficient time for the execution engine to exploit the edge.
- **Why this matters:** An automatic all-day event veto can create `OVER_VETO / MISSED_OPPORTUNITY` by discarding a valid pre-event continuation window.
- **Proposed analytical adjustment:** For every event-adjacent state explicitly distinguish `EVENT_AS_VETO` from `EVENT_AS_EXPIRY_CONSTRAINT`.
  - `EVENT_AS_EXPIRY_CONSTRAINT`: current edge may remain ACTIVE, but `valid_until` must expire safely before the event-risk window and the next review must be scheduled before that expiry.
  - `EVENT_AS_VETO`: use only when event proximity is already causing material fragmentation, liquidity deterioration, transmission failure, unstable price control, unfavorable path asymmetry, or an execution window too short to justify a new trade.
- **EDGE_CONDITIONAL transparency requirement:** Whenever any market is classified `EDGE_CONDITIONAL`, the deep analysis must explicitly show:
  1. **Why it is not EDGE_ACTIVE now**;
  2. **Decisive blocker(s)** ranked by importance;
  3. **Non-decisive caution factors** separately;
  4. **Exact missing/insufficient evidence**;
  5. **Exact upgrade trigger(s) to EDGE_ACTIVE**;
  6. **Exact downgrade trigger(s) to BIAS_ONLY / NO_EDGE / EVENT_OR_FRAGMENTED**;
  7. **Whether a scheduled event is a true veto or only a validity-window constraint**;
  8. **Current usable time window / valid-until logic**;
  9. **What specific live evidence would remove each blocker**;
  10. **Whether the conditional state may still contain a pre-event directional opportunity that is being withheld only because evidence quality is not yet sufficient.**
- **Hindsight firewall:** This is a methodology candidate, not a claim that the prior XAUUSD call was wrong. It must be validated forward by comparing event-adjacent conditional states against realized pre-event paths and the evidence that was actually available at the original timestamps.
- **Rival explanation:** High-impact event days may genuinely exhibit unstable liquidity/positioning well before the scheduled release, so a shorter validity window alone may sometimes be insufficient protection.
- **Status:** `CANDIDATE`
- **Confidence:** medium-high as an architectural improvement; empirical effect on edge quality is not yet validated.
- **Validation requirement:** Accumulate multiple independent event-adjacent cases across XAUUSD, FX, and US indices; measure `OVER_VETO`, `UNDER_VETO`, pre-event continuation quality, state stability, and whether `valid_until` would have protected the system before the event reset.
- **Core Vault change now:** NO. Apply as a provisional analysis/output contract and promote only after forward validation.


### 2026-08-07 16:10 Tehran — POST-NFP FORWARD REVIEW
- **Regime:** July 2026 Employment Situation released; pre-cash US session.
- **New facts:** NFP -23K vs ~+80K consensus; unemployment 4.1%; participation 61.4%; AHE 3.2% YoY; May+June revisions -103K. Treasury yields and USD fell post-release; Nasdaq-100 futures led around +0.8%.
- **XAUUSD prior:** BULLISH / EDGE_CONDITIONAL / NO_TRADE. **Review:** CORRECT_DIRECTION; POSSIBLE_OVER_VETO remains unresolved because the archive lacks a reliable start-price path and richer blocker state. Exact MFE/MAE unavailable.
- **NASDAQ100 prior:** MILD_BEARISH / BIAS_ONLY / NO_TRADE. **Review:** WRONG_DIRECTION / NARRATIVE_MISREAD with DATA_LIMITATION on exact start path. Positive multi-subsector guidance and relative index leadership should have reduced weight on localized AI sell-the-news. Permission NO_TRADE was not a false permission.
- **SP500 prior:** NEUTRAL / NO_EDGE / NO_TRADE. **Review:** CORRECT_STATE through the event boundary; the post-NFP rate-relief state is a new regime, not hindsight evidence against the prior no-edge call.
- **DJIA prior:** MILD_BEARISH_RELATIVE_WEAKNESS / EDGE_RELATIVE / NO_TRADE. **Review:** CORRECT_RELATIVE_STATE; NQ remained the stronger rate-sensitive index.
- **EURUSD prior:** MILD_BEARISH / BIAS_ONLY / NO_TRADE. **Review:** UNRESOLVED / DATA_LIMITATION; pre-event path was range-like and NFP resets the causal regime at 16:00 Tehran.
- **USDJPY prior:** BULLISH / EDGE_CONDITIONAL / NO_TRADE. **Review:** CORRECT_DIRECTION / CORRECT_VETO_LOGIC into the event; intervention risk justified withholding permission. NFP creates a new regime.
- **Causal post-mortem:** The labor report is not a one-dimensional weak-jobs signal. Payrolls and large downward revisions are dovish, while 4.1% unemployment is partly explained by a 264K monthly labor-force decline. Weak wage growth and falling yields/USD make the dovish interpretation materially stronger, but pair-specific transmission remains necessary.
- **Evidence available then:** pre-NFP consensus, earlier weak ADP/ISM employment evidence, strong gold/NQ pre-event price behavior, tech/software guidance, intervention/BOJ risk.
- **Missing evidence then:** the actual NFP/revisions/wages, post-release rate reaction, cash breadth, broker-level intraday path and live positioning.
- **OBSERVATION — cross-asset differentiation after labor shock:** A large payroll miss with lower yields can be bullish for duration-heavy NQ while leaving broad/cyclical indices less clean; NQ>SP/DJIA relative response helps distinguish rate relief from broad growth optimism.
- **OBSERVATION — unemployment headline quality:** A lower unemployment rate must be decomposed through participation/labor-force changes before it is used as an opposing force. In this case labor force fell 264K, limiting the bullish-labor interpretation of 4.1%.
- **Existing event-proximity learning:** receives another supportive forward observation, but **status remains CANDIDATE**. This run does not prove the rule because the persistent archive did not contain every intermediate active pre-event call.
- **Rival explanations:** pre-cash futures may reverse when cash breadth arrives; the payroll decline is partly concentrated in local-government education; inflation/oil may reassert hawkish pressure; post-event price moves can be positioning rather than durable causal repricing.
- **Confidence:** medium-high on the factual labor interpretation; medium on generalization.
- **Validation requirement:** repeat across independent NFP/CPI/FOMC cases, preserve event-time state, measure post-event persistence and OVER_VETO/UNDER_VETO by symbol.
- **Core Vault change now:** NO. No promotion to VALIDATED or CANONICAL.
