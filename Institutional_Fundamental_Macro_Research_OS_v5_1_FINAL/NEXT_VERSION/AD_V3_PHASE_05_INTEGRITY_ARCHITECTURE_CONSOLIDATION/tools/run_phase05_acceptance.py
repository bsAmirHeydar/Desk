#!/usr/bin/env python3
from pathlib import Path
import sys,json,tempfile,shutil,importlib.util,importlib
P=Path(__file__).resolve().parents[1]; N=P.parent; REPO=N.parents[1]; sys.path.insert(0,str(N))
from AD_V3_PHASE_05_INTEGRITY_ARCHITECTURE_CONSOLIDATION.runtime.integrity import compile_integrity, canonical_counts, load

def ck(n,ok,d=None): return {'name':n,'status':'PASS' if ok else 'FAIL','detail':d}
def main():
    r=compile_integrity(False); checks=[]
    checks.append(ck('all governed surfaces have ownership class',r['audits']['architecture']['status']=='PASS',r['audits']['architecture']))
    checks.append(ck('no architecture ownership drift',not r['architecture_drift'],r['architecture_drift']))
    checks.append(ck('historical P01 snapshot preserved',r['audits']['freeze']['p01_historical_manifest_preserved'] is True))
    checks.append(ck('current P01 scientific freeze valid',r['audits']['freeze']['p01']['status']=='PASS',r['audits']['freeze']['p01']))
    dep=[x for x in r['audits']['freeze']['p01']['surfaces'] if x['classification']=='DEPLOYMENT_MUTABLE']
    checks.append(ck('legitimate deployment evolution not science corruption',all(x['current_freeze_ok'] for x in dep),dep))
    # Negative freeze attack in an isolated synthetic repo built from immutable historical surfaces.
    p1=N/'AD_V3_PHASE_01_TOTAL_GOLD_KNOWLEDGE_SCIENCE_FOUNDATION'; spec=importlib.util.spec_from_file_location('p01_kc_neg',p1/'runtime/knowledge_compiler.py'); km=importlib.util.module_from_spec(spec); spec.loader.exec_module(km)
    hist=load(p1/'baseline/v2_frozen_surface_manifest.json'); policy=load(p1/'config/v2_freeze_boundary_policy.json'); mut=set(policy['deployment_mutable_surfaces'])
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        immutable=[]
        for s in hist['surfaces']:
            if s['rel'] in mut: continue
            src=REPO/s['rel']; dst=root/s['rel']; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst); immutable.append(dst)
        before=km.verify_v2_freeze(root); immutable[0].write_bytes(immutable[0].read_bytes()+b'\nP05_NEGATIVE_TEST')
        after=km.verify_v2_freeze(root)
    checks.append(ck('actual V2 scientific baseline drift still fails closed',before['status']=='PASS' and after['status']=='FAIL_CLOSED',{'before':before['status'],'after':after['status']}))
    checks.append(ck('P02 current source count derives from registry',r['counts']['source_contracts']==r['counts']['declared']['source_contracts'],r['counts']))
    checks.append(ck('P02 generated metadata current and provenance-bound',r['audits']['metadata']['status']=='PASS',r['audits']['metadata']))
    checks.append(ck('P02 generated metadata excluded from acquisition immutable hash surface',r['audits']['freeze']['p02_generated_metadata_boundary_ok'] is True))
    checks.append(ck('Run alias resolves to Gold',load(P/'config/canonical_runtime_contract.json')['chat_semantics']['Run']=='Run Gold'))
    checks.append(ck('Gold is current active Alpha Desk scope',r['audits']['command_contract']['active_subject']=='Gold'))
    checks.append(ck('run Gold preserves fail-closed promotion routing',r['audits']['command_contract']['status']=='PASS',r['audits']['command_contract']))
    # Promotion negative tests use the production pure gate enforcer; no override exists in promote().
    p4=N/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING'; pm=importlib.import_module('AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.promotion'); policy=load(p4/'config/promotion_policy.json')
    allgood={g:True for g in policy['promotion_requires']}; blocked={}
    for g in policy['promotion_requires']:
        trial=dict(allgood); trial[g]=False
        try: pm.enforce_declared_gates(policy,trial); blocked[g]=False
        except ValueError: blocked[g]=True
    checks.append(ck('every declared promotion gate independently blocks promotion',all(blocked.values()),blocked))
    checks.append(ck('automatic promotion forbidden',policy.get('automatic_promotion_forbidden') is True))
    checks.append(ck('declared promotion gates equal machine gates',r['audits']['promotion_governance']['status']=='PASS',r['audits']['promotion_governance']))
    checks.append(ck('rollback remains available',hasattr(pm,'rollback')))
    checks.append(ck('runtime artifacts classified and gitignored',r['audits']['artifact_governance']['status']=='PASS',r['audits']['artifact_governance']))
    checks.append(ck('substantive Gold science unchanged',r['audits']['science_unchanged']['status']=='PASS',r['audits']['science_unchanged']))
    checks.append(ck('V3 promotion not performed by P05',r['v3_promotion_performed'] is False and r['expected_v3_state']=='SHADOW_COMMISSIONING'))
    checks.append(ck('trade execution authority remains NONE',r['trade_execution_authority']=='NONE'))
    status='PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL'
    out={'phase':'AD-V3-P05','version':r['version'],'acceptance_status':status,'check_count':len(checks),'checks':checks,'counts':canonical_counts(),'architecture_drift_count':len(r['architecture_drift']),'freeze_conflict_count':len(r['freeze_conflicts']),'metadata_drift_count':len(r['registry_metadata_drift']),'command_contract_drift_count':len(r['command_contract_drift']),'promotion_governance_drift_count':len(r['promotion_gate_drift']),'deployment':'SHADOW_COMMISSIONING','production_promotion_performed':False,'trade_execution_authority':'NONE'}
    (P/'artifacts').mkdir(exist_ok=True); (P/'artifacts/P05_ACCEPTANCE_RECEIPT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if status=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
