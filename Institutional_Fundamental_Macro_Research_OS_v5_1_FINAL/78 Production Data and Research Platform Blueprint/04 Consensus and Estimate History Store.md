---
title: "04 Consensus and Estimate History Store"
type: platform-specification
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [data-platform, research-engineering]
---
# 04 Consensus and Estimate History Store

## Purpose

Preserve individual and aggregate forecasts, company estimates and revision histories.

## Components

Contributor snapshots; distribution statistics; anonymization controls; estimate lineage.

## Interfaces

The service publishes versioned schemas, lineage events, quality states, ownership metadata and machine-readable contracts. Upstream and downstream dependencies are explicit.

## Acceptance gate

Historical consensus is available without survivorship or latest-estimate contamination.

## Operational risks

Address licensing, timestamp ambiguity, delayed delivery, schema drift, partial outages, duplicate records, unit changes, security and silent fallback.
