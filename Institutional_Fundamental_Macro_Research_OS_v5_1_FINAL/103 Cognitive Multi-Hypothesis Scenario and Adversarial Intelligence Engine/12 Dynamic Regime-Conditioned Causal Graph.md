# Dynamic Regime-Conditioned Causal Graph

Canonical knowledge describes possible relationships. A live decision requires a **run-specific graph** showing which relationships are active now.

Nodes may represent facts, expectations, policy, rates, FX, credit, volatility, liquidity, positioning, flow, mechanics, narratives, assets or real-state consequences. Edges are typed and receive a state: active, dormant, weakening, broken or uncertain. Every material edge has a horizon and evidence locator.

The graph is not built to maximize node count. It should include the smallest set of load-bearing paths needed to explain the current decision plus explicit rival paths. Correlated or confirming edges are visually distinct from causal edges. When an expected leader fails, the edge is weakened or broken and model-disagreement risk rises.
