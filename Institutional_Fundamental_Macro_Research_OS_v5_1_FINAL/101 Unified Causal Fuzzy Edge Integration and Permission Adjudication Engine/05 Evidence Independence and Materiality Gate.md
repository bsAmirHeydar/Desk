# Evidence Independence and Materiality Gate

Every load-bearing D3 modifier must satisfy D1 provenance rules.

## Materiality
- `DECISION_CRITICAL`
- `MATERIAL`
- `SUPPORTING`
- `CONTEXTUAL`

## Independence
Observations sharing one `root_id` count as one causal root. A Fed shock observed in rates, USD and equity futures cannot be represented as three independent confirmations unless the evidence establishes distinct causal roots.

## Unknown handling
- decision-critical unknown → `INSUFFICIENT_EVIDENCE` or `NO_TRADE`;
- material secondary unknown → confidence cap + earlier review;
- contextual unknown → disclose only.
