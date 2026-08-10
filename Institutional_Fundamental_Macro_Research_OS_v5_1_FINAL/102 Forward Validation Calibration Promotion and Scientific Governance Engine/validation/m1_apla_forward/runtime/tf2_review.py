from pathlib import Path
from datetime import datetime, timezone
import json, hashlib
from .util import now,load as load_json

REVIEW_VERSION='TF2.0.0'
M1_CAPS=['CLAIM_ONTOLOGY','UNKNOWN_PRESERVATION','PROVENANCE','SOURCE_DEPENDENCY','PROXY_GOVERNANCE','CAUSAL_GOVERNANCE','CONTRADICTION_PRESERVATION','PROTOCOL_ROUTER','ESCALATION','EXCEPTIONS','QUARANTINE','LANGUAGE_DISCIPLINE','POINT_IN_TIME']
LENS_IDS=['V01_SCOPE_AND_LENS_ROUTER','V02_EPISTEMIC_FRAGILITY_AUDITOR','V03_STORY_MODEL_SOURCE_REMOVAL','V04_INVARIANT_AND_UNKNOWNS_ANALYST','V10_FRAGILITY_GEOMETRY','V11_EXPOSURE_OPTIONALITY_TAIL','V12_NETWORK_COMMON_MODE_FORCED_ACTORS','V13_INCENTIVE_TRANSFER_INTERVENTION']

def _canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def _sha(x):return 'sha256:'+hashlib.sha256(_canon(x).encode('utf-8')).hexdigest()
def _seal(obj):x=dict(obj);x.pop('seal',None);return _sha(x)
def _verify(obj):return isinstance(obj,dict) and obj.get('seal')==_seal(obj)
def _dt(s):
    if not isinstance(s,str) or not s:raise ValueError('timestamp required')
    t=s[:-1]+'+00:00' if s.endswith('Z') else s;d=datetime.fromisoformat(t)
    if d.tzinfo is None:raise ValueError('timezone-aware timestamp required')
    return d.astimezone(timezone.utc)
def _data_root(v):
    import os
    e=os.environ.get('ALPHALAB_DATA_ROOT')
    return Path(e).expanduser().resolve() if e else Path(v).resolve().parent/'AlphaLab_Data'
def _forward(v):return _data_root(v)/'forward'
def _read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def _configured_markets(v):
    try:return list(load_json(Path(v)/'RUNTIME'/'Production Commissioning'/'config'/'commissioning_policy.json').get('shadow_instruments') or [])
    except Exception:return []
def _tf_payload_ok(c):
    if 'payload_hash' not in c:return False
    return c['payload_hash']==_sha({k:c[k] for k in c if k not in ('payload_hash','seal')})
def _m1_cap(code):
    if code in ('M001_MISSING_OR_INVALID_CUTOFF','M002_LOOKAHEAD_POLICY','M010_FUTURE_INFORMATION','M050_RETROSPECTIVE_REGIME_LEAKAGE'):return 'POINT_IN_TIME'
    if code=='M011_PROVENANCE_GAP':return 'PROVENANCE'
    if code=='M012_UNKNOWN_TO_ZERO':return 'UNKNOWN_PRESERVATION'
    if code in ('M013_PROXY_CONTRACT_GAP','M015_PROXY_OUT_OF_DOMAIN','M016_PROXY_OUT_OF_HORIZON'):return 'PROXY_GOVERNANCE'
    if code=='M020_PSEUDO_INDEPENDENCE':return 'SOURCE_DEPENDENCY'
    if code in ('M030_CAUSAL_NO_MECHANISM','M031_CAUSAL_NOT_IDENTIFIED','M051_CIRCULAR_VALIDATION'):return 'CAUSAL_GOVERNANCE'
    if code in ('M061_INDIRECT_AS_DIRECT',):return 'CLAIM_ONTOLOGY'
    if code=='M062_CONTRADICTION_SUPPRESSED':return 'CONTRADICTION_PRESERVATION'
    if code in ('M070_SINGLE_HYPOTHESIS_WITHOUT_JUSTIFICATION','M071_NO_INVALIDATION_TRIGGER'):return 'ESCALATION'
    if code in ('M040_FAKE_PRECISION','M041_UNCALIBRATED_CALIBRATED_CLAIM'):return 'LANGUAGE_DISCIPLINE'
    return 'CLAIM_ONTOLOGY'
