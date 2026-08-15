---
title: "Trade Permission Timing and Technical Boundary"
type: constitutional-method
status: shadow-development
version: "0.1.0"
---
# Trade Permission, Timing and Technical Boundary

## Core separation

A strong Directional Pressure state does not automatically authorize a trade.

The intended V2 separation is:

```text
Pressure → allowed directional thesis
Transmission / path / event risk → opportunity quality
Technical trigger → entry timing
Operational gate → final execution permission
```

## Price may change trade quality without changing Pressure

Valid example:

```text
Directional Pressure = BUY_HIGH
Price Transmission = NEGATIVE
Unmodeled Driver Risk = HIGH
Allowed Side = BUY_ONLY
Trade Permission = WAIT / NO_TRADE
```

This is not inconsistent. It protects the causal thesis from momentum contamination while protecting capital from premature entries.

## Technical authority

Technical structure may later determine:

- whether the user-defined setup exists;
- timing;
- stop/reference placement;
- trigger quality;
- path risk;
- local execution permission.

Technical structure may not determine Fundamental Directional Pressure.

## No forced trade

A high-pressure/high-unreleased-pressure hypothesis can remain `NO_TRADE` indefinitely if:

- transmission is unresolved;
- missing-driver risk is decision-critical;
- event hazard dominates;
- technical trigger is absent;
- liquidity/execution conditions are unacceptable.

## Outside-strategy edges

If price/mechanics reveal a valid counter-directional mechanical edge while the Fundamental strategy remains opposite, that edge must be routed as an outside-strategy research object. It cannot silently flip the Fundamental strategy.
