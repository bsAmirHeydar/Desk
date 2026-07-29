---
title: "12 Anti-Boilerplate and Knowledge Density Standard"
type: core-standard
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [anti-boilerplate, editorial, knowledge-density]
---
# 12 Anti-Boilerplate and Knowledge Density Standard

## Problem definition

Repeated institutional-sounding language creates the appearance of depth while lowering retrieval quality, auditability and learning value. Shared doctrine belongs in central standards; subject notes must contain subject-specific knowledge.

## Prohibited duplication

A domain note must not repeat generic paragraphs on evidence, horizons, governance, implementation or model cards when a canonical standard exists. It should link to the standard and document only what is unique to the domain.

## Required subject density

A substantive note must contain a material share of the following:

- definitions unique to the topic;
- variable and unit tables;
- accounting identities or model equations;
- source-specific data fields;
- transformations and estimation details;
- institutional mechanics;
- historical examples;
- rival models and discriminating evidence;
- failure modes unique to the topic;
- implementation artifacts and acceptance tests.

## Duplication metrics

The validation pipeline must report:

- exact duplicate paragraphs;
- normalized duplicate paragraphs;
- paragraphs appearing in more than 20 notes;
- paragraphs appearing in more than 100 notes;
- near-duplicate documents by similarity;
- repeated equations without topic-specific interpretation.

## Editorial gates

A note fails editorial review when:

- replacing the title with another topic leaves most of the note valid;
- domain-specific variables are absent;
- source routes are generic or contaminated;
- the note contains instructions to build a model but no specification of inputs, outputs and tests;
- examples are hypothetical when historical evidence is available;
- the note adds no information beyond its parent MOC.

## Compression rule

When multiple notes share doctrine, move the doctrine to a core standard and preserve concise links. Deleting repeated prose is an improvement when it raises information density and retrieval precision.
