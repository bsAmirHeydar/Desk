from pathlib import Path
from contextlib import contextmanager
from datetime import datetime, timezone
import json,hashlib,os,tempfile
from .util import now

VERSION='RUN2.0.0'
FORBIDDEN=('OPENAI_API_KEY','API_KEY','ACCESS_TOKEN','AUTHORIZATION','COOKIE','REFRESH_TOKEN')

def _canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def _sha(x):return 'sha256:'+hashlib.sha256(_canon(x).encode('utf-8')).hexdigest()
def _dt(s):
    if not s:return datetime.min.replace(tzinfo=timezone.utc)
    t=s[:-1]+'+00:00' if str(s).endswith('Z') else str(s)
    try:d=datetime.fromisoformat(t);return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except Exception:return datetime.min.replace(tzinfo=timezone.utc)

def _safe_subject(s):return ''.join(c if c.isalnum() or c in ('-','_','.') else '_' for c in str(s or 'UNKNOWN'))
def _root(data_root):p=Path(data_root)/'runs';p.mkdir(parents=True,exist_ok=True);return p
@contextmanager
def _lock(path):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);fd=None
    try:fd=os.open(str(p),os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,(now()+'\n').encode());os.fsync(fd);os.close(fd);fd=None;yield
    finally:
        try:
            if fd is not None:os.close(fd)
        except Exception:pass
        try:p.unlink()
        except FileNotFoundError:pass

