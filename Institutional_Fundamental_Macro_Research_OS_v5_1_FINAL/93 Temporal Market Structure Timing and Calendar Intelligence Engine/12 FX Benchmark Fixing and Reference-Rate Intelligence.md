---
title: "12 FX Benchmark Fixing and Reference-Rate Intelligence"
type: canonical-methodology
status: canonical
version: 15.0.0
created: 2026-08-08
updated: 2026-08-08
language: en
---
# FX Benchmark Fixing and Reference-Rate Intelligence

Model transactional FX benchmarks separately from information-only reference rates. WMR 4pm London is a benchmark execution clock; ECB reference rates are not treated as equivalent transactional fixes.

Track benchmark time, London DST, month/quarter-end overlap, known/reasonably modelled hedge/rebalance flow, confidence and post-fix decay.

Never infer fix direction from price behavior. Directional benchmark-flow estimates require documented benchmark obligations, actual rebalance/hedge model or explicit high-quality proxy.
