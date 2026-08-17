# AD-V3-P07 Release Notes

- Replaced the V3 normal commissioning broad synchronous refresh with a horizon-aware P07 planning layer.
- Preserved the complete 192-fact / P02 full-snapshot contract for P03.
- Added Live Kernel, Context Cache and Conditional Escalation scheduling tiers.
- Added economic-time-aware freshness authority and point-in-time-safe context caching.
- Added NORMAL, FULL_REFRESH and CACHE_ONLY modes.
- Preserved direct-DXY provider gap identity and daily/EOD rate authority; no fake intraday provider was added.
- Added separate live/context health and governed P07 coverage for P03.
- Added minimal Data Kernel truthfulness to the P04 model/report.
- No Gold ontology, causal-root, semantic-authority, decision-science, true-forward, promotion or trade-execution authority changes.
- Added a bounded P01 discovery exclusion for the downstream P07 operational phase so runtime/cache/docs named Gold are not misclassified as new scientific authority; P01 fact ontology and scientific constitution are unchanged.