def _atomic_create(path,obj):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():raise RuntimeError('immutable capsule already exists: '+str(p))
    with _lock(p.parent/'.capsule.lock'):
        if p.exists():raise RuntimeError('immutable capsule already exists: '+str(p))
        fd,tmp=tempfile.mkstemp(prefix='.'+p.name+'.',suffix='.tmp',dir=str(p.parent));os.close(fd);t=Path(tmp)
        try:
            data=(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode('utf-8')
            with t.open('wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
            os.replace(t,p)
        finally:
            if t.exists():t.unlink()
    return p

def _append_jsonl(path,obj):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    line=_canon(obj)+'\n';lock=p.with_suffix(p.suffix+'.lock')
    with _lock(lock):
        with p.open('a',encoding='utf-8',newline='\n') as f:f.write(line);f.flush();os.fsync(f.fileno())

def _secret_scan(obj,path=''):
    bad=[]
    if isinstance(obj,dict):
        for k,v in obj.items():
            kp=(path+'.'+str(k)).strip('.')
            if any(x in str(k).upper() for x in FORBIDDEN):bad.append(kp)
            bad.extend(_secret_scan(v,kp))
    elif isinstance(obj,list):
        for i,v in enumerate(obj):bad.extend(_secret_scan(v,f'{path}[{i}]'))
    return bad

def _root_manifest(pack):
    vals=[]
    def walk(x):
        if isinstance(x,dict):
            hit={}
            for k,v in x.items():
                lk=str(k).lower()
                if lk in ('root_source_id','root_id','root_identity','root_source') and isinstance(v,(str,int,float)):hit['root_source_id']=str(v)
                if lk in ('source_id','publication_source_id') and isinstance(v,(str,int,float)):hit['publication_source_id']=str(v)
            if hit.get('root_source_id'):vals.append(hit)
            for v in x.values():walk(v)
        elif isinstance(x,list):
            for y in x:walk(y)
    walk(pack);seen=set();out=[]
    for x in vals:
        key=(x.get('root_source_id'),x.get('publication_source_id'))
        if key not in seen:seen.add(key);out.append(x)
    return out

def migrate_legacy(data_root):
    root=_root(data_root);legacy=root/'legacy_index.jsonl';seen=set()
    if legacy.is_file():
        for line in legacy.read_text(encoding='utf-8').splitlines():
            try:seen.add(json.loads(line).get('legacy_id'))
            except Exception:pass
    added=0;fwd=Path(data_root)/'forward'/'commitments'
    if fwd.is_dir():
        for p in sorted(fwd.glob('TF1_*.json')):
            try:o=json.loads(p.read_text(encoding='utf-8'));lid=o.get('commitment_id') or p.stem
            except Exception:continue
            if lid in seen:continue
            row={'legacy_id':lid,'source':'TRUE_FORWARD_COMMITMENT','run_id':o.get('run_id'),'subject':o.get('subject'),'truth_state':o.get('truth_state'),'reviewability':o.get('reviewability') or ('FULL_REVIEWABILITY' if o.get('true_forward_version')=='TF1.0.1' else 'LIMITED_REVIEWABILITY'),'path':str(p),'indexed_at':now()}
            _append_jsonl(legacy,row);seen.add(lid);added+=1
    return {'status':'PASS','added':added,'legacy_index':str(legacy),'historical_records_rewritten':False}

def read_index(data_root):
    p=_root(data_root)/'index.jsonl';out=[]
    if not p.is_file():return out
    for line in p.read_text(encoding='utf-8').splitlines():
        if not line.strip():continue
        try:out.append(json.loads(line))
        except Exception:out.append({'integrity':'INVALID_JSON_LINE'})
    return out

def find_previous(data_root,compiled,subject):
    rows=[r for r in read_index(data_root) if r.get('subject')==subject and r.get('mode')==compiled.get('mode') and r.get('horizon')==compiled.get('active_horizon') and r.get('primary_research_class')==compiled.get('primary_research_class') and r.get('quality_status') in ('PASS','PASS_WITH_WARNINGS','PARTIAL')]
    rows.sort(key=lambda r:_dt(r.get('as_of')),reverse=True)
    for r in rows:
        p=Path(r.get('path',''))
        if p.is_file():
            try:return json.loads(p.read_text(encoding='utf-8'))
            except Exception:pass
    return None

def detect_changes(previous,current):
    if not previous:return {'has_comparison':False,'comparison_run_id':None,'items':[]}
    items=[]
    checks=[('direction','Direction'),('permission','Permission')]
    for k,label in checks:
        a=previous.get(k);b=current.get(k)
        if a!=b:items.append({'field':k,'from':a,'to':b,'label':label})
    for k in ('force','consumption','remaining_pressure','persistence','reversal'):
        a=(previous.get('force_lifecycle') or {}).get(k);b=(current.get('force_lifecycle') or {}).get(k)
        if a!=b:items.append({'field':k,'from':a,'to':b,'label':k})
    pu=set(map(str,previous.get('unknowns') or []));cu=set(map(str,current.get('unknowns') or []))
    for x in sorted(cu-pu):items.append({'field':'unknown','change':'ADDED','value':x})
    return {'has_comparison':True,'comparison_run_id':previous.get('run_id'),'items':items}

def _evidence_manifest(rt,run_id):
    return [{'logical_name':x['logical_name'],'world':x['world'],'stage':x['stage'],'artifact_hash':x['artifact_hash']} for x in rt.catalog.list_artifacts(run_id) if x.get('world') in ('EVIDENCE','COGNITION','DECISION','META')]

def _art(rt,rid,name,default=None):
    try:return rt.store.load_artifact_json(rid,name)
    except Exception:return default

def build_capsule(rt,run_id,compiled,canonical,quality,previous=None):
    m=rt.store.load_manifest(run_id);ri=_art(rt,run_id,'research_intent',{}) or {};plan=_art(rt,run_id,'method_plan',{}) or {};hyp=_art(rt,run_id,'hypothesis_set',{}) or {};causal=_art(rt,run_id,'causal_graph',{}) or {};sc=_art(rt,run_id,'scenario_tree',{}) or {};adv=_art(rt,run_id,'adversarial_review',{}) or {};md=_art(rt,run_id,'model_disagreement',{}) or {};pm=_art(rt,run_id,'premortem',{}) or {}
    subject=str(m.get('subject') or canonical.get('subject'))
    fl=canonical.get('science',{}).get('force_lifecycle',{})
    unknowns=canonical.get('science',{}).get('uncertainty') or []
    base={'schema_version':'1.0.0','capsule_version':VERSION,'run_id':run_id,'request_id':compiled.get('request_id'),'parent_run_id':None,'comparison_run_id':previous.get('run_id') if previous else None,'subject':subject,'canonical_subject':subject,'asset_family':m.get('asset_family'),'mode':compiled.get('mode'),'as_of':m.get('analysis_cutoff_utc') or canonical.get('analysis_cutoff_utc'),'cutoff':m.get('analysis_cutoff_utc'),'horizon':compiled.get('active_horizon'),'original_command':'run '+subject,'compiled_request':compiled,'research_classes':compiled.get('research_classes'),'primary_research_class':compiled.get('primary_research_class'),'method_plan':plan,'vault_version':m.get('vault_version'),'vault_commit':m.get('vault_commit'),'scientific_stack_version':'V21.3.0','m1_version':plan.get('method_version'),'r2_prompt_pack_version':m.get('prompt_pack_version'),'r3_version':m.get('runtime_version'),'run1_version':'RUN1.0.0','run2_version':VERSION,'ui2_version':'UI2.1.0','apl_a_version':'APL-A 1.0.0','source_manifest':_evidence_manifest(rt,run_id),'root_source_manifest':_root_manifest(_art(rt,run_id,'decision_evidence_pack',{}) or {}),'evidence_ledger':_art(rt,run_id,'decision_evidence_pack',{}) or {},'claim_ledger':_art(rt,run_id,'claim_ledger',{}) or {},'cluster_results':{k:_art(rt,run_id,v,{}) or {} for k,v in {'timing':'temporal_clearance','fundamental':'fundamental_state','expectations':'policy_reaction_state','narrative':'narrative_state','positioning':'positioning_state','flow':'flow_state','funding':'funding_plumbing_state','mechanics':'mechanics_capacity_state'}.items()},'cluster_coverage':quality.get('cluster_coverage',{}),'contradiction_ledger':quality.get('contradiction_ledger',[]),'unknowns':unknowns,'hypotheses':hyp,'causal_state':causal,'scenarios':sc,'thesis_destroyer':adv,'model_disagreement':md,'premortem':pm,'direction':canonical.get('decision',{}).get('final_direction'),'permission':canonical.get('decision',{}).get('permission'),'force_lifecycle':fl,'m1_method_health':canonical.get('method_health',{}),'apl_a_findings':canonical.get('apl_a',{}),'run_quality_receipt':quality,'quality_status':quality.get('status'),'canonical_result_hash':canonical.get('canonical_result_hash'),'decision_seal':canonical.get('decision',{}).get('decision_seal_hash'),'reproducibility_state':'EVIDENCE_SNAPSHOT_REPRODUCIBLE' if _art(rt,run_id,'decision_evidence_pack',{}) else 'PARTIAL_EXTERNAL_REPRODUCIBILITY','created_at':now()}
    base['changes_since_previous']=detect_changes(previous,base);return base

def persist(data_root,capsule):
    bad=_secret_scan(capsule)
    if bad:raise RuntimeError('secret-like fields forbidden in capsule: '+','.join(bad[:10]))
    q=json.loads(json.dumps(capsule['run_quality_receipt']))
    for g in q['gates']:
        if g['gate_id']=='PERSISTENCE':g['status']='PASS';g['detail']={'atomic_write':True,'append_only_index':True}
    # recompute multidimensional status deterministically
    blocking={'PRE_RUN_INTEGRITY','POINT_IN_TIME_INTEGRITY','M1_HARD_GATE','CAUSAL_LANGUAGE','DIRECTION_AUTHORITY','APL_A_SEPARATION','REPORT_FIDELITY'}
    fails=[g['gate_id'] for g in q['gates'] if g['status']=='FAIL'];warn=[g['gate_id'] for g in q['gates'] if g['status']=='WARN']
    q['hard_failures']=fails;q['warnings']=warn
    q['status']=q['scientific_process_status']='BLOCKED' if any(x in blocking for x in fails) else ('PARTIAL' if fails else ('PASS_WITH_WARNINGS' if warn else 'PASS'))
    cap=json.loads(json.dumps(capsule));cap['run_quality_receipt']=q;cap['quality_status']=q['status'];cap.pop('capsule_hash',None);cap['capsule_hash']=_sha(cap)
    dt=_dt(cap.get('as_of'));yr=f'{dt.year:04d}' if dt.year>1 else 'UNKNOWN';mo=f'{dt.month:02d}' if dt.year>1 else '00';p=_root(data_root)/_safe_subject(cap['subject'])/yr/mo/cap['run_id']/'capsule.json';_atomic_create(p,cap)
    verify=json.loads(p.read_text(encoding='utf-8'));h=verify.pop('capsule_hash',None)
    if h!=_sha(verify):raise RuntimeError('capsule hash verification failed after write')
    row={'run_id':cap['run_id'],'request_id':cap['request_id'],'subject':cap['subject'],'as_of':cap['as_of'],'horizon':cap['horizon'],'mode':cap['mode'],'primary_research_class':cap.get('primary_research_class'),'direction':cap.get('direction'),'permission':cap.get('permission'),'quality_status':cap['quality_status'],'capsule_hash':cap['capsule_hash'],'path':str(p),'created_at':cap['created_at']}
    _append_jsonl(_root(data_root)/'index.jsonl',row);_append_jsonl(_root(data_root)/'events.jsonl',{'event':'CAPSULE_SEALED','run_id':cap['run_id'],'capsule_hash':cap['capsule_hash'],'at':now(),'path':str(p)})
    return cap,{'status':'PASS','path':str(p),'capsule_hash':cap['capsule_hash'],'index':str(_root(data_root)/'index.jsonl'),'event_log':str(_root(data_root)/'events.jsonl')}

def verify_capsule(path):
    p=Path(path)
    try:o=json.loads(p.read_text(encoding='utf-8'));h=o.pop('capsule_hash',None);ok=h==_sha(o);return {'status':'PASS' if ok else 'FAIL','path':str(p),'capsule_hash':h,'errors':[] if ok else ['CAPSULE_HASH_MISMATCH']}
    except Exception as e:return {'status':'FAIL','path':str(p),'errors':[str(e)]}

def status(data_root):
    rows=read_index(data_root);valid=[r for r in rows if r.get('integrity')!='INVALID_JSON_LINE'];last=valid[-1] if valid else None;vr=verify_capsule(last['path']) if last and last.get('path') else None
    return {'schema_version':'1.0.0','status':'PASS' if (vr is None or vr.get('status')=='PASS') else 'FAIL','run2_version':VERSION,'runs':len(valid),'latest':last,'latest_integrity':vr,'persistence_root':str(_root(data_root)),'authority':{'direction':'NONE','broker_write':'NONE','apl_a':'SHADOW_ONLY'}}
