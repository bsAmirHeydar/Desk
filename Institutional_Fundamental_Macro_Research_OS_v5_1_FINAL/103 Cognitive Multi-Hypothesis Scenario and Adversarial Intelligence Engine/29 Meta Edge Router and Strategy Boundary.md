# Meta Edge Router and Strategy Boundary

A market can have a real directional opportunity that is not Fundamental. V21 distinguishes `NO EDGE` from `EDGE OUTSIDE THIS STRATEGY`.

The router can classify Fundamental, Mechanical, Forced-Flow, Event-Repricing, Liquidity-Dislocation, Relative-Value or Unclassified edges. Only `FUNDAMENTAL_EDGE` belongs to the current Fundamental strategy permission path.

Outside-strategy edges are logged and routed to a separate research queue. They have **zero permission effect** in V21. This protects the purity of the Fundamental strategy while preventing the brain from pretending that a non-fundamental market move does not exist.
