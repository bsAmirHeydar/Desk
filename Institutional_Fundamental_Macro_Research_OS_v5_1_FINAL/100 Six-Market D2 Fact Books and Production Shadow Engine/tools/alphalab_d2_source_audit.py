#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
p=argparse.ArgumentParser();p.add_argument('--vault-root',required=True);a=p.parse_args();r=Path(a.vault_root);q=r/'100 Six-Market D2 Fact Books and Production Shadow Engine/config/d2_source_registry.json';e=[]
try:x=json.loads(q.read_text(encoding='utf-8'))
except Exception as z:print(json.dumps({'status':'FAIL','errors':[str(z)]},indent=2));sys.exit(2)
ids=[s.get('source_id') for s in x.get('sources',[])]; tiers={'OFFICIAL_PRIMARY','OFFICIAL_SECONDARY','EXCHANGE_ADMINISTRATOR','REGULATED_FILING','INSTITUTIONAL_PUBLIC','LICENSED','PUBLIC_PROXY','MEDIA_CONFIRMATION','UNVERIFIED'}
access=set(x.get('access_classes',[]));fresh=set(x.get('freshness_classes',[]));horizons=set(x.get('horizons',[]))
if len(ids)!=len(set(ids)):e.append('DUPLICATE_SOURCE_ID')
for s in x.get('sources',[]):
 sid=str(s.get('source_id'))
 if s.get('tier') not in tiers:e.append('BAD_TIER_'+sid)
 if s.get('access_class') not in access:e.append('BAD_ACCESS_CLASS_'+sid)
 if s.get('freshness_class') not in fresh:e.append('BAD_FRESHNESS_CLASS_'+sid)
 if not isinstance(s.get('fact_semantics'),list) or not s.get('fact_semantics'):e.append('MISSING_FACT_SEMANTICS_'+sid)
 if not set(s.get('current_state_horizons',[])).issubset(horizons):e.append('BAD_CURRENT_HORIZON_'+sid)
 if not set(s.get('context_horizons',[])).issubset(horizons):e.append('BAD_CONTEXT_HORIZON_'+sid)
 if s.get('availability_default')=='LICENSED_REQUIRED' and s.get('tier')!='LICENSED':e.append('LICENSED_STATE_ON_NONLICENSED_SOURCE_'+sid)
 if s.get('tier')=='LICENSED' and s.get('access_class')!='LICENSED_REQUIRED':e.append('LICENSED_SOURCE_FALSE_ACCESS_'+sid)
 note=s.get('source_note')
 if note:
  if '#U2014' in note or '#U2019' in note:e.append('ENCODING_PLACEHOLDER_IN_SOURCE_NOTE_'+sid)
  if not (r/note).exists():e.append('SOURCE_NOTE_MISSING_'+sid)
print(json.dumps({'status':'PASS' if not e else 'FAIL','sources':len(ids),'licensed_placeholders':sum(1 for s in x.get('sources',[]) if s.get('tier')=='LICENSED'),'rule':x.get('rule'),'observability_rule':x.get('observability_rule'),'errors':e},indent=2));sys.exit(0 if not e else 2)
