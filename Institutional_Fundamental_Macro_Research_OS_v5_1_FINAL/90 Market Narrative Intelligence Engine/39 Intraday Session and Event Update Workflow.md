---
title: "Intraday Session and Event Update Workflow"
type: canonical-method
status: canonical
version: 12.0.0
created: 2026-08-06
updated: 2026-08-06
language: en
tags: [v12, market-narrative, daily-intelligence]
---
# Intraday Session and Event Update Workflow

## Incremental update principle

Load the prior immutable daily state. Freeze the new cutoff. Ingest only information that became available after the prior record. Preserve every unchanged field and explain every changed field.

## Change classification

A new observation may change V11 force, persistence, consumption or remaining pressure; V12 attention, validity, dominance, price control or transition risk; or none of them.

## Required update records

Support scheduled event, unscheduled shock, policy clarification, earnings release, causal-leader change, flow hijack, quiet-period decay, narrative displacement and no-material-change records.

## No rewrite rule

Store the first-change timestamp and parent record. Do not update a prior state with knowledge from a later reaction. If the market move reveals a rival model, create a new adjudication record.
