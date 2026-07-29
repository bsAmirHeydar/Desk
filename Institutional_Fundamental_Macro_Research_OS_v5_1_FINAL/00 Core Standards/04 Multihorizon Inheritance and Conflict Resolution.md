---
title: "04 Multihorizon Inheritance and Conflict Resolution"
type: standard
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - institutional-standard
  - fundamental-research
  - governance
---
# 04 Multihorizon Inheritance and Conflict Resolution

> [!abstract] Purpose
> Integrate structural, cyclical, tactical, swing, daily, event, and microstructure evidence without allowing one horizon to silently override another.

## Horizon stack

| Layer | Typical persistence | Primary question | Valid influence |
|---|---:|---|---|
| Structural | 2–10+ years | What institutions/capacity constrain the distribution? | Prior and strategic valuation |
| Cyclical | 3–24 months | Where are growth, inflation, credit, and policy moving? | Regime and medium-horizon risk |
| Tactical | 2–12 weeks | What assumption is being repriced? | Campaign direction/expression |
| Swing | 2–10 days | Can the impulse persist through the next catalysts? | Position permission and holding plan |
| Daily | Session to 2 days | What changed since the prior close? | Directional permission |
| Event | Seconds to days | What is the surprise vector and reaction? | State update and event path |
| Microstructure | Milliseconds to hours | How does demand meet liquidity? | Timing, cost, path—not macro truth |

## Inheritance rules

1. Lower horizons inherit higher-horizon priors.
2. New evidence updates only the layers it can logically inform.
3. A daily move does not reverse a structural state without a transmission mechanism.
4. A structural view cannot override an intraday stop.
5. Conflicts reduce confidence or change expression; they are not averaged blindly.
6. Horizon-specific invalidation and expiry are separate.

## State object

```yaml
structural:
  distribution:
  evidence:
  expiry:
cyclical:
  distribution:
  transition_probability:
tactical:
  priced_gap:
  catalysts:
swing:
  impulse:
  half_life:
daily:
  permission:
event:
  surprise_vector:
microstructure:
  liquidity_state:
conflicts:
  - layers:
    resolution:
```

## Half-life

For an impulse \(z_t\), estimate persistence rather than assigning a narrative:

\[
z_{t+h}=\rho_h z_t+\varepsilon_{t+h},\qquad
h_{1/2}=\frac{\ln(0.5)}{\ln|\rho|}
\]

Use event- and regime-conditioned survival curves. A shock can have a short price half-life but a long state-information half-life, or vice versa.

## Conflict matrix

Examples:

- **Structural bullish / tactical bearish** — favor tactical short through a relative or defined-risk expression; do not call the structural thesis invalid.
- **Cyclical disinflation / daily inflation surprise** — determine whether policy-path repricing persists beyond event liquidity.
- **Swing thesis valid / intraday leader reverses** — cancel new entries; existing position follows predefined stop and re-entry rules.
- **Macro coherent / microstructure adverse** — maintain thesis but reduce urgency/size or wait for executable liquidity.
- **Technical trigger / macro no-trade** — no trade; permission is a necessary condition in this system.

## Cross-horizon aggregation

Never sum arbitrary scores. Estimate conditional value:

\[
EV(a,h)=\sum_s P(s|\mathcal I_t,h)\,[Payoff(a,s,h)-Cost(a,h)]
\]

Higher-horizon states affect scenario probabilities and terminal distributions. Lower-horizon states affect timing, path, cost, and stop-out probability.

## Audit

Record which layer changed, why, what inherited fields were updated, and which were deliberately unchanged. This prevents a session loss from rewriting a long-term worldview.
