#!/usr/bin/env python3
from __future__ import annotations
import datetime, json, pathlib, re

REQUIRED_CANDIDATE_FIELDS = [
    'narrative_id','title','selected_facts','ignored_facts','interpretive_claim','causal_chain',
    'target_assets','active_horizons','attention_state','narrative_validity','narrative_dominance',
    'price_control','flow_control','narrative_persistence','fact_persistence','narrative_saturation',
    'narrative_consumption','remaining_narrative_power','fragility','replacement_risk',
    'observability_tier','confidence','field_level_provenance','next_update_trigger'
]
REQUIRED_MARKET_ROWS={'nasdaq_100','sp500','gold','eurusd'}


def load_json(path):
    return json.loads(pathlib.Path(path).read_text(encoding='utf-8'))

def parse_time(s):
    if not isinstance(s,str): raise ValueError('timestamp must be a string')
    return datetime.datetime.fromisoformat(s.replace('Z','+00:00'))

def state(doc):
    return doc.get('v12_market_intelligence_state') if isinstance(doc,dict) else None

def structural_errors(doc):
    errors=[]; s=state(doc)
    if not isinstance(s,dict): return ['missing v12_market_intelligence_state']
    required=['methodology','inherited_v11_state','fact_universe','attention','narratives','leaders','reflexivity','daily_state','provenance','validation']
    for k in required:
        if k not in s: errors.append(f'missing top-level section {k}')
    m=s.get('methodology',{})
    for k in ['vault_release','schema_version','analysis_timestamp_utc','new_york_timestamp','cutoff_policy','analyst_or_agent','scoring_mode']:
        if k not in m: errors.append(f'missing methodology.{k}')
    if m.get('vault_release')!='12.0.0': errors.append('vault_release must be 12.0.0')
    if m.get('schema_version')!='12.0.0': errors.append('schema_version must be 12.0.0')
    for k in ['direction','force','fact_persistence','consumption','remaining_pressure','reversal_risk','asymmetry']:
        if k not in s.get('inherited_v11_state',{}): errors.append(f'missing inherited_v11_state.{k}')
    for k in ['facts','fact_clusters','ignored_facts']:
        if not isinstance(s.get('fact_universe',{}).get(k),list): errors.append(f'fact_universe.{k} must be a list')
    for k in ['asset_horizon_maps','evidence_ledger']:
        if not isinstance(s.get('attention',{}).get(k),list): errors.append(f'attention.{k} must be a list')
    for k in ['candidates','dominant_by_asset_horizon','strongest_challengers','dormant_narratives','transition_watch']:
        if not isinstance(s.get('narratives',{}).get(k),list): errors.append(f'narratives.{k} must be a list')
    for k in ['causal_leader','attention_leader','price_controller','flow_controller','media_leader']:
        if k not in s.get('leaders',{}): errors.append(f'missing leaders.{k}')
    for k in ['active_feedback_loops','break_conditions']:
        if not isinstance(s.get('reflexivity',{}).get(k),list): errors.append(f'reflexivity.{k} must be a list')
    for k in ['executive_market_map','watchlist','next_update_triggers']:
        if not isinstance(s.get('daily_state',{}).get(k),list): errors.append(f'daily_state.{k} must be a list')
    for k in ['field_level_ledger','unavailable_inputs','confidence_caps']:
        if not isinstance(s.get('provenance',{}).get(k),list): errors.append(f'provenance.{k} must be a list')
    return errors

def separation_errors(doc):
    errors=[]; s=state(doc) or {}
    facts=s.get('fact_universe',{}).get('facts',[])
    fids={x.get('fact_id') for x in facts if isinstance(x,dict)}
    if None in fids: errors.append('every fact requires fact_id')
    nids=set()
    for n in s.get('narratives',{}).get('candidates',[]):
        if not isinstance(n,dict): errors.append('narrative candidate must be object'); continue
        nid=n.get('narrative_id');
        if not nid: errors.append('narrative candidate missing narrative_id')
        if nid in fids: errors.append(f'narrative_id duplicates fact_id: {nid}')
        if nid in nids: errors.append(f'duplicate narrative_id: {nid}')
        nids.add(nid)
        for fld in REQUIRED_CANDIDATE_FIELDS:
            if fld not in n: errors.append(f'{nid or "candidate"} missing {fld}')
        for fid in n.get('selected_facts',[]):
            if fid not in fids: errors.append(f'{nid} references unknown fact {fid}')
        if 'narrative_validity' not in n or 'narrative_dominance' not in n:
            errors.append(f'{nid} must separate validity and dominance')
        if 'fact_persistence' not in n or 'narrative_persistence' not in n:
            errors.append(f'{nid} must separate fact and narrative persistence')
    return errors

def no_hindsight_errors(doc):
    errors=[]; s=state(doc) or {}; m=s.get('methodology',{})
    try: cutoff=parse_time(m.get('analysis_timestamp_utc'))
    except Exception as e: return [f'invalid cutoff: {e}']
    timed=[]
    for f in s.get('fact_universe',{}).get('facts',[]): timed.append(('fact',f.get('fact_id'),f.get('timestamp_utc')))
    for e in s.get('attention',{}).get('evidence_ledger',[]): timed.append(('attention evidence',e.get('evidence_id'),e.get('timestamp_utc')))
    for kind,ident,ts in timed:
        try:
            if parse_time(ts)>cutoff: errors.append(f'{kind} {ident} is after analysis cutoff')
        except Exception as ex: errors.append(f'{kind} {ident} invalid timestamp: {ex}')
    return errors

