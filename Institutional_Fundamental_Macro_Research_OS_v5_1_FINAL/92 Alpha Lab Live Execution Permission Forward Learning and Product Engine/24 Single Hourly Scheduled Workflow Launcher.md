---
title: "Single Hourly Scheduled Workflow Launcher"
type: scheduled-workflow-profile
status: active
version: 14.1.0
---
# Single Hourly Scheduled Workflow Launcher

Use one scheduled workflow only. Run hourly in `Asia/Tehran` using the exact Full-Vault Forward-Learning Production Prompt.

Every invocation re-adjudicates all six markets. Event sensitivity is evaluated inside each run. The scheduled workflow must not silently downgrade to a quick refresh.

If the platform cannot schedule more frequently than hourly, do not claim sub-hourly execution. Exact event-time reactions require a separately supported external trigger/API architecture.

Email stays simple and attachment-free. HTML remains the complete human-facing product in chat.


<!-- ALPHALAB_V15_TIMING_BEGIN -->
The single hourly workflow must rebuild the V15 temporal clock graph from current official calendars/methodologies on every run.
<!-- ALPHALAB_V15_TIMING_END -->

