# AD-V3-P03 REV 3.3.5

## Semantic Dependency Evidence Closure
- Attaches exact current/previous dependency observations for derived semantic facts.
- Adds evidence diagnostics without converting diagnostics into Direction.
- Rejects semantic-bundle attempts to bypass inactive current-horizon authority.
- Keeps P03 SHADOW_ONLY; production Direction and trade Permission remain false.

# AD-V3-P03 Release Notes

Initial causal-brain implementation. SHADOW_ONLY. No production Direction or trade permission authority.

## REV 3.3.1
- Fixed live temporal handoff bug that discarded observations newer than receipt generation time.
- P03 now binds to exact P02 acquisition_run_id and requires all 192 current observations.
- Added fail-closed handoff integrity receipt and tampered/early-timestamp attack tests.

## REV 3.3.2
- Separates background stock bias from fresh directional impulse.
- Unchanged positive/negative real yields no longer re-fire session Direction.
- Adds background_bias and impulse_direction to root states.
- Makes persistence signal/horizon-aware instead of using the longest active contract horizon.
- Expectations repricing now requires actual impulse/repricing evidence.
- Added live-discovered anti-refire and horizon-persistence attack tests.

## REV 3.3.3
- Enforces fact `active_horizons` before causal, transaction, or mechanical pressure can affect the current reasoning horizon.
- Prevents monthly/slow facts such as SGE withdrawals and physical imports from leaking into SESSION_1_6H transaction pressure.
- Separates explicit signed net flow, level delta, and gross activity semantics.
- A positive gross level is no longer interpreted as bullish merely because it is above zero.
- GLD/IAU holdings use changes in levels; SGE withdrawals and China/India imports use reference-period level changes; delivery/trade activity requires richer directional semantics.

## REV 3.3.4
- Adds a first-class Semantic Evidence Packet exporter for the exact P02 acquisition run consumed by P03.
- Each semantic request is paired with current and previous observations, source/provenance fields, epistemic quality, warnings, horizon eligibility, and authority scope.
- Structural background, current-horizon causal authority, mechanical context, and vulnerability context are explicitly labeled to prevent semantic overreach.
- Evidence packet itself grants no Direction or permission and performs no network access.


## REV 3.3.6 — Economic Comparison Anchor Integrity

- separates previous acquisition fetch from previous economic observation;
- adds distinct reference-period/event-time/published-at comparison anchors;
- exposes `NO_DISTINCT_ECONOMIC_ANCHOR` when a valid prior economic state is unavailable;
- forbids treating repeated fetch equality as zero economic impulse or NEUTRAL direction;
- preserves existing no-refire semantics and all SHADOW_ONLY authority boundaries.
