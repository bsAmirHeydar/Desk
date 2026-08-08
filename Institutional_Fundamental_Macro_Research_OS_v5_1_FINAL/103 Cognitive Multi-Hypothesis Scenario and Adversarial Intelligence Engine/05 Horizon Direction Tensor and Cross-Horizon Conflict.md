# Horizon Direction Tensor and Cross-Horizon Conflict

V11 already requires horizon-specific states; V21 makes that requirement a first-class production object. Direction is not one scalar. The system maintains separate Fundamental directions for micro, short, session, daily, multi-day, swing, cyclical and structural horizons.

The active trading strategy must name its horizon explicitly. A structural bullish prior may coexist with a session bearish state. That is not an error and must not be averaged into `NEUTRAL` unless the active horizon itself is genuinely neutral.

Each horizon keeps Direction, force, persistence, consumption, remaining asymmetry, reversal hazard, causal leader and next update trigger. Cross-horizon conflict is labeled as alignment, tactical override, structural/tactical divergence, contested or unresolved.

Only the Module 89 state at the **active strategy horizon** supplies the Direction authority used by the Fundamental strategy. Longer horizons are priors; shorter horizons can describe path risk and event mechanics but do not silently overwrite the active-horizon direction.
