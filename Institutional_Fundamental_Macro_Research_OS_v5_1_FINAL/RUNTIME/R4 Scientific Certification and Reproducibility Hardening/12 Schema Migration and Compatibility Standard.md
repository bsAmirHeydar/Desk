# Schema Migration and Compatibility Standard

R4 requires forward runtime compatibility across R1→R4.

Older component self-tests must accept a certified downstream runtime when their own contracts remain active. Runtime version equality is not used to falsely mark inherited components as absent.

Schema migration rules:
- additive/idempotent migrations are permitted;
- silent destructive column reinterpretation is forbidden;
- scientific schemas remain authoritative over runtime convenience schemas;
- a schema-version change that alters scientific meaning requires a new scientific/runtime version and re-certification;
- catalog initialization may be repeated without data loss.
