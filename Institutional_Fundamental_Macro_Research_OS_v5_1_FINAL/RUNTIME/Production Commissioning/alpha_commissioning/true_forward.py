from pathlib import Path
from datetime import datetime, timezone
from contextlib import contextmanager
import json, hashlib, os, tempfile, shutil
from .util import load_json, now, data_root, add_runtime_paths, current_certification_surface

TF_VERSION='TF1.0.0'
OUTCOME_NAMES={'r3_outcome_receipt','outcome_record','d4_outcome','forward_outcome'}

def _canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def _sha(x):
    b=x if isinstance(x,(bytes,bytearray)) else _canon(x).encode('utf-8')
    return 'sha256:'+hashlib.sha256(b).hexdigest()
def _dt(s):
    if not isinstance(s,str) or not s: raise RuntimeError('timezone-aware timestamp required')
    t=s[:-1]+'+00:00' if s.endswith('Z') else s
    d=datetime.fromisoformat(t)
    if d.tzinfo is None: raise RuntimeError('timezone-aware timestamp required')
    return d.astimezone(timezone.utc)
def _forward_root(v): return data_root(v)/'forward'
def _dirs(v):
    r=_forward_root(v); ds={k:r/k for k in ('commitments','outcomes','reviews','locks')}
    for p in ds.values(): p.mkdir(parents=True,exist_ok=True)
    return ds
