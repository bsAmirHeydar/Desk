# Direction-Aware Portfolio Shadow Model

Portfolio control remains SHADOW in V16.1.

Factor loadings describe **instrument-price sensitivity** to a factor. The portfolio gate then multiplies them by trade side and risk units, so BUY and SELL exposures can offset rather than being counted as identical bets.

Outputs include:
- signed factor exposure by family;
- unknown material exposures;
- same-direction root-factor concentration;
- offsetting exposures;
- concentration warnings;
- covariance status (`UNAVAILABLE`, `PARTIAL`, `EMPIRICAL`).

A root-count or ordinal loading is not a covariance model. Until forward telemetry supports stable factor estimates and stress behavior, the gate may warn and rank but may not silently remove trades. Promotion to ENFORCED requires versioned acceptance tests and bridge support.