def _lens_map(v):
    base=Path(v)/'RUNTIME'/'APL-A Alpha Perspective Layer'/'prompt_registry';out={}
    for p in base.glob('*/manifest.json'):
        try:
            x=_read(p);lid=x.get('process_id') or p.parent.name
            for o in x.get('outputs',[]):out[o.get('logical_name')]=lid
        except Exception:pass
    return out

def _reviews(root,cutoff):
    by={}
    for p in sorted((root/'reviews').glob('REV_TF1_*.json')):
        try:
            r=_read(p)
            if not _verify(r):continue
            if _dt(r['reviewed_at_utc'])>cutoff:continue
            by.setdefault(r.get('commitment_id'),[]).append(r)
        except Exception:pass
    return by

def _outcomes(root,cutoff):
    out={}
    for p in sorted((root/'outcomes').glob('OUT_TF1_*.json')):
        try:
            o=_read(p)
            if not _verify(o):
                out[o.get('commitment_id') or p.stem[4:]]={'_invalid':'OUTCOME_SEAL_INVALID','raw':o};continue
            if _dt(o['linked_at_utc'])>cutoff:
                out[o.get('commitment_id')]={'_pending_at_cutoff':True,'raw':o};continue
            out[o.get('commitment_id')]=o
        except Exception as e:out[p.stem[4:]]={'_invalid':'OUTCOME_PARSE_OR_TIME_INVALID','error':str(e)}
    return out

def _classify(c,o,cutoff):
    errs=[]
    if not _verify(c) or not _tf_payload_ok(c):return 'INVALID_SEAL',['COMMITMENT_SEAL_OR_PAYLOAD_HASH_INVALID']
    try:
        seal=_dt(c['sealed_at_utc']); ac=_dt(c['analysis_cutoff_utc'])
    except Exception:return 'INVALID_TIME_ORDER',['INVALID_COMMITMENT_TIME']
    if seal>cutoff:return 'AFTER_REVIEW_CUTOFF',['SEALED_AFTER_REVIEW_CUTOFF']
    if ac>seal:return 'INVALID_TIME_ORDER',['ANALYSIS_CUTOFF_AFTER_SEAL']
    ts=c.get('truth_state')
    if ts=='SHADOW_LIVE':return 'VALID_SHADOW_LIVE',[]
    if ts!='TRUE_FORWARD':return {'WALK_FORWARD':'WALK_FORWARD','HISTORICAL_REPLAY':'HISTORICAL_REPLAY','SYNTHETIC':'SYNTHETIC'}.get(ts,'METHOD_INVALID'),['NON_TF1_TRUTH_STATE']
    if o and o.get('_invalid'):return 'INVALID_SEAL',[o['_invalid']]
    if o and o.get('_pending_at_cutoff'):return 'OUTCOME_PENDING',['OUTCOME_LINKED_AFTER_REVIEW_CUTOFF']
    if o:
        try:
            if o.get('commitment_seal')!=c.get('seal'):return 'INVALID_SEAL',['OUTCOME_COMMITMENT_SEAL_MISMATCH']
            obs=_dt(o['observed_at_utc']);linked=_dt(o['linked_at_utc'])
            if obs<=seal or linked<obs:return 'INVALID_TIME_ORDER',['OUTCOME_TIME_ORDER_INVALID']
        except Exception:return 'INVALID_TIME_ORDER',['OUTCOME_TIME_INVALID']
    return 'VALID_TRUE_FORWARD',errs

