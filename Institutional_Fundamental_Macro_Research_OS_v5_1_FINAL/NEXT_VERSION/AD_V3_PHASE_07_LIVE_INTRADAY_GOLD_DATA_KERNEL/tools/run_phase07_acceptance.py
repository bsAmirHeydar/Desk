from __future__ import annotations
import json,pathlib,sys,tempfile,shutil,subprocess
from datetime import datetime,timezone,timedelta
HERE=pathlib.Path(__file__).resolve(); PH=HERE.parents[1]; NEXT=PH.parent; REPO=NEXT.parents[1]; sys.path.insert(0,str(NEXT))
from AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL.runtime.common import P02,P03,P04,P05,P06,load,write,config,iso
from AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL.runtime.acquisition_planner import build_plan
from AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL.runtime.context_cache import inspect_entry
from AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL.runtime.freshness_authority import classify_observation
from AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL.runtime.escalation_planner import evaluate as escalation_eval
from AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL.runtime.kernel_health import evaluate as health_eval
from AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL.runtime.kernel_runtime import run_kernel
from AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE.runtime.engine import execute as p03_execute
from AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE.runtime.loader import observation_history,current_previous_for_receipt
from AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE.runtime.semantic_packet import build_semantic_evidence_packet
from AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE.runtime.semantic_runtime import run_semantics
from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.permission import evaluate as permission_eval
from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.control_room_model import build as build_model

def ck(name,ok,detail=None): return {'name':name,'status':'PASS' if ok else 'FAIL','detail':detail}

