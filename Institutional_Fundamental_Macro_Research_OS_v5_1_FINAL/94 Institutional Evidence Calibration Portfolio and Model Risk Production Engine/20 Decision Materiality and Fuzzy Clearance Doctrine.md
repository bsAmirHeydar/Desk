# Decision Materiality and Fuzzy Clearance Doctrine

V16.1 replaces blanket completeness with **decision materiality**. Accuracy is maximized by being strict about facts that can change the decision and flexible about secondary uncertainty.

## Three evidence/clock materiality tiers
- `DECISION_CRITICAL`: if wrong, stale or unresolved, the direction/Edge/permission could materially change.
- `MATERIAL_SECONDARY`: relevant to confidence, validity window, challenger strength or sizing research, but its absence alone must not manufacture `NO_TRADE`.
- `CONTEXTUAL`: useful context; absence is disclosed and never blocks.

## Four evidence-clearance states
- `CLEAR`: decision-critical evidence is sufficiently resolved.
- `CLEAR_WITH_CONFIDENCE_CAP`: secondary uncertainty remains; keep the thesis but cap confidence/validity.
- `HOLD`: a decision-critical unknown could plausibly flip the Edge; wait for resolution.
- `BLOCK`: identity, provenance, lookahead, corruption or other logical failure makes the decision unsafe.

## Marginal-decision test
Before any hard block ask:
> If this unresolved item were removed or resolved the other way, could the current direction, Edge class or permission change?

If **no**, it is not a hard blocker. If **yes**, classify the item as decision-critical and state the exact state transition it can cause.

## Fuzzy discipline
Fuzzy does not mean vague. Use explicit linguistic states and rival cases rather than arbitrary pseudo-probabilities. A state may be directionally strong while confidence is capped, or temporally usable while a contextual clock is unknown.

## Anti-over-veto rule
`NO_TRADE` must never be the default consequence of generic incompleteness. It is justified only by absent Edge, material opposition/fragmentation, unsafe timing, decision-critical evidence uncertainty, or operational safety failure.
