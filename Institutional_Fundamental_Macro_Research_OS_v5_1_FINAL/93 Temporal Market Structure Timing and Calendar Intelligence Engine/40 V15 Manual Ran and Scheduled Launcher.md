---
title: "40 V15 Manual Ran and Scheduled Launcher"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
---
# V15 Manual Ran and Scheduled Launcher

Commands `ران`, `ران تست`, `ران تست رو اجرا کن` invoke the V15 Full-Vault Timing-Integrated Production Prompt at maximum depth. The one canonical hourly scheduled workflow uses the same prompt.

Every run rebuilds the temporal clock graph from current official schedules/methodology rather than carrying stale timing state.

Hourly platform scheduling does not guarantee an exact run at each sub-hour event; V15 still sets event-specific `valid_until` and `next_review`, while exact external triggers require separately supported infrastructure.
