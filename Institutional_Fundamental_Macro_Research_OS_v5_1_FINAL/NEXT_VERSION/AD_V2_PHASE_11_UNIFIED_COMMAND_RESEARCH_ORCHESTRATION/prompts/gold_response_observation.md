# Alpha Desk V2 Gold Response Observation

Normalize the **subsequent** T0/T1 observation snapshots against the already-sealed expected signature. Return only `v2_response_observation`.

Hard laws:
- The sealed Pressure state and expected signature are immutable.
- Do not alter Pressure roots, magnitude, class, expected method/range/pathways or signature timestamps.
- Build actual_response only from T0/T1 point-in-time observations.
- When a metric is missing, preserve UNKNOWN/UNAVAILABLE rather than guessing.
- Build P05-compatible Gold observations from direct facts/proxies with their source/provenance.
- Price reversal alone cannot confirm liquidity grab, absorption, institutional accumulation, forced liquidation or release.
- Do not create Trade Permission or Broker action.