def attention_provenance_errors(doc):
    errors=[]; s=state(doc) or {}; mode=s.get('methodology',{}).get('scoring_mode')
    for row in s.get('attention',{}).get('asset_horizon_maps',[]):
        if 'attention_share' in row and mode!='EMPIRICALLY_CALIBRATED_MODE':
            errors.append('precise attention_share requires EMPIRICALLY_CALIBRATED_MODE')
        for fld in ['market','horizon','attention_object','attention_band','attention_acceleration','evidence_ids']:
            if fld not in row: errors.append(f'attention map missing {fld}')
    evid=s.get('attention',{}).get('evidence_ledger',[])
    ids=set()
    for e in evid:
        for fld in ['evidence_id','timestamp_utc','provenance','source_locator','supports']:
            if fld not in e: errors.append(f'attention evidence missing {fld}')
        ids.add(e.get('evidence_id'))
    for row in s.get('attention',{}).get('asset_horizon_maps',[]):
        for eid in row.get('evidence_ids',[]):
            if eid not in ids: errors.append(f'attention map references unknown evidence {eid}')
    return errors

def confidence_cap_errors(doc):
    errors=[]; s=state(doc) or {}; caps=s.get('provenance',{}).get('confidence_caps',[])
    cap_fields={x.get('field') for x in caps if isinstance(x,dict)}
    unavailable=set(s.get('provenance',{}).get('unavailable_inputs',[]))
    for n in s.get('narratives',{}).get('candidates',[]):
        conf=n.get('confidence',0); tier=n.get('observability_tier','')
        if conf>70 and tier in ['TIER_0_OFFICIAL_PUBLIC','TIER_1_PUBLIC_MARKET','TIER_2_REPUTABLE_INSTITUTIONAL_PUBLIC'] and n.get('flow_control') not in ['UNDETERMINED','LOW']:
            errors.append(f"{n.get('narrative_id')} flow/adoption confidence exceeds public-data boundary")
    if 'PROPRIETARY_POSITIONING' in unavailable and 'flow_controller' not in cap_fields:
        errors.append('missing confidence cap for flow_controller when proprietary positioning unavailable')
    return errors

def independence_errors(doc):
    errors=[]; s=state(doc) or {}
    graph=s.get('cross_asset_graph',[])
    for edge in graph:
        if edge.get('edge_type') not in ['CAUSAL','CONFIRMATION','MECHANICAL','CORRELATED','ATTENTION','FLOW','UNCERTAIN']:
            errors.append('cross-asset edge missing valid edge_type')
        if 'independence' not in edge: errors.append('cross-asset edge missing independence')
    return errors

def daily_output_errors(doc, require_all_markets=False):
    errors=[]; s=state(doc) or {}; rows=s.get('daily_state',{}).get('executive_market_map',[])
    required=['market','fundamental_direction','force','dominant_fact_cluster','fact_persistence','fact_consumption','remaining_pressure','dominant_narrative','narrative_validity','narrative_dominance','narrative_persistence','narrative_saturation','strongest_challenger','attention_shift_risk','edge_availability','confidence']
    markets=set()
    for r in rows:
        markets.add(r.get('market'))
        for f in required:
            if f not in r: errors.append(f'executive row {r.get("market")} missing {f}')
    if require_all_markets and not REQUIRED_MARKET_ROWS.issubset(markets):
        errors.append(f'multi-market daily output missing markets: {sorted(REQUIRED_MARKET_ROWS-markets)}')
    return errors

def all_errors(doc, require_all_markets=False):
    out=[]
    for fn in [structural_errors,separation_errors,no_hindsight_errors,attention_provenance_errors,confidence_cap_errors,independence_errors]: out.extend(fn(doc))
    out.extend(daily_output_errors(doc,require_all_markets))
    return out

LINK_RE=re.compile(r'\[\[([^\]]+)\]\]')

def link_report(vault_root):
    root=pathlib.Path(vault_root)
    md=list(root.rglob('*.md'))
    exact={p.relative_to(root).with_suffix('').as_posix():p for p in md}
    bybase={}
    for p in md: bybase.setdefault(p.stem,[]).append(p)
    unresolved=[]; ambiguous=[]
    for p in md:
        text=p.read_text(encoding='utf-8',errors='replace')
        for raw in LINK_RE.findall(text):
            target=raw.split('|',1)[0].split('#',1)[0].strip().replace('\\','/')
            if not target or target.startswith(('http://','https://','mailto:')): continue
            if target.endswith('.md'): target=target[:-3]
            ok=False
            if target in exact: ok=True
            else:
                stem=pathlib.PurePosixPath(target).name
                hits=bybase.get(stem,[])
                if len(hits)==1: ok=True
                elif len(hits)>1: ambiguous.append({'source':p.relative_to(root).as_posix(),'target':target})
            if not ok and not any(x['source']==p.relative_to(root).as_posix() and x['target']==target for x in ambiguous):
                unresolved.append({'source':p.relative_to(root).as_posix(),'target':target})
    return {'unresolved':unresolved,'ambiguous':ambiguous,'counts':{'unresolved':len(unresolved),'ambiguous':len(ambiguous)}}

def frontmatter_and_fence_errors(vault_root, paths):
    errors=[]; root=pathlib.Path(vault_root)
    for rel in paths:
        p=root/rel
        if p.suffix.lower()!='.md' or not p.is_file(): continue
        t=p.read_text(encoding='utf-8',errors='replace')
        if not t.startswith('---\n'): errors.append(f'{rel}: missing frontmatter opener')
        elif '\n---\n' not in t[4:2000]: errors.append(f'{rel}: missing frontmatter closer')
        if t.count('```')%2: errors.append(f'{rel}: unbalanced code fences')
    return errors
