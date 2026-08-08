# Paired Causal Effect Estimation

The highest-value D4 comparison is paired: actual and counterfactual outcomes for the **same frozen run**.

Examples:
- V19 veto versus `REMOVE_MODIFIER` branch;
- D3 delay versus immediate baseline branch;
- confidence-cap policy versus uncapped reference policy;
- positive-support shadow promotion versus V19 no-trade branch.

Primary paired quantity:
`delta_R = R_policy - R_reference`

Also report deltas in MFE, MAE, trigger rate, expiry rate, time-to-MFE and tail outcomes.

Pairing reduces confounding, but it does not create randomized causal identification. D4 therefore calls these **policy-effect estimates**, not experimental treatment effects.
