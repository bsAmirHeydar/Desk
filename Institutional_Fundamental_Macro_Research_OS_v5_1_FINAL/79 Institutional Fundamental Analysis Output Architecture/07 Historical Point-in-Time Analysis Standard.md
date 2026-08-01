---
title: "07 Historical Point-in-Time Analysis Standard"
type: institutional-standard
status: canonical
version: 10.4.0
created: 2026-07-29
updated: 2026-08-01
language: en
tags: [institutional-analysis, fundamental-only, point-in-time, hybrid-state]
---
# Historical Point-in-Time Analysis Standard

## Objective

Reconstruct what a disciplined desk could have known at each historical cutoff with sufficient daily and intraday observation density to support fundamental backtesting.

## Hybrid requirement

Apply [[88 Hybrid Daily Session Event Fundamental State Engine/01 Architecture and Horizon Separation]], mandatory records, session handoffs, event micro-windows, state decay and density validation. A sparse event map is not a complete historical reconstruction.

## Hard separation

### Ex-ante layer

- information published by cutoff;
- contemporaneous vintages, consensus and pricing;
- known institutional rules;
- uncertainty that existed then;
- mandatory no-change and decay reassessments.

### Ex-post layer

- later revisions and outcomes;
- retrospective attribution and counterfactuals.

Ex-post information may audit but never contaminate ex-ante records.

## Required outputs

- frozen information-set manifest;
- initial state and daily baselines;
- session and event records;
- state-decay ledger;
- cross-asset causal-leader matrix;
- density and gap validation;
- missing archives and confidence ceiling;
- optional separate ex-post audit.
