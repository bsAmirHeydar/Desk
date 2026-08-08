# Modifier Attribution and Root-Level Sampling

Each evaluated modifier is identified by a stable `modifier_id`, science, causal channel, rule version and root-event identifiers.

## Units of analysis
D4 reports both:
- observation N;
- **independent root-event N**.

Promotion gates use independent-root N where dependence is material.

If one macro event creates 20 related intraday observations, D4 may describe all 20, but cannot pretend it has 20 independent causal events.

When several modifiers fire simultaneously, D4 distinguishes:
- isolated modifier cases;
- interacting modifier bundles;
- same-root bundles;
- independent-root combinations.

Unidentified interaction effects remain `UNDETERMINED`; they are not allocated by arbitrary score splitting.
