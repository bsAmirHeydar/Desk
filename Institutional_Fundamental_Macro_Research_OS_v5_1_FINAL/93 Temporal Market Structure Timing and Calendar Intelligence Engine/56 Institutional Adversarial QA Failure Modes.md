---
title: "Institutional Adversarial QA Failure Modes"
type: adversarial-qa-standard
status: canonical
version: 15.1.0
created: 2026-08-08
updated: 2026-08-08
language: en
tags: [timing, qa, model-risk]
---
# Institutional Adversarial QA Failure Modes

V15.1 is rejected if any material case shows an unhandled version of the following:

1. event-exists-therefore-veto shortcut;
2. fixed T-minus threshold treated as universal science;
3. session label treated as direction;
4. month/quarter/year-end given unsourced directional sign;
5. expiry given generic sign or generic product mapping;
6. AM/PM settlement conflation;
7. SOQ/cash-open/expiry double counting;
8. futures roll interpreted directionally without mechanism;
9. CFD clock confused with reference-market clock;
10. holiday in one centre treated as global closure;
11. DST fixed-offset error;
12. trade date/civil date/value date conflation;
13. tentative Treasury schedule treated as final;
14. central-bank event time invented when official time is TBD;
15. revised calendar used as if known earlier in historical review;
16. stale source calendar accepted without refresh;
17. participant-control inference presented as observed fact;
18. price pattern/technical indicator leaks into timing clearance;
19. real-time price/volume used to manufacture timing direction;
20. clock collision resolved by naive additive score;
21. one root mechanism counted multiple times;
22. timing `CLEAR` upgrades `BIAS_ONLY` to Active;
23. hard fundamental/narrative blocker waived by favorable timing;
24. safe execution window shorter than likely exploit time but still cleared;
25. permission TTL survives past known hazard;
26. next required review is earlier than scheduler capability but permission stays valid;
27. transport latency ignored near expiry;
28. missing material clock silently assumed benign;
29. insufficient time-to-exploit sample causes universal no-trade starvation;
30. outcome hindsight used to rewrite prior clock evidence;
31. one missed move promoted directly into a canonical timing rule;
32. over-veto is not measured against a no-timing control.

Every production validator and benchmark suite must cover these classes directly or through equivalent tests.
