# Dependence Robustness and Independent Root Events

Market observations are serially and causally dependent. D4 therefore avoids naive IID claims.

Preferred descriptive uncertainty uses resampling by independent root event or trading day when identifiers are available. Observation-level bootstrap is permitted only as a labelled fallback.

Reports must disclose:
- raw observation N;
- unique run N;
- unique trading-day N;
- independent root-event N;
- chosen resampling unit;
- unresolved dependence limitations.

Sample floors are governance gates, not statistical proof.

## V21 executable enforcement
`alphalab_d4_calibrate.py` now reports raw N, realized N, censored/no-trigger N, unique runs, unique trading days, independent roots, the actual resampling unit, cluster count and whether observation-level fallback was used. Positive-authority review cannot claim dependence-aware evidence when root clusters existed but were ignored.
