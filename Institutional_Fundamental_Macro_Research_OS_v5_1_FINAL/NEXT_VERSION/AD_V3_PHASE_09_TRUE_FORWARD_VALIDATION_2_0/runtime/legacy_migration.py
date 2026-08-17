from __future__ import annotations
from pathlib import Path
import json
from .common import P04

def audit_legacy(p04_root=None):
    p4=Path(p04_root) if p04_root else P04; outp=p4/'artifacts'/'commissioning'/'outcomes.jsonl'; rows=[]
    if outp.exists():
        for line in outp.read_text(encoding='utf-8-sig').splitlines():
            if line.strip():
                try:rows.append(json.loads(line))
                except Exception:pass
    c={'P09_COMPATIBLE':0,'P09_INCOMPATIBLE':0,'UNKNOWN_COMPATIBILITY':0,'LEGACY_ONLY':0}; details=[]
    for o in rows:
        ok=all(o.get(k) is not None for k in ('precommit_id','direction_candidate','anchor','outcome_anchor')) and bool(o.get('horizon')) and bool(o.get('maturity_time'))
        cls='P09_COMPATIBLE' if ok else 'P09_INCOMPATIBLE';c[cls]+=1;details.append({'legacy_outcome_id':o.get('outcome_id'),'classification':cls,'reason':'FULL_P09_TIMING_METADATA_PRESENT' if ok else 'MISSING_FIXED_HORIZON_OR_MATURITY_METADATA'})
    return {'record_type':'AD_V3_P09_LEGACY_MIGRATION_RECEIPT','legacy_sample_count':len(rows),'counts':c,'details':details,'legacy_samples_grant_p09_maturity':False}