def _maturity(valid_mature,coverage,configured):
    if valid_mature<=0:return 'INSUFFICIENT'
    mk=len(coverage['markets']);rc=len(coverage['research_classes']);hz=len(coverage['horizons'])
    if mk<2 or rc<2:return 'EARLY'
    if mk>=2 and rc>=2 and hz>=2:
        if mk>=4 and rc>=4 and hz>=3:
            if configured and set(configured).issubset(set(coverage['markets'])) and rc>=6 and hz>=4:return 'SUBSTANTIAL'
            return 'MODERATE'
        return 'DEVELOPING'
    return 'EARLY'
def _labels(revs,target_type,target):
    out=[]
    for r in revs:
        a=r.get('assessment') or {}; typ=a.get('target_type'); key=a.get('capability') if target_type=='M1_CAPABILITY' else a.get('lens_id')
        if typ==target_type and key==target:out.append(r.get('classification'))
    return [x for x in out if x]
def _recommend(labels,maturity,is_apl=False):
    harmful={'FALSE_HARD_BLOCK','QUARANTINE_CAUSING_FALSE_POSITIVE','DECISION_THREATENING_FALSE_POSITIVE'}
    if harmful.intersection(labels):return 'REQUIRES_REPAIR'
    if not labels:return 'INSUFFICIENT_EVIDENCE'
    if is_apl:
        if maturity=='SUBSTANTIAL' and 'UNIQUE_VALUE' in labels and 'ACTIONABLE' in labels and 'FALSE_POSITIVE' not in labels:return 'ADVISORY_CANDIDATE'
        if maturity in ('MODERATE','SUBSTANTIAL') and ('UNIQUE_VALUE' in labels or 'ACTIONABLE' in labels) and 'FALSE_POSITIVE' not in labels:return 'RESEARCH_TRIGGER_CANDIDATE'
        return 'RETAIN_SHADOW'
    if maturity in ('MODERATE','SUBSTANTIAL') and 'TRUE_POSITIVE' in labels and 'FALSE_POSITIVE' not in labels:return 'RETAIN_CURRENT_AUTHORITY'
    return 'RETAIN_CURRENT_AUTHORITY'

def _host_state(v):
    p=_data_root(v)/'commissioning'/'host_certificate.json'
    if not p.is_file():return {'status':'HOST_CERTIFICATION_INCOMPLETE'}
    try:
        x=_read(p);return {'status':x.get('status'),'classification':x.get('classification'),'created_at_utc':x.get('created_at_utc')}
    except Exception:return {'status':'HOST_CERTIFICATE_INVALID'}
def _shadow_state(v):
    c=_data_root(v)/'commissioning'; cand=sorted(c.glob('*shadow*.json')) if c.is_dir() else []
    rows=[]
    for p in cand:
        try:
            x=_read(p);rows.append({'file':p.name,'status':x.get('status'),'classification':x.get('classification')})
        except Exception:rows.append({'file':p.name,'status':'INVALID'})
    return {'records':rows,'status':'PENDING' if not rows else ('PASS' if all(r['status']=='PASS' for r in rows) else 'PARTIAL')}

