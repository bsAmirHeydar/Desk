---
title: "Phase 01 Formula and Identity Atlas"
type: reference
status: canonical
version: 6.2.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [fundamental-foundations, phase-01, formula-atlas]
---
# Phase 01 Formula and Identity Atlas

> [!abstract] Purpose
> Collect the minimum formal language used across the Foundations Canon. Every formula must be accompanied by definitions, units, assumptions, identification status and failure conditions in its full monograph.

| Formula | Expression | Institutional use |
|---|---|---|
| **Conditional probability** | $$P(A\mid B)=P(A\cap B)/P(B)$$ | Probability after restricting the reference set to B. |
| **Bayes theorem** | $$P(H\mid D)\propto P(D\mid H)P(H)$$ | Update prior beliefs with evidence likelihood. |
| **Total probability** | $$P(A)=\sum_iP(A\mid R_i)P(R_i)$$ | Combine mutually exclusive regime outcomes. |
| **Expected value** | $$\mathbb E[X]=\sum_xxP(X=x)$$ | Probability-weighted average, insufficient alone under tails or constraints. |
| **Variance** | $$Var(X)=\mathbb E[(X-\mu)^2]$$ | Second-moment dispersion. |
| **Covariance** | $$Cov(X,Y)=\mathbb E[(X-\mu_X)(Y-\mu_Y)]$$ | Joint linear variation. |
| **Correlation** | $$\rho_{XY}=Cov(X,Y)/(\sigma_X\sigma_Y)$$ | Standardized linear dependence. |
| **Brier score** | $$BS=(p-y)^2$$ | Proper score for binary probability forecasts. |
| **Log score** | $$LS=-\log p(y)$$ | Strongly penalizes assigning low probability to realized outcomes. |
| **Bayes factor** | $$BF_{10}=p(D\mid M_1)/p(D\mid M_0)$$ | Relative evidence for two models. |
| **Present value** | $$P_t=\mathbb E_t[\sum_jM_{t,t+j}CF_{t+j}]$$ | Expected payoffs discounted by state prices. |
| **Simple growth** | $$g_t=(x_t-x_{t-1})/x_{t-1}$$ | Relative change from the prior level. |
| **Log growth** | $$\Delta\ln x_t\approx g_t$$ | Additive approximation for small changes. |
| **Compounding** | $$X_T=X_0\prod_t(1+r_t)$$ | Cumulative multiplicative change. |
| **First-order dynamics** | $$x_{t+1}=a+\rho x_t+\varepsilon_{t+1}$$ | Persistence and mean reversion benchmark. |
| **Half-life** | $$HL=\ln(0.5)/\ln|\rho|$$ | Shock-decay benchmark for a stable AR(1). |
| **State-space transition** | $$x_t=Fx_{t-1}+Gu_t+w_t$$ | Latent-state law of motion. |
| **Measurement equation** | $$y_t=Hx_t+v_t$$ | Noisy observations of latent state. |
| **Linear system** | $$\mathbf y=\mathbf A\mathbf x+\varepsilon$$ | Matrix mapping from drivers to outcomes. |
| **Network propagation** | $$\mathbf l=(I-A)^{-1}\mathbf s$$ | Linear propagation under stability. |
| **Potential outcome effect** | $$\tau_i=Y_i(1)-Y_i(0)$$ | Unit-level causal contrast, only one side observed. |
| **Average treatment effect** | $$ATE=\mathbb E[Y(1)-Y(0)]$$ | Population-average causal estimand. |
| **Instrumental-variable ratio** | $$\beta_{IV}=Cov(Z,Y)/Cov(Z,X)$$ | Simple IV estimand under relevance and exclusion. |
| **Difference in differences** | $$\delta=(\bar Y_{T,post}-\bar Y_{T,pre})-(\bar Y_{C,post}-\bar Y_{C,pre})$$ | Treatment effect under parallel-trend assumptions. |
| **Expected utility** | $$a^*=\arg\max_a\sum_sp_sU(W(a,s))$$ | Mandate-dependent choice under uncertainty. |
| **Value of perfect information** | $$EVPI=\mathbb E[\max_aU(a,\theta)]-\max_a\mathbb E[U(a,\theta)]$$ | Upper bound on resolving uncertainty. |
| **Minimax regret** | $$a^*=\arg\min_a\max_P[V^*(P)-V(a,P)]$$ | Robust choice across plausible models. |
| **Lagrangian** | $$\mathcal L=f(x)+\lambda[g(x)-c]$$ | Constrained optimization and shadow value. |
| **Debt dynamics** | $$b_t=((1+r_t)/(1+g_t))b_{t-1}-pb_t+valuation_t$$ | Debt-ratio law of motion. |
| **Return decomposition** | $$R\approx Carry+CashFlowNews+ValuationChange+RiskPremiumChange+Residual$$ | Fundamental payoff decomposition. |
| **Relative research-pricing gap** | $$Gap_{A,B}=(Research_A-Priced_A)-(Research_B-Priced_B)$$ | Relative conclusion after aligning objects and horizons. |
| **Scenario expected value** | $$\mathbb E[V]=\sum_sp_sV_s$$ | Probability-weighted scenario value. |
| **Expected shortfall** | $$ES_\alpha=\mathbb E[L\mid L\ge VaR_\alpha]$$ | Average loss in the selected tail. |
| **Transition matrix** | $$P_{ij}=Pr(S_{t+1}=j\mid S_t=i)$$ | Regime transition probabilities. |
| **Admissible historical information** | $$x_i\in\mathcal I_T\iff PublicationTime_i\le T$$ | Point-in-time cutoff rule. |

## Formula governance

- An equation is not evidence.
- An identity is not a causal model.
- A parameter estimate is not invariant across regimes unless tested.
- Approximation error, units and timing must be disclosed.
- A formula without variable definitions and domain restrictions does not satisfy the canon.

## Related canon

- [[78 Phase 01 Institutional Fundamental Foundations Canon/04 Probability Bayesian Forecasting and Decision/00 MOC]]
- [[78 Phase 01 Institutional Fundamental Foundations Canon/03 Causality Identification and Information/00 MOC]]
- [[78 Phase 01 Institutional Fundamental Foundations Canon/06 Multihorizon Synthesis and Institutional Conclusions/00 MOC]]
