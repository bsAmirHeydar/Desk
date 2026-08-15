# Continuous calibration

After freeze and outcome phases, P08 runs P07 calibration on the currently persisted outcome links and evaluates promotion gates with independent-validator approval fixed to FALSE.

P08 may report:
- `TRUE_FORWARD_PENDING`
- `ELIGIBLE_FOR_INDEPENDENT_REVIEW`

It cannot report a commissioned authority change. It cannot auto-promote. It cannot set operator approval. It cannot create positive trade permission.
