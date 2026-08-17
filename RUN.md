# ALPHA DESK — CANONICAL RUN CONTRACT

## Current active scope: Gold only

For this Alpha Desk project, the human command:

```text
Run
```

means exactly:

```text
Run Gold
```

`Gold` and `XAUUSD` are accepted Gold aliases. Other markets are not part of the current active Alpha Desk scope unless explicitly re-enabled by a future version.

## Local certified route

```powershell
.\AlphaDesk.ps1 run Gold
```

Routing is fail-closed:

- if V3 promotion state is `PRODUCTION_V3`, `run Gold` routes to V3;
- otherwise `run Gold` routes to the retained **V2 fallback / certified baseline**.

V3 is currently **SHADOW_COMMISSIONING**, so P05 does not claim or perform V3 production promotion.

## V3 shadow commissioning

```powershell
.\AlphaDesk.ps1 commission Gold
```

This explicitly addresses the V3 shadow pipeline. It is not a production-promotion command.

## Integrity status

```powershell
.\AlphaDesk.ps1 v3-integrity-status
```

This is offline/deterministic and does not acquire live data or alter promotion/true-forward state.

## Scientific invariants

No lookahead; no fake precision; UNKNOWN remains UNKNOWN; Pressure ≠ Price; Stock ≠ Impulse; Gross Activity ≠ Signed Flow; Previous Fetch ≠ Previous Economic State; Direction ≠ Edge ≠ Permission; automatic promotion is forbidden; broker execution authority remains NONE.

P10 will later own the final unified one-run production runtime. P05 only makes the command contract unambiguous.
