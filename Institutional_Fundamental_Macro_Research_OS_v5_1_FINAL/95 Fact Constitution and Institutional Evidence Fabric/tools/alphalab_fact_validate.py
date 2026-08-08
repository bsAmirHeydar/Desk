#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys,datetime
p=argparse.ArgumentParser(); p.add_argument('--fact',required=True); p.add_argument('--policy',required=True); p.add_argument('--cutoff'); p.add_argument('--output'); a=p.parse_args()
f=json.loads(Path(a.fact).read_text(encoding='utf-8')); pol=json.loads(Path(a.policy).read_text(encoding='utf-8'))
errors=[]; caps=[]; holds=[]
req=['fact_id','primary_class','availability_state','decision_materiality','source','time']
for k in req:
    if k not in f: errors.append('MISSING_'+k.upper())
classes=set(sum(pol['classes'].values(),[]))
if f.get('primary_class') not in classes: errors.append('INVALID_PRIMARY_CLASS')
if f.get('availability_state') not in set(pol['availability_states']): errors.append('INVALID_AVAILABILITY_STATE')
mat=f.get('decision_materiality')
if mat not in {'DECISION_CRITICAL','MATERIAL','SUPPORTING','CONTEXTUAL'}: errors.append('INVALID_DECISION_MATERIALITY')
src=f.get('source') or {}; tier=src.get('tier')
if tier not in set(pol['source_tiers']): errors.append('INVALID_SOURCE_TIER')
if f.get('load_bearing') and tier in set(pol.get('load_bearing_forbidden_tiers',[])): errors.append('UNVERIFIED_CANNOT_BE_LOAD_BEARING')
if f.get('load_bearing') and tier in set(pol.get('normally_supporting_only_tiers',[])): caps.append('SUPPORTING_SOURCE_AS_LOAD_BEARING')
if f.get('primary_class')=='PUBLIC_PROXY': caps.append('PUBLIC_PROXY_NOT_DIRECT_TARGET')
if f.get('primary_class')=='DERIVED_FACT':
    if not f.get('parent_fact_ids'): errors.append('DERIVED_FACT_MISSING_PARENT_LINEAGE')
    if not f.get('derivation_method_id'): errors.append('DERIVED_FACT_MISSING_METHOD_LINEAGE')
if f.get('primary_class')=='NARRATIVE_INFERENCE' and f.get('direction_role')=='FUNDAMENTAL_ROOT': errors.append('NARRATIVE_CANNOT_BE_FUNDAMENTAL_DIRECTION_ROOT')
# availability
if f.get('availability_state') in {'UNAVAILABLE','UNDETERMINED'}:
    if mat=='DECISION_CRITICAL': holds.append('DECISION_CRITICAL_'+f.get('availability_state'))
    elif mat=='MATERIAL': caps.append('MATERIAL_'+f.get('availability_state'))
# timestamps
T=f.get('time') or {}; pub=T.get('publication_time'); conf=f.get('timestamp_confidence','UNRESOLVED'); skew=f.get('timestamp_disagreement_seconds')
if pub is None:
    if mat=='DECISION_CRITICAL': holds.append('UNRESOLVED_PUBLICATION_TIME')
    elif mat=='MATERIAL': caps.append('UNRESOLVED_PUBLICATION_TIME_MATERIAL')
if skew is not None:
    if skew > pol['timestamp_material_conflict_seconds']:
        if mat=='DECISION_CRITICAL': holds.append('MATERIAL_TIMESTAMP_CONFLICT')
        else: errors.append('MATERIAL_TIMESTAMP_CONFLICT')
    elif skew > 0 and skew <= pol['timestamp_tolerance_seconds']:
        caps.append('SMALL_CLOCK_SKEW')
    elif skew > pol['timestamp_tolerance_seconds']:
        caps.append('TIMESTAMP_CONFLICT_REQUIRES_RECONCILIATION')
# historical cutoff
if a.cutoff and pub:
    try:
        cut=datetime.datetime.fromisoformat(a.cutoff.replace('Z','+00:00')); pt=datetime.datetime.fromisoformat(pub.replace('Z','+00:00'))
        if pt > cut: errors.append('FUTURE_VINTAGE_AT_CUTOFF')
    except Exception: errors.append('INVALID_DATETIME')
status='REJECTED' if errors else ('HOLD' if holds else ('ELIGIBLE_WITH_CAP' if caps else 'ELIGIBLE'))
out={'status':status,'errors':errors,'holds':holds,'confidence_caps':sorted(set(caps)),'fact_id':f.get('fact_id')}
if a.output: Path(a.output).write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,indent=2)); sys.exit(2 if errors else (3 if holds else 0))
