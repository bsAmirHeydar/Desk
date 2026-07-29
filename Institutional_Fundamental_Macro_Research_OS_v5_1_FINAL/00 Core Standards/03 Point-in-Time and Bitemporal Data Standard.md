---
title: "03 Point-in-Time and Bitemporal Data Standard"
type: core-standard
status: evergreen
version: 6.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags: [point-in-time, bitemporal, vintages, lookahead]
---
# 03 Point-in-Time and Bitemporal Data Standard

## Objective

Historical research must recreate what the institution could have known at the decision cutoff. The latest database value is not a historical observation; it is the latest vintage of an observation that may have changed repeatedly.

## Required temporal fields

Every observation must preserve at least:

- `valid_time_start`: when the phenomenon applies;
- `valid_time_end`: end of the applicable period, if relevant;
- `publication_time`: official release time;
- `available_to_desk_time`: time the desk could lawfully and operationally access it;
- `ingestion_time`: platform receipt time;
- `system_time_start`: when the record entered the database;
- `system_time_end`: when it was superseded;
- `vintage_id`: immutable vintage identifier;
- `revision_type`: first release, routine revision, benchmark revision, reclassification or correction.

## Admissible historical query

A historical query must answer:

> Return the latest record whose publication and desk-availability timestamps are no later than the decision cutoff, while preserving the value that was valid in the system at that time.

The query must not use present-day constituent membership, adjusted corporate data, revised national accounts or current instrument specifications unless the task is explicitly ex-post.

## Release calendar control

A release calendar must store:

- expected release timestamp and timezone;
- actual publication timestamp;
- reference period;
- release status and delay;
- source document or endpoint;
- embargo or access restrictions;
- revision schedule;
- seasonal-adjustment status;
- holiday and daylight-saving transformations.

## Point-in-time objects beyond macro data

The same standard applies to:

- consensus and analyst estimates;
- company guidance and filings;
- index constituents and weights;
- futures contract specifications and delivery baskets;
- option chains and open interest;
- ratings and credit outlooks;
- sanctions lists and regulations;
- commodity inventory and shipping data;
- central-bank communications;
- news and transcript archives.

## Contamination tests

Research fails if any of the following occur:

1. current data replace first-release data;
2. the timestamp is rounded past the decision cutoff;
3. revised index constituents are used historically;
4. survivorship removes failed issuers or contracts;
5. a document published later is treated as contemporaneous;
6. the outcome is used to select the explanatory variables;
7. data-availability latency is ignored;
8. a licensed feed is assumed available when it was not operationally accessible.

## Required pseudo-real-time replay

For each historical decision, reconstruct:

- the information set;
- the priced baseline;
- the model versions available;
- the desk's data latency;
- the decision state before outcome observation;
- subsequent revisions in a separate ex-post layer.
