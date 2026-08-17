from __future__ import annotations
from pathlib import Path
import copy
from jsonschema import Draft202012Validator
from .common import load_json, sha256_obj, stable_id, iso
from .semantic_bundle import fallback_result, p03_item

DIRECTIONAL={'BULLISH_GOLD','BEARISH_GOLD','MIXED'}

def _schema_errors(schema,obj):
    v=Draft202012Validator(schema)
    return sorted([('/'.join(str(x) for x in e.absolute_path)+': '+e.message).lstrip(': ') for e in v.iter_errors(obj)])

def _reject(req,code,detail=None):
    x=fallback_result(req,'AUTHORITY_LIMIT')
    x['reasoning_summary']=code+((': '+str(detail)) if detail else '')+'. UNKNOWN preserved; no additive authority used.'
    x['uncertainty']=['AUTHORITY_LIMIT']
    return x

def _validate_one(req,raw):
    if raw.get('request_id')!=req['request_id'] or raw.get('fact_id')!=req['fact_id'] or raw.get('observation_id')!=req['observation_id']:
        return None,'REQUEST_IDENTITY_MISMATCH'
    allowed=set(req.get('allowed_evidence_ids') or []); cited=set(raw.get('evidence_ids') or [])
    if not cited.issubset(allowed): return None,'UNAUTHORIZED_EVIDENCE_ID'
    for c in raw.get('contradictions') or []:
        if not set(c.get('evidence_ids') or []).issubset(allowed): return None,'UNAUTHORIZED_CONTRADICTION_EVIDENCE_ID'
    effect=raw.get('effect_on_gold'); kind=raw.get('effect_kind'); status=raw.get('status'); auth=req.get('authority') or {}; con=req.get('constraints') or {}; guards=con.get('hard_guards') or {}
    if effect in DIRECTIONAL and not cited: return None,'DIRECTIONAL_CLAIM_WITHOUT_EVIDENCE'
    if raw.get('is_additive'):
        if not auth.get('is_additive'): return None,'ADDITIVE_AUTHORITY_VIOLATION'
        if raw.get('causal_owner_id')!=req.get('causal_root'): return None,'CAUSAL_OWNER_MISMATCH'
    elif raw.get('causal_owner_id') not in (None,'') and raw.get('causal_owner_id')!=req.get('causal_root'):
        return None,'CAUSAL_OWNER_IDENTITY_MISMATCH'
    if con.get('authority_scope')=='STRUCTURAL_BACKGROUND_ONLY':
        if raw.get('is_additive'): return None,'STRUCTURAL_SESSION_AUTHORITY_VIOLATION'
        if kind=='IMPULSE': return None,'STRUCTURAL_PRIOR_PROMOTED_TO_CURRENT_IMPULSE'
    if not con.get('horizon_active',True) and req.get('pressure_plane') in ('CAUSAL_FUNDAMENTAL','REALIZED_TRANSACTION','MECHANICAL_FORCED') and effect in DIRECTIONAL:
        return None,'HORIZON_AUTHORITY_VIOLATION'
    if kind=='IMPULSE' and effect!='UNKNOWN' and not (con.get('economic_comparison_available') or con.get('explicit_event_evidence')):
        return None,'ECONOMIC_ANCHOR_REQUIRED_FOR_IMPULSE'
    freshness=str(con.get('freshness_state') or '').upper()
    if ('STALE' in freshness or freshness in ('DEGRADED','LIMITED')) and effect in DIRECTIONAL and raw.get('strength') in ('MEDIUM','HIGH'):
        return None,'STALE_EVIDENCE_AUTHORITY_UPGRADE'
    if guards.get('positioning_is_not_direction') and effect in DIRECTIONAL: return None,'POSITIONING_IS_NOT_DIRECTION'
    if guards.get('price_is_not_causal_pressure') and raw.get('is_additive'): return None,'PRICE_CANNOT_REWRITE_CAUSAL_PRESSURE'
    if status=='INSUFFICIENT_EVIDENCE' and (effect!='UNKNOWN' or raw.get('is_additive') or raw.get('strength')!='UNKNOWN'):
        return None,'INSUFFICIENT_EVIDENCE_MUST_REMAIN_UNKNOWN'
    if status=='CONTRADICTORY' and effect not in ('MIXED','UNKNOWN'):
        return None,'CONTRADICTION_FORCED_TO_SINGLE_DIRECTION'
    if status=='CONTRADICTORY' and raw.get('is_additive'):
        return None,'CONTRADICTORY_RESULT_CANNOT_BE_ADDITIVE'
    x=copy.deepcopy(raw)
    if con.get('epistemic_state')=='PUBLIC_PROXY' or con.get('directness')=='PROXY':
        if x.get('strength') in ('HIGH','MEDIUM'):
            x['strength']='LOW'; x['governance_note']='PROXY_STRENGTH_CAPPED_LOW'
    return x,None

