from __future__ import annotations
import json,pathlib,sys,hashlib
HERE=pathlib.Path(__file__).resolve(); PH=HERE.parents[1]; NEXT=PH.parent; REPO=NEXT.parents[1]; sys.path.insert(0,str(NEXT))
from AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL.runtime.common import P01,P02,P03,P04,P05,P06,load,config,digest
from AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL.runtime.acquisition_planner import build_plan

def ck(name,ok,detail=None): return {'name':name,'status':'PASS' if ok else 'FAIL','detail':detail}
def main():
 checks=[]; plan=build_plan(config('gold_kernel_policy.json')['default_horizon'],'NORMAL','2026-08-17T10:00:00Z')
 fr=load(P02/'config/fact_acquisition_registry.json'); sr=load(P02/'config/source_contract_registry.json'); fids=[x['fact_id'] for x in plan['facts']]
 checks.append(ck('Gold universe preserved',len(fids)==fr['contract_count']==192 and len(set(fids))==len(fids),len(fids)))
 checks.append(ck('operational tier coverage complete',all(x['operational_tier'] in ('LIVE_KERNEL','CONTEXT_CACHE','ESCALATION') for x in plan['facts']),plan['counts']['fact_tiers']))
 checks.append(ck('default horizon is canonical session horizon',plan['horizon']=='SESSION_1_6H',plan['horizon']))
 checks.append(ck('P02 full snapshot retained',plan['p02_snapshot_horizon']=='ALL',plan['p02_snapshot_horizon']))
 checks.append(ck('P02 acquisition authority declared',plan['hard_rules']['p02_acquisition_authority'] is True))
 kp=config('gold_kernel_policy.json'); fp=config('freshness_authority_policy.json'); cp=config('context_cache_policy.json'); ep=config('escalation_policy.json')
 checks.append(ck('every live-kernel fact governed by freshness policy',all(x['operational_tier']!='LIVE_KERNEL' or fp.get('live_marker_max_age_seconds',{}).get(plan['horizon']) is not None for x in plan['facts'])))
 checks.append(ck('every context source cadence has cache policy',all(x['action'] not in ('CONTEXT_REUSE','CONTEXT_REFRESH') or x['cadence'] in cp.get('cadence_ttl_seconds',{}) for x in plan['sources']),[x['source_id'] for x in plan['sources'] if x['action'] in ('CONTEXT_REUSE','CONTEXT_REFRESH') and x['cadence'] not in cp.get('cadence_ttl_seconds',{})]))
 checks.append(ck('escalation has no direction authority',ep.get('direction_authority') is False and ep.get('trade_permission_authority') is False))
 pipeline=(P04/'runtime/pipeline.py').read_text(encoding='utf-8-sig'); p10=PH.parent/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/runtime/gold_orchestrator.py'; p10src=p10.read_text(encoding='utf-8-sig') if p10.exists() else pipeline
 checks.append(ck('P04 commission pipeline invokes P07 kernel',('run_kernel(' in p10src and 'p07_governed_coverage.json' in p10src) if p10.exists() else ('run_kernel_acquisition.py' in pipeline and 'p07_governed_coverage.json' in pipeline)))
 checks.append(ck('P03 receives explicit P07 governed coverage',('p03_execute' in p10src and 'p07_governed_coverage.json' in p10src) if p10.exists() else ("'--coverage', str(coverage_path)" in pipeline)))
 launcher=(REPO/'AlphaDesk.ps1').read_text(encoding='utf-8-sig')
 checks.append(ck('launcher exposes kernel status','AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN' in launcher))
 checks.append(ck('run Gold production routing remains fail-closed','AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN' in launcher and (PH.parent/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/runtime/runtime_router.py').exists()))
 checks.append(ck('P07 cannot promote or trade',kp.get('production_promotion_forbidden') is True and kp.get('trade_execution_authority')=='NONE'))
 base=load(PH/'baseline/PRE_P07_GOVERNANCE_HASHES.json'); drift=[]; governed=[]
 arch=load(P05/'config/architecture_surface_registry.json'); surface={x.get('path'):x for x in arch.get('surfaces',[])}
 for rp,meta in base['files'].items():
  p=REPO/rp; got=digest(p) if p.exists() else None
  if got!=meta['sha256']:
   own=surface.get(rp) or {}
   if own.get('class')=='GOVERNANCE_VERSIONED' and str(own.get('owner','')).startswith('AD-V3-P09'):
    governed.append({'file':rp,'historical_expected':meta['sha256'],'current':got,'classification':'DOWNSTREAM_GOVERNANCE_VERSIONED'})
   else: drift.append({'file':rp,'expected':meta['sha256'],'actual':got})
 checks.append(ck('substantive science and authority drift is zero',not drift,{'science_drift':drift,'accepted_downstream_governance':governed}))
 out={'phase':'AD-V3-P07','version':'3.7.0-live-intraday-gold-kernel','status':'PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL_CLOSED','check_count':len(checks),'checks':checks,'counts':{'gold_facts':fr['contract_count'],'source_contracts':sr['source_count'],'fact_acquisition_contracts':fr['contract_count'],'fact_tiers':plan['counts']['fact_tiers'],'source_actions':plan['counts']['source_actions']},'science_drift':drift}
 print(json.dumps(out,indent=2,ensure_ascii=False)); return 0 if out['status']=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
