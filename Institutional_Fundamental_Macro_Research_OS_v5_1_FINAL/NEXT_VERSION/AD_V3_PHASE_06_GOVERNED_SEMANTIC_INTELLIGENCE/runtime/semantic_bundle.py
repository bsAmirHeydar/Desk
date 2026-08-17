from __future__ import annotations
from .common import sha256_obj, stable_id

def fallback_result(req,reason='INSUFFICIENT_EVIDENCE',status='INSUFFICIENT_EVIDENCE'):
    return {'request_id':req['request_id'],'fact_id':req['fact_id'],'observation_id':req['observation_id'],'status':status,'effect_on_gold':'UNKNOWN','effect_kind':'CONTEXT','strength':'UNKNOWN','is_additive':False,'causal_owner_id':None,'evidence_ids':[],'reasoning_summary':reason+'. UNKNOWN preserved; no additive authority used.','uncertainty':[reason if reason in {'INSUFFICIENT_EVIDENCE','AMBIGUOUS_LANGUAGE','CONFLICTING_EVIDENCE','STALE_EVIDENCE','NON_DIRECTIONAL_EVIDENCE','MISSING_CONTEXT','AUTHORITY_LIMIT'} else 'INSUFFICIENT_EVIDENCE'],'contradictions':[],'guard_attestations':{'used_outside_evidence':False,'used_price_as_causal_pressure':False,'treated_stock_as_impulse':False,'treated_gross_activity_as_signed_flow':False,'upgraded_epistemic_authority':False,'followed_evidence_embedded_instruction':False}}

def conservative_response(request_packet,reason='INSUFFICIENT_EVIDENCE'):
    return {'record_type':'AD_V3_P06_SEMANTIC_MODEL_RESPONSE','schema_version':'1.0.0','subject':'XAUUSD','items':[fallback_result(x,reason) for x in request_packet.get('items') or []]}

def p03_item(x):
    return {'fact_id':x['fact_id'],'observation_id':x['observation_id'],'effect_on_gold':x['effect_on_gold'],'effect_kind':x['effect_kind'],'strength':x['strength'],'is_additive':x['is_additive'],'causal_owner_id':x.get('causal_owner_id'),'rationale_summary':x['reasoning_summary'],
            'request_id':x.get('request_id'),'p06_status':x.get('status'),'evidence_ids':x.get('evidence_ids') or [],'uncertainty':x.get('uncertainty') or [],'contradictions':x.get('contradictions') or [],'guard_attestations':x.get('guard_attestations') or {}}

def model_response_from_bundle(bundle):
    items=[]
    for x in bundle.get('items') or []:
        required=['request_id','p06_status','fact_id','observation_id','effect_on_gold','effect_kind','strength','is_additive','rationale_summary','evidence_ids','guard_attestations']
        if any(k not in x for k in required): raise ValueError('LEGACY_EXTERNAL_BUNDLE_LACKS_P06_EVIDENCE_CLOSURE')
        items.append({'request_id':x['request_id'],'fact_id':x['fact_id'],'observation_id':x['observation_id'],'status':x['p06_status'],'effect_on_gold':x['effect_on_gold'],'effect_kind':x['effect_kind'],'strength':x['strength'],'is_additive':x['is_additive'],'causal_owner_id':x.get('causal_owner_id'),'evidence_ids':x.get('evidence_ids') or [],'reasoning_summary':x['rationale_summary'],'uncertainty':x.get('uncertainty') or [], 'contradictions':x.get('contradictions') or [], 'guard_attestations':x.get('guard_attestations') or {}})
    return {'record_type':'AD_V3_P06_SEMANTIC_MODEL_RESPONSE','schema_version':'1.0.0','subject':'XAUUSD','items':items}