def inspect(vault_root,review_cutoff_utc=None):
    v=Path(vault_root).resolve();cut_s=review_cutoff_utc or now();cut=_dt(cut_s);root=_forward(v); root.mkdir(parents=True,exist_ok=True)
    for n in ('commitments','outcomes','reviews','locks'):(root/n).mkdir(parents=True,exist_ok=True)
    outs=_outcomes(root,cut); revs=_reviews(root,cut); rows=[];included=[];excluded=[];mature=[]
    for p in sorted((root/'commitments').glob('TF1_*.json')):
        try:c=_read(p)
        except Exception:
            excluded.append({'record_id':p.stem,'classification':'INVALID_SEAL','reasons':['COMMITMENT_PARSE_INVALID']});continue
        cid=c.get('commitment_id') or p.stem;cl,why=_classify(c,outs.get(cid),cut);reviewability=c.get('reviewability') or ('FULL_M1_APL_SNAPSHOT' if c.get('method',{}).get('findings_snapshot') is not None and c.get('apl_a',{}).get('artifact_payloads') is not None else 'LIMITED_REVIEWABILITY')
        row={'commitment_id':cid,'classification':cl,'reasons':why,'truth_state':c.get('truth_state'),'true_forward_version':c.get('true_forward_version','TF1.0.0'),'subject':c.get('subject'),'research_class':c.get('research_class'),'horizon':c.get('horizon'),'sealed_at_utc':c.get('sealed_at_utc'),'reviewability':reviewability,'commitment':c,'outcome':outs.get(cid),'reviews':revs.get(cid,[])}
        rows.append(row)
        if cl=='VALID_TRUE_FORWARD':
            included.append(cid);o=outs.get(cid)
            if o and not o.get('_pending_at_cutoff') and o.get('observation_state') in ('OBSERVABLE','PARTIALLY_OBSERVABLE'):mature.append(row)
        else:excluded.append({'record_id':cid,'classification':cl,'reasons':why})
    cov={'markets':sorted({r['subject'] for r in mature if r.get('subject')}),'research_classes':sorted({r['research_class'] for r in mature if r.get('research_class')}),'horizons':sorted({r['horizon'] for r in mature if r.get('horizon')}),'tf_versions':sorted({r['true_forward_version'] for r in mature if r.get('true_forward_version')})}
    configured=_configured_markets(v);mat=_maturity(len(mature),cov,configured)
    return {'vault':v,'cutoff':cut_s,'root':root,'rows':rows,'included':included,'excluded':excluded,'mature':mature,'coverage':cov,'configured_markets':configured,'maturity':mat,'reviews':revs}

def _m1_matrix(state):
    records=[]
    for cap in M1_CAPS:
        evidence=[];labels=[];markets=set();horizons=set();versions=set();finding_n=0
        for r in state['mature']:
            c=r['commitment'];mf=list(c.get('method',{}).get('findings_snapshot') or [])
            hits=[f for f in mf if _m1_cap(f.get('code'))==cap]
            labs=_labels(r['reviews'],'M1_CAPABILITY',cap)
            if hits or labs:
                evidence.append(r['commitment_id']);finding_n+=len(hits);labels.extend(labs);markets.add(r.get('subject'));horizons.add(r.get('horizon'));versions.add(c.get('method',{}).get('version'))
        cov={'markets':sorted(x for x in markets if x),'horizons':sorted(x for x in horizons if x),'research_classes':[]};m=_maturity(len(evidence),cov,[])
        records.append({'subject':cap,'evidence_count':len(evidence),'finding_count':finding_n,'review_labels':sorted(labels),'version_set':sorted(x for x in versions if x),'market_coverage':cov['markets'],'horizon_coverage':cov['horizons'],'maturity':m,'harmful_false_positives':sum(x in ('FALSE_HARD_BLOCK','QUARANTINE_CAUSING_FALSE_POSITIVE','DECISION_THREATENING_FALSE_POSITIVE') for x in labels),'false_negatives':sum(x=='FALSE_NEGATIVE' for x in labels),'recommendation':_recommend(labels,m,False)})
    return {'subject_type':'M1_CAPABILITY','records':records,'authority_unchanged':True}
def _apl_matrix(state,v):
    lmap=_lens_map(v);records=[]
    for lid in LENS_IDS:
        evidence=[];labels=[];markets=set();horizons=set();versions=set();inv=0;findings=0
        for r in state['mature']:
            c=r['commitment'];a=c.get('apl_a') or {};active=set(a.get('active_lenses') or (a.get('telemetry_snapshot') or {}).get('active_lenses') or []);payloads=a.get('artifact_payloads') or {}
            emitted=[n for n in payloads if lmap.get(n)==lid]
            labs=_labels(r['reviews'],'APL_A_LENS',lid)
            if lid in active:inv+=1
            if emitted or labs or lid in active:
                evidence.append(r['commitment_id']);findings+=len(emitted);labels.extend(labs);markets.add(r.get('subject'));horizons.add(r.get('horizon'));versions.add(a.get('version'))
        cov={'markets':sorted(x for x in markets if x),'horizons':sorted(x for x in horizons if x),'research_classes':[]};m=_maturity(len(evidence),cov,[])
        records.append({'subject':lid,'evidence_count':len(evidence),'invocation_count':inv,'finding_payload_count':findings,'review_labels':sorted(labels),'version_set':sorted(x for x in versions if x),'market_coverage':cov['markets'],'horizon_coverage':cov['horizons'],'maturity':m,'unique_value':sum(x=='UNIQUE_VALUE' for x in labels),'actionable':sum(x=='ACTIONABLE' for x in labels),'false_positives':sum('FALSE_POSITIVE' in str(x) for x in labels),'false_negatives':sum(x=='FALSE_NEGATIVE' for x in labels),'recommendation':_recommend(labels,m,True)})
    return {'subject_type':'APL_A_LENS','records':records,'authority_unchanged':True}
