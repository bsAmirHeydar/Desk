---
title: "16 Pseudo-Real-Time Backtest Engine"
type: platform-specification
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [data-platform, research-engineering]
---
# 16 Pseudo-Real-Time Backtest Engine

## Purpose

Replay historical decisions using only admissible data and model versions.

## Components

Cutoff scheduler; vintage queries; event labels; cost and latency model.

## Interfaces

The service publishes versioned schemas, lineage events, quality states, ownership metadata and machine-readable contracts. Upstream and downstream dependencies are explicit.

## Acceptance gate

Replays match archived snapshots and prohibit outcome leakage.

## Operational risks

Address licensing, timestamp ambiguity, delayed delivery, schema drift, partial outages, duplicate records, unit changes, security and silent fallback.
