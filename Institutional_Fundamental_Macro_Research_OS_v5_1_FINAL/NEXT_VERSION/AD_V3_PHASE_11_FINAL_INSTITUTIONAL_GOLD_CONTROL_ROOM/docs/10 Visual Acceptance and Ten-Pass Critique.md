# P11 Visual Acceptance and Ten-Pass Critique

P11 was refined as one final Control Room, not ten alternative designs. The critiques below were performed against rendered deterministic fixtures and Chromium viewport checks.

## Pass 1 — Information hierarchy
**Finding:** The renderer needed a strict separation between the immediate research decision and forensic detail.  
**Correction:** The first viewport now prioritizes headline, Direction, Strength, Dominance, Research Permission, Edge, Consumption, Fragility, decision time and authority state. Deep provenance is below the decision layer.

## Pass 2 — Institutional minimalism
**Finding:** Rendering all 192 Fact rows directly in the page created an unnecessarily long report even though each row was collapsed.  
**Correction:** The full evidence universe is now behind an `Advanced` disclosure. Causal roots remain directly explorable while the 192-Fact universe opens only when requested.

## Pass 3 — Decision clarity
**Finding:** WAIT must not look like missing output.  
**Correction:** WAIT is presented as a valid research permission with blockers/constraints, consumption, fragility and Watch Next context. BUY/SELL remain explicitly research permission, not execution.

## Pass 4 — Scientific honesty
**Finding:** Fundamental pressure and price behaviour can visually look contradictory to a human reader.  
**Correction:** Pressure planes and Price Transmission are separate sections with an explicit `Pressure ≠ Price` explanation. Price never overwrites causal pressure in presentation logic.

## Pass 5 — Data-health clarity
**Finding:** One aggregate completeness number would hide the distinction between fresh session data and slow/known gaps.  
**Correction:** Live Kernel, Context, Semantic state and Admission are shown separately. Important gaps include a human-readable impact statement and cached context is not called live.

## Pass 6 — Evidence discoverability
**Finding:** The expert audit path needed to be available without overwhelming normal use.  
**Correction:** Root-first exploration exposes role/direction/importance/magnitude/freshness/persistence. Root details lead to Fact/Observation/Source metadata. Full universe search/filter is behind advanced disclosure.

## Pass 7 — RTL typography and mixed technical text
**Finding:** Long English technical identifiers inside an RTL layout can force width expansion and reduce readability.  
**Correction:** Technical identifiers use explicit LTR islands with `overflow-wrap:anywhere`; source IDs and long Fact IDs remain readable without reversing timestamps or breaking the page.

## Pass 8 — Mobile usability
**Finding:** Initial Chromium testing at 390px found 43px page-level overflow, mainly from data-health cards containing long identifiers and nested grids.  
**Correction:** Grid/card children now use `min-width:0`, long LTR text wraps safely, pills can wrap, and mobile containment is explicit. Final Chromium metrics: `scrollWidth == clientWidth` at 390px.

## Pass 9 — Accessibility and security
**Finding:** Forensic disclosure must remain keyboard-safe and untrusted evidence must never become executable HTML.  
**Correction:** Native `details/summary`, accessible labels, focus states, reduced-motion CSS, semantic landmarks, CSP, HTML escaping and safe-protocol URL filtering are enforced. XSS fixture with `<script>alert(1)</script>` remains text only.

## Pass 10 — Final simplification
**Finding:** The report should contain only information that helps decide, understand, monitor, invalidate or audit.  
**Correction:** No fake confidence gauges, no giant master narrative, no remote chart dependencies, no default 192-row dump, no decorative dashboard widgets. The final order is: Now → Changed → Drivers → Pressure → Transmission → Watch → Invalidation → Events → Data → Forward → Evidence → Audit.

## Visual acceptance
Chromium deterministic browser acceptance passed at:
- 1920×1080
- 1440×900
- 1366×768
- 768×1024 tablet
- 390×844 mobile

For every viewport:
- RTL remained active;
- required decision/evidence regions rendered;
- page-level horizontal overflow was zero;
- the self-contained HTML required no network access for core state.
