# Append-only V2 persistence

P06 uses a separate namespace under the mutable data root:

`<data_root>/alpha_desk_v2/`

This preserves V1 run memory unchanged.

## Files
- `runs/index.jsonl` — append-only capsule extension index;
- `runs/events.jsonl` — append-only lifecycle events;
- `history/XAUUSD/<horizon>.jsonl` — semantic timeline rows;
- immutable per-run `capsule_extension.json`;
- optional derived `report_model.json` and `explorer.html` beside operator outputs, not as scientific authority.

Historical rows are never rewritten. New schema versions append new records.
