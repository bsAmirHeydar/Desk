---
title: "11 Entity and Instrument Master"
type: platform-specification
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [data-platform, research-engineering]
---
# 11 Entity and Instrument Master

## Purpose

Create canonical, time-varying identities and specifications.

## Components

Legal entities; securities; contracts; exchanges; baskets; corporate actions; aliases.

## Interfaces

The service publishes versioned schemas, lineage events, quality states, ownership metadata and machine-readable contracts. Upstream and downstream dependencies are explicit.

## Acceptance gate

No ambiguous identifiers or future mappings enter historical research.

## Operational risks

Address licensing, timestamp ambiguity, delayed delivery, schema drift, partial outages, duplicate records, unit changes, security and silent fallback.
