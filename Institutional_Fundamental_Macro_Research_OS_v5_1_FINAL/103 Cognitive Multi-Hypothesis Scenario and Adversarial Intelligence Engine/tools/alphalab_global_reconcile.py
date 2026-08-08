#!/usr/bin/env python3
from pathlib import Path
import argparse,json
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.add_argument('--vault-root');a=p.parse_args();x=json.loads(Path(a.input).read_text(encoding='utf-8'));root=Path(a.vault_root).resolve() if a.vault_root else Path(__file__).resolve().parents[2]
q=root/'103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine/config/global_root_ontology.json';ont=json.loads(q.read_text(encoding='utf-8')) if q.exists() else {'roots':{}}
alias={};state_alias={}
for canon,spec in ont.get('roots',{}).items():
 for z in spec.get('aliases',[]):alias[z.upper()]=canon
 for z,c in spec.get('state_aliases',{}).items():state_alias[(canon,z.upper())]=c
claims={};markets=[]
for m in x.get('market_intents') or []:
 markets.append(m)
 for c in m.get('root_direction_claims') or []:
  raw=str(c.get('root_id',''));canon=alias.get(raw.upper(),raw);st=state_alias.get((canon,str(c.get('root_state','')).upper()),str(c.get('root_state','')).upper());claims.setdefault(canon,[]).append({'instrument':m.get('instrument'),'state':st,'raw_root':raw})
inc=[]
for rid,vals in claims.items():
 states={v['state'] for v in vals if v['state'] not in {'','UNDETERMINED','MIXED'}}
 if len(states)>1:inc.append({'root_id':rid,'claims':vals})
state='INCONSISTENT' if inc else ('MULTI_DRIVER_BUT_COHERENT' if len(claims)>1 else 'COHERENT')
out={'state':state,'market_intents':markets,'implied_global_roots':sorted(claims),'inconsistencies':inc,'resolution_actions':['REVIEW_CANONICAL_ROOT_CLAIMS'] if inc else [],'direction_override_applied':False};Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(json.dumps(out,ensure_ascii=False))