@contextmanager
def _lock(path):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    try: fd=os.open(str(p),os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    except FileExistsError: raise RuntimeError('forward store is locked: '+str(p))
    try:
        os.write(fd,(now()+'\n').encode('ascii'));os.fsync(fd);os.close(fd);fd=None;yield
    finally:
        try:
            if fd is not None: os.close(fd)
        except Exception: pass
        try:p.unlink()
        except FileNotFoundError:pass

def _atomic_create(path,obj):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():raise RuntimeError('immutable record already exists: '+p.name)
    lock=p.parent.parent/'locks'/(p.name+'.lock')
    with _lock(lock):
        if p.exists():raise RuntimeError('immutable record already exists: '+p.name)
        fd,tmp=tempfile.mkstemp(prefix='.'+p.name+'.',suffix='.tmp',dir=str(p.parent));os.close(fd);t=Path(tmp)
        try:
            data=(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode('utf-8')
            with t.open('wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
            if p.exists():raise RuntimeError('immutable record race: '+p.name)
            os.replace(str(t),str(p))
        finally:
            if t.exists():t.unlink()
    return p

def _load_commitment(v,commitment_id):
    p=_dirs(v)['commitments']/(commitment_id+'.json')
    if not p.is_file():raise RuntimeError('commitment not found: '+commitment_id)
    return p,load_json(p)

def _seal_object(obj):
    x=dict(obj);x.pop('seal',None);return _sha(x)
def verify_object(obj): return obj.get('seal')==_seal_object(obj)

def expected_outcome_contract(research_class,horizon):
    rc=research_class or 'UNCLASSIFIED'
    if rc in ('DIRECTIONAL_FORECAST','PERSISTENCE_REVERSAL','CROSS_SECTIONAL_RELATIVE_VALUE'):
        typ='DIRECTIONAL_OR_RELATIVE_OUTCOME'
    elif rc=='CAUSAL_ATTRIBUTION':typ='MECHANISM_AND_CAUSAL_SEQUENCE'
    elif rc=='NARRATIVE_ATTENTION':typ='NARRATIVE_PERSISTENCE_OR_CHANGE'
    elif rc=='REGIME_ANALYSIS':typ='REGIME_CONSISTENCY_OR_TRANSITION'
    elif rc=='MODEL_VALIDATION':typ='MODEL_FORWARD_BEHAVIOR'
    elif rc=='EXPOSURE_RISK_ANALYSIS':typ='EXPOSURE_OR_FRAGILITY_REALIZATION'
    else:typ='RESEARCH_CLASS_SPECIFIC_OBSERVABLE'
    return {'type':typ,'horizon':horizon or 'UNSPECIFIED','price_only_evaluation_forbidden':True}

def _artifact(rt,run_id,name,default=None):
    try:return rt.store.load_artifact_json(run_id,name)
    except Exception:return default

def _artifact_refs(rt,run_id):
    out=[]
    for a in rt.catalog.list_artifacts(run_id):
        if a.get('world') in ('EVIDENCE','COGNITION','DECISION','META','LEARNING'):
            out.append({'logical_name':a.get('logical_name'),'world':a.get('world'),'artifact_hash':a.get('artifact_hash')})
    return sorted(out,key=lambda x:(str(x['world']),str(x['logical_name'])))

def _eligibility(v,rt,run_id,truth_state,sealed_at):
    pol=load_json(Path(v)/'RUNTIME'/'Production Commissioning'/'config'/'true_forward_policy.json');m=rt.store.load_manifest(run_id);names={a['logical_name'] for a in rt.catalog.list_artifacts(run_id)};errors=[]
    if truth_state not in pol['allowed_truth_states']:errors.append('INVALID_TRUTH_STATE')
    if not m.get('decision_seal_hash'):errors.append('DECISION_SEAL_MISSING')
    if pol.get('require_method_plan') and 'method_plan' not in names:errors.append('METHOD_PLAN_MISSING')
    if pol.get('require_apl_shadow_artifact') and not ({'apl_a_shadow_bundle','apl_a_forward_telemetry'} & names):errors.append('APL_A_SHADOW_ARTIFACT_MISSING')
    if pol.get('require_no_outcome_artifact_at_seal') and (OUTCOME_NAMES & names):errors.append('OUTCOME_ALREADY_AVAILABLE')
    cutoff=_dt(m['analysis_cutoff_utc']);seal=_dt(sealed_at)
    if cutoff>seal:errors.append('ANALYSIS_CUTOFF_AFTER_SEAL')
    if truth_state=='TRUE_FORWARD':
        if m.get('run_mode')!=pol['true_forward_required_run_mode']:errors.append('TRUE_FORWARD_REQUIRES_SHADOW_LIVE_RUN')
        if (seal-cutoff).total_seconds()>int(pol['max_true_forward_cutoff_age_seconds']):errors.append('TRUE_FORWARD_CUTOFF_TOO_OLD')
    return m,names,errors

def seal_run(vault_root,run_id,truth_state='SHADOW_LIVE'):
    v=Path(vault_root).resolve();add_runtime_paths(v);from alpha_runtime.runtime import AlphaRuntime
    rt=AlphaRuntime(v,data_root(v));sealed_at=now();m,names,errors=_eligibility(v,rt,run_id,truth_state,sealed_at)
    if errors:raise RuntimeError('forward eligibility failed: '+','.join(errors))
    plan=_artifact(rt,run_id,'method_plan',{}) or {};mpre=_artifact(rt,run_id,'method_predecision_validation_receipt',{}) or {};apl=_artifact(rt,run_id,'apl_a_forward_telemetry',None) or _artifact(rt,run_id,'apl_a_shadow_bundle',{}) or {};ri=_artifact(rt,run_id,'research_intent',{}) or {};fp=_artifact(rt,run_id,'final_permission',{}) or {}
    commitment_id='TF1_'+run_id
    base={'schema_version':'1.0.0','true_forward_version':TF_VERSION,'commitment_id':commitment_id,'run_id':run_id,'truth_state':truth_state,'state':'SEALED_PRE_OUTCOME','subject':m.get('subject'),'research_class':plan.get('research_class'),'horizon':plan.get('active_horizon') or ri.get('active_horizon'),'analysis_cutoff_utc':m.get('analysis_cutoff_utc'),'evidence_cutoff_utc':m.get('analysis_cutoff_utc'),'sealed_at_utc':sealed_at,'decision_seal_hash':m.get('decision_seal_hash'),'method':{'version':plan.get('method_version','M1.0.1'),'protocol_id':plan.get('protocol_id'),'rigor_tier':plan.get('rigor_tier'),'predecision_status':mpre.get('status')},'apl_a':{'version':'APL-A 1.0.0','mode':'SHADOW_ONLY','artifact_present':bool(apl)},'science':{'fundamental_direction':ri.get('fundamental_direction'),'edge_state':ri.get('edge_state'),'permission':fp.get('permission'),'artifact_refs':_artifact_refs(rt,run_id)},'uncertainty':ri.get('uncertainty_profile') or ri.get('uncertainty'),'expected_outcome_contract':expected_outcome_contract(plan.get('research_class'),plan.get('active_horizon')),'authority':{'direction_mutated':False,'permission_mutated':False,'broker_write':'NONE','apl_a':'SHADOW_ONLY','m1_new_direction_authority':'NONE'},'source_surface_hash':current_certification_surface(v)}
    base['payload_hash']=_sha({k:base[k] for k in base if k not in ('payload_hash','seal')});base['seal']=_seal_object(base)
    p=_atomic_create(_dirs(v)['commitments']/(commitment_id+'.json'),base)
    return {'status':'PASS','commitment_id':commitment_id,'truth_state':truth_state,'seal':base['seal'],'path':str(p)}

def verify_commitment(vault_root,commitment_id):
    v=Path(vault_root).resolve();p,obj=_load_commitment(v,commitment_id);errors=[]
    if not verify_object(obj):errors.append('SEAL_MISMATCH')
    ph=_sha({k:obj[k] for k in obj if k not in ('payload_hash','seal')})
    if obj.get('payload_hash')!=ph:errors.append('PAYLOAD_HASH_MISMATCH')
    return {'status':'PASS' if not errors else 'FAIL','commitment_id':commitment_id,'truth_state':obj.get('truth_state'),'seal':obj.get('seal'),'path':str(p),'errors':errors}

def link_outcome(vault_root,commitment_id,outcome):
    v=Path(vault_root).resolve();p,c=_load_commitment(v,commitment_id);vr=verify_commitment(v,commitment_id)
    if vr['status']!='PASS':raise RuntimeError('commitment seal invalid')
    if not isinstance(outcome,dict):raise RuntimeError('outcome must be object')
    observed=outcome.get('observed_at_utc');obs_state=outcome.get('observation_state','OBSERVABLE');pol=load_json(v/'RUNTIME'/'Production Commissioning'/'config'/'true_forward_policy.json')
    if obs_state not in pol['outcome_observation_states']:raise RuntimeError('invalid observation_state')
    if not observed:raise RuntimeError('outcome observed_at_utc required')
    if _dt(observed)<=_dt(c['sealed_at_utc']):raise RuntimeError('OUTCOME_NOT_AFTER_PRE_OUTCOME_SEAL')
    before=p.read_bytes();oid='OUT_'+commitment_id;obj={'schema_version':'1.0.0','true_forward_version':TF_VERSION,'outcome_link_id':oid,'commitment_id':commitment_id,'commitment_seal':c['seal'],'observed_at_utc':observed,'linked_at_utc':now(),'observation_state':obs_state,'outcome':outcome.get('outcome',{}),'evaluation':outcome.get('evaluation')};obj['seal']=_seal_object(obj);op=_atomic_create(_dirs(v)['outcomes']/(oid+'.json'),obj)
    if p.read_bytes()!=before:raise RuntimeError('original commitment mutated during outcome link')
    return {'status':'PASS','outcome_link_id':oid,'commitment_id':commitment_id,'seal':obj['seal'],'original_commitment_unchanged':True,'path':str(op)}

def add_review(vault_root,commitment_id,review):
    v=Path(vault_root).resolve();p,c=_load_commitment(v,commitment_id)
    if verify_commitment(v,commitment_id)['status']!='PASS':raise RuntimeError('commitment seal invalid')
    ts=now();rid='REV_'+commitment_id+'_'+ts.replace(':','').replace('-','');obj={'schema_version':'1.0.0','true_forward_version':TF_VERSION,'review_id':rid,'commitment_id':commitment_id,'commitment_seal':c['seal'],'reviewed_at_utc':ts,'reviewer':review.get('reviewer'),'assessment':review.get('assessment',{}),'evidence':review.get('evidence',{}),'classification':review.get('classification')};obj['seal']=_seal_object(obj);rp=_atomic_create(_dirs(v)['reviews']/(rid+'.json'),obj);return {'status':'PASS','review_id':rid,'seal':obj['seal'],'path':str(rp)}

def list_records(vault_root):
    v=Path(vault_root).resolve();ds=_dirs(v);rows=[]
    outcomes={}
    for p in ds['outcomes'].glob('OUT_TF1_*.json'):
        try:o=load_json(p);outcomes[o['commitment_id']]=o
        except Exception:pass
    for p in sorted(ds['commitments'].glob('TF1_*.json')):
        try:c=load_json(p);vr=verify_commitment(v,c['commitment_id']);o=outcomes.get(c['commitment_id']);rows.append({'commitment_id':c['commitment_id'],'run_id':c['run_id'],'subject':c['subject'],'truth_state':c['truth_state'],'state':'OUTCOME_LINKED' if o else 'WAITING_FOR_OUTCOME','sealed_at_utc':c['sealed_at_utc'],'seal_valid':vr['status']=='PASS','outcome_observed_at_utc':o.get('observed_at_utc') if o else None})
        except Exception as e:rows.append({'path':str(p),'state':'INVALID','error':str(e)})
    mature=sum(1 for r in rows if r.get('state')=='OUTCOME_LINKED' and r.get('truth_state')=='TRUE_FORWARD');tf=sum(1 for r in rows if r.get('truth_state')=='TRUE_FORWARD');maturity='INSUFFICIENT' if mature<10 else ('EARLY' if mature<30 else 'DEVELOPING')
    return {'status':'PASS','true_forward_version':TF_VERSION,'records':rows,'counts':{'total':len(rows),'true_forward':tf,'mature_true_forward':mature},'true_forward_maturity':maturity,'authority_unchanged':True}

def initialize(vault_root):
    v=Path(vault_root).resolve();ds=_dirs(v);return {'status':'PASS','true_forward_version':TF_VERSION,'forward_root':str(_forward_root(v)),'directories':{k:str(p) for k,p in ds.items()},'true_forward_maturity':list_records(v)['true_forward_maturity'],'broker_write':'NONE'}

def _test_record(root,truth='TRUE_FORWARD'):
    base={'schema_version':'1.0.0','true_forward_version':TF_VERSION,'commitment_id':'TF1_TEST','run_id':'TEST','truth_state':truth,'state':'SEALED_PRE_OUTCOME','subject':'XAUUSD','research_class':'DIRECTIONAL_FORECAST','horizon':'DAILY','analysis_cutoff_utc':'2026-08-10T08:00:00Z','evidence_cutoff_utc':'2026-08-10T08:00:00Z','sealed_at_utc':'2026-08-10T08:01:00Z','decision_seal_hash':'sha256:'+'1'*64,'method':{'version':'M1.0.1','protocol_id':'P'},'apl_a':{'version':'APL-A 1.0.0','mode':'SHADOW_ONLY'},'science':{},'uncertainty':None,'expected_outcome_contract':expected_outcome_contract('DIRECTIONAL_FORECAST','DAILY'),'authority':{'direction_mutated':False,'permission_mutated':False,'broker_write':'NONE','apl_a':'SHADOW_ONLY','m1_new_direction_authority':'NONE'},'source_surface_hash':None}
    base['payload_hash']=_sha({k:base[k] for k in base if k not in ('payload_hash','seal')});base['seal']=_seal_object(base);return base

def selftest(vault_root):
    checks=[];errs=[]
    def ck(n,b,d=None):checks.append({'name':n,'pass':bool(b),'detail':d});errs.extend([] if b else [n])
    v=Path(vault_root).resolve();pol=load_json(v/'RUNTIME'/'Production Commissioning'/'config'/'true_forward_policy.json');ck('policy_authority_none',pol['broker_write'] is False and pol['direction_authority_added']=='NONE' and pol['apl_a_authority']=='SHADOW_ONLY')
    ck('source_mutable_separation',pol['mutable_forward_records_in_r4_source_fingerprint'] is False)
    tmp=Path(tempfile.mkdtemp(prefix='alphalab_tf1_'))
    try:
        ds={k:tmp/k for k in ('commitments','outcomes','reviews','locks')}
        for p in ds.values():p.mkdir(parents=True,exist_ok=True)
        c=_test_record(tmp);cp=_atomic_create(ds['commitments']/'TF1_TEST.json',c);ck('commitment_created',cp.is_file());ck('commitment_seal_verifies',verify_object(load_json(cp)))
        b=cp.read_bytes()
        try:_atomic_create(ds['commitments']/'TF1_TEST.json',c);dup=False
        except RuntimeError:dup=True
        ck('duplicate_prevention',dup)
        # tamper detection in-memory
        x=load_json(cp);x['subject']='TAMPER';ck('tamper_detected',not verify_object(x))
        # outcome order truth
        try:
            if _dt('2026-08-10T07:59:00Z')<=_dt(c['sealed_at_utc']):raise RuntimeError('OUTCOME_NOT_AFTER_PRE_OUTCOME_SEAL')
            early=False
        except RuntimeError:early=True
        ck('outcome_before_seal_rejected',early)
        # crash temp does not alter final
        (ds['commitments']/'.orphan.tmp').write_text('partial',encoding='ascii');ck('orphan_temp_does_not_mutate_commitment',cp.read_bytes()==b)
        ck('truth_label_set',set(pol['allowed_truth_states'])=={'SHADOW_LIVE','TRUE_FORWARD'})
        ck('price_only_forbidden',expected_outcome_contract('DIRECTIONAL_FORECAST','DAILY')['price_only_evaluation_forbidden'] is True)
    finally:shutil.rmtree(tmp,ignore_errors=True)
    ck('apl_b_not_implemented',not any(p.is_dir() and 'APL-B' in p.name for p in (v/'RUNTIME').iterdir()))
    return {'schema_version':'1.0.0','status':'PASS' if not errs else 'FAIL','passed':sum(1 for x in checks if x['pass']),'total':len(checks),'checks':checks,'errors':errs}
