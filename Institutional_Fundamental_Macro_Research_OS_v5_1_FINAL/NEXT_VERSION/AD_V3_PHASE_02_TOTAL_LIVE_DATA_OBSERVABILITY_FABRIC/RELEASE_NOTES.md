
## Revision 3.2.3 - Official API and Free Fallback Hardening

- Replaces the first real-run BLS 403 paths with one official BLS Public Data API POST batch for CPI, core CPI, PPI, payrolls, unemployment, wages and JOLTS.
- Uses dedicated Federal Reserve H.10 daily pages for Broad, AFE and EME dollar indexes.
- Uses FRED public CSV as an explicit official-republisher proxy for Census retail sales when Census HTML blocks automated retrieval.
- Derives 5y5y forward inflation from Treasury breakeven observations instead of depending on a fragile FRED web page.
- Adds CME-hosted delayed Gold/Fed-funds JSON acquisition plus official CME Daily Bulletin PDF fallbacks; no licensed-real-time claim is made.
- Adds TLS-safe official-government / industry-proxy fallbacks for PBoC policy and SGE withdrawals while preserving PUBLIC_PROXY semantics.
- Adds official RBI USDINR extraction as a PUBLIC_PROXY input for India affordability; it is not treated as the full affordability state.
- Adds request-method/header/body-aware source contracts and dedup signatures, allowing deterministic POST acquisition without embedded credentials.
- Keeps Coverage fail-closed: fallbacks improve observability but never downgrade a failed Direct fact into a falsely observed Direct fact.

# AD-V3-P02 Release Notes

Adds mandatory live-data and observability fabric for the complete P01 Gold fact universe. Remains shadow-only and does not alter V2 production authority.

## Revision 3.2.2 - Live Network Adapter Hardening
- Fixes executor/PublicHttpClient contract mismatch discovered by the first real-machine live acquisition.
- Executor now calls `fetch(source_id, url)` and consumes the canonical FetchResult fields: `status`, `http_status`, `retrieved_at`, and `elapsed_ms`.
- Network worker exceptions are converted into explicit `FETCH_FAILED` source attempts so the coverage gate can fail closed instead of terminating with an uncaught traceback.
- Deterministic acceptance now includes a network-adapter contract smoke test and a worker-exception containment test.
- No Direction or trade-permission authority is introduced.


## REV 3.2.4
Closes the final three blockers observed in the first VPN live run with direct Census retail, Fed H.10 INR, and proxy-disciplined current India duty policy evidence. Fail-closed coverage rules are unchanged.
