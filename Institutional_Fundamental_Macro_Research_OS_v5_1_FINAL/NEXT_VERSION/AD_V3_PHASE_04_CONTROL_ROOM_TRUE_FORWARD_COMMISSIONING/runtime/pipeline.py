from __future__ import annotations
import subprocess, sys, json, shutil
from pathlib import Path
from .common import load_json, write_json, stable_id, iso
from .semantic_runtime import load_or_build
from .promotion import load_state as load_promotion
from .permission import evaluate as permission_eval
from .commissioning import build_precommit, update as update_commissioning
from .control_room_model import build as build_model
from .renderer import render, brief
from .capsule import build as build_capsule

def _current_fact_observation(data_root,fact_id,acquisition_run_id):
    import json
    obs=Path(data_root)/'observations'/'gold_fact_observations.jsonl'
    if not obs.exists(): return None
    hit=None
    for line in obs.read_text(encoding='utf-8-sig').splitlines():
        if not line.strip(): continue
        try: o=json.loads(line)
        except Exception: continue
        if o.get('fact_id')==fact_id and o.get('acquisition_run_id')==acquisition_run_id: hit=o
    return hit

def _price_anchor_from_store(data_root,p03):
    run_id=(p03.get('handoff_integrity') or {}).get('acquisition_run_id')
    o=_current_fact_observation(data_root,'XAUUSD_SPOT_PRICE',run_id)
    if not o or not isinstance(o.get('value'),(int,float)): return None
    marker=o.get('reference_period') or o.get('event_time') or o.get('published_at') or o.get('retrieved_at')
    return {'value':float(o['value']),'economic_marker':marker,'reference_period':o.get('reference_period'),'event_time':o.get('event_time'),'published_at':o.get('published_at'),'retrieved_at':o.get('retrieved_at'),'observation_id':o.get('observation_id'),'acquisition_run_id':run_id}

def _run_json(cmd,allow=(0,)):
    r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace')
    if r.returncode not in allow: raise RuntimeError('COMMAND_FAILED '+str(r.returncode)+'\n'+r.stderr[-1200:])
    try: obj=json.loads(r.stdout.lstrip('\ufeff'))
    except Exception as e: raise RuntimeError('JSON_OUTPUT_PARSE_FAILED '+repr(e)+'\n'+r.stdout[-1200:])
    return r.returncode,obj

def run(repo_root,horizon='SESSION_1_6H',skip_p02=False,semantic_bundle_path=None,p02_data_root_override=None,output_root_override=None):
    repo=Path(repo_root); nxt=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL'/'NEXT_VERSION'; p02=nxt/'AD_V3_PHASE_02_TOTAL_LIVE_DATA_OBSERVABILITY_FABRIC'; p03=nxt/'AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE'; p04=nxt/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING'
    data=Path(p02_data_root_override) if p02_data_root_override else p02/'artifacts'/'live_store'; outroot=Path(output_root_override) if output_root_override else p04/'artifacts'; runs=outroot/'runs'; runs.mkdir(parents=True,exist_ok=True)
    stamp=iso().replace('-','').replace(':',''); run_id=stable_id('P04RUN',{'stamp':stamp,'horizon':horizon,'data':str(data)})
    rd=runs/run_id; rd.mkdir(parents=True,exist_ok=False)
    if not skip_p02:
        code,cov=_run_json([sys.executable,str(p02/'tools'/'run_gold_live_acquisition.py'),'--horizon','ALL','--json'],allow=(0,2))
        write_json(rd/'p02_coverage.json',cov)
    else:
        receipts=sorted((data/'receipts').glob('*.json'),key=lambda p:p.stat().st_mtime,reverse=True)
        if not receipts: raise RuntimeError('NO_P02_COVERAGE_RECEIPT')
        cov=load_json(receipts[0]); code=0; write_json(rd/'p02_coverage.json',cov)
    if cov.get('analysis_admission')=='BLOCKED' or not cov.get('analysis_may_start'): raise RuntimeError('P02_BLOCKED')
    _,pre=_run_json([sys.executable,str(p03/'tools'/'run_causal_brain.py'),'--p02-data-root',str(data),'--horizon',horizon,'--json']); write_json(rd/'p03_pre_semantic.json',pre)
    packet_path=rd/'semantic_evidence_packet.json'; sr=subprocess.run([sys.executable,str(p03/'tools'/'export_semantic_evidence_packet.py'),'--p02-data-root',str(data),'--horizon',horizon,'--output',str(packet_path)],capture_output=True,text=True)
    if sr.returncode!=0: raise RuntimeError('SEMANTIC_PACKET_EXPORT_FAILED '+sr.stderr[-1000:])
    packet=load_json(packet_path); bundle=load_or_build(packet,semantic_bundle_path); write_json(rd/'semantic_adjudication_bundle.json',bundle)
    _,final=_run_json([sys.executable,str(p03/'tools'/'run_causal_brain.py'),'--p02-data-root',str(data),'--horizon',horizon,'--adjudication',str(rd/'semantic_adjudication_bundle.json'),'--json']); write_json(rd/'p03_final.json',final)
    promotion=load_promotion(p04); permission=permission_eval(final,promotion); write_json(rd/'permission.json',permission)
    price_anchor=_price_anchor_from_store(data,final)
    precommit=build_precommit(run_id,final,permission,price_anchor); write_json(rd/'precommit.json',precommit)
    commissioning=update_commissioning(p04,precommit,price_anchor); write_json(rd/'commissioning_snapshot.json',commissioning)
    latest_dir=outroot/'latest'; prev=None
    if (latest_dir/'latest_control_room.json').exists(): prev=load_json(latest_dir/'latest_control_room.json')
    model=build_model(run_id,final,packet,bundle,permission,commissioning,promotion,prev); write_json(rd/'control_room.json',model)
    helps=load_json(p04/'config'/'help_registry.json'); (rd/'control_room.html').write_text(render(model,helps),encoding='utf-8'); (rd/'brief.txt').write_text(brief(model),encoding='utf-8')
    cap=build_capsule(run_id,rd,precommit,promotion.get('state')=='PRODUCTION_V3')
    latest_dir.mkdir(parents=True,exist_ok=True)
    for src,name in [(rd/'control_room.json','latest_control_room.json'),(rd/'control_room.html','latest_control_room.html'),(rd/'brief.txt','latest_brief.txt'),(rd/'capsule.json','latest_capsule.json'),(rd/'precommit.json','latest_precommit.json'),(rd/'p03_final.json','latest_p03_final.json'),(rd/'semantic_evidence_packet.json','latest_semantic_evidence_packet.json')]: shutil.copy2(src,latest_dir/name)
    receipt={'record_type':'AD_V3_P04_PIPELINE_RECEIPT','run_id':run_id,'generated_at_utc':iso(),'status':'PASS','p02_admission':cov.get('analysis_admission'),'p02_degraded_nonblocking':code==2 and bool(cov.get('analysis_may_start')),'p03_handoff_complete':bool((final.get('handoff_integrity') or {}).get('complete')),'direction_candidate':permission.get('direction'),'research_action_candidate':permission.get('research_action_candidate'),'official_permission':permission.get('official_permission'),'semantic_mode':bundle.get('adjudication_mode','GOVERNED_BUNDLE'),'control_room':str(rd/'control_room.html'),'capsule_id':cap.get('capsule_id'),'production_authority':promotion.get('state')=='PRODUCTION_V3'}; write_json(rd/'pipeline_receipt.json',receipt); write_json(latest_dir/'latest_pipeline_receipt.json',receipt); return receipt
