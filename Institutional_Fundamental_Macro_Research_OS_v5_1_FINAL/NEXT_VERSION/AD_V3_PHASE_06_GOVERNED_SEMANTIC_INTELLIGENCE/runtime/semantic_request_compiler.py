from __future__ import annotations
from pathlib import Path
from .common import load_json, stable_id, sha256_obj

SEMANTIC_MODES={'SEMANTIC_ADJUDICATION_REQUIRED','STRUCTURAL_PRIOR_ONLY','MECHANICAL_SEMANTIC'}

def _add_evidence(out,seen,obs,fact_id,relation):
    if not isinstance(obs,dict): return
    eid=obs.get('observation_id')
    if not eid or eid in seen: return
    seen.add(eid)
    out.append({'evidence_id':str(eid),'fact_id':str(obs.get('fact_id') or fact_id),'relation':relation,'observation':obs})

def semantic_population(p03_root):
    reg=load_json(Path(p03_root)/'config/fact_reasoning_registry.json')
    contracts=reg['contracts']
    canonical=[x for x in contracts if x.get('reasoning_mode')=='SEMANTIC_ADJUDICATION_REQUIRED']
    governable=[x for x in contracts if x.get('reasoning_mode') in SEMANTIC_MODES]
    session=[x for x in canonical if 'SESSION_1_6H' in (x.get('active_horizons') or [])]
    return {'canonical_semantic_facts':len(canonical),'session_semantic_facts':len(session),'governable_p03_request_contracts':len(governable),'canonical_fact_ids':[x['fact_id'] for x in canonical],'governable_fact_ids':[x['fact_id'] for x in governable]}

def compile_request_packet(packet,p03_root):
    p03_root=Path(p03_root)
    reg=load_json(p03_root/'config/fact_reasoning_registry.json')
    cmap={x['fact_id']:x for x in reg['contracts']}
    items=[]
    for src in packet.get('items') or []:
        fid=src['fact_id']; c=cmap.get(fid)
        if not c or c.get('reasoning_mode') not in SEMANTIC_MODES:
            raise ValueError('P06_UNGOVERNED_P03_SEMANTIC_REQUEST:'+fid)
        evidence=[]; seen=set()
        _add_evidence(evidence,seen,src.get('current_observation'),fid,'CURRENT_OBSERVATION')
        _add_evidence(evidence,seen,src.get('previous_economic_observation'),fid,'PREVIOUS_ECONOMIC_OBSERVATION')
        _add_evidence(evidence,seen,src.get('previous_fetch_observation') or src.get('previous_observation'),fid,'PREVIOUS_FETCH_NOT_ECONOMIC')
        for dep in src.get('dependency_evidence') or []:
            df=dep.get('fact_id') or fid
            _add_evidence(evidence,seen,dep.get('current_observation'),df,'DEPENDENCY_CURRENT_OBSERVATION')
            _add_evidence(evidence,seen,dep.get('previous_economic_observation'),df,'DEPENDENCY_PREVIOUS_ECONOMIC_OBSERVATION')
            _add_evidence(evidence,seen,dep.get('previous_fetch_observation') or dep.get('previous_observation'),df,'DEPENDENCY_PREVIOUS_FETCH_NOT_ECONOMIC')
        cur=src.get('current_observation') or {}; diag=src.get('evidence_diagnostics') or {}; guards=src.get('hard_guards') or {}
        rid=stable_id('P06REQ',{'source_packet':packet.get('packet_id'),'fact_id':fid,'observation_id':src.get('requested_observation_id'),'horizon':packet.get('horizon')})
        authority={
          'effect_on_gold':True,'strength':True,'is_additive':bool(src.get('may_add_to_current_causal_direction')),
          'causal_owner_id':src.get('causal_root_family') if src.get('may_add_to_current_causal_direction') else None,
          'allowed_effects':['BULLISH_GOLD','BEARISH_GOLD','NEUTRAL','MIXED','NO_DIRECTION','UNKNOWN'],
          'allowed_effect_kinds':['STOCK','IMPULSE','SHOCK','CONFIRMATION','VULNERABILITY','CONTEXT'],
          'allowed_strength':['LOW','MEDIUM','HIGH','UNKNOWN']
        }
        constraints={
          'reasoning_mode':c.get('reasoning_mode'),'role':src.get('role'),'authority_scope':src.get('authority_scope'),'horizon_active':bool(src.get('horizon_active',True)),
          'hard_guards':guards,'economic_comparison_available':bool(diag.get('economic_comparison_available')),
          'economic_anchor_status':diag.get('economic_anchor_status'),'explicit_event_evidence':bool(cur.get('event_time') or cur.get('published_at')),
          'epistemic_state':cur.get('epistemic_state'),'directness':cur.get('directness'),'freshness_state':cur.get('freshness_state') or (cur.get('metadata') or {}).get('freshness_state') or (cur.get('metadata') or {}).get('freshness'),'warnings':cur.get('warnings') or [],
          'outside_evidence_authority':False,'web_search_authority':False,'conversation_memory_authority':False,
          'previous_fetch_is_not_previous_economic_state':True
        }
        items.append({
          'request_id':rid,'fact_id':fid,'observation_id':src.get('requested_observation_id'),'causal_root':src.get('causal_root_family'),
          'pressure_plane':src.get('pressure_plane'),'horizon':packet.get('horizon'),'question':'Interpret only the supplied evidence for this exact registered Gold fact under the stated authority. Preserve UNKNOWN when unsupported.',
          'allowed_evidence_ids':[x['evidence_id'] for x in evidence],'evidence':evidence,'authority':authority,'constraints':constraints
        })
    out={'record_type':'AD_V3_P06_SEMANTIC_REQUEST_PACKET','schema_version':'1.0.0','packet_id':stable_id('P06REQPKT',{'source':packet.get('packet_id'),'items':[(x['request_id'],x['allowed_evidence_ids']) for x in items]}),'subject':'XAUUSD','horizon':packet.get('horizon'),'source_semantic_packet_id':packet.get('packet_id'),'items':items}
    out['request_packet_sha256']=sha256_obj(out)
    return out
