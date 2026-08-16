# 08 — Scope, Rollback and Non-Promotion

P01 is a shadow-only foundation. It must not:

- modify `AlphaDesk.ps1`;
- alter V2 run/Control Room behavior;
- fetch live data;
- calculate V3 Direction;
- grant BUY/SELL permission;
- broker/exchange orders;
- promote V3 to production.

Rollback is deletion of the P01 phase directory only. Since V2 hashes are frozen, rollback does not require restoring V2 files when P01 is correctly installed.
