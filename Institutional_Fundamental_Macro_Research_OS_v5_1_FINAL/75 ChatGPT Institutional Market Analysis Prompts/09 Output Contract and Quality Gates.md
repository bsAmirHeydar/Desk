---
title: "Output Contract and Quality Gates"
type: standard
status: evergreen
version: 5.1.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - prompts
  - output-contract
  - quality-gates
---
# Output Contract and Quality Gates

Every full analysis must produce the following sections unless genuinely inapplicable.

## Required output

1. **Analysis identity** — market, instrument, mode, exact cutoff, timezone, session status, assumed holding period and data limitations.
2. **Executive verdict** — the dominant causal regime, what is priced, the most vulnerable assumption, and the practical trading implication.
3. **Vault route used** — the most relevant MOCs and notes selected from the uploaded ZIP.
4. **Multihorizon state table** — structural through microstructure, including direction, confidence, expected half-life and conflicts.
5. **Economic state** — growth, inflation, labor, policy, fiscal, liquidity, credit, external balance and relevant physical/industry state.
6. **Expectations and pricing** — consensus distribution, policy curve, yields, valuation, implied volatility, positioning and what the market already discounts.
7. **Asset-specific driver tree** — direct, indirect, conditional and rival drivers.
8. **Transmission map** — the complete causal path from evidence to the chosen market.
9. **Cross-asset confirmation** — rates, FX, equities, credit, commodities, volatility and funding, as relevant.
10. **Positioning, flows and market plumbing** — crowding, dealer/systematic flows, issuance, rebalancing, collateral, funding and liquidity.
11. **Scenario distribution** — base, upside, downside and tail scenarios with probabilities, triggers, expected path and falsifiers.
12. **Current or historical catalyst clock** — exact event times and which variables matter within each release.
13. **Fundamental permission** — `LONG_ONLY`, `SHORT_ONLY`, `TWO_WAY_REDUCED` or `NO_TRADE`, with confidence ceiling and explicit reasons.
14. **Day-trading handoff** — what must happen before entry, causal leader, confirmations, vetoes, expiry and no-trade conditions.
15. **Swing handoff** — two-to-ten-day thesis, carry, path dependency, overnight risks, next catalysts and thesis half-life.
16. **Invalidation architecture** — fundamental invalidation, market-implied invalidation, technical handoff and time expiry.
17. **Unknowns and evidence gaps** — unavailable, stale, paywalled, estimated or conflicting information.
18. **Claim–evidence ledger** — Fact, Estimate, Inference, Scenario or Unknown, with sources.
19. **Machine-readable context object** — YAML matching [[00 Core Standards/17 Context Object and Permission Schema Standard]].
20. **Bottom-line decision memo** — what matters now, what does not matter, what would change the view and what must not be traded.

## Quality gates

The answer fails institutional quality if any of the following occurs:

- It treats good/bad economic news as mechanically bullish/bearish without pricing and regime analysis.
- It confuses economic state with expectations, or expectations with asset payoff.
- It uses current revised data in a historical reconstruction.
- It hides missing information behind confident prose.
- It assigns probabilities without explaining their basis and uncertainty.
- It lists facts that do not affect probability, path, timing, payoff or permission.
- It ignores a material rival causal model.
- It uses one horizon to override another without an inheritance/conflict rule.
- It turns a fundamental thesis into permission to move a technical stop or average into loss.
- It cites a source that does not support the attached claim.
- It produces a directional verdict without stating what is already priced.
- It omits transaction costs, liquidity or event-gap risk when they are material.

## Evidence labels

Use these labels explicitly:

- **FACT** — directly observed and source-supported.
- **ESTIMATE** — model, survey or market-implied estimate.
- **INFERENCE** — reasoned interpretation from evidence.
- **SCENARIO** — conditional future path.
- **UNKNOWN** — unavailable or not reliably reconstructable.
- **EX-POST** — known only after a historical cutoff; prohibited from the reconstructed state.
