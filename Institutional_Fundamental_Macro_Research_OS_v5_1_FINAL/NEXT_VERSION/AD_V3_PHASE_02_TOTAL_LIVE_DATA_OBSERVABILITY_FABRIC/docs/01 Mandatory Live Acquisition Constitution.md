# Mandatory Live Acquisition Constitution

1. Every applicable P01 fact has exactly one acquisition contract.
2. Every applicable public fact marked mandatory must be attempted before analysis admission.
3. Shared sources are fetched once per run and fan out to fact extractors.
4. A successful HTTP response is not a successful fact observation unless the fact parser/evidence test succeeds.
5. `FETCH_FAILED`, `PARSE_FAILED`, `PAID_ONLY`, and `PRIVATE_UNOBSERVABLE` never become neutral facts.
6. P02 never changes Direction and never grants BUY/SELL.
