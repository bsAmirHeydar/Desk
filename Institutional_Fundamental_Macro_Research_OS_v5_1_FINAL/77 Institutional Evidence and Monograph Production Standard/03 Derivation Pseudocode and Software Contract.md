---
title: "03 Derivation Pseudocode and Software Contract"
type: institutional-standard
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [institutional-reference]
---

# 03 Derivation Pseudocode and Software Contract

Every quantitative monograph must bridge prose and production software.

## Required layers

- mathematical statement with assumptions;
- symbol and dimension table;
- derivation of the estimand or algorithm;
- language-neutral pseudocode;
- reference implementation;
- optimized production implementation if needed;
- synthetic data generator;
- unit, property and regression tests;
- numerical stability and complexity discussion;
- reproducible example with fixed seed and environment.

## Contract

Inputs, outputs, missing-value behavior, exceptions, tolerances, timezones, units and ordering must be explicit. A notebook screenshot is not an implementation contract. A second environment must reproduce the reference outputs within declared tolerances.
