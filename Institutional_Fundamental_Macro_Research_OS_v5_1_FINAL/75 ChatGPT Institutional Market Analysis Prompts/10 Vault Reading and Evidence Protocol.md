---
title: "Vault Reading and Evidence Protocol"
type: protocol
status: evergreen
version: 5.1.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - prompts
  - vault-reading
  - evidence
---
# Vault Reading and Evidence Protocol

## Required behavior after the ZIP is uploaded

1. Inspect the archive and identify the Vault root rather than assuming a filename or directory layout.
2. Read `00 HOME.md`, `01 COVERAGE MATRIX.md`, the relevant MOCs, core standards and the market-specific driver books before forming a conclusion.
3. Search the Vault semantically and by keywords for the requested market, its causal drivers, horizon, country, event and execution context.
4. Do **not** summarize the entire Vault. Build a focused research route and state which notes materially shaped the analysis.
5. Treat the Vault as methodology, ontology, model library and control framework. Treat live or historical external evidence as the factual input.
6. Resolve contradictions by using [[00 Core Standards/04 Multihorizon Inheritance and Conflict Resolution]] and [[73 Economic Schools Competing Models and Adversarial Synthesis/00 Economic Schools Competing Models and Adversarial Synthesis MOC]].
7. Preserve the boundary between fundamental permission and technical execution.

## CURRENT evidence protocol

- Browse the web because the answer depends on current information.
- Establish an exact timestamp and timezone.
- Prefer primary and official sources: central banks, statistical agencies, treasuries, exchanges, regulators, issuer filings and official industry agencies.
- Use reputable market sources for consensus, positioning or contemporaneous interpretation when primary sources do not provide them.
- Distinguish observation time, reference period, release time, retrieval time and revision vintage.
- Verify current officeholders, policy settings, schedules, contract specifications and market status rather than relying on memory.
- Cite factual statements inline.
- If live price, consensus or positioning data is unavailable, label it `UNKNOWN` or `ESTIMATE`; never invent it.

## HISTORICAL evidence protocol

- Freeze the information set at the user’s exact cutoff.
- Search for documents, releases and market information published **at or before** that cutoff.
- Use first-release/vintage data where possible; later revisions are excluded from the reconstructed decision state.
- Record publication timestamps and timezone when event sequencing matters.
- Do not use later outcomes to choose the narrative, variables or weights.
- If a later source is the only surviving archive of an earlier document, it may be used only to recover contemporaneous content; mark the archival status and prevent later interpretation from leaking into the analysis.
- Separate `RECONSTRUCTED POINT-IN-TIME VIEW` from any optional `EX-POST AUDIT`.
- If consensus history, intraday pricing or first-release values cannot be recovered, state the gap and lower confidence.

## Source priority

1. Official release or filing.
2. Official methodology or historical archive.
3. Exchange, regulator or recognized market infrastructure.
4. Reputable institutional research or data provider.
5. High-quality contemporaneous financial reporting.
6. Secondary commentary, only when clearly labeled.

A lower-priority source may not override a higher-priority source without explaining the conflict.
