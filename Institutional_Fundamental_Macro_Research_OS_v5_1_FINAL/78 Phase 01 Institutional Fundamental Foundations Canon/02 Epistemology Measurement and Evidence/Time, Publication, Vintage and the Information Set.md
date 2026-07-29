---
title: "Time, Publication, Vintage and the Information Set"
type: monograph
status: canonical
version: 6.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [fundamental-foundations, phase-01, epistemology]
---

# Time, Publication, Vintage and the Information Set

> [!abstract] Canonical thesis
> Economic truth, reference period, publication time, revision vintage and analyst retrieval time are different clocks. Point-in-time reasoning requires all of them to prevent hindsight contamination and false real-time confidence.

## Beginner intuition

A report about June may be published in July, revised in August and benchmarked next year. An analyst studying a July decision cannot use the later values, even if they are more accurate today.

## Institutional definitions and distinctions

| Term or distinction | Precise meaning |
|---|---|
| Event time | When the underlying economic activity occurred. |
| Reference period | The period the statistic describes. |
| Release time | When information became public. |
| Vintage | The version of a series available at a specific time. |
| Retrieval time | When the researcher accessed or stored the source. |
| Information set | Everything demonstrably available to the decision-maker by a cutoff time. |

## Mechanism map

1. Record event and reference periods.
2. Record official release timestamp and timezone.
3. Preserve first release and every revision.
4. Capture market and policy expectations available before release.
5. Reconstruct decision information without future summaries.
6. Audit accidental use of revised or post-cutoff evidence.

## Formal structure and notation

### Bitemporal record

$$
X=(value,valid\_time,known\_time,vintage)
$$

Valid time represents the period the value describes; known time represents when it became available. Both are required.

### Revision decomposition

$$
X_t^{final}-X_t^{first}=News_t+Method_t+Benchmark_t
$$

Revisions can reflect new source information, method or seasonal-factor changes, and comprehensive benchmarks.

## Competing interpretations and adversarial synthesis

| View | What it explains | Where it can fail |
|---|---|---|
| Latest-data research | Uses the best current estimate of history. | Misrepresents real-time forecasting and decision difficulty. |
| First-release research | Matches the initial information set. | First releases may be noisy and not the object some theories address. |
| Multi-vintage research | Studies both real-time decisions and later truth estimates. | Requires careful storage and separate evaluation questions. |

## Historical and institutional cases

### Payroll revisions

Initial labor strength can later be revised materially; the policy and market response must be evaluated against the first release.

### GDP benchmark revisions

Historical growth paths can change because of source data and methodology, altering apparent model performance if vintages are ignored.

## Multihorizon interpretation

- **Structural/secular:** identify persistent institutions, stocks or constraints governing **Time, Publication, Vintage and the Information Set**; begin with: Record event and reference periods.
- **Cyclical:** determine how the mechanism changes across expansion, slowdown, recession, recovery, inflation and disinflation; interrogate: Record official release timestamp and timezone.
- **Tactical/multi-week:** identify which expectation, valuation or policy assumption is vulnerable; test: Preserve first release and every revision.
- **Event/current:** define the new information, contemporaneous expectation and first observable mechanism; verify: Capture market and policy expectations available before release.
- Use the full inheritance and conflict standard in [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Horizon Inheritance, Conflict Resolution and Double-Counting Control]].

## Failure modes and red-team tests

- Using a current chart to describe what was known historically.
- Applying a release date without the exact time and timezone.
- Ignoring embargoes, leaks and asynchronous dissemination.
- Comparing forecasts made against different data vintages.
- Calling a later revision an obvious fact that decision-makers missed.

## Worked reasoning protocol

Apply [[78 Phase 01 Institutional Fundamental Foundations Canon/Phase 01 Canonical Research Protocol]] to **Time, Publication, Vintage and the Information Set**. The topic-specific sequence is:

1. Record event and reference periods.
2. Record official release timestamp and timezone.
3. Preserve first release and every revision.
4. Capture market and policy expectations available before release.
5. Reconstruct decision information without future summaries.
6. Audit accidental use of revised or post-cutoff evidence.

## Exercises and accreditation questions

1. Build a five-clock timeline for a CPI release.
2. Explain how vintage choice changes a recession-forecast evaluation.
3. Audit a historical memo for hindsight contamination.

## Annotated source canon

- **Federal Reserve Bank of St. Louis ALFRED documentation.** Real-time periods and historical vintages for macro data.
- **Bureau of Economic Analysis revision policies.** Advance, second, third and comprehensive estimate architecture.
- **00 Core Standards/03 Point-in-Time and Bitemporal Data Standard.** Vault canonical time and vintage contract.

## Related canon

- [[00 Core Standards/03 Point-in-Time and Bitemporal Data Standard]]
- [[69 Historical Point-in-Time Case Laboratory/00 Historical Point-in-Time Case Laboratory MOC]]

---

Previous: [[78 Phase 01 Institutional Fundamental Foundations Canon/02 Epistemology Measurement and Evidence/Source Hierarchy, Provenance and Claim-Level Citation]] · Next: [[78 Phase 01 Institutional Fundamental Foundations Canon/02 Epistemology Measurement and Evidence/Uncertainty Taxonomy — Risk, Ambiguity, Ignorance and Model Error]] · Module: [[78 Phase 01 Institutional Fundamental Foundations Canon/00 Phase 01 Institutional Fundamental Foundations Canon MOC]]
