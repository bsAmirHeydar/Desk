# Outcome Maturity and Horizon Contract

An outcome is not valid merely because price moved after a call. D4 scores at the horizon intended by the decision and execution profile.

Supported research horizon families include intraday/event/session/daily/multi-day. The exact maturity clock is versioned in `config/outcome_horizon_policy.json`.

## Mandatory distinctions
- research thesis horizon;
- permission validity window;
- execution trigger window;
- realized position holding period;
- counterfactual evaluation window.

A no-trigger decision cannot be scored as a realized trade. It is reported separately as `EXPIRY_WITHOUT_TRIGGER` and may still enter signal-level path analysis.

A 2–5 day thesis is never declared wrong from a 15-minute adverse move. Conversely, an intraday permission is not rewarded because price eventually moved days after validity expired.