def _interaction(state,v):
    rows=[];lmap=_lens_map(v);same={'SOURCE_DEPENDENCY':{'V02_EPISTEMIC_FRAGILITY_AUDITOR','V03_STORY_MODEL_SOURCE_REMOVAL'},'UNKNOWN_PRESERVATION':{'V04_INVARIANT_AND_UNKNOWNS_ANALYST'},'CONTRADICTION_PRESERVATION':{'V04_INVARIANT_AND_UNKNOWNS_ANALYST'}}
    for r in state['mature']:
        c=r['commitment'];caps={_m1_cap(f.get('code')) for f in (c.get('method',{}).get('findings_snapshot') or [])};a=c.get('apl_a') or {};lenses=set(a.get('active_lenses') or (a.get('telemetry_snapshot') or {}).get('active_lenses') or [])
        if not caps and not lenses:rel='NONE'
        elif caps and not lenses:rel='M1_ONLY'
        elif lenses and not caps:rel='APL_ONLY'
        elif any(ls & lenses for cap,ls in same.items() if cap in caps):rel='BOTH_SAME'
        else:rel='BOTH_COMPLEMENTARY'
        rows.append({'commitment_id':r['commitment_id'],'relation':rel,'m1_capabilities':sorted(caps),'apl_lenses':sorted(lenses),'review_state':'UNRESOLVED_UNLESS_EXPLICIT_REVIEW_LABEL_EXISTS'})
    return {'records':rows,'counts':{k:sum(x['relation']==k for x in rows) for k in ['NONE','M1_ONLY','APL_ONLY','BOTH_SAME','BOTH_COMPLEMENTARY','CONFLICT']},'authority_unchanged':True}

def preflight(vault_root):
    v=Path(vault_root).resolve();checks=[]
    def ck(n,b,d=None):checks.append({'name':n,'pass':bool(b),'detail':d})
    try:tf=load_json(v/'RUNTIME'/'Production Commissioning'/'TRUE_FORWARD_MANIFEST.json');ck('tf1_present',str(tf.get('true_forward_version','')).startswith('TF1.'))
    except Exception as e:ck('tf1_present',False,str(e))
    try:fv=load_json(v/'102 Forward Validation Calibration Promotion and Scientific Governance Engine'/'validation'/'m1_apla_forward'/'M1_APLA_FORWARD_VALIDATION_MANIFEST.json');ck('fv1_present',fv.get('version')=='FV1.0.0')
    except Exception as e:ck('fv1_present',False,str(e))
    try:m=load_json(v/'RUNTIME'/'Core Research Method Kernel'/'METHOD_KERNEL_MANIFEST.json');ck('m1_authority_unchanged',m.get('authority',{}).get('direction')=='NONE')
    except Exception as e:ck('m1_authority_unchanged',False,str(e))
    try:a=load_json(v/'RUNTIME'/'APL-A Alpha Perspective Layer'/'APL_A_MANIFEST.json');ck('apl_shadow_only',a.get('mode')=='SHADOW_ONLY' and a.get('authority',{}).get('direction')=='NONE')
    except Exception as e:ck('apl_shadow_only',False,str(e))
    ck('no_apl_b',not any(p.is_dir() and 'APL-B' in p.name for p in (v/'RUNTIME').iterdir()))
    cp=load_json(v/'CURRENT_PRODUCTION_MANIFEST.json');ck('direction_fundamental_only',cp.get('decision_authority',{}).get('direction')=='FUNDAMENTAL_ONLY')
    needed=['TF2_TRUE_FORWARD_REVIEW_MANIFEST.json','schemas/AlphaLab_D4_TF2_Review_Snapshot.schema.json','schemas/AlphaLab_D4_TF2_Readiness_Matrix.schema.json','config/tf2_review_policy.json'];base=v/'102 Forward Validation Calibration Promotion and Scientific Governance Engine'/'validation'/'m1_apla_forward';ck('tf2_source_present',all((base/x).is_file() for x in needed))
    rb=load_json(v/'RUNTIME'/'R4 Scientific Certification and Reproducibility Hardening'/'config'/'certification_surface_baseline.json');volatile=[k for k in rb.get('files',{}) if 'AlphaLab_Data/' in k or '__pycache__' in k or k.endswith('.pyc')];ck('r4_excludes_mutable_forward',not volatile,volatile)
    bad=[x for x in checks if not x['pass']];return {'status':'PASS' if not bad else 'FAIL','review_version':REVIEW_VERSION,'checks':checks,'errors':[x['name'] for x in bad]}

