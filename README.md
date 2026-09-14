# Desk — Fundamental Alpha Lab

**AI-augmented fundamental research workspace for structured evidence gathering, market analysis, and repeatable investment-research workflows.**

Desk is designed to turn a broad market or asset request into a structured research process rather than a loose sequence of prompts.

The goal is to make fundamental research more **repeatable, reviewable, and evidence-led** by separating:

- the research question;
- evidence retrieval;
- method routing;
- analytical perspective;
- report generation;
- and the distinction between evidence, inference, and judgment.

## Why This Exists

A large language model can generate fluent analysis very quickly. The difficult part is not producing text; it is controlling the research process:

- What evidence should be retrieved?
- Which assumptions are being made?
- Which analytical method fits the question?
- What is fact versus inference?
- How should conflicting evidence be handled?
- Can the process be repeated for another market without rebuilding the workflow manually?

Desk is an attempt to turn those questions into a reusable research system.

## Research Workflow

A canonical run compiles a simple request into a structured workflow that can include:

1. live evidence retrieval;
2. semantic request compilation;
3. method routing;
4. scientific execution logic;
5. an independent analytical perspective layer;
6. a structured final report.

The project is intended as a **research workspace**, not as an autonomous investment-decision engine. Final interpretation and capital decisions remain human responsibilities.

## Example

### Chat usage

Upload the complete Vault and type:

```text
run NASDAQ100
```

That command activates the canonical Chat-Native Run Contract defined in `RUN.md`.

You do not need to manually specify prompts, clusters, mode, horizon, depth, or report format for the standard workflow.

## Local Runtime Equivalent

```powershell
.\AlphaLab.ps1 run NASDAQ100
```

Advanced research remains available through:

```powershell
.\AlphaLab.ps1 research ...
```

Commissioning / TF / scheduler operations remain under:

```powershell
.\AlphaLab_Commission.ps1
```

## Portfolio Context

This repository is part of my broader work in investment research, systematic decision architecture, and AI-augmented research tooling.

For systematic trading research and strategy validation, see [Decision Alpha Lab](https://github.com/bsAmirHeydar/decision-alpha-lab).

## Status

Active research-tooling project.

## Disclaimer

This project is for research and analytical workflow development. It is not financial advice and does not provide autonomous capital-allocation authority.
