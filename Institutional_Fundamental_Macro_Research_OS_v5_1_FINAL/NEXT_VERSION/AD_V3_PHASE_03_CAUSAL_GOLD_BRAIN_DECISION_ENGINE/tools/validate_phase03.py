from __future__ import annotations
import json, pathlib, sys
P=pathlib.Path(__file__).resolve().parents[1]; N=P.parent

def load(p): return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def check(name,ok,detail=None): return {'name':name,'status':'PASS' if ok else 'FAIL','detail':detail}
def main():
    checks=[]; reason=load(P/'config/fact_reasoning_registry.json'); roots=load(P/'config/root_family_registry.json'); policy=load(P/'config/causal_brain_policy.json'); planes=load(P/'config/pressure_plane_policy.json')
    p01=N/'AD_V3_PHASE_01_TOTAL_GOLD_KNOWLEDGE_SCIENCE_FOUNDATION'; p02=N/'AD_V3_PHASE_02_TOTAL_LIVE_DATA_OBSERVABILITY_FABRIC'
    checks.append(check('p01 installed',p01.exists())); checks.append(check('p02 installed',p02.exists()))
    p01facts=load(p01/'config/gold_master_fact_registry.json')['facts'] if p01.exists() else []
    p02facts=load(p02/'config/fact_acquisition_registry.json')['contracts'] if p02.exists() else []
    rf={x['fact_id'] for x in reason['contracts']}; checks.append(check('exact 192 reasoning contracts',len(reason['contracts'])==192,len(reason['contracts']))); checks.append(check('unique reasoning contracts',len(rf)==192)); checks.append(check('p01 p02 p03 exact fact parity',rf=={x['fact_id'] for x in p01facts}=={x['fact_id'] for x in p02facts}))
    checks.append(check('twelve independent root families',len(roots['roots'])==12,len(roots['roots']))); checks.append(check('four pressure planes',set(planes['planes'])=={'CAUSAL_FUNDAMENTAL','REALIZED_TRANSACTION','MECHANICAL_FORCED','STRUCTURAL_CARRY'}))
    checks.append(check('price facts non additive',all(not x['can_add_to_session_causal_direction'] for x in reason['contracts'] if x['role']=='TARGET_PRICE_RESPONSE')))
    checks.append(check('event shocks non additive',all(not x['can_add_to_session_causal_direction'] for x in reason['contracts'] if x['role']=='EVENT_SHOCK')))
    checks.append(check('positioning non additive',all(not x['can_add_to_session_causal_direction'] for x in reason['contracts'] if x['role']=='POSITIONING_STATE')))
    checks.append(check('structural direct session authority false',all(not x['can_add_to_session_causal_direction'] for x in reason['contracts'] if x['pressure_plane']=='STRUCTURAL_CARRY')))
    checks.append(check('only root eligible can add',all((not x['can_add_to_session_causal_direction']) or x['causal_root_eligible'] for x in reason['contracts'])))
    checks.append(check('production authority false',policy['authority']['production_direction_authority'] is False and policy['authority']['production_trade_permission_authority'] is False))
    checks.append(check('no numeric pressure score',planes['no_numeric_pressure_score'] is True))
    required=[P/'runtime/engine.py',P/'runtime/interpreter.py',P/'runtime/planes.py',P/'runtime/transmission.py',P/'runtime/decision.py',P/'runtime/semantic_packet.py',P/'tools/run_causal_brain.py',P/'tools/export_semantic_evidence_packet.py']
    checks.append(check('required runtime surfaces present',all(x.exists() for x in required),[str(x) for x in required if not x.exists()]))

    # Immutable payload integrity (baseline excludes itself).
    import hashlib
    hreg=load(P/'baseline/P03_IMMUTABLE_HASHES.json'); drift=[]
    for row in hreg.get('files',[]):
        fp=P/row['path']
        if (not fp.exists()) or hashlib.sha256(fp.read_bytes()).hexdigest()!=row['sha256']: drift.append(row['path'])
    checks.append(check('p03 immutable payload hashes',not drift,drift))
    out={'phase':'AD-V3-P03','status':'PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL','checks':checks,'fact_count':len(reason['contracts']),'root_count':len(roots['roots'])}
    print(json.dumps(out,indent=2)); return 0 if out['status']=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
