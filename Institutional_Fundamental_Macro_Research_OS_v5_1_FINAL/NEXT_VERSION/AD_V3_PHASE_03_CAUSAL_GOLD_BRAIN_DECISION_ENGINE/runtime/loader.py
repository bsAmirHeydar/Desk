from __future__ import annotations
import json
from pathlib import Path
from .common import load_json

def latest_receipt(data_root):
    ps=sorted((Path(data_root)/'receipts').glob('*.json'),key=lambda p:p.stat().st_mtime)
    if not ps: raise FileNotFoundError('NO_P02_COVERAGE_RECEIPT')
    return load_json(ps[-1])

def observation_history(data_root, cutoff=None):
    p=Path(data_root)/'observations'/'gold_fact_observations.jsonl'
    if not p.exists(): raise FileNotFoundError('NO_P02_OBSERVATION_LOG')
    by={}
    for line in p.read_text(encoding='utf-8-sig').splitlines():
        if not line.strip(): continue
        o=json.loads(line)
        if cutoff and str(o.get('retrieved_at',''))>str(cutoff): continue
        by.setdefault(o['fact_id'],[]).append(o)
    for fid,rows in by.items(): rows.sort(key=lambda x:(x.get('retrieved_at') or '',x.get('revision_number') or 0))
    return by

def current_previous(history):
    out={}
    for fid,rows in history.items(): out[fid]={'current':rows[-1], 'previous':rows[-2] if len(rows)>1 else None}
    return out

def _economic_marker(obs):
    if not obs:
        return None
    for key in ('reference_period','event_time','published_at'):
        val=obs.get(key)
        if val not in (None,''):
            return {'kind':key,'value':str(val)}
    return None

def _previous_economic_observation(rows, cur, excluded_run_id=None):
    if cur is None:
        return None, 'NO_CURRENT_OBSERVATION'
    marker=_economic_marker(cur)
    if marker is None:
        return None, 'NO_CURRENT_ECONOMIC_MARKER'
    candidates=[]
    for r in rows:
        if r is cur:
            continue
        if excluded_run_id and r.get('acquisition_run_id')==excluded_run_id:
            continue
        if (r.get('retrieved_at') or '') > (cur.get('retrieved_at') or ''):
            continue
        rm=_economic_marker(r)
        if rm is None:
            continue
        if rm!=marker:
            candidates.append(r)
    if not candidates:
        return None, 'NO_DISTINCT_ECONOMIC_ANCHOR'
    candidates.sort(key=lambda x:(x.get('retrieved_at') or '',x.get('revision_number') or 0))
    return candidates[-1], 'DISTINCT_ECONOMIC_ANCHOR_AVAILABLE'

def current_previous_for_receipt(history, coverage):
    """Bind P03 to the exact P02 acquisition run when available.

    `previous` intentionally remains the previous fetch/run for no-refire
    semantics and backwards compatibility. REV 3.3.6 additionally exposes
    `previous_economic`, the most recent earlier observation with a distinct
    explicit economic/source clock.
    """
    run_id=coverage.get('acquisition_run_id')
    cutoff=coverage.get('observation_cutoff_utc') or coverage.get('acquisition_completed_at_utc') or coverage.get('generated_at_utc')
    out={}
    if run_id:
        for fid,rows in history.items():
            current=[r for r in rows if r.get('acquisition_run_id')==run_id]
            cur=current[-1] if current else None
            prevs=[r for r in rows if r.get('acquisition_run_id')!=run_id and (not cur or (r.get('retrieved_at') or '') <= (cur.get('retrieved_at') or ''))]
            prev_fetch=prevs[-1] if prevs else None
            prev_econ,econ_status=_previous_economic_observation(rows,cur,run_id)
            out[fid]={
                'current':cur,
                'previous':prev_fetch,
                'previous_fetch':prev_fetch,
                'previous_economic':prev_econ,
                'economic_anchor_status':econ_status
            }
        return out, {'exact_run_bound':True,'acquisition_run_id':run_id,'cutoff_utc':cutoff}
    for fid,rows in history.items():
        eligible=[r for r in rows if not cutoff or (r.get('retrieved_at') or '')<=cutoff]
        cur=eligible[-1] if eligible else None
        prev_fetch=eligible[-2] if len(eligible)>1 else None
        prev_econ,econ_status=_previous_economic_observation(eligible,cur,None)
        out[fid]={
            'current':cur,
            'previous':prev_fetch,
            'previous_fetch':prev_fetch,
            'previous_economic':prev_econ,
            'economic_anchor_status':econ_status
        }
    return out, {'exact_run_bound':False,'acquisition_run_id':None,'cutoff_utc':cutoff}

def load_bundle(path):
    if not path: return {'record_type':'AD_V3_P03_SEMANTIC_ADJUDICATION_BUNDLE','subject':'XAUUSD','items':[]}
    return load_json(path)
