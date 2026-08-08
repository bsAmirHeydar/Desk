# Cross-Science Root-Cause Fusion — V21 Hardened

Module 101 constructs one deduplicated root map across Positioning, Flow, Funding, Mechanics and Capacity.

A single causal event may generate descendants in several sciences. D3 tracks `root_id`, parent/child lineage, observation type, materiality, horizon and independence from the Fundamental driver.

## V21 hardening: deduplicate independence, not effects

Earlier implementations could retain only the most severe observation for a root. V21 explicitly forbids that simplification when the same root carries materially different channels.

Example:

`CPI downside surprise → rates channel → supportive Nasdaq`

and simultaneously:

`CPI downside surprise → growth-scare channel → obstructive Nasdaq`.

The independent-root count remains **one**, but both channels remain in the root record. The root can be `CONTESTED`. A contested root cannot be counted as a clean confirmation merely because one descendant is supportive, and it cannot be multiplied because several datasets observe the same event.

The V21 root-channel map records every material channel, alignment, obstruction, evidence grade, horizon and unresolved conflict. Module 103 supplies the broader hypothesis/scenario context; Module 101 retains causal-modulation authority only.
