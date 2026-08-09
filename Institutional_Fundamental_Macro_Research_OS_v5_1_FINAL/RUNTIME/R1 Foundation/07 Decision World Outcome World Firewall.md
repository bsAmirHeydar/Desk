# Decision World / Outcome World Firewall

## Decision World

Contains only information allowed to influence the decision at the analysis cutoff:

- retrieved/admitted evidence;
- fact state;
- market state;
- cognition;
- D3/D4 governance state available at the cutoff;
- research intent and permission.

## Outcome World

Contains information that becomes legal only after Decision Freeze:

- later price path;
- execution fills;
- realized costs;
- MFE/MAE;
- outcome labels.

## Learning World

Contains counterfactuals, telemetry and calibration artifacts derived after freeze.

## Runtime enforcement

- Writing OUTCOME/LEARNING artifacts before a valid Decision Seal is forbidden.
- Writing or replacing DECISION artifacts after a valid Decision Seal is forbidden.
- Replay code receives snapshot references, never an unrestricted future-data path.
- A decision-world verifier recomputes every sealed hash.

This boundary is structural. Prompt instructions alone are not considered sufficient lookahead protection.
