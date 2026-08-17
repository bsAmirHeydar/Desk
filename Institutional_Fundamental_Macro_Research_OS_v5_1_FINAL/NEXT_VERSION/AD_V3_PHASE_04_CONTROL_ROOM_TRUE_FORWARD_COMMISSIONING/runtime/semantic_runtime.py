from __future__ import annotations
from .common import load_json

DIRECTIONAL={'BULLISH_GOLD','BEARISH_GOLD','MIXED'}

def _unknown_item(item,why):
    return {'fact_id':item['fact_id'],'observation_id':item['requested_observation_id'],'effect_on_gold':'UNKNOWN','effect_kind':'CONTEXT','strength':'UNKNOWN','is_additive':False,'causal_owner_id':None,'rationale_summary':why}

def conservative_bundle(packet):
    items=[]
    for it in packet.get('items',[]):
        diag=it.get('evidence_diagnostics') or {}
        why=[]
        if not it.get('horizon_active',True): why.append('fact is inactive for the current reasoning horizon')
        if diag.get('current_previous_value_equal') is True: why.append('current fetch carries no new value versus previous fetch')
        if diag.get('economic_anchor_status') in ('NO_CURRENT_ECONOMIC_MARKER','NO_DISTINCT_ECONOMIC_ANCHOR'): why.append('no distinct economic-time comparison anchor')
        if it.get('hard_guards',{}).get('derived_fact_requires_dependency_evidence_review'):
            if not diag.get('dependency_current_observations_complete') or not diag.get('dependency_exact_acquisition_run_complete'): why.append('derived dependency closure is incomplete')
            deps=it.get('dependency_evidence') or []
            if deps and all((d.get('current_previous_value_equal') is True) for d in deps): why.append('attached dependencies show no fresh fetch-level change')
        cur=it.get('current_observation') or {}
        if cur.get('warnings'): why.append('evidence carries acquisition/parsing warnings')
        if not why: why.append('evidence is not sufficient for a governed directional semantic claim')
        items.append(_unknown_item(it,'; '.join(why)+'. UNKNOWN preserved; no additive authority used.'))
    return {'record_type':'AD_V3_P03_SEMANTIC_ADJUDICATION_BUNDLE','subject':'XAUUSD','items':items,'adjudication_mode':'CONSERVATIVE_EVIDENCE_ONLY'}

def validate_and_govern(packet,bundle):
    if bundle.get('record_type')!='AD_V3_P03_SEMANTIC_ADJUDICATION_BUNDLE' or bundle.get('subject')!='XAUUSD': raise ValueError('SEMANTIC_BUNDLE_HEADER_INVALID')
    pmap={x['fact_id']:x for x in packet.get('items',[])}; bitems=bundle.get('items') or []
    if set(pmap)!=set(x.get('fact_id') for x in bitems): raise ValueError('SEMANTIC_BUNDLE_REQUEST_ACCOUNTING_MISMATCH')
    governed=[]
    for raw in bitems:
        fid=raw.get('fact_id'); req=pmap[fid]
        if raw.get('observation_id')!=req.get('requested_observation_id'): raise ValueError('OBSERVATION_REFERENCE_MISMATCH:'+fid)
        x=dict(raw); scope=req.get('authority_scope'); cur=req.get('current_observation') or {}; diag=req.get('evidence_diagnostics') or {}
        if not req.get('horizon_active',True) and req.get('pressure_plane') in ('CAUSAL_FUNDAMENTAL','REALIZED_TRANSACTION','MECHANICAL_FORCED') and x.get('effect_on_gold') in DIRECTIONAL: raise ValueError('HORIZON_AUTHORITY_VIOLATION:'+fid)
        if scope=='STRUCTURAL_BACKGROUND_ONLY' and x.get('is_additive'): raise ValueError('STRUCTURAL_SESSION_AUTHORITY_VIOLATION:'+fid)
        if x.get('is_additive') and not req.get('may_add_to_current_causal_direction'): raise ValueError('ADDITIVE_AUTHORITY_VIOLATION:'+fid)
        if x.get('is_additive') and x.get('causal_owner_id')!=req.get('causal_root_family'): raise ValueError('CAUSAL_OWNER_MISMATCH:'+fid)
        if req.get('hard_guards',{}).get('derived_fact_requires_dependency_evidence_review') and x.get('effect_on_gold') in DIRECTIONAL:
            if not diag.get('dependency_current_observations_complete') or not diag.get('dependency_exact_acquisition_run_complete'): raise ValueError('DERIVED_DEPENDENCY_EVIDENCE_INCOMPLETE:'+fid)
        if x.get('effect_kind')=='IMPULSE' and x.get('effect_on_gold')!='UNKNOWN':
            if not diag.get('economic_comparison_available') and not cur.get('event_time') and not cur.get('published_at'): raise ValueError('ECONOMIC_ANCHOR_REQUIRED_FOR_IMPULSE:'+fid)
        if (cur.get('epistemic_state')=='PUBLIC_PROXY' or cur.get('directness')=='PROXY') and x.get('strength') in ('HIGH','MEDIUM'):
            x['strength']='LOW'; x['governance_note']='PROXY_STRENGTH_CAPPED_LOW'
        governed.append(x)
    return {'record_type':'AD_V3_P03_SEMANTIC_ADJUDICATION_BUNDLE','subject':'XAUUSD','items':governed,'adjudication_mode':bundle.get('adjudication_mode','OPERATOR_GOVERNED_BUNDLE'),'governance_status':'PASS','source_substitution_performed':False,'external_network_used':False}

def load_or_build(packet,bundle_path=None):
    b=load_json(bundle_path) if bundle_path else conservative_bundle(packet)
    return validate_and_govern(packet,b)
