---
title: "Cross-Release Dependency and Retrieval Graph"
type: architecture
status: canonical
version: 7.0.0
release: "Mega Canon v7.0"
created: 2026-07-30
updated: 2026-07-30
language: en
tags: [fundamental-only, retrieval]
---

# Cross-Release Dependency and Retrieval Graph

```mermaid
graph TD
F[Release 01 Foundations] --> M[02 Macro State]
M --> I[03 Inflation Labor Demand]
M --> P[04 Fiscal Monetary]
P --> R[05 Rates Treasury Repo]
R --> C[06 Banking Credit NBFI]
R --> X[07 Dollar FX EM]
M --> E[08 Corporate Equity]
X --> K[09 Commodities]
R --> D[10 Real Digital Derivatives]
C --> G[11 Cross-Asset Geopolitics]
G --> B[12 Country and Historical Atlas]
B --> S[13 Measurement and Synthesis]
S --> A[14 Retrieval and Final Audit]
```

## Retrieval rule

Start with the requested object, then retrieve its direct release, upstream state releases, financing and policy releases, relevant cross-asset release, country context, measurement method and final output contract. Do not retrieve every note indiscriminately.