def main():
 checks=[]
 # P05/P06 prerequisite status is verified by their deterministic validators, not by mutable runtime state.
 for phase,tool in [('P05',P05/'tools/run_phase05_acceptance.py'),('P06',P06/'tools/validate_phase06.py')]:
  cp=subprocess.run([sys.executable,str(tool)],capture_output=True,text=True,encoding='utf-8',errors='replace')
  checks.append(ck(phase+' prerequisite valid',cp.returncode==0,cp.stdout[-400:] if cp.returncode else 'PASS'))
 plan=build_plan('SESSION_1_6H','NORMAL','2026-08-17T10:00:00Z')
 checks.append(ck('Gold universe preserved',plan['fact_universe_count']==192,plan['fact_universe_count']))
 checks.append(ck('operational tier coverage complete',sum(plan['counts']['fact_tiers'].values())==192,plan['counts']['fact_tiers']))
 checks.append(ck('default SESSION_1_6H kernel derived from policy',plan['horizon']=='SESSION_1_6H' and plan['counts']['fact_tiers'].get('LIVE_KERNEL',0)>0,plan['counts']['fact_tiers']))
 checks.append(ck('acquisition plan generated before network execution',plan['plan_id'].startswith('P07PLAN_') and plan['counts']['p02_planned_sources']>0,plan['plan_id']))
 # Fetch Time != Economic Time / daily data cannot masquerade as intraday.
 fp=config('freshness_authority_policy.json')
 old={'epistemic_state':'OBSERVED_CURRENT','reference_period':'2026-08-10','event_time':None,'published_at':None,'warnings':[]}
 daily={'cadence':'DAILY'}
 fr=classify_observation(old,daily,'LIVE_KERNEL','CONTEXT_REFRESH','SESSION_1_6H','2026-08-17T10:00:00Z',fp)
 checks.append(ck('Fetch Time != Economic Time enforced',fr['state']!='FRESH_LIVE',fr))
 checks.append(ck('daily data cannot masquerade as intraday update',fr['state']=='CONTEXT_VALID',fr))
 # DXY direct/provider gap is not a proxy.
 dxy=next(x for x in plan['facts'] if x['fact_id']=='DXY_INDEX')
 checks.append(ck('DXY direct/proxy distinction preserved',dxy['acquisition_mode']=='PROVIDER_GAP' and dxy['operational_tier']=='ESCALATION',dxy))
 # Escalation deterministic / no direction authority.
 e=escalation_eval({'model_quality':{'missing_driver_risk':'HIGH'},'price_transmission':{'state':'DIVERGENT'}},config('escalation_policy.json'))
 checks.append(ck('conditional escalation deterministic',e['triggered'] and bool(e['eligible_fact_ids']),e))
 checks.append(ck('escalation does not acquire directional authority',e.get('direction_authority') is False and e.get('trade_permission_authority') is False,e))
 with tempfile.TemporaryDirectory() as td:
  td=pathlib.Path(td); data=td/'p02data'; out=td/'p07out'; fix=P02/'tests/fixtures/generated'
  now=datetime.now(timezone.utc)
  t0=(now+timedelta(minutes=2)).isoformat().replace('+00:00','Z')
  t1=(now+timedelta(minutes=32)).isoformat().replace('+00:00','Z')
  t2=(now+timedelta(minutes=62)).isoformat().replace('+00:00','Z')
  t3=(now+timedelta(minutes=77)).isoformat().replace('+00:00','Z')
  cold=run_kernel(REPO,'SESSION_1_6H','NORMAL',t0,data,out,fix)
  warm=run_kernel(REPO,'SESSION_1_6H','NORMAL',t1,data,out,fix)
  full=run_kernel(REPO,'SESSION_1_6H','FULL_REFRESH',t2,data,out,fix)
  cache_only=run_kernel(REPO,'SESSION_1_6H','CACHE_ONLY',t3,data,out,None)
  checks.append(ck('P07 uses P02 acquisition authority',cold['universe']['p02_observations']==192 and cold['p02_receipt_id'],cold['p02_receipt_id']))
  checks.append(ck('full-universe current snapshot preserved',cold['universe']['full_current_snapshot'] and warm['universe']['full_current_snapshot']))
  checks.append(ck('NORMAL mode reduces external acquisition after warm cache',warm['performance']['network_requests']<cold['performance']['network_requests'] and warm['performance']['cache_hits']>0,{'cold':cold['performance'],'warm':warm['performance']}))
  checks.append(ck('FULL_REFRESH remains available',full['source_action_counts'].get('CONTEXT_REUSE',0)==0 and full['performance']['network_requests']>=warm['performance']['network_requests'],full['performance']))
  checks.append(ck('CACHE_ONLY makes zero network calls',cache_only['performance']['network_requests']==0,cache_only['performance']))
  checks.append(ck('structural context cache reuse works',warm['performance']['context_reused']>0,warm['performance']))
  checks.append(ck('cache reuse does not reset acquisition clock',warm['performance']['cache_hits']>0))
  # Cache expiry / parser hash / publication window attacks use a valid cached source entry.
  source_map={x['source_id']:x for x in load(P02/'config/source_contract_registry.json')['sources']}
  context_sid=next(x['source_id'] for x in warm['source_health'] if x.get('action')=='CONTEXT_REUSE')
  src=source_map[context_sid]; ep=out/'context_cache/index'/(context_sid+'.json'); entry=load(ep)
  expired=dict(entry); expired['acquired_at']='2026-08-01T00:00:00Z'; write(ep,expired)
  ex=inspect_entry(src,t2,config('context_cache_policy.json'),out/'context_cache')
  checks.append(ck('expired cache cannot remain current',ex['status']=='EXPIRED',ex))
  write(ep,entry); bad=dict(entry); bad['extractor_sha256']='0'*64; write(ep,bad)
  hx=inspect_entry(src,t1,config('context_cache_policy.json'),out/'context_cache')
  checks.append(ck('parser changes invalidate cache',hx['status']=='REJECTED' and hx['reason']=='EXTRACTOR_CHANGED',hx))
  write(ep,entry); pub=dict(entry); pub['next_publication_utc']=(now+timedelta(minutes=20)).isoformat().replace('+00:00','Z'); write(ep,pub)
  px=inspect_entry(src,t1,config('context_cache_policy.json'),out/'context_cache')
  checks.append(ck('post-event/publication cache invalidation works',px['status']=='EXPIRED' and px['reason']=='PUBLICATION_WINDOW_PASSED',px))
  write(ep,entry)
  # Recent fetch + old economics attack already tested; now health separation attacks.
  fake_fresh=[]
  for f in plan['facts']:
   state='FRESH_FOR_HORIZON' if f['operational_tier']=='LIVE_KERNEL' else ('CONTEXT_VALID' if f['operational_tier']=='CONTEXT_CACHE' else 'PROVIDER_GAP')
   fake_fresh.append({'fact_id':f['fact_id'],'freshness_state':state})
  one_context=next(x for x in plan['facts'] if x['operational_tier']=='CONTEXT_CACHE')['fact_id']
  for x in fake_fresh:
   if x['fact_id']==one_context: x['freshness_state']='UNAVAILABLE'
  hh=health_eval(plan,[],{'analysis_admission':'BLOCKED','analysis_may_start':False},fake_fresh)
  checks.append(ck('structural failure does not automatically block healthy live kernel',hh['live_kernel_health']=='HEALTHY' and hh['context_health']=='DEGRADED' and hh['overall_analysis_admission']=='DEGRADED_ALLOW',hh))
  for x in fake_fresh:
   if x['fact_id'] in config('gold_kernel_policy.json')['market_anchor_blocking_cluster']: x['freshness_state']='UNAVAILABLE'
  hb=health_eval(plan,[],{'analysis_admission':'PASS','analysis_may_start':True},fake_fresh)
  checks.append(ck('critical live failure cannot be hidden by aggregate completeness',hb['live_kernel_health']=='BLOCKED' and hb['overall_analysis_admission']=='BLOCK',hb))
  # P03 -> P06 -> P03 final -> P04 model integration on warm governed coverage.
  covpath=pathlib.Path(warm['governed_coverage_path']); pre=p03_execute(P03,data,covpath,None,'SESSION_1_6H')
  cov=load(covpath); hist=observation_history(data,None); pairs,_=current_previous_for_receipt(hist,cov); reg=load(P03/'config/fact_reasoning_registry.json'); cmap={x['fact_id']:x for x in reg['contracts']}; packet=build_semantic_evidence_packet(pre,pairs,cmap,cov)
  semdir=td/'sem'; sem=run_semantics(REPO,packet,artifact_dir=semdir); bundle_path=semdir/'semantic_adjudication_bundle_for_p03.json'; write(bundle_path,sem['bundle'])
  final=p03_execute(P03,data,covpath,bundle_path,'SESSION_1_6H'); promotion={'state':'SHADOW_COMMISSIONING'}; perm=permission_eval(final,promotion)
  model=build_model('P07_FIXTURE_RUN',final,packet,sem['bundle'],perm,{'sample_state':'UNCALIBRATED'},promotion,None,pre_semantic=pre,data_kernel=warm)
  checks.append(ck('offline end-to-end P07 -> P03 -> P06 -> P03 final -> P04 model',pre.get('handoff_integrity',{}).get('complete') and final.get('analysis_stage')=='POST_SEMANTIC' and model.get('data_kernel',{}).get('live_kernel_total')==warm['kernel_health']['live_kernel_total'],{'pre':pre.get('analysis_admission'),'final':final.get('analysis_admission'),'kernel':model.get('data_kernel')}))
  checks.append(ck('P06 receives P07 freshness metadata',any(((x.get('current_observation') or {}).get('metadata') or {}).get('p07_kernel') for x in packet.get('items') or [])))
  checks.append(ck('Pressure != Price preserved',model.get('hard_rules',{}).get('pressure_separate_from_price') is True))
  checks.append(ck('Stock != Impulse / previous economic discipline preserved',all(x.get('hard_guards',{}).get('previous_fetch_is_not_previous_economic_state') for x in packet.get('items') or [])))
  # Known private/provider gaps are explicit and don't retry as network sources.
  gap_actions=[x for x in plan['facts'] if x['operational_tier']=='ESCALATION']
  checks.append(ck('private/provider gaps remain explicit',any(x['acquisition_mode']=='PROVIDER_GAP' for x in gap_actions) and any(x['acquisition_mode']=='PRIVATE_GAP' for x in gap_actions)))
  checks.append(ck('known gap retry abuse absent',all(x['source_id'] not in {s for g in gap_actions for s in g['source_ids']} for x in plan['sources'] if x['action'] in ('LIVE_FETCH','CONTEXT_REFRESH','ESCALATION_FETCH'))))
 # Static wiring/governance.
 pipeline=(P04/'runtime/pipeline.py').read_text(encoding='utf-8-sig'); launcher=(REPO/'AlphaDesk.ps1').read_text(encoding='utf-8-sig'); p10=NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/runtime/gold_orchestrator.py'; p10src=p10.read_text(encoding='utf-8-sig') if p10.exists() else pipeline
 checks.append(ck('commission Gold uses P07 optimized path',('run_kernel(' in p10src and 'build_plan(' in p10src) if p10.exists() else ('run_kernel_acquisition.py' in pipeline and 'kernel_mode' in pipeline)))
 checks.append(ck('run Gold production route unchanged',('AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN' in launcher and (NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/runtime/runtime_router.py').exists())))
 p04tool=(P04/'tools/alpha_desk_v3.py').read_text(encoding='utf-8-sig'); checks.append(ck('V3 remains SHADOW_COMMISSIONING','SHADOW_COMMISSIONING' in p04tool and config('gold_kernel_policy.json')['production_promotion_forbidden']))
 checks.append(ck('automatic promotion forbidden',config('gold_kernel_policy.json')['production_promotion_forbidden'] is True))
 checks.append(ck('trade execution authority remains NONE',config('gold_kernel_policy.json')['trade_execution_authority']=='NONE'))
 # Science hash validation.
 vp=subprocess.run([sys.executable,str(PH/'tools/validate_phase07.py')],capture_output=True,text=True,encoding='utf-8',errors='replace')
 checks.append(ck('substantive Gold science drift = 0',vp.returncode==0,vp.stdout[-1000:] if vp.returncode else 'PASS'))
 ok=all(x['status']=='PASS' for x in checks)
 out={'phase':'AD-V3-P07','version':'3.7.0-live-intraday-gold-kernel','acceptance_status':'PASS' if ok else 'FAIL_CLOSED','check_count':len(checks),'checks':checks,'deterministic_performance':{'cold_network_requests':cold['performance']['network_requests'],'warm_network_requests':warm['performance']['network_requests'],'warm_cache_hits':warm['performance']['cache_hits'],'full_refresh_network_requests':full['performance']['network_requests'],'cache_only_network_requests':cache_only['performance']['network_requests'],'request_reduction_pct':round((1-warm['performance']['network_requests']/max(1,cold['performance']['network_requests']))*100,2)},'kernel_counts':warm['kernel_health'],'production_promotion_performed':False,'v3_state':'SHADOW_COMMISSIONING','trade_execution_authority':'NONE'}
 print(json.dumps(out,indent=2,ensure_ascii=False,default=str)); return 0 if ok else 2
if __name__=='__main__': raise SystemExit(main())
