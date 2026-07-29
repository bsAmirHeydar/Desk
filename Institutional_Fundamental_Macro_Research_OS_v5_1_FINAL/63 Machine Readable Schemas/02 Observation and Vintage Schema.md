---
title: "02 Observation and Vintage Schema"
type: schema
status: evergreen
version: 5.0.0
created: 2026-07-29
updated: 2026-07-29
language: en
tags:
  - schema
  - machine-readable
  - research-governance
---
# 02 Observation and Vintage Schema

```yaml
schema_version: 5.0.0
observation_id: string
entity: string
series_id: string
valid_time: datetime
source_publication_time: datetime
ingestion_time: datetime
system_time_start: datetime
system_time_end: datetime|null
vintage_id: string
value: number|string|null
unit: string
frequency: string
seasonal_adjustment: string
status: [first_release, revised, benchmark_revised, corrected]
source_key: string
source_location: string
raw_artifact_hash: string
parser_version: string
quality_flags: [string]
```

The pair `(observation_id, vintage_id)` is immutable. A correction creates a new row. Queries accept an `as_of` system time and return the latest admissible vintage.
