#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
import jsonschema
p=argparse.ArgumentParser();p.add_argument('--vault-root',required=True);p.add_argument('--receipt',required=True);a=p.parse_args()
r=Path(a.vault_root);x=json.loads(Path(a.receipt).read_text(encoding='utf-8')); errs=[]
mod=r/'100 Six-Market D2 Fact Books and Production Shadow Engine'; schp=mod/'schemas/AlphaLab_Observability_Receipt.schema.json'
try:
    sch=json.loads(schp.read_text(encoding='utf-8')); jsonschema.validators.validator_for(sch).check_schema(sch)
    resolver=jsonschema.RefResolver(base_uri=(mod/'schemas').resolve().as_uri()+'/',referrer=sch)
    jsonschema.validate(x,sch,resolver=resolver)
except Exception as exc:
    errs.append('SCHEMA:'+str(exc))
reg=json.loads((mod/'config/fact_observability_registry.json').read_text(encoding='utf-8'))
mp=json.loads((mod/'config/six_market_observability_map.json').read_text(encoding='utf-8'))
sr=json.loads((mod/'config/d2_source_registry.json').read_text(encoding='utf-8'))
fams={z['family_id'] for z in reg['families']}; sources={s['source_id']:s for s in sr['sources']}
inst=x.get('instrument'); horizon=x.get('active_horizon'); cells=mp.get('markets',{}).get(inst,{})
items=x.get('items',[]); ids=[i.get('family_id') for i in items]
if len(ids)!=len(set(ids)): errs.append('DUPLICATE_FAMILY_ITEM')
# Baseline materiality is a prior. Every applicable baseline-material family must be explicitly receipted.
for fid,c in cells.items():
    if c.get('materiality')!='NOT_MATERIAL' and horizon in c.get('active_horizons',[]) and fid not in ids:
        errs.append('MISSING_BASELINE_MATERIAL_FAMILY_'+fid)
for i in items:
    fid=i.get('family_id')
    if fid not in fams: errs.append('UNKNOWN_FAMILY_'+str(fid)); continue
    expected=cells.get(fid,{}).get('materiality')
    base=i.get('baseline_materiality'); runtime=i.get('runtime_materiality')
    if expected and base!=expected: errs.append('BASELINE_MATERIALITY_MISMATCH_'+fid)
    if runtime!=base and not (i.get('materiality_reason') or '').strip(): errs.append('RUNTIME_MATERIALITY_CHANGE_WITHOUT_REASON_'+fid)
    if runtime=='NOT_MATERIAL' and i.get('coverage_state')!='NOT_MATERIAL': errs.append('RUNTIME_NOT_MATERIAL_REQUIRES_NOT_MATERIAL_COVERAGE_'+fid)
    if i.get('coverage_state')=='NOT_MATERIAL' and runtime!='NOT_MATERIAL': errs.append('NOT_MATERIAL_COVERAGE_ON_RUNTIME_MATERIAL_FAMILY_'+fid)
    for sid in i.get('admitted_source_ids',[]):
        if sid not in sources: errs.append('UNKNOWN_SOURCE_'+sid); continue
        s=sources[sid]
        if i.get('coverage_state') in {'DIRECT_MATERIAL_COVERAGE','PARTIAL_DIRECT'} and horizon not in s.get('current_state_horizons',[]) and i.get('freshness_state')=='FRESH': errs.append('STALE_SOURCE_CLAIMED_CURRENT_'+fid+'_'+sid)
        if s.get('access_class')=='LICENSED_REQUIRED' and i.get('access_state')!='LICENSED_AVAILABLE': errs.append('LICENSED_SOURCE_WITHOUT_ACCESS_ATTESTATION_'+sid)
        if s.get('access_class')=='SUBSCRIPTION_REQUIRED' and i.get('access_state') not in {'SUBSCRIPTION_AVAILABLE','MIXED_AVAILABLE'}: errs.append('SUBSCRIPTION_SOURCE_WITHOUT_ACCESS_ATTESTATION_'+sid)
    if i.get('coverage_state') in {'DIRECT_MATERIAL_COVERAGE','PARTIAL_DIRECT','DELAYED_DIRECT'} and not i.get('admitted_source_ids'): errs.append('DIRECT_COVERAGE_WITHOUT_ADMITTED_SOURCE_'+fid)
    if i.get('coverage_state')=='PROXY_ONLY' and i.get('evidence_class') not in {'PROXY','MODEL_INFERENCE','MIXED'}: errs.append('PROXY_STATE_BAD_EVIDENCE_CLASS_'+fid)
if x.get('silent_gap_count')!=0: errs.append('SILENT_GAP_COUNT_NONZERO')
print(json.dumps({'status':'PASS' if not errs else 'FAIL','instrument':inst,'active_horizon':horizon,'items':len(items),'errors':errs},indent=2));sys.exit(0 if not errs else 2)
