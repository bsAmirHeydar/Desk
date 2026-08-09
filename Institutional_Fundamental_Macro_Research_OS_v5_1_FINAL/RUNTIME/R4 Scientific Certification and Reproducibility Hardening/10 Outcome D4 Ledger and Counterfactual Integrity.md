# Outcome, D4 Ledger and Counterfactual Integrity

Certification checks that:
- forward observation is frozen before outcome knowledge;
- outcome requires decision seal;
- `NO_TRADE` and `NO_TRIGGER` remain distinct;
- counterfactual branches are defined from the frozen information set;
- ex-post best-entry/stop/exit optimization is not promoted to a valid counterfactual;
- D4 canonical schemas are validated before append;
- ledger sequence, previous hash, payload hash and JSONL projection verify;
- calibration is review-only and cannot mutate the Promotion Registry;
- numeric predictive probability is not fabricated without calibrated authority.
