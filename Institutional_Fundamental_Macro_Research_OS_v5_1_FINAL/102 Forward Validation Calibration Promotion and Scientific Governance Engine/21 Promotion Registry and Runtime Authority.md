# Promotion Registry and Runtime Authority

`config/promotion_registry.json` is the sole D4 authority registry.

Each active record identifies:
- promotion ID and modifier ID/version;
- market/horizon/regime scope;
- authority class;
- allowed preconditions;
- validation record IDs;
- independent validator decision;
- activation time;
- suspension/retirement triggers.

## Initial V20 registry
The release ships with **no new promoted rules**. Therefore D4 cannot change V19 permissions at installation time.

Runtime behavior is fail-closed:
- unknown modifier → shadow/report only;
- registry mismatch → no new authority;
- expired/suspended rule → no promoted effect;
- scope mismatch → no promoted effect.

## V21 scope and conflict resolution
The authority gate now matches promotion scope across instrument, horizon, session, regime, Fundamental direction, evidence grade and execution profile. More specific scope wins; risk-reducing constraints have precedence over positive permission restoration/creation. `CONFIDENCE_CAP` and `VALIDITY_SHORTEN` now produce explicit runtime effects rather than a receipt-only label.