def build_snapshot(vault_root,review_cutoff_utc=None,store=True):
    v=Path(vault_root).resolve();pf=preflight(v)
    if pf['status']!='PASS':raise RuntimeError('TF2 preflight failed: '+','.join(pf['errors']))
    st=inspect(v,review_cutoff_utc);m1=_m1_matrix(st);apl=_apl_matrix(st,v);inter=_interaction(st,v)
    valid_tf=len(st['included']);mature=len(st['mature'])
    if valid_tf==0:fd='FORWARD_DATA_NOT_YET_AVAILABLE'
    elif mature==0:fd='OUTCOME_MATURITY_PENDING'
    else:fd='TRUE_FORWARD_'+st['maturity']
    repairs=[]
    if any(r['recommendation']=='REQUIRES_REPAIR' for r in m1['records']+apl['records']):repairs.append('CURRENT_LAYER_REPAIR_REQUIRED')
    if any(x['classification'] in ('INVALID_SEAL','INVALID_TIME_ORDER') for x in st['excluded']):repairs.append('FORWARD_INTEGRITY_REVIEW_REQUIRED')
    if 'FORWARD_INTEGRITY_REVIEW_REQUIRED' in repairs:next_gate='REPAIR_FORWARD_INTEGRITY'
    elif 'CURRENT_LAYER_REPAIR_REQUIRED' in repairs:next_gate='REPAIR_CURRENT_LAYERS_AND_GATHER_NEW_FORWARD_EVIDENCE'
    elif st['maturity'] in ('MODERATE','SUBSTANTIAL'):next_gate='SELECTIVE_AUTHORITY_CERTIFICATION_CANDIDATE_REVIEW_ONLY'
    else:next_gate='CONTINUE_TF1_TRUE_FORWARD_ACCUMULATION'
    coverage={**st['coverage'],'configured_markets':st['configured_markets'],'valid_true_forward_count':valid_tf,'mature_true_forward_count':mature,'limited_reviewability_count':sum(r['reviewability']!='FULL_M1_APL_SNAPSHOT' for r in st['rows'] if r['classification']=='VALID_TRUE_FORWARD')}
    core={'schema_version':'1.0.0','review_version':REVIEW_VERSION,'review_cutoff_utc':st['cutoff'],'created_at_utc':now(),'forward_data_state':fd,'maturity':st['maturity'],'coverage':coverage,'record_forensics':{'included_record_ids':st['included'],'excluded_records':st['excluded'],'classification_counts':{k:sum(r['classification']==k for r in st['rows']) for k in sorted({r['classification'] for r in st['rows']})},'legacy_limited_reviewability_preserved':True},'m1_readiness':m1,'apl_a_readiness':apl,'interaction':inter,'host':_host_state(v),'shadow_universe':_shadow_state(v),'repair_candidates':repairs,'authority':{'direction':'UNCHANGED_FUNDAMENTAL_ONLY','permission':'UNCHANGED','broker_write':'NONE','apl_a':'SHADOW_ONLY','m1_new_direction_authority':'NONE','auto_promotion':False},'apl_b':'NOT_IMPLEMENTED','next_gate':next_gate,'source_versions':{'m1':'M1.0.1','apl_a':'APL-A 1.0.0','fv1':'FV1.0.0','tf1_current':'TF1.0.1'}}
    core['review_id']='TF2_'+hashlib.sha256(_canon({'cutoff':core['review_cutoff_utc'],'included':core['record_forensics']['included_record_ids'],'excluded':core['record_forensics']['excluded_records'],'versions':core['source_versions']}).encode('utf-8')).hexdigest()[:20]
    core['seal']=_seal(core)
    if store:
        p=_forward(v)/'reviews'/(core['review_id']+'.json');p.parent.mkdir(parents=True,exist_ok=True)
        if p.exists():
            old=_read(p)
            if not _verify(old):raise RuntimeError('existing immutable TF2 review seal invalid')
            return {'status':'PASS','review':old}
        else:
            import os,tempfile
            fd,tmp=tempfile.mkstemp(prefix='.'+p.name+'.',suffix='.tmp',dir=str(p.parent));os.close(fd);t=Path(tmp)
            try:
                t.write_text(json.dumps(core,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');os.replace(str(t),str(p))
            finally:
                if t.exists():t.unlink()
        core['path']=str(p)
    return {'status':'PASS','review':core}

def latest(vault_root):
    v=Path(vault_root).resolve();p=_forward(v)/'reviews';rows=[]
    for f in sorted(p.glob('TF2_*.json')) if p.is_dir() else []:
        try:
            x=_read(f);rows.append({'review_id':x.get('review_id'),'review_cutoff_utc':x.get('review_cutoff_utc'),'forward_data_state':x.get('forward_data_state'),'maturity':x.get('maturity'),'seal_valid':_verify(x),'path':str(f)})
        except Exception:pass
    return {'status':'PASS','review_version':REVIEW_VERSION,'reviews':rows,'latest':rows[-1] if rows else None}

def selftest(vault_root):
    import tempfile,os,shutil
    v=Path(vault_root).resolve();checks=[]
    def ck(n,b,d=None):checks.append({'name':n,'pass':bool(b),'detail':d})
    ck('preflight',preflight(v)['status']=='PASS')
    td=Path(tempfile.mkdtemp(prefix='alphalab_tf2_'));old=os.environ.get('ALPHALAB_DATA_ROOT');os.environ['ALPHALAB_DATA_ROOT']=str(td)
    try:
        s=build_snapshot(v,'2026-08-10T10:00:00Z',store=False)['review'];ck('empty_evidence_truthful',s['forward_data_state']=='FORWARD_DATA_NOT_YET_AVAILABLE' and s['maturity']=='INSUFFICIENT');ck('authority_unchanged',s['authority']['broker_write']=='NONE' and s['authority']['apl_a']=='SHADOW_ONLY');ck('no_score_collapse',not any('score' in k.lower() for k in s.keys()));ck('next_gate_accumulation',s['next_gate']=='CONTINUE_TF1_TRUE_FORWARD_ACCUMULATION')
        s2=build_snapshot(v,'2026-08-10T10:00:00Z',store=True)['review'];s3=build_snapshot(v,'2026-08-10T10:00:00Z',store=True)['review'];ck('review_immutable_reproducible',s2['review_id']==s3['review_id'] and s2['seal']==s3['seal'])
    finally:
        if old is None:os.environ.pop('ALPHALAB_DATA_ROOT',None)
        else:os.environ['ALPHALAB_DATA_ROOT']=old
        shutil.rmtree(td,ignore_errors=True)
    ck('apl_b_absent',not any(p.is_dir() and 'APL-B' in p.name for p in (v/'RUNTIME').iterdir()))
    bad=[x for x in checks if not x['pass']];return {'status':'PASS' if not bad else 'FAIL','review_version':REVIEW_VERSION,'passed':len(checks)-len(bad),'total':len(checks),'checks':checks,'errors':[x['name'] for x in bad]}
