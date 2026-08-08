#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
p=argparse.ArgumentParser();p.add_argument('--vault-root',required=True);a=p.parse_args();r=Path(a.vault_root);q=r/'100 Six-Market D2 Fact Books and Production Shadow Engine/config/d2_source_registry.json';e=[]
try:x=json.loads(q.read_text(encoding='utf-8'))
except Exception as z:print(json.dumps({'status':'FAIL','errors':[str(z)]},indent=2));sys.exit(2)
ids=[s.get('source_id') for s in x.get('sources',[])]; tiers={'OFFICIAL_PRIMARY','OFFICIAL_SECONDARY','EXCHANGE_ADMINISTRATOR','REGULATED_FILING','INSTITUTIONAL_PUBLIC','LICENSED','PUBLIC_PROXY','MEDIA_CONFIRMATION','UNVERIFIED'}
if len(ids)!=len(set(ids)):e.append('DUPLICATE_SOURCE_ID')
for s in x.get('sources',[]):
    if s.get('tier') not in tiers:e.append('BAD_TIER_'+str(s.get('source_id')))
    if s.get('availability_default')=='LICENSED_REQUIRED' and s.get('tier')!='LICENSED':e.append('LICENSED_STATE_ON_NONLICENSED_SOURCE_'+str(s.get('source_id')))
    if s.get('tier')=='LICENSED' and s.get('availability_default')!='LICENSED_REQUIRED':e.append('LICENSED_SOURCE_FALSE_AVAILABILITY_'+str(s.get('source_id')))
print(json.dumps({'status':'PASS' if not e else 'FAIL','sources':len(ids),'licensed_placeholders':sum(1 for s in x.get('sources',[]) if s.get('tier')=='LICENSED'),'rule':x.get('rule'),'errors':e},indent=2));sys.exit(0 if not e else 2)
