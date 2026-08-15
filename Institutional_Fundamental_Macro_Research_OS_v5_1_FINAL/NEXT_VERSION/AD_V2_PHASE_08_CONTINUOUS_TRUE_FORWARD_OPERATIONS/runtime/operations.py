#!/usr/bin/env python3
from __future__ import annotations
from datetime import datetime,timezone,timedelta
from pathlib import Path
import json,hashlib,os
from .store import root,lock,seal_cycle,append,hsh,read_jsonl,atomic_create
from .eligibility import freeze_new
from .outcomes import mature_pending
from .observations import ingest

def dt(s):
    d=datetime.fromisoformat(str(s).replace('Z','+00:00'));return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
def _load_json(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def _phase_parent(phase_root):return Path(phase_root).resolve().parent

def _import_inbox(data_root,obs_policy,now_utc=None):
    rt=root(data_root);inbox=rt/'inbox';processed=rt/'inbox_processed';inbox.mkdir(parents=True,exist_ok=True);processed.mkdir(parents=True,exist_ok=True);files=sorted(list(inbox.glob('*.json'))+list(inbox.glob('*.jsonl')));added=0;dupe=0;errs=[]
    for p in files:
        try:
            if p.suffix.lower()=='.jsonl':rows=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
            else:
                obj=json.loads(p.read_text(encoding='utf-8'));rows=obj if isinstance(obj,list) else [obj]
            r=ingest(data_root,rows,obs_policy,now_utc=now_utc);added+=r['added'];dupe+=r['identical_duplicates'];os.replace(p,processed/p.name)
        except Exception as e:errs.append({'file':str(p),'error':str(e)})
    return {'status':'PASS' if not errs else 'PASS_WITH_WARNINGS','files_seen':len(files),'added':added,'duplicates':dupe,'errors':errs}

def _calibrate(data_root,phase_parent):
    import sys
    if str(phase_parent) not in sys.path:sys.path.insert(0,str(phase_parent))
    from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.true_forward import load_links,status as p07_status
    from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.calibration import calibrate
    from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.promotion import evaluate
    p07root=phase_parent/'AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION';pol=_load_json(p07root/'config/promotion_policy.json');links=load_links(data_root);rep=calibrate(links);dec=evaluate(rep,pol,independent_validator_approved=False,existing_d4_promoted_rule=False);rt=root(data_root)
    rh=hsh(rep);rp=rt/'calibration'/rh.replace(':','_')/'calibration.json'
    if not rp.exists():
        from .store import atomic_create
        atomic_create(rp,rep);append(rt/'calibration/index.jsonl',{'report_id':rep['report_id'],'report_hash':rh,'path':str(rp),'true_forward':rep['sample_counts']['true_forward'],'episodes':rep['sample_counts']['true_forward_independent_episodes']})
    dh=hsh(dec);dp=rt/'promotion_observations'/dh.replace(':','_')/'promotion_observation.json'
    if not dp.exists():
        from .store import atomic_create
        atomic_create(dp,dec);append(rt/'promotion_observations/index.jsonl',{'decision_id':dec['decision_id'],'decision_hash':dh,'status':dec['status'],'highest_eligible_class':dec.get('highest_eligible_class'),'path':str(dp)})
    return {'p07_status':p07_status(data_root),'calibration':rep,'promotion_observation':dec,'calibration_path':str(rp),'promotion_path':str(dp)}

def run_cycle(data_root,phase_root,*,now_utc=None):
    phase_root=Path(phase_root).resolve();phase_parent=_phase_parent(phase_root);policy=_load_json(phase_root/'config/continuous_forward_policy.json');obs_policy=_load_json(phase_root/'config/observation_policy.json');now=dt(now_utc) if now_utc else datetime.now(timezone.utc);started=now.isoformat().replace('+00:00','Z');cid='P08CYCLE_'+hashlib.sha256((started+'|'+str(data_root)).encode()).hexdigest()[:24].upper();rt=root(data_root)
    try:
        with lock(rt/'cycle.lock'):
            # Seal a first-cycle activation boundary so pre-P08 history cannot be
            # misrepresented as late true-forward evidence.
            ap=rt/'activation.json'
            if ap.exists():
                activation=json.loads(ap.read_text(encoding='utf-8'))
            else:
                cutoff=(now-timedelta(seconds=int(policy.get('bootstrap_lookback_seconds',0)))).isoformat().replace('+00:00','Z')
                activation={'schema_version':'1.0.0','phase':'AD-V2-P08','record_type':'P08_ACTIVATION_RECEIPT','activated_at_utc':started,'activation_cutoff_utc':cutoff,'pre_activation_runs_action':policy.get('pre_activation_runs_action'),'authority':{'trade_permission':'V1_INHERITED','broker':'NONE'}}
                activation['activation_hash']=hsh(activation);atomic_create(ap,activation)
            # hard order invariant: freeze before inbox/observation reading
            fr=freeze_new(data_root,phase_parent,policy,now_utc=started,activation_cutoff_utc=activation['activation_cutoff_utc'])
            inbox=_import_inbox(data_root,obs_policy,now_utc=started)
            mat=mature_pending(data_root,phase_parent,now_utc=started)
            cal=_calibrate(data_root,phase_parent)
            finished=datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
            rec={'schema_version':'1.0.0','phase':'AD-V2-P08','record_type':'P08_CYCLE_RECEIPT','cycle_id':cid,'status':'PASS_WITH_WARNINGS' if inbox['errors'] else 'PASS','started_at_utc':started,'finished_at_utc':finished,'activation':activation,'freeze_phase':{'new_commitments':len(fr['new_commitments']),'late_rejections':len(fr['late_rejections']),'baseline_ignored':len(fr.get('baseline_ignored',[])),'skipped':len(fr['skipped']),'invalid':len(fr['invalid']),'observation_store_read':fr['observation_store_read']},'observation_ingest':inbox,'maturity_phase':{'new_outcome_links':len(mat['new_outcome_links']),'observation_store_read':mat['observation_store_read'],'status_counts':{}},'p07_status':cal['p07_status'],'calibration':{'report_id':cal['calibration']['report_id'],'path':cal['calibration_path'],'true_forward':cal['calibration']['sample_counts']['true_forward'],'independent_episodes':cal['calibration']['sample_counts']['true_forward_independent_episodes']},'promotion_observation':{'decision_id':cal['promotion_observation']['decision_id'],'status':cal['promotion_observation']['status'],'highest_eligible_class':cal['promotion_observation'].get('highest_eligible_class'),'independent_validator_approved':False,'auto_promoted':False},'integrity':{'status':'PASS','freeze_before_observation_read':fr['observation_store_read'] is False and mat['observation_store_read'] is True,'late_runs_not_true_forward':True,'profile_bound_before_outcome':True,'auto_promotion':False,'v1_authority_unchanged':True},'authority':{'trade_permission':'V1_INHERITED','broker':'NONE','deployment':'CONTINUOUS_TRUE_FORWARD_SHADOW'}}
            counts={}
            for x in mat['results']:counts[x['status']]=counts.get(x['status'],0)+1
            rec['maturity_phase']['status_counts']=counts;rec['cycle_hash']=hsh(rec);seal_cycle(data_root,rec);append(rt/'events.jsonl',{'event':'P08_CYCLE_COMPLETE','cycle_id':cid,'status':rec['status'],'at':finished,'cycle_hash':rec['cycle_hash']});return rec
    except FileExistsError:
        return {'schema_version':'1.0.0','phase':'AD-V2-P08','record_type':'P08_CYCLE_RECEIPT','cycle_id':cid,'status':'BUSY','started_at_utc':started,'authority':{'trade_permission':'V1_INHERITED','broker':'NONE'}}

def status(data_root):
    rt=root(data_root);cycles=read_jsonl(rt/'cycles/index.jsonl');bind=read_jsonl(rt/'bindings/index.jsonl');disp=read_jsonl(rt/'run_dispositions/index.jsonl');mat=read_jsonl(rt/'maturity/index.jsonl');prof=read_jsonl(rt/'profiles/index.jsonl');cal=read_jsonl(rt/'calibration/index.jsonl');prom=read_jsonl(rt/'promotion_observations/index.jsonl');activation=None
    if (rt/'activation.json').is_file():
        try:activation=json.loads((rt/'activation.json').read_text(encoding='utf-8'))
        except:activation={'integrity':'INVALID'}
    try:
        import sys;phase_parent=Path(__file__).resolve().parents[2]
        if str(phase_parent) not in sys.path:sys.path.insert(0,str(phase_parent))
        from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.true_forward import status as p07_status
        p7=p07_status(data_root)
    except Exception as e:p7={'status':'FAIL','error':str(e)}
    return {'schema_version':'1.0.0','phase':'AD-V2-P08','status':'PASS' if p7.get('status')=='PASS' else 'FAIL','activation':activation,'cycles':len(cycles),'latest_cycle':cycles[-1] if cycles else None,'bindings':len(bind),'late_rejections':len([x for x in disp if x.get('status')=='LATE_TRUE_FORWARD_REJECTED']),'mature_linked':len([x for x in mat if x.get('status')=='MATURE_LINKED']),'evaluation_profiles':len(prof),'calibration_snapshots':len(cal),'promotion_observations':len(prom),'p07':p7,'root':str(rt),'authority':{'trade_permission':'V1_INHERITED','broker':'NONE','deployment':'CONTINUOUS_TRUE_FORWARD_SHADOW'}}
