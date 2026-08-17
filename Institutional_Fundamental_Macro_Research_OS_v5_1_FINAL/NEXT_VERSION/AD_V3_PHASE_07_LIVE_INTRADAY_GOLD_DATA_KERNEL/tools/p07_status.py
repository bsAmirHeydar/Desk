from __future__ import annotations
import json,pathlib,sys
HERE=pathlib.Path(__file__).resolve(); PH=HERE.parents[1]; sys.path.insert(0,str(PH.parent))
from AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL.runtime.common import P02,P04,load,config
from AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL.runtime.acquisition_planner import build_plan

def main():
 plan=build_plan(config('gold_kernel_policy.json')['default_horizon'],'NORMAL')
 latest=PH/'artifacts/latest/latest_kernel_receipt.json'; last=load(latest) if latest.exists() else None
 sr=load(P02/'config/source_contract_registry.json')
 provider=[]
 for x in plan['facts']:
  if x['operational_tier']=='ESCALATION' and x['acquisition_mode']=='PROVIDER_GAP': provider.append(x['fact_id'])
 out={'phase':'AD-V3-P07','version':'3.7.0-live-intraday-gold-kernel','acceptance_status':(load(PH/'PHASE_07_HANDOFF.json').get('p07_status') if (PH/'PHASE_07_HANDOFF.json').exists() else 'NOT_YET_RECORDED'),'default_horizon':plan['horizon'],'fact_tiers':plan['counts']['fact_tiers'],'source_actions_current_plan':plan['counts']['source_actions'],'cache_path':str(PH/'artifacts/context_cache'),'known_critical_provider_gaps':provider,'last_kernel':({'run_id':last.get('run_id'),'health':last.get('kernel_health'),'performance':last.get('performance'),'admission':last.get('analysis_admission')} if last else None),'v3_state':'SHADOW_COMMISSIONING','production_promotion_performed':False,'trade_execution_authority':'NONE'}
 print(json.dumps(out,indent=2,ensure_ascii=False)); return 0
if __name__=='__main__': raise SystemExit(main())
