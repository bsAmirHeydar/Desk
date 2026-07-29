---
title: "09 Positioning and Flow Data Pipeline"
type: platform-specification
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [data-platform, research-engineering]
---
# 09 Positioning and Flow Data Pipeline

## Purpose

Store observed positions and explicitly modeled exposures for funds, ETFs, dealers and systematic strategies.

## Components

Observed/proxy flags; mandate metadata; uncertainty fields; rebalance calendar.

## Interfaces

The service publishes versioned schemas, lineage events, quality states, ownership metadata and machine-readable contracts. Upstream and downstream dependencies are explicit.

## Acceptance gate

Estimated exposures are never confused with reported observations.

## Operational risks

Address licensing, timestamp ambiguity, delayed delivery, schema drift, partial outages, duplicate records, unit changes, security and silent fallback.
