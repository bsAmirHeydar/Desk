from __future__ import annotations
import json, pathlib, re, sys
HERE=pathlib.Path(__file__).resolve(); PHASE=HERE.parents[1]; NEXT=PHASE.parent; P01=NEXT/'AD_V3_PHASE_01_TOTAL_GOLD_KNOWLEDGE_SCIENCE_FOUNDATION'

def load(p): return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
def check(name, ok, detail=None): return {'name':name,'status':'PASS' if ok else 'FAIL','detail':detail}

def main(json_out=False):
 checks=[]
 fr=load(PHASE/'config/fact_acquisition_registry.json'); sr=load(PHASE/'config/source_contract_registry.json'); pol=load(PHASE/'config/acquisition_policy.json'); ep=load(PHASE/'config/freshness_vintage_policy.json')
 facts=fr['contracts']; sources=sr['sources']; smap={x['source_id']:x for x in sources}
 checks.append(check('p01 installed',P01.exists()))
 p01_ids=[]
 if P01.exists() and (P01/'config/gold_master_fact_registry.json').exists():
  p01=load(P01/'config/gold_master_fact_registry.json'); p01facts=p01.get('facts') or p01.get('objects') or p01.get('registry') or []
  if isinstance(p01facts,dict): p01facts=list(p01facts.values())
  p01_ids=[x.get('fact_id') or x.get('id') for x in p01facts]
 checks.append(check('exact 192 fact contracts',len(facts)==192 and fr.get('contract_count')==192,len(facts)))
 checks.append(check('unique fact contracts',len({x['fact_id'] for x in facts})==len(facts)))
 if p01_ids:
  checks.append(check('p01 p02 fact id exact parity',set(p01_ids)=={x['fact_id'] for x in facts},{'p01':len(p01_ids),'p02':len(facts),'missing':sorted(set(p01_ids)-{x['fact_id'] for x in facts})[:20],'extra':sorted({x['fact_id'] for x in facts}-set(p01_ids))[:20]}))
 checks.append(check('source count declared',sr.get('source_count')==len(sources),len(sources)))
 checks.append(check('unique source ids',len(smap)==len(sources)))
 badrefs=sorted({sid for f in facts for sid in f.get('source_ids',[]) if sid not in smap})
 checks.append(check('all fact source refs valid',not badrefs,badrefs))
 mandatory=[f for f in facts if f.get('must_attempt_when_applicable')]
 checks.append(check('mandatory attempt contracts present',len(mandatory)>=120,len(mandatory)))
 badpublic=[]
 for f in mandatory:
  usable=False
  for sid in f['source_ids']:
   s=smap[sid]
   if s.get('access_class','').startswith('PUBLIC') or s.get('collector_type')=='STATIC':
    if s.get('machine_endpoint') or s.get('canonical_url') or s.get('collector_type')=='STATIC': usable=True
  if not usable: badpublic.append(f['fact_id'])
 checks.append(check('mandatory facts have public/static retrieval contract',not badpublic,badpublic))
 gap_modes={'PRIVATE_GAP','PAID_GAP','LICENSED_GAP','PROVIDER_GAP'}
 gap_bad=[f['fact_id'] for f in facts if f['acquisition_mode'] in gap_modes and f.get('must_attempt_when_applicable')]
 checks.append(check('known gaps never fake mandatory public fetch',not gap_bad,gap_bad))
 checks.append(check('network acquisition enabled in p02',pol.get('network_fetch_by_p02') is True))
 checks.append(check('credentials in source tree forbidden',pol.get('credentials_in_source_tree_forbidden') is True))
 checks.append(check('direction authority remains false',pol.get('direction_authority_granted',False) is False))
 checks.append(check('trade permission authority remains false',pol.get('trade_permission_authority_granted',False) is False))
 required_time={'reference_period','event_time','published_at','first_seen_at','retrieved_at','revision_number','supersedes_observation_id'}
 txt=json.dumps(ep)
 checks.append(check('time vintage fields defined',all(k in txt for k in required_time),sorted(required_time)))
 checks.append(check('retrieval time not measurement time rule','retrieved_at' in txt and ('never' in txt.lower() or 'NEVER' in txt)))
 # inspect source tree for obvious secrets and forbidden authority literals
 secret=[]; forbidden=[]
 for p in list((PHASE/'config').rglob('*'))+list((PHASE/'runtime').rglob('*'))+list((PHASE/'tools').rglob('*')):
  if not p.is_file(): continue
  t=p.read_text(encoding='utf-8',errors='ignore')
  if re.search(r'(?i)(api[_-]?key|secret|token|password)\s*[=:]\s*["\'][A-Za-z0-9_\-]{12,}',t): secret.append(str(p.relative_to(PHASE)))
  if re.search(r'"direction_authority_granted"\s*:\s*true|"trade_permission_authority_granted"\s*:\s*true',t,re.I): forbidden.append(str(p.relative_to(PHASE)))
 checks.append(check('no embedded credentials',not secret,secret))
 checks.append(check('no p02 decision authority literal',not forbidden,forbidden))
 # required docs/schemas/runtime
 req=['runtime/executor.py','runtime/http_client.py','runtime/extractors.py','runtime/planner.py','schemas/AlphaDesk_V3_P02_CoverageReceipt.schema.json','tools/run_gold_live_acquisition.py','PHASE_02_HANDOFF.json']
 missing=[x for x in req if not (PHASE/x).exists()]
 checks.append(check('required p02 surfaces present',not missing,missing))
 status='PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL'
 out={'phase':'AD-V3-P02','status':status,'checks':checks,'fact_count':len(facts),'source_count':len(sources),'mandatory_attempt_contracts':len(mandatory)}
 print(json.dumps(out,indent=2,ensure_ascii=False) if json_out else '\n'.join([f"[{c['status']}] {c['name']}" for c in checks]))
 return 0 if status=='PASS' else 1
if __name__=='__main__': raise SystemExit(main('--json' in sys.argv))