def validate_response(request_packet,response,phase_root,mode='AUTO_GOVERNED',model_meta=None,fallback_reason=None):
    phase_root=Path(phase_root); schema=load_json(phase_root/'schemas/semantic_model_response.schema.json')
    schema_errors=_schema_errors(schema,response)
    reqs=request_packet.get('items') or []; reqmap={x['request_id']:x for x in reqs}; out=[]; receipt_items=[]; global_errors=[]
    if schema_errors:
        global_errors=['SCHEMA_REJECTED:'+x for x in schema_errors]
    else:
        ids=[x.get('request_id') for x in response.get('items') or []]
        if len(ids)!=len(set(ids)): global_errors.append('DUPLICATE_REQUEST_RESPONSE')
        if set(ids)-set(reqmap): global_errors.append('EXTRA_REQUEST_RESPONSE:'+','.join(sorted(set(ids)-set(reqmap))))
    rawmap={} if global_errors else {x['request_id']:x for x in response.get('items') or []}
    rejected=0; fallback=0; validated=0
    for req in reqs:
        raw=rawmap.get(req['request_id'])
        if global_errors:
            x=_reject(req,'GLOBAL_MODEL_RESPONSE_REJECTED',' | '.join(global_errors)); rejected+=1; fallback+=1; code='GLOBAL_MODEL_RESPONSE_REJECTED'
        elif raw is None:
            x=_reject(req,'MISSING_REQUEST_RESPONSE'); rejected+=1; fallback+=1; code='MISSING_REQUEST_RESPONSE'
        else:
            x,err=_validate_one(req,raw)
            if err:
                x=_reject(req,err); rejected+=1; fallback+=1; code=err
            else:
                validated+=1; code='VALIDATED'
        out.append(x); receipt_items.append({'request_id':req['request_id'],'fact_id':req['fact_id'],'status':code,'effect_on_gold':x['effect_on_gold'],'is_additive':x['is_additive']})
    unknown=sum(1 for x in out if x.get('effect_on_gold')=='UNKNOWN')
    status='PASS' if rejected==0 and not fallback_reason else 'DEGRADED'
    receipt={'record_type':'AD_V3_P06_SEMANTIC_VALIDATION_RECEIPT','receipt_id':stable_id('P06VAL',{'request':request_packet.get('packet_id'),'response':sha256_obj(response),'mode':mode,'errors':global_errors}),'generated_at_utc':iso(),'status':status,'mode':mode,'request_count':len(reqs),'validated_count':validated,'unknown_count':unknown,'rejected_count':rejected,'fallback_count':fallback if fallback_reason is None else max(fallback,len(reqs)),'fallback_reason':fallback_reason,'global_errors':global_errors,'items':receipt_items,'model_meta':model_meta or {}}
    bundle={'record_type':'AD_V3_P03_SEMANTIC_ADJUDICATION_BUNDLE','subject':'XAUUSD','items':[p03_item(x) for x in out],'adjudication_mode':mode,'governance_status':'PASS' if status in ('PASS','DEGRADED') else 'FAIL_CLOSED','source_substitution_performed':False,'external_network_used':False,'p06_semantic':{'phase':'AD-V3-P06','validation_status':status,'validation_receipt_id':receipt['receipt_id'],'request_count':len(reqs),'validated_count':validated,'unknown_count':unknown,'rejected_count':rejected,'fallback_count':receipt['fallback_count'],'fallback_reason':fallback_reason,'model_meta':model_meta or {}}}
    return bundle,receipt
