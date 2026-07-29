---
title: "06 Yield Curve and Policy Pricing Service"
type: platform-specification
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [data-platform, research-engineering]
---
# 06 Yield Curve and Policy Pricing Service

## Purpose

Construct nominal, real, OIS, forward and meeting-dated curves.

## Components

Instrument cash-flow library; bootstrapping; interpolation; uncertainty; historical specifications.

## Interfaces

The service publishes versioned schemas, lineage events, quality states, ownership metadata and machine-readable contracts. Upstream and downstream dependencies are explicit.

## Acceptance gate

Curves price inputs within tolerance and expose model disagreement.

## Operational risks

Address licensing, timestamp ambiguity, delayed delivery, schema drift, partial outages, duplicate records, unit changes, security and silent fallback.
