---
title: "Revision, Missingness, Selection and Survivorship Bias"
type: monograph
status: canonical
version: 6.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [fundamental-foundations, phase-01, epistemology]
---

# Revision, Missingness, Selection and Survivorship Bias

> [!abstract] Canonical thesis
> The observed dataset is a selected and revised record, not a neutral mirror. Missingness mechanisms, sample entry and exit, delistings, reporting incentives and historical revisions can change the apparent relationship.

## Analytical intuition

If failed companies disappear from a database, past investment results look better. If only countries with good data are studied, conclusions may not generalize. If missing observations occur during crises, filling them with normal values hides stress.

## Institutional definitions and distinctions

| Term or distinction | Precise meaning |
|---|---|
| MCAR, MAR, MNAR | Missing completely at random, conditionally random, or dependent on unobserved values. |
| Selection bias | Systematic difference between observed and target populations. |
| Survivorship bias | Exclusion of failed, delisted, merged or discontinued units. |
| Backfill bias | Historical observations added only after an entity enters a database or index. |
| Revision bias | Using later estimates whose error properties differ from the real-time data. |

## Mechanism map

1. Document inclusion rules and coverage changes.
2. Classify missingness and test crisis concentration.
3. Preserve dead securities, discontinued series and historical constituents.
4. Separate first-release and final-vintage questions.
5. Use bounds or sensitivity when missingness is non-random.
6. Report how sample construction changes conclusions.

## Formal structure and notation

### Selection condition

$$
\mathbb E[Y\mid Selected=1]\neq \mathbb E[Y]
$$

Observed samples can differ systematically from the population, invalidating naive generalization.

### Inverse probability weighting

$$
\hat\mu=\frac{1}{N}\sum_i\frac{S_iY_i}{\hat p_i}
$$

Weighting can address selection under strong assumptions that selection probabilities are estimable and all confounders observed.

## Competing interpretations and adversarial synthesis

| View | What it explains | Where it can fail |
|---|---|---|
| Complete-case analysis | Simple and transparent. | Biased unless missingness is benign. |
| Model-based imputation | Uses observed relationships to restore incomplete data. | Creates false certainty when missingness is informative. |
| Partial identification | Reports bounds under weaker assumptions. | May produce wide intervals that are less convenient for decisions. |

## Historical and institutional cases

### Equity index history

Using current constituents to study historical index fundamentals creates survivorship and composition bias.

### Emerging-market crises

Data availability can deteriorate exactly when capital controls, defaults or political disruptions make the observations most important.

## Multihorizon interpretation

- **Structural/secular:** identify persistent institutions, stocks or constraints governing **Revision, Missingness, Selection and Survivorship Bias**; begin with: Document inclusion rules and coverage changes.
- **Cyclical:** determine how the mechanism changes across expansion, slowdown, recession, recovery, inflation and disinflation; interrogate: Classify missingness and test crisis concentration.
- **Tactical/multi-week:** identify which expectation, valuation or policy assumption is vulnerable; test: Preserve dead securities, discontinued series and historical constituents.
- **Event/current:** define the new information, contemporaneous expectation and first observable mechanism; verify: Separate first-release and final-vintage questions.
- Use the full inheritance and conflict standard in [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Horizon Inheritance, Conflict Resolution and Double-Counting Control]].

## Failure modes and red-team tests

- Forward-filling a crisis series without annotation.
- Using only surviving funds or securities.
- Ignoring index reconstitution history.
- Imputing values from the outcome variable.
- Treating a cleaned vendor database as raw truth.

## Worked reasoning protocol

Apply [[78 Phase 01 Institutional Fundamental Foundations Canon/Phase 01 Canonical Research Protocol]] to **Revision, Missingness, Selection and Survivorship Bias**. The topic-specific sequence is:

1. Document inclusion rules and coverage changes.
2. Classify missingness and test crisis concentration.
3. Preserve dead securities, discontinued series and historical constituents.
4. Separate first-release and final-vintage questions.
5. Use bounds or sensitivity when missingness is non-random.
6. Report how sample construction changes conclusions.

## Adversarial analytical checks and accreditation questions

1. Audit a historical equity sample for survivorship and backfill bias.
2. Design sensitivity bounds for missing sovereign reserve data.
3. Compare first-release and final-vintage performance of a recession indicator.

## Annotated source canon

- **Donald Rubin, Multiple Imputation for Nonresponse in Surveys.** Missing-data taxonomy and model-based treatment.
- **James Heckman selection literature.** Selection mechanisms and correction under explicit assumptions.
- **CRSP and index methodology documentation.** Historical constituents, delistings and corporate actions.

## Related canon

- [[53 Research Statistics Forecasting and Causal Inference/00 MOC]]
- [[55 Data Platform Ontology Lineage and Governance/00 MOC]]

---

Previous: [[78 Phase 01 Institutional Fundamental Foundations Canon/02 Epistemology Measurement and Evidence/Uncertainty Taxonomy — Risk, Ambiguity, Ignorance and Model Error]] · Next: [[78 Phase 01 Institutional Fundamental Foundations Canon/02 Epistemology Measurement and Evidence/Conflicts of Interest, Incentives and Institutional Bias]] · Module: [[78 Phase 01 Institutional Fundamental Foundations Canon/00 Phase 01 Institutional Fundamental Foundations Canon MOC]]
