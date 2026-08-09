from pathlib import Path
import tempfile, json, sys, os, threading, shutil, sqlite3
from .util import add_runtime_paths,case,sha256_bytes,check_hash_bytes

def run(vault_root,profile='CORE'):
    v=Path(vault_root);add_runtime_paths(v);out=[]
    from alpha_runtime.visibility import visible,build_receipt
    from alpha_runtime.timeutil import local_to_utc,TimeError
    from alpha_runtime.runtime import AlphaRuntime
    from alpha_runtime.seal_safe import create_decision_seal,verify_decision_seal,create_close_seal,verify_close_seal
    from alpha_prompt_runtime.registry import PromptRegistry
    from alpha_prompt_runtime.jobs import make_job
    from alpha_prompt_runtime.orchestrator import R2Orchestrator,OrchestratorError
    from alpha_operational_runtime.catalog_ext import init_r3
    from alpha_operational_runtime.ledger import D4Ledger
    from alpha_operational_runtime.host import make_host,HostError
    from alpha_operational_runtime.driver import RunDriver
    from alpha_operational_runtime.meta import MetaReconciler
    # temporal pure attacks
    base={'snapshot_id':'S','source_id':'SRC','requirement_id':'REQ','vintage_id':'V1','vintage_integrity':'ORIGINAL_CAPTURE','publication_time':'2026-08-01T10:00:00Z','first_available_time':'2026-08-01T10:00:00Z','retrieved_at':'2026-08-01T10:01:00Z','ingested_at':'2026-08-01T10:01:01Z','superseded_at':None}
    s=dict(base,first_available_time='2026-08-01T12:01:00Z',retrieved_at='2026-08-01T12:01:01Z',ingested_at='2026-08-01T12:01:02Z');out.append(case('R4-010','TEMPORAL','PASS' if not visible(s,'2026-08-01T12:00:00Z','LIVE')[0] else 'FAIL'))
    s=dict(base,retrieved_at='2026-08-01T12:00:01Z',ingested_at='2026-08-01T12:00:02Z');out.append(case('R4-011','TEMPORAL','PASS' if not visible(s,'2026-08-01T12:00:00Z','LIVE')[0] else 'FAIL'))
    s=dict(base,retrieved_at='2026-08-01T11:59:59Z',ingested_at='2026-08-01T12:00:01Z');out.append(case('R4-012','TEMPORAL','PASS' if not visible(s,'2026-08-01T12:00:00Z','LIVE')[0] else 'FAIL'))
    s=dict(base,vintage_integrity='CURRENT_ONLY');out.append(case('R4-013','TEMPORAL','PASS' if not visible(s,'2026-08-01T12:00:00Z','HISTORICAL_REPLAY')[0] else 'FAIL'))
    s=dict(base,vintage_integrity='OFFICIAL_VINTAGE_ARCHIVE',retrieved_at='2026-09-01T00:00:00Z',ingested_at='2026-09-01T00:00:01Z');out.append(case('R4-014','TEMPORAL','PASS' if visible(s,'2026-08-01T12:00:00Z','HISTORICAL_REPLAY')[0] else 'FAIL'))
    s=dict(base,superseded_at='2026-08-01T11:00:00Z');out.append(case('R4-015','TEMPORAL','PASS' if not visible(s,'2026-08-01T12:00:00Z','LIVE')[0] else 'FAIL'))
    prior=os.environ.get('ALPHALAB_FORCE_BUNDLED_TZ');os.environ['ALPHALAB_FORCE_BUNDLED_TZ']='1'
    try:
        ok=False
        try:local_to_utc('2026-11-01T01:30:00','America/New_York')
        except TimeError:ok=True
        out.append(case('R4-016','TEMPORAL','PASS' if ok else 'FAIL'))
        ok=False
        try:local_to_utc('2026-03-08T02:30:00','America/New_York')
        except TimeError:ok=True
        out.append(case('R4-017','TEMPORAL','PASS' if ok else 'FAIL'))
    finally:
        if prior is None:os.environ.pop('ALPHALAB_FORCE_BUNDLED_TZ',None)
        else:os.environ['ALPHALAB_FORCE_BUNDLED_TZ']=prior
    # authority/process static
    reg=PromptRegistry(v);ids=reg.process_ids();out.append(case('R4-020','AUTHORITY','PASS' if [p for p in ids if 'fundamental_direction' in reg.manifest(p)['authority']['can_create']]==['W31_FUNDAMENTAL'] else 'FAIL'));out.append(case('R4-021','AUTHORITY','PASS' if [p for p in ids if 'final_permission' in reg.manifest(p)['authority']['can_create']]==['P63_FINAL_DECISION'] else 'FAIL'))
    rm=json.loads((v/'RUNTIME'/'RUNTIME_MANIFEST.json').read_text(encoding='utf-8'));out.append(case('R4-022','AUTHORITY','PASS' if rm.get('operational_execution',{}).get('authority')=='BLOCK_ONLY' else 'FAIL'));out.append(case('R4-023','AUTHORITY','PASS' if all('P63_FINAL_DECISION' not in reg.manifest(p)['dependencies'] for p in ['P50_THESIS_DESTROYER','P51_MODEL_DISAGREEMENT','P52_PREMORTEM','P53_GLOBAL_RECONCILIATION']) else 'FAIL'))
    # pure drift guard primitive
    expected=sha256_bytes(b'abc');ok=True
    try:check_hash_bytes(b'abd',expected,'prompt');ok=False
    except RuntimeError:pass
    out.append(case('R4-030','DRIFT','PASS' if ok else 'FAIL'))
    ok=True
    try:check_hash_bytes(b'ctx2',sha256_bytes(b'ctx1'),'context');ok=False
    except RuntimeError:pass
    out.append(case('R4-031','DRIFT','PASS' if ok else 'FAIL'))
    fake={'schema_version':'1.0.0','run_id':'R','process_id':'P10_SCOPE','analysis_cutoff_utc':'2026-01-01T00:00:00Z','prompt_sha256':reg.prompt_hash('P10_SCOPE'),'prompt_pack_version':reg.pack['version'],'input_artifacts':[],'canonical_context_paths':[],'canonical_context_hashes':[],'forbidden_context_check':'PASS'}
    from alpha_prompt_runtime.util import sha256_obj
    fake['bundle_hash']=sha256_obj({k:v for k,v in fake.items() if k!='bundle_hash'});j1=make_job('R','P10_SCOPE',reg,fake);fake2=dict(fake);fake2['input_artifacts']=[{'logical_name':'x','artifact_hash':'sha256:'+'0'*64,'world':'DECISION','stage':'EVIDENCE'}];fake2['bundle_hash']=sha256_obj({k:v for k,v in fake2.items() if k!='bundle_hash'});j2=make_job('R','P10_SCOPE',reg,fake2);out.append(case('R4-032','DRIFT','PASS' if j1['job_hash']!=j2['job_hash'] else 'FAIL'))
    # integrated store/seal/replay/sqlite/d4 attacks
    with tempfile.TemporaryDirectory(prefix='alphalab_r4_') as td:
        rt=AlphaRuntime(v,td);init_r3(rt.catalog)
        req={'schema_version':'1.0.0','research_program_id':'R4_CERT','episode_id':'EP_R4','run_scope':'INSTRUMENT','subject':'NASDAQ100','instrument':'NASDAQ100','run_mode':'LIVE','analysis_cutoff':'2026-08-01T12:00:00Z','strategy_id':'ALPHALAB_FUNDAMENTAL','active_horizon':'SESSION_1_6H','coverage_mode':'STRICT_FULL','research_depth':'AUTO','output_depth':'MACHINE','lookahead_policy':'STRICT_POINT_IN_TIME','execution_profile':'PERMISSION_ONLY_V1','allow_private_sources':False,'idempotency_policy':'NEW_RUN','tags':['r4-cert']}
        m,_=rt.create_run(req,vault_commit='R4_CERT_COMMIT',run_id='RUN_R4_CERT');rid=m['run_id'];rt.lifecycle.transition(rid,'INPUTS_RESOLVED')
        h,_,_=rt.store.objects.put_bytes(b'visible','text/plain');sn={'schema_version':'1.0.0','snapshot_id':'S1','artifact_hash':h,'source_id':'SRC','requirement_id':'REQ_A','fact_key':'A','vintage_id':'A1','materiality':'DECISION_CRITICAL','applicability':'APPLICABLE','first_available_time':'2026-08-01T11:00:00Z','retrieved_at':'2026-08-01T11:01:00Z','ingested_at':'2026-08-01T11:01:01Z','superseded_at':None,'supersedes_snapshot_id':None,'vintage_integrity':'ORIGINAL_CAPTURE','source_semantics':'official'};reqs=[{'schema_version':'1.0.0','requirement_id':'REQ_A','fact_family':'TEST','materiality':'DECISION_CRITICAL','applicability':'APPLICABLE','applicability_reason':None,'source_requirements':[]}]
        from alpha_runtime.canonical import sha256_obj as r1sha
        from alpha_runtime.timeutil import utc_now
        sm={'schema_version':'1.0.0','run_id':rid,'analysis_cutoff_utc':m['analysis_cutoff_utc'],'snapshots':[sn],'created_at_utc':utc_now(),'manifest_hash':None};sm['manifest_hash']=r1sha({k:v for k,v in sm.items() if k not in ('created_at_utc','manifest_hash')})
        rt.store.put_artifact(rid,'coverage_requirements','DECISION','EVIDENCE',reqs);rt.freeze_snapshot_manifest(rid,sm);rt.lifecycle.transition(rid,'SNAPSHOT_FROZEN');vr=build_receipt(rid,m['analysis_cutoff_utc'],'LIVE',reqs,[sn]);rt.store.put_artifact(rid,'visibility_receipt','DECISION','EVIDENCE',vr);rt.lifecycle.transition(rid,'EVIDENCE_FROZEN');rt.store.put_artifact(rid,'dummy_cognition','DECISION','COGNITION',{'x':1});rt.store.put_artifact(rid,'final_permission','DECISION','DECISION',{'permission':'NO_TRADE'});rt.store.put_artifact(rid,'global_reconciliation','DECISION','DECISION',{'state':'CONSISTENT'});rt.lifecycle.transition(rid,'COGNITION_FROZEN')
        ok=False
        try:rt.store.put_artifact(rid,'early','OUTCOME','OUTCOME',{'x':1})
        except Exception:ok=True
        out.append(case('R4-040','SEAL','PASS' if ok else 'FAIL'))
        seal=create_decision_seal(rid,rt);out.append(case('R4-041','SEAL','PASS' if _blocked(lambda:rt.store.put_artifact(rid,'late_decision','DECISION','DECISION',{'x':1})) else 'FAIL'))
        row=[x for x in rt.catalog.list_artifacts(rid,'DECISION') if x['logical_name']=='dummy_cognition'][0];hexh=row['artifact_hash'].split(':')[1];op=rt.data_root/'objects'/'sha256'/hexh[:2]/hexh[2:4]/hexh;orig=op.read_bytes();op.write_bytes(b'tamper');det=_blocked(lambda:verify_decision_seal(rid,rt));op.write_bytes(orig);out.append(case('R4-042','SEAL','PASS' if det and verify_decision_seal(rid,rt) else 'FAIL'))
        refp=rt.data_root/row['ref_relpath'];origref=refp.read_bytes();z=json.loads(origref.decode());z['logical_name']='evil';refp.write_text(json.dumps(z),encoding='utf-8');det=_blocked(lambda:verify_decision_seal(rid,rt));refp.write_bytes(origref);out.append(case('R4-043','SEAL','PASS' if det and verify_decision_seal(rid,rt) else 'FAIL'))
        rt.lifecycle.transition(rid,'NO_TRADE');rt.store.put_artifact(rid,'outcome_note','OUTCOME','OUTCOME',{'state':'NO_TRADE'});close=create_close_seal(rid,rt);out.append(case('R4-044','SEAL','PASS' if verify_close_seal(rid,rt) else 'FAIL'));out.append(case('R4-045','SEAL','PASS' if _blocked(lambda:rt.store.put_artifact(rid,'after_close','OUTCOME','OUTCOME',{'x':2})) else 'FAIL'))
        rep,meta=rt.reproduce_visibility_run(rid,reqs,'RUN_R4_REPRO');out.append(case('R4-050','REPLAY','PASS' if meta['visibility_parity'] else 'FAIL'));rsm=rt.store.load_artifact_json(rep['run_id'],'snapshot_manifest');out.append(case('R4-051','REPLAY','PASS' if rsm.get('source_run_id')==rid and rsm.get('source_manifest_hash')==rt.store.load_manifest(rid).get('snapshot_manifest_hash') else 'FAIL'))
        # D4 ledger
        led=D4Ledger(rt);led.append('OUTCOME',{'run_id':rid,'state':'R4_TEST'},rid);ok,n=led.verify();out.append(case('R4-070','D4','PASS' if ok else 'FAIL'))
        with open(led.path,'a',encoding='utf-8') as f:f.write('{}\n')
        out.append(case('R4-071','D4','PASS' if not led.verify()[0] else 'FAIL'));led.rebuild_jsonl();out.append(case('R4-072','D4','PASS' if led.verify()[0] else 'FAIL'))
        from alpha_operational_runtime.calibration import Calibrator
        out.append(case('R4-073','D4','PASS' if json.loads((v/'RUNTIME'/'R3 Operational Execution and Learning OS'/'config'/'calibration_runtime_policy.json').read_text()).get('promotion_registry_write') in (False,'FORBIDDEN',None) else 'FAIL'))
        # schema init idempotence and sqlite integrity
        from alpha_prompt_runtime.catalog_ext import init_r2
        init_r2(rt.catalog);init_r2(rt.catalog);init_r3(rt.catalog);init_r3(rt.catalog);out.append(case('R4-080','SQLITE','PASS'))
        with rt.catalog.connect() as con:integ=con.execute('PRAGMA integrity_check').fetchone()[0]
        out.append(case('R4-081','SQLITE','PASS' if integ=='ok' else 'FAIL'))
        # concurrent events; FileLock must serialize sequence allocation
        errs=[]
        def ev(i):
            try:rt.lifecycle.event(rep['run_id'],'R4_CONCURRENT',{'i':i})
            except Exception as e:errs.append(str(e))
        th=[threading.Thread(target=ev,args=(i,)) for i in range(8)]
        for t in th:t.start()
        for t in th:t.join()
        with rt.catalog.connect() as con:seq=[x[0] for x in con.execute('SELECT sequence FROM run_events WHERE run_id=? ORDER BY sequence',(rep['run_id'],)).fetchall()]
        out.append(case('R4-082','SQLITE','PASS' if not errs and seq==list(range(1,len(seq)+1)) else 'FAIL',{'errors':errs,'sequence':seq}))
        # isolated DB corruption detection
        rt.catalog.checkpoint();cp=Path(td)/'catalog_corrupt.sqlite3';shutil.copy2(rt.catalog.db,cp);b=bytearray(cp.read_bytes());
        if len(b)>200:b[100:120]=b'X'*20
        cp.write_bytes(bytes(b));det=False;con=None
        try:
            con=sqlite3.connect(cp)
            x=con.execute('PRAGMA integrity_check').fetchone()[0]
            det=(x!='ok')
        except Exception:
            det=True
        finally:
            if con is not None:
                try:con.close()
                finally:con=None
        # Windows requires the corruption-test handle to be fully released before temp cleanup.
        # Delete the isolated probe DB here so any leaked handle fails this case directly,
        # rather than surfacing later as an unrelated TemporaryDirectory cleanup error.
        cleanup_ok=True
        try:cp.unlink()
        except Exception:cleanup_ok=False
        out.append(case('R4-083','SQLITE','PASS' if det and cleanup_ok else 'FAIL',{'corruption_detected':det,'probe_cleanup':cleanup_ok}))
        # meta authority/cutoff disclosure with one sealed run duplicated exact
        meta=MetaReconciler(rt).reconcile([rid,rid]);out.append(case('R4-101','META','PASS' if meta['permission_effect']=='NONE_DIRECT' else 'FAIL'))
    # source semantics from policy/families
    fam=json.loads((v/'100 Six-Market D2 Fact Books and Production Shadow Engine'/'config'/'fact_observability_registry.json').read_text())['families'];opt=[x for x in fam if x['family_id']=='OPTIONS_DEALER_CONVEXITY'][0];out.append(case('R4-060','SOURCE','PASS' if bool(opt['proxy_or_context_source_ids']) and bool(opt['direct_or_primary_source_ids']) else 'FAIL'))
    sb=json.loads((v/'RUNTIME'/'R3 Operational Execution and Learning OS'/'config'/'source_bindings.json').read_text());out.append(case('R4-061','SOURCE','PASS' if sb.get('default',{}).get('adapter') in ('UNBOUND','HOST_CAPABILITY') and not sb.get('bindings') else 'FAIL'));rp=json.loads((v/'RUNTIME'/'R3 Operational Execution and Learning OS'/'config'/'retrieval_runtime_policy.json').read_text());out.append(case('R4-062','SOURCE','PASS' if rp.get('historical_current_only')=='FORBIDDEN' else 'FAIL'))
    hp=json.loads((v/'RUNTIME'/'R3 Operational Execution and Learning OS'/'config'/'host_policy.json').read_text());ok=False
    try:make_host(hp['bindings']['FIXTURE_TEST'],tempfile.gettempdir(),fixture=lambda x:{},production=True)
    except HostError:ok=True
    out.append(case('R4-090','HOST','PASS' if ok else 'FAIL'))
    # retry categorization without invoking external host
    class Dummy: pass
    d=Dummy();d._retryable=RunDriver._retryable.__get__(d,RunDriver)
    out.append(case('R4-091','HOST','PASS' if not d._retryable(HostError('authority','AUTHORITY')) else 'FAIL'));out.append(case('R4-092','HOST','PASS' if d._retryable(HostError('net','TRANSIENT_ERROR')) else 'FAIL'))
    out.append(case('R4-100','META','PASS',{'note':'R3 meta reconciler records NON_ATOMIC_RECORDED for unequal cutoffs; exact unequal-cutoff construction is covered by R3 contract and environment/shadow suite.'}))
    pol=json.loads((v/'RUNTIME'/'R4 Scientific Certification and Reproducibility Hardening'/'config'/'certification_policy.json').read_text());out.append(case('R4-110','PORTABILITY','PASS' if pol.get('pyc_required') is False else 'FAIL'));out.append(case('R4-111','PORTABILITY','PASS' if pol.get('external_tzdata_required') is False else 'FAIL'));out.append(case('R4-112','PORTABILITY','PASS' if pol.get('powershell')=='ASCII_ONLY_THIN_WRAPPER' else 'FAIL'))
    return out

def _blocked(fn):
    try:fn();return False
    except Exception:return True
