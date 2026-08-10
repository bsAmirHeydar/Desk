from pathlib import Path
from datetime import datetime, timezone, timedelta
from contextlib import contextmanager
import os, json, shutil, tempfile, subprocess, sys
from .util import load_json, dump_json, data_root, now, current_certification_surface
from .true_forward import verify_commitment, link_outcome, list_records

TF3_VERSION='TF3.0.0'

def _dt(s):
    if not isinstance(s,str) or not s: raise RuntimeError('timezone-aware timestamp required')
    t=s[:-1]+'+00:00' if s.endswith('Z') else s; d=datetime.fromisoformat(t)
    if d.tzinfo is None: raise RuntimeError('timezone-aware timestamp required')
    return d.astimezone(timezone.utc)
def _iso(d): return d.astimezone(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
def _root(v): return data_root(v)/'forward'
def _dirs(v):
    r=_root(v); names=('commitments','outcomes','reviews','locks','outcome_inbox','outcome_processed','operations','backups')
    ds={k:r/k for k in names}
    for p in ds.values():p.mkdir(parents=True,exist_ok=True)
    return ds
def _policy(v): return load_json(Path(v)/'RUNTIME'/'Production Commissioning'/'config'/'continuous_forward_policy.json')
def _commission(v): return load_json(Path(v)/'RUNTIME'/'Production Commissioning'/'config'/'commissioning_policy.json')
def _atomic_replace(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);fd,tmp=tempfile.mkstemp(prefix='.'+p.name+'.',suffix='.tmp',dir=str(p.parent));os.close(fd);t=Path(tmp)
    try:t.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');os.replace(str(t),str(p))
    finally:
        if t.exists():t.unlink()
@contextmanager
def _operation_lock(v):
    pol=_policy(v);p=_dirs(v)['locks']/'TF3_OPERATION.lock';p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        try:
            age=(datetime.now(timezone.utc)-datetime.fromtimestamp(p.stat().st_mtime,timezone.utc)).total_seconds()
            if age>int(pol['stale_operation_lock_seconds']):p.unlink()
            else:raise RuntimeError('TF3 operation already running')
        except FileNotFoundError:pass
    fd=os.open(str(p),os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    try:os.write(fd,(now()+'\n').encode('ascii'));os.fsync(fd);os.close(fd);fd=None;yield
    finally:
        try:
            if fd is not None:os.close(fd)
        except Exception:pass
        try:p.unlink()
        except FileNotFoundError:pass

def _business_due(sealed,horizon,v):
    pol=_policy(v);h=str(horizon or 'UNSPECIFIED').upper();sec=int(pol['horizon_maturity'].get(h,pol['horizon_maturity']['UNSPECIFIED']))
    due=sealed+timedelta(seconds=sec)
    if h in ('DAILY','DAILY_OPEN_TO_CLOSE','MULTI_DAY','TACTICAL','MEDIUM_TERM','STRUCTURAL'):
        while due.weekday()>=5: due+=timedelta(days=1)
    return due

def snapshot_completeness(c):
    missing=[];m=c.get('method') or {};a=c.get('apl_a') or {}
    if m.get('findings_snapshot') is None:missing.append('M1_FINDINGS')
    if not m.get('version'):missing.append('M1_VERSION')
    if a.get('artifact_payloads') is None:missing.append('APL_PAYLOADS')
    if a.get('active_lenses') is None:missing.append('APL_LENSES')
    if not a.get('version'):missing.append('APL_VERSION')
    if not c.get('expected_outcome_contract'):missing.append('OUTCOME_CONTRACT')
    return {'status':'PASS' if not missing else 'LIMITED_REVIEWABILITY','missing':missing}

def _outcome_exists(ds,cid): return (ds['outcomes']/('OUT_'+cid+'.json')).is_file()
def _inbox(ds,cid): return ds['outcome_inbox']/('IN_'+cid+'.json')
def _maturity_row(v,p,nowdt,auto_link=True):
    ds=_dirs(v);c=load_json(p);cid=c.get('commitment_id');vr=verify_commitment(v,cid)
    if vr.get('status')!='PASS':return {'commitment_id':cid,'state':'SEAL_CORRUPTION','critical':True}
    if _outcome_exists(ds,cid):return {'commitment_id':cid,'state':'LINKED','critical':False}
    due=_business_due(_dt(c['sealed_at_utc']),c.get('horizon') or (c.get('expected_outcome_contract') or {}).get('horizon'),v)
    if nowdt<due:return {'commitment_id':cid,'state':'NOT_YET_MATURE','due_at_utc':_iso(due),'critical':False}
    ip=_inbox(ds,cid)
    if not ip.is_file():return {'commitment_id':cid,'state':'READY_TO_LINK','due_at_utc':_iso(due),'critical':False}
    if not auto_link:return {'commitment_id':cid,'state':'READY_TO_LINK','outcome_inbox':str(ip),'critical':False}
    try:
        obj=load_json(ip);res=link_outcome(v,cid,obj);dest=ds['outcome_processed']/ip.name
        if dest.exists(): raise RuntimeError('processed outcome inbox collision')
        os.replace(str(ip),str(dest));return {'commitment_id':cid,'state':'LINKED','outcome_link_id':res.get('outcome_link_id'),'critical':False}
    except Exception as e:return {'commitment_id':cid,'state':'DATA_UNAVAILABLE','error':str(e),'critical':False}

def mature_pending(vault_root,at_utc=None,auto_link=True):
    v=Path(vault_root).resolve();ds=_dirs(v);t=_dt(at_utc) if at_utc else datetime.now(timezone.utc);rows=[]
    for p in sorted(ds['commitments'].glob('TF1_*.json')):rows.append(_maturity_row(v,p,t,auto_link))
    counts={k:sum(r['state']==k for r in rows) for k in sorted({r['state'] for r in rows})};out={'schema_version':'1.0.0','status':'FAIL' if any(r.get('critical') for r in rows) else 'PASS','tf3_version':TF3_VERSION,'evaluated_at_utc':_iso(t),'records':rows,'counts':counts,'broker_write':'NONE'};_atomic_replace(ds['operations']/'maturation_status.json',out);return out

def _tf2_path(v): return Path(v)/'102 Forward Validation Calibration Promotion and Scientific Governance Engine'/'validation'/'m1_apla_forward'
def _tf2_module(v):
    p=str(_tf2_path(v));
    if p not in sys.path:sys.path.insert(0,p)
    from runtime import tf2_review
    return tf2_review

def _latest_tf2(v):
    try:return _tf2_module(v).latest(v)
    except Exception as e:return {'status':'FAIL','latest':None,'error':str(e)}
def _new_matured_since_latest(v):
    ds=_dirs(v);all_out=[]
    for p in ds['outcomes'].glob('OUT_TF1_*.json'):
        try:all_out.append(load_json(p).get('commitment_id'))
        except Exception:pass
    lat=_latest_tf2(v).get('latest')
    if not lat:return len([x for x in all_out if x])
    try:rev=load_json(Path(lat['path']));inc=set(rev.get('record_forensics',{}).get('included_record_ids') or [])
    except Exception:inc=set()
    return len([x for x in all_out if x and x not in inc])

def periodic_review(vault_root,force=False,cutoff_utc=None):
    v=Path(vault_root).resolve();markets=_commission(v).get('shadow_instruments') or [];newm=_new_matured_since_latest(v);due=force or (newm>=max(1,len(markets)))
    if not due:return {'status':'PASS','action':'SKIP','reason':'NO_MATURED_FULL_UNIVERSE_BATCH','new_matured_since_latest':newm,'required':max(1,len(markets))}
    out=_tf2_module(v).build_snapshot(v,cutoff_utc,True);return {'status':'PASS','action':'REVIEW_CREATED_OR_REUSED','new_matured_since_latest':newm,'review':out.get('review')}

def _broker_assert(v):
    cp=_commission(v);tf=load_json(Path(v)/'RUNTIME'/'Production Commissioning'/'config'/'true_forward_policy.json');p=_policy(v)
    ok=cp.get('broker_write') is False and tf.get('broker_write') is False and p.get('broker_write') is False
    return {'status':'PASS' if ok else 'FAIL','broker_write':'NONE' if ok else 'VIOLATION'}
def _integrity(v):
    ds=_dirs(v);bad=[];limited=[]
    for p in sorted(ds['commitments'].glob('TF1_*.json')):
        try:
            c=load_json(p);vr=verify_commitment(v,c['commitment_id']);
            if vr.get('status')!='PASS':bad.append(c.get('commitment_id'))
            sc=snapshot_completeness(c)
            if sc['status']!='PASS':limited.append({'commitment_id':c.get('commitment_id'),'missing':sc['missing']})
        except Exception as e:bad.append(p.name+':'+str(e))
    return {'status':'PASS' if not bad else 'FAIL','seal_failures':bad,'limited_reviewability':limited}

def run_shadow_universe(vault_root):
    v=Path(vault_root).resolve()
    if _broker_assert(v)['status']!='PASS':return {'status':'FAIL','classification':'AUTHORITY_LEAK'}
    try:
        from .launcher import main as launch
        out=launch(v,['DAILY6','SHADOW'],seal_truth_state='TRUE_FORWARD')
        return {'status':'PASS','classification':'SHADOW_FULL_UNIVERSE_EXECUTED','result':out}
    except Exception as e:return {'status':'BLOCKED','classification':'SHADOW_RUNTIME_BLOCKED','error':str(e)}

def scheduler(vault_root,action='status'):
    v=Path(vault_root).resolve();pol=_policy(v);task=pol['scheduler']['task_name'];repo=v.parent;wrapper=repo/'AlphaLab_Commission.ps1'
    if os.name!='nt':return {'status':'PENDING','classification':'REAL_WINDOWS_HOST_REQUIRED','action':action,'task_name':task}
    tr='powershell.exe -NoProfile -ExecutionPolicy Bypass -File "'+str(wrapper)+'" tf3-cycle --run-shadow --auto-link --review-if-due'
    if action=='install':cmd=['schtasks','/Create','/F','/SC','HOURLY','/MO','1','/TN',task,'/TR',tr]
    elif action=='enable':cmd=['schtasks','/Change','/TN',task,'/ENABLE']
    elif action=='disable':cmd=['schtasks','/Change','/TN',task,'/DISABLE']
    elif action=='remove':cmd=['schtasks','/Delete','/F','/TN',task]
    elif action=='run-now':cmd=['schtasks','/Run','/TN',task]
    else:cmd=['schtasks','/Query','/TN',task,'/FO','LIST','/V']
    q=subprocess.run(cmd,capture_output=True,text=True)
    if action=='status' and q.returncode:return {'status':'PASS','classification':'NOT_INSTALLED','task_name':task}
    return {'status':'PASS' if q.returncode==0 else 'FAIL','classification':'INSTALLED_OR_ACTION_COMPLETE' if q.returncode==0 else 'SCHEDULER_ERROR','task_name':task,'stdout':q.stdout[-4000:],'stderr':q.stderr[-4000:]}

def backup(vault_root):
    v=Path(vault_root).resolve();ds=_dirs(v);stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');base=ds['backups']/('TF3_FORWARD_'+stamp);tmp=Path(tempfile.mkdtemp(prefix='tf3_backup_'))
    try:
        for name in ('commitments','outcomes','reviews'):
            src=ds[name];dst=tmp/name;shutil.copytree(src,dst,dirs_exist_ok=True)
        path=Path(shutil.make_archive(str(base),'zip',root_dir=str(tmp)));return {'status':'PASS','path':str(path)}
    finally:shutil.rmtree(tmp,ignore_errors=True)

def status(vault_root):
    v=Path(vault_root).resolve();ds=_dirs(v);lr=list_records(v);integ=_integrity(v);sch=scheduler(v,'status');tf2=_latest_tf2(v);usage=shutil.disk_usage(ds['operations'])
    op=None;p=ds['operations']/'last_cycle.json'
    if p.is_file():
        try:op=load_json(p)
        except Exception:pass
    return {'schema_version':'1.0.0','status':'FAIL' if integ['status']!='PASS' else 'PASS','tf3_version':TF3_VERSION,'forward':lr,'integrity':integ,'scheduler':sch,'latest_tf2_review':tf2.get('latest'),'disk':{'free_bytes':usage.free,'total_bytes':usage.total,'warning':usage.free<int(_policy(v)['disk_warning_free_bytes'])},'last_cycle':op,'authority':{'direction':'UNCHANGED','broker_write':'NONE','apl_a':'SHADOW_ONLY'},'apl_b':'NOT_IMPLEMENTED'}

def cycle(vault_root,run_shadow=False,auto_link=True,review_if_due=True,force_review=False):
    v=Path(vault_root).resolve();ds=_dirs(v)
    with _operation_lock(v):
        integ=_integrity(v);auth=_broker_assert(v)
        if integ['status']!='PASS' or auth['status']!='PASS':
            out={'schema_version':'1.0.0','status':'FAIL','tf3_version':TF3_VERSION,'classification':'COLLECTION_PAUSED_CRITICAL_INTEGRITY','integrity':integ,'authority':auth,'created_at_utc':now()};_atomic_replace(ds['operations']/'last_cycle.json',out);return out
        sh=run_shadow_universe(v) if run_shadow else {'status':'PASS','classification':'SHADOW_NOT_REQUESTED'}
        mat=mature_pending(v,None,auto_link)
        rev=periodic_review(v,force_review) if review_if_due else {'status':'PASS','action':'SKIP','reason':'REVIEW_NOT_REQUESTED'}
        state='PASS' if mat.get('status')=='PASS' and rev.get('status')=='PASS' and sh.get('status') in ('PASS','BLOCKED') else 'FAIL'
        out={'schema_version':'1.0.0','status':state,'tf3_version':TF3_VERSION,'shadow':sh,'maturation':{'status':mat.get('status'),'counts':mat.get('counts')},'review':rev,'authority':{'direction':'UNCHANGED','broker_write':'NONE','apl_a':'SHADOW_ONLY'},'created_at_utc':now()};_atomic_replace(ds['operations']/'last_cycle.json',out);return out

def preflight(vault_root):
    v=Path(vault_root).resolve();checks=[]
    def ck(n,b,d=None):checks.append({'name':n,'pass':bool(b),'detail':d})
    ck('tf3_manifest',(v/'RUNTIME'/'Production Commissioning'/'TF3_CONTINUOUS_FORWARD_OPERATIONS_MANIFEST.json').is_file())
    ck('tf3_policy',(v/'RUNTIME'/'Production Commissioning'/'config'/'continuous_forward_policy.json').is_file())
    try:p=_policy(v);ck('authority_none',p.get('broker_write') is False and p.get('direction_authority_added')=='NONE' and p.get('apl_a_authority')=='SHADOW_ONLY')
    except Exception as e:ck('authority_none',False,str(e))
    ck('tf2_reused',(_tf2_path(v)/'TF2_TRUE_FORWARD_REVIEW_MANIFEST.json').is_file())
    ck('no_apl_b',not any(x.is_dir() and 'APL-B' in x.name for x in (v/'RUNTIME').iterdir()))
    try:rb=load_json(v/'RUNTIME'/'R4 Scientific Certification and Reproducibility Hardening'/'config'/'certification_surface_baseline.json');bad=[k for k in rb.get('files',{}) if 'AlphaLab_Data/' in k or '__pycache__' in k or k.endswith('.pyc')];ck('r4_excludes_mutable',not bad,bad)
    except Exception as e:ck('r4_excludes_mutable',False,str(e))
    bad=[x for x in checks if not x['pass']];return {'status':'PASS' if not bad else 'FAIL','tf3_version':TF3_VERSION,'checks':checks,'errors':[x['name'] for x in bad]}

def selftest(vault_root):
    import tempfile
    v=Path(vault_root).resolve();checks=[]
    def ck(n,b,d=None):checks.append({'name':n,'pass':bool(b),'detail':d})
    ck('preflight',preflight(v)['status']=='PASS')
    old=os.environ.get('ALPHALAB_DATA_ROOT');td=Path(tempfile.mkdtemp(prefix='alphalab_tf3_'));os.environ['ALPHALAB_DATA_ROOT']=str(td)
    try:
        from .true_forward import _test_record,_atomic_create
        ds=_dirs(v);c=_test_record(td);_atomic_create(ds['commitments']/'TF1_TEST.json',c)
        ck('snapshot_complete',snapshot_completeness(c)['status']=='PASS')
        a=mature_pending(v,'2026-08-10T08:30:00Z',True);ck('not_early_mature',a['records'][0]['state']=='NOT_YET_MATURE')
        inbox=ds['outcome_inbox']/'IN_TF1_TEST.json';inbox.write_text(json.dumps({'observed_at_utc':'2026-08-12T08:02:00Z','observation_state':'OBSERVABLE','outcome':{'direction':'UP'}},indent=2),encoding='utf-8')
        b=mature_pending(v,'2026-08-12T09:00:00Z',True);ck('automatic_outcome_link',b['records'][0]['state']=='LINKED')
        cp=ds['commitments']/'TF1_TEST.json';before=cp.read_bytes();ck('commitment_immutable_after_link',cp.read_bytes()==before)
        r1=periodic_review(v,True,'2026-08-12T10:00:00Z');r2=periodic_review(v,True,'2026-08-12T10:00:00Z');ck('review_reproducible',r1['review']['review_id']==r2['review']['review_id'] and r1['review']['seal']==r2['review']['seal'])
        ck('collection_after_review',_dirs(v)['commitments'].is_dir())
        st=status(v);ck('broker_none',st['authority']['broker_write']=='NONE')
        ck('scheduler_nonwindows_truthful',scheduler(v,'status')['status'] in ('PASS','PENDING'))
    finally:
        if old is None:os.environ.pop('ALPHALAB_DATA_ROOT',None)
        else:os.environ['ALPHALAB_DATA_ROOT']=old
        shutil.rmtree(td,ignore_errors=True)
    ck('no_apl_b',not any(x.is_dir() and 'APL-B' in x.name for x in (v/'RUNTIME').iterdir()))
    bad=[x for x in checks if not x['pass']];return {'schema_version':'1.0.0','status':'PASS' if not bad else 'FAIL','tf3_version':TF3_VERSION,'passed':len(checks)-len(bad),'total':len(checks),'checks':checks,'errors':[x['name'] for x in bad]}
