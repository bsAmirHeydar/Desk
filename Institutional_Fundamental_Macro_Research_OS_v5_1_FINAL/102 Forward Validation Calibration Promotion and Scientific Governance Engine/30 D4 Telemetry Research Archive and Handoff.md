# D4 Telemetry, Research Archive and Handoff

D4 is the final architectural deployment but not a one-time experiment. It establishes a permanent learning loop.

Each production run emits a D4 Authority Receipt describing:
- V19 baseline decision;
- active promoted rule IDs, if any;
- shadow candidates evaluated;
- final permission after registry enforcement;
- registry version/hash;
- required outcome maturity clocks.

When outcomes mature, append Outcome and Counterfactual records. Periodic calibration produces immutable reports and promotion proposals.

D4 therefore transitions Alpha Lab from feature-building into continuous scientific operation.
