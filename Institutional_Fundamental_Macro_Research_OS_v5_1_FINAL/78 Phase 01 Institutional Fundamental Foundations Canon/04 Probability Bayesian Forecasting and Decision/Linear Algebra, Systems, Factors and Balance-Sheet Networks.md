---
title: "Linear Algebra, Systems, Factors and Balance-Sheet Networks"
type: monograph
status: canonical
version: 6.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [fundamental-foundations, phase-01, mathematics]
---

# Linear Algebra, Systems, Factors and Balance-Sheet Networks

> [!abstract] Canonical thesis
> Vectors and matrices provide the language for multi-variable states, exposures, accounting systems, factor decompositions and networks. Their usefulness depends on economic interpretation, rank, identification and stable units.

## Analytical intuition

A country, bank or portfolio has many linked quantities at once. A vector lists them; a matrix describes how they relate, transform or transmit shocks.

## Institutional definitions and distinctions

| Term or distinction | Precise meaning |
|---|---|
| Vector | Ordered collection of variables or exposures. |
| Matrix | Array representing transformations, covariances, accounting links or network connections. |
| Rank | Number of independent dimensions represented. |
| Eigenvalue | Scale factor associated with a system direction; relevant to persistence and stability. |
| Factor | Common latent or observed driver explaining co-movement. |

## Mechanism map

1. Define economically meaningful vector components.
2. Standardize units before combining.
3. Use matrices for accounting, covariance, transition or network structure.
4. Check rank and collinearity.
5. Interpret factors through loadings and external evidence.
6. Stress network propagation and feedback.

## Formal structure and notation

### Linear system

$$
\mathbf y=\mathbf A\mathbf x+\boldsymbol\varepsilon
$$

Matrix A maps drivers x to outcomes y under stated approximation.

### Covariance matrix

$$
\Sigma=\mathbb E[(\mathbf x-\boldsymbol\mu)(\mathbf x-\boldsymbol\mu)^\top]
$$

Covariance captures second moments but can be unstable and regime dependent.

### Network propagation

$$
\mathbf l=(\mathbf I-\mathbf A)^{-1}\mathbf s
$$

The inverse maps direct shocks s through interconnected exposures when stability conditions hold.

## Competing interpretations and adversarial synthesis

| View | What it explains | Where it can fail |
|---|---|---|
| Observed factors | Interpretability and direct measurement. | May omit latent common drivers. |
| Statistical factors | Compress high-dimensional information. | Rotation and economic meaning can be ambiguous. |
| Network models | Represent counterparties and propagation. | Exposure data and nonlinear defaults are difficult. |

## Historical and institutional cases

### Input-output shocks

Sector disruptions propagate through production coefficients and substitution constraints.

### Bank network stress

Common assets and interbank claims create indirect losses beyond bilateral exposure.

## Multihorizon interpretation

- **Structural/secular:** identify persistent institutions, stocks or constraints governing **Linear Algebra, Systems, Factors and Balance-Sheet Networks**; begin with: Define economically meaningful vector components.
- **Cyclical:** determine how the mechanism changes across expansion, slowdown, recession, recovery, inflation and disinflation; interrogate: Standardize units before combining.
- **Tactical/multi-week:** identify which expectation, valuation or policy assumption is vulnerable; test: Use matrices for accounting, covariance, transition or network structure.
- **Event/current:** define the new information, contemporaneous expectation and first observable mechanism; verify: Check rank and collinearity.
- Use the full inheritance and conflict standard in [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/Horizon Inheritance, Conflict Resolution and Double-Counting Control]].

## Failure modes and red-team tests

- Combining variables with incompatible units.
- Interpreting principal components as causal factors.
- Ignoring estimation error in covariance matrices.
- Using a linear inverse near instability without nonlinear constraints.
- Treating low rank as proof of one economic driver.

## Worked reasoning protocol

Apply [[78 Phase 01 Institutional Fundamental Foundations Canon/Phase 01 Canonical Research Protocol]] to **Linear Algebra, Systems, Factors and Balance-Sheet Networks**. The topic-specific sequence is:

1. Define economically meaningful vector components.
2. Standardize units before combining.
3. Use matrices for accounting, covariance, transition or network structure.
4. Check rank and collinearity.
5. Interpret factors through loadings and external evidence.
6. Stress network propagation and feedback.

## Adversarial analytical checks and accreditation questions

1. Write a sectoral-balance vector and accounting matrix.
2. Interpret a two-factor loading matrix.
3. Calculate shock propagation in a small network.

## Annotated source canon

- **Strang, Introduction to Linear Algebra.** Core vector and matrix reasoning.
- **Leontief, input-output economics.** Economic network accounting.
- **Network science and systemic-risk literature.** Propagation and centrality.

## Related canon

- [[53 Research Statistics Forecasting and Causal Inference/00 53 Research Statistics Forecasting and Causal Inference MOC]]
- [[32 Private Credit NBFI and Hidden Leverage/00 32 Private Credit NBFI and Hidden Leverage MOC]]

---

Module: [[78 Phase 01 Institutional Fundamental Foundations Canon/00 Phase 01 Institutional Fundamental Foundations Canon MOC]]
