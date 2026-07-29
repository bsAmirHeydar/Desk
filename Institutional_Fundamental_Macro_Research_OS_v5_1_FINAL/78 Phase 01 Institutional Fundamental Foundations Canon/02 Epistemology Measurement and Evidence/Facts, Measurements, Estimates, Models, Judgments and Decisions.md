---
title: "Facts, Measurements, Estimates, Models, Judgments and Decisions"
type: monograph
status: canonical
version: 6.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [fundamental-foundations, phase-01, epistemology]
---

# Facts, Measurements, Estimates, Models, Judgments and Decisions

> [!abstract] Canonical thesis
> Institutional research must label the epistemic type of every statement. Observations, constructed measurements, estimates, model outputs, judgments and decisions have different error structures and cannot be presented as one undifferentiated “fact.”

## Beginner intuition

A statistical agency reports a price index. That index is constructed from samples and methods. An economist estimates trend inflation from it. A committee judges whether inflation is persistent. A portfolio manager decides how much risk to hold. Each step adds assumptions.

## Institutional definitions and distinctions

| Term or distinction | Precise meaning |
|---|---|
| Observation | A recorded datum or event, conditional on source, timestamp and collection process. |
| Constructed measurement | A statistic created through sampling, weighting, adjustment, classification and aggregation. |
| Estimate | An inferred value for an unobserved quantity, with model and sampling uncertainty. |
| Model output | A result conditional on equations, parameters, priors and data transformations. |
| Judgment | A reasoned synthesis that may include qualitative institutional knowledge. |
| Decision | An action or conclusion chosen under objectives, constraints and uncertainty. |

## Mechanism map

1. Assign an epistemic label to each claim.
2. Attach source and information-time metadata.
3. Record transformations and model dependence.
4. Separate parameter uncertainty, measurement error and structural uncertainty.
5. Identify where judgment enters the chain.
6. Do not promote a decision conclusion back into the evidence layer as a fact.

## Formal structure and notation

### Measurement model

$$
Y_t^{obs}=Y_t^{true}+b_t+\epsilon_t
$$

Observed data can contain systematic bias b and random error epsilon; “official” does not mean error-free or conceptually complete.

### Decision layer

$$
a^*=\arg\max_a \mathbb{E}[U(a,\theta)\mid \mathcal I]-C(a)
$$

A decision depends on beliefs about state theta, utility or mandate U, and implementation cost C. Different mandates can produce different rational decisions from the same evidence.

## Competing interpretations and adversarial synthesis

| View | What it explains | Where it can fail |
|---|---|---|
| Naive realism | Treats published statistics as direct observations of reality. | Ignores construction, revisions and conceptual choices. |
| Radical constructivism | Emphasizes that all measures are model-laden. | Can become unable to rank better and worse measurement. |
| Critical measurement realism | Accepts an underlying reality while auditing how institutions measure it. | Requires detailed metadata and humility. |

## Historical and institutional cases

### Unemployment rate

The rate is official but depends on survey classification, participation and reference period; broader measures can tell a different labor story.

### Potential output

Potential is not observed. Different filters and production functions produce different gaps and can revise history materially.

## Multihorizon interpretation

- **Structural/secular:** identify persistent institutions, stocks or constraints governing **Facts, Measurements, Estimates, Models, Judgments and Decisions**; begin with: Assign an epistemic label to each claim.
- **Cyclical:** determine how the mechanism changes across expansion, slowdown, recession, recovery, inflation and disinflation; interrogate: Attach source and information-time metadata.
- **Tactical/multi-week:** identify which expectation, valuation or policy assumption is vulnerable; test: Record transformations and model dependence.
- **Event/current:** define the new information, contemporaneous expectation and first observable mechanism; verify: Separate parameter uncertainty, measurement error and structural uncertainty.
- Use the full inheritance and conflict standard in [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Horizon Inheritance, Conflict Resolution and Double-Counting Control]].

## Failure modes and red-team tests

- Calling an estimate an observation.
- Reporting a model percentile without model uncertainty.
- Suppressing judgment behind a numerical score.
- Using decision outcomes to validate evidence without accounting for luck.
- Treating all data disagreement as equally informative.

## Worked reasoning protocol

Apply [[78 Phase 01 Institutional Fundamental Foundations Canon/Phase 01 Canonical Research Protocol]] to **Facts, Measurements, Estimates, Models, Judgments and Decisions**. The topic-specific sequence is:

1. Assign an epistemic label to each claim.
2. Attach source and information-time metadata.
3. Record transformations and model dependence.
4. Separate parameter uncertainty, measurement error and structural uncertainty.
5. Identify where judgment enters the chain.
6. Do not promote a decision conclusion back into the evidence layer as a fact.

## Exercises and accreditation questions

1. Label each sentence in a central-bank report by epistemic type.
2. Rewrite a market memo so facts, estimates and judgments are visually separated.
3. Identify where mandate changes a decision despite unchanged beliefs.

## Annotated source canon

- **Karl Popper, The Logic of Scientific Discovery.** Falsifiability, severe testing, and the difference between explanation and immunized narrative.
- **Thomas Kuhn, The Structure of Scientific Revolutions.** Paradigms, normal science, and the institutional persistence of models.
- **Daniel Kahneman, Thinking, Fast and Slow.** Bias, overconfidence, substitution, and judgment under uncertainty.
- **Federal Reserve, BIS, IMF and national statistical manuals.** Primary institutional definitions and measurement conventions relevant to epistemic labeling.
- **Morgenstern, On the Accuracy of Economic Observations.** Classic analysis of error and construction in economic data.
- **National statistical agency quality frameworks.** Accuracy, coherence, relevance, timeliness and revision dimensions.

## Related canon

- [[00 Core Standards/02 Evidence Source Lineage and Claim Types]]
- [[26 Epistemic Control and Decision Science/00 MOC]]

---

Next: [[78 Phase 01 Institutional Fundamental Foundations Canon/02 Epistemology Measurement and Evidence/Measurement Theory for Economic and Financial Concepts]] · Module: [[78 Phase 01 Institutional Fundamental Foundations Canon/00 Phase 01 Institutional Fundamental Foundations Canon MOC]]
