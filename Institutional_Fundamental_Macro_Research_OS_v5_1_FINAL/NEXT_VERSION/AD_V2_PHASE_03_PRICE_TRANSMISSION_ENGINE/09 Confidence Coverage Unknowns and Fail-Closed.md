---
title: "Transmission Confidence Coverage Unknowns and Fail-Closed"
type: scientific-contract
status: shadow-development
---
# Confidence and Unknowns

P03 confidence is separate from Pressure confidence.

Transmission confidence depends on:

- target-response data quality;
- expected-signature provenance;
- unit integrity;
- timing integrity;
- pathway coverage;
- timestamp alignment;
- observed-window completeness.

A high-confidence P02 Pressure state can coexist with low-confidence P03 Transmission if price or pathway data are poor.

## Fail-closed conditions

P03 fails closed when:

- P02 Pressure integrity does not pass;
- Pressure fingerprint does not match the frozen signature;
- horizon differs;
- expected signature was declared after response observation began;
- target instrument differs;
- expected and actual units differ;
- an empirical signature lacks validation reference;
- forbidden post-hoc methods are used.

Missing optional pathway data does not automatically hard-fail; it degrades pathway coverage and confidence.
