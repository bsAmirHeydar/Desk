from pathlib import Path
import tempfile, json, os
from .runtime import AlphaRuntime
from .visibility import build_receipt
from .seal_safe import create_decision_seal,verify_decision_seal,create_close_seal,verify_close_seal,SealError
from .replay import reproduce_visibility
from .canonical import sha256_obj
from .timeutil import local_to_utc, TimeError, utc_now


def run(vault_root):
    checks=[]
    def ck(name,cond,msg=None): checks.append({"name":name,"pass":bool(cond),"message":msg});
    with tempfile.TemporaryDirectory(prefix='alphalab_r1_') as td:
        rt=AlphaRuntime(vault_root,td)
        req={"schema_version":"1.0.0","research_program_id":"TEST_FUNDAMENTAL","episode_id":"EP_TEST","run_scope":"INSTRUMENT","subject":"NASDAQ100","instrument":"NASDAQ100","run_mode":"LIVE","analysis_cutoff":"2026-08-01T12:00:00Z","strategy_id":"ALPHALAB_FUNDAMENTAL","active_horizon":"SESSION_1_6H","coverage_mode":"STRICT_FULL","research_depth":"AUTO","output_depth":"MACHINE","lookahead_policy":"STRICT_POINT_IN_TIME","execution_profile":None,"allow_private_sources":False,"idempotency_policy":"NEW_RUN","tags":["selftest"]}
        m,_=rt.create_run(req,run_id='RUN_TEST_LIVE')
        ck('run_created',m['state']=='REQUESTED')
        # object dedup
        a=rt.store.objects.put_bytes(b'abc'); b=rt.store.objects.put_bytes(b'abc'); ck('content_address_dedup',a[0]==b[0] and a[1]==b[1])
        rt.lifecycle.transition(m['run_id'],'INPUTS_RESOLVED')
        # snapshots
        def obj(name,content):
            h,rel,n=rt.store.objects.put_bytes(content.encode(),'text/plain'); return h
        snaps=[
          {"schema_version":"1.0.0","snapshot_id":"S_VISIBLE","artifact_hash":obj('v','visible'),"source_id":"SRC","requirement_id":"REQ_A","fact_key":"A","vintage_id":"A1","materiality":"DECISION_CRITICAL","applicability":"APPLICABLE","first_available_time":"2026-08-01T11:00:00Z","retrieved_at":"2026-08-01T11:01:00Z","superseded_at":None,"supersedes_snapshot_id":None,"vintage_integrity":"ORIGINAL_CAPTURE","source_semantics":"official"},
          {"schema_version":"1.0.0","snapshot_id":"S_FUTURE","artifact_hash":obj('f','future'),"source_id":"SRC","requirement_id":"REQ_B","fact_key":"B","vintage_id":"B1","materiality":"DECISION_CRITICAL","applicability":"APPLICABLE","first_available_time":"2026-08-01T13:00:00Z","retrieved_at":"2026-08-01T13:01:00Z","superseded_at":None,"supersedes_snapshot_id":None,"vintage_integrity":"ORIGINAL_CAPTURE","source_semantics":"official"},
          {"schema_version":"1.0.0","snapshot_id":"S_OLD","artifact_hash":obj('o','old'),"source_id":"SRC","requirement_id":"REQ_C","fact_key":"C","vintage_id":"C1","materiality":"MATERIAL","applicability":"APPLICABLE","first_available_time":"2026-08-01T10:00:00Z","retrieved_at":"2026-08-01T10:01:00Z","superseded_at":"2026-08-01T11:30:00Z","supersedes_snapshot_id":None,"vintage_integrity":"ORIGINAL_CAPTURE","source_semantics":"official"},
          {"schema_version":"1.0.0","snapshot_id":"S_REV","artifact_hash":obj('r','revision'),"source_id":"SRC","requirement_id":"REQ_C","fact_key":"C","vintage_id":"C2","materiality":"MATERIAL","applicability":"APPLICABLE","first_available_time":"2026-08-01T11:30:00Z","retrieved_at":"2026-08-01T11:31:00Z","superseded_at":None,"supersedes_snapshot_id":"S_OLD","vintage_integrity":"ORIGINAL_CAPTURE","source_semantics":"official"},
          {"schema_version":"1.0.0","snapshot_id":"S_ARCHIVE","artifact_hash":obj('a','archive'),"source_id":"SRC","requirement_id":"REQ_D","fact_key":"D","vintage_id":"D1","materiality":"SUPPORTING","applicability":"APPLICABLE","first_available_time":"2026-08-01T09:00:00Z","retrieved_at":"2026-09-01T00:00:00Z","superseded_at":None,"supersedes_snapshot_id":None,"vintage_integrity":"OFFICIAL_VINTAGE_ARCHIVE","source_semantics":"archive"},
          {"schema_version":"1.0.0","snapshot_id":"S_CURRENT","artifact_hash":obj('c','current'),"source_id":"SRC","requirement_id":"REQ_E","fact_key":"E","vintage_id":"E_CURRENT","materiality":"SUPPORTING","applicability":"APPLICABLE","first_available_time":"2026-08-01T09:00:00Z","retrieved_at":"2026-09-01T00:00:00Z","superseded_at":None,"supersedes_snapshot_id":None,"vintage_integrity":"CURRENT_ONLY","source_semantics":"latest-only"},
          {"schema_version":"1.0.0","snapshot_id":"S_LATE_INGEST","artifact_hash":obj('i','late-ingest'),"source_id":"SRC","requirement_id":"REQ_F","fact_key":"F","vintage_id":"F1","materiality":"MATERIAL","applicability":"APPLICABLE","publication_time":"2026-08-01T10:00:00Z","first_available_time":"2026-08-01T10:00:00Z","retrieved_at":"2026-08-01T10:01:00Z","ingested_at":"2026-08-01T12:05:00Z","superseded_at":None,"supersedes_snapshot_id":None,"vintage_integrity":"ORIGINAL_CAPTURE","source_semantics":"official"}
        ]
        reqs=[{"schema_version":"1.0.0","requirement_id":x,"fact_family":"TEST","materiality":mat,"applicability":"APPLICABLE","applicability_reason":None,"source_requirements":[]} for x,mat in [('REQ_A','DECISION_CRITICAL'),('REQ_B','DECISION_CRITICAL'),('REQ_C','MATERIAL'),('REQ_D','SUPPORTING'),('REQ_E','SUPPORTING'),('REQ_F','MATERIAL'),('REQ_MISSING','CONTEXTUAL')]]
        sm={"schema_version":"1.0.0","run_id":m['run_id'],"analysis_cutoff_utc":m['analysis_cutoff_utc'],"snapshots":snaps,"created_at_utc":utc_now(),"manifest_hash":None}; sm['manifest_hash']=sha256_obj({k:v for k,v in sm.items() if k not in ('created_at_utc','manifest_hash')})
        rt.store.put_artifact(m['run_id'],'coverage_requirements','DECISION','EVIDENCE',reqs)
        rt.freeze_snapshot_manifest(m['run_id'],sm); rt.lifecycle.transition(m['run_id'],'SNAPSHOT_FROZEN')
        live_receipt=build_receipt(m['run_id'],m['analysis_cutoff_utc'],'LIVE',reqs,snaps); rt.store.put_artifact(m['run_id'],'visibility_receipt','DECISION','EVIDENCE',live_receipt)
        rows={x['requirement_id']:x for x in live_receipt['requirements']}; ck('future_excluded',rows['REQ_B']['selected_snapshot_id'] is None); ck('late_ingest_excluded',rows['REQ_F']['selected_snapshot_id'] is None); ck('revision_selected',rows['REQ_C']['selected_snapshot_id']=='S_REV'); ck('no_silent_gap',rows['REQ_MISSING']['status']=='UNAVAILABLE')
        hist=build_receipt('RUN_HIST',m['analysis_cutoff_utc'],'HISTORICAL_REPLAY',reqs,snaps); hrows={x['requirement_id']:x for x in hist['requirements']}; ck('official_archive_admissible',hrows['REQ_D']['selected_snapshot_id']=='S_ARCHIVE'); ck('current_only_forbidden',hrows['REQ_E']['selected_snapshot_id'] is None)
        rt.lifecycle.transition(m['run_id'],'EVIDENCE_FROZEN'); rt.store.put_artifact(m['run_id'],'dummy_cognition','DECISION','COGNITION',{"state":"TEST"}); rt.lifecycle.transition(m['run_id'],'COGNITION_FROZEN')
        # outcome firewall before seal
        blocked=False
        try: rt.store.put_artifact(m['run_id'],'too_early','OUTCOME','OUTCOME',{"x":1})
        except Exception: blocked=True
        ck('outcome_firewall_preseal',blocked)
        seal=create_decision_seal(m['run_id'],rt); ck('decision_seal_created',bool(seal['decision_root_hash'])); ck('decision_seal_verifies',verify_decision_seal(m['run_id'],rt))
        blocked2=False
        try: rt.store.put_artifact(m['run_id'],'late_decision','DECISION','DECISION',{"x":2})
        except Exception: blocked2=True
        ck('decision_mutation_blocked',blocked2)
        rt.store.put_artifact(m['run_id'],'outcome','OUTCOME','OUTCOME',{"gross_r":1.0}); ck('outcome_postseal_allowed',True)
        # replay parity over the original frozen decision-world snapshots
        replay_manifest,replay_meta=rt.reproduce_visibility_run(m['run_id'],reqs,'RUN_REPRO'); ck('replay_visibility_parity',replay_meta['visibility_parity'] and replay_manifest['state']=='EVIDENCE_FROZEN')
        replay_sm=rt.store.load_artifact_json('RUN_REPRO','snapshot_manifest'); ck('replay_snapshot_provenance',replay_sm.get('source_run_id')==m['run_id'] and replay_sm.get('source_manifest_hash')==rt.store.load_manifest(m['run_id']).get('snapshot_manifest_hash'))
        # lifecycle/event monotonic
        with rt.catalog.connect() as c: seq=[x[0] for x in c.execute("SELECT sequence FROM run_events WHERE run_id=? ORDER BY sequence",(m['run_id'],)).fetchall()]
        ck('event_sequences_monotonic',seq==list(range(1,len(seq)+1)))
        # catalog integrity
        with rt.catalog.connect() as c: integ=c.execute('PRAGMA integrity_check').fetchone()[0]
        ck('sqlite_integrity',integ=='ok')
        # DST ambiguity/nonexistence using the bundled timezone fallback. This makes
        # the runtime independent of an external tzdata pip package on Windows.
        prior_force=os.environ.get('ALPHALAB_FORCE_BUNDLED_TZ')
        os.environ['ALPHALAB_FORCE_BUNDLED_TZ']='1'
        try:
            amb=False
            try: local_to_utc('2026-11-01T01:30:00','America/New_York')
            except TimeError: amb=True
            ck('dst_ambiguity_rejected',amb)
            nonexist=False
            try: local_to_utc('2026-03-08T02:30:00','America/New_York')
            except TimeError: nonexist=True
            ck('dst_nonexistent_time_rejected',nonexist)
        finally:
            if prior_force is None: os.environ.pop('ALPHALAB_FORCE_BUNDLED_TZ',None)
            else: os.environ['ALPHALAB_FORCE_BUNDLED_TZ']=prior_force
        # tamper detection
        row=[x for x in rt.catalog.list_artifacts(m['run_id'],'DECISION') if x['logical_name']=='dummy_cognition'][0]; hexh=row['artifact_hash'].split(':')[1]; p=rt.data_root/'objects'/'sha256'/hexh[:2]/hexh[2:4]/hexh; original=p.read_bytes(); p.write_bytes(b'tampered')
        tamper=False
        try: verify_decision_seal(m['run_id'],rt)
        except Exception: tamper=True
        p.write_bytes(original); ck('tamper_detected',tamper); ck('seal_reverifies_after_restore',verify_decision_seal(m['run_id'],rt))
        # reference-view tamper is also detected against the authoritative catalog
        rrow=[x for x in rt.catalog.list_artifacts(m['run_id'],'DECISION') if x['logical_name']=='dummy_cognition'][0]; refp=rt.data_root/rrow['ref_relpath']; ref_original=refp.read_text(encoding='utf-8'); ref=json.loads(ref_original); ref['artifact_hash']='sha256:'+'0'*64; refp.write_text(json.dumps(ref),encoding='utf-8'); ref_tamper=False
        try: verify_decision_seal(m['run_id'],rt)
        except Exception: ref_tamper=True
        refp.write_text(ref_original,encoding='utf-8'); ck('ref_tamper_detected',ref_tamper); ck('seal_reverifies_after_ref_restore',verify_decision_seal(m['run_id'],rt))
        # close seal after outcome maturation
        rt.lifecycle.transition(m['run_id'],'NO_TRADE') if rt.store.load_manifest(m['run_id'])['state']=='DECISION_FROZEN' else None
        if rt.store.load_manifest(m['run_id'])['state']=='NO_TRADE': rt.lifecycle.transition(m['run_id'],'OUTCOME_MATURED')
        close=create_close_seal(m['run_id'],rt); ck('run_close_seal_created',bool(close['run_close_hash'])); ck('run_close_seal_verifies',verify_close_seal(m['run_id'],rt))
        blocked3=False
        try: rt.store.put_artifact(m['run_id'],'late_learning','LEARNING','LEARNING',{'x':1})
        except Exception: blocked3=True
        ck('post_close_mutation_blocked',blocked3)
        rt.catalog.checkpoint()
    passed=sum(1 for x in checks if x['pass']); return {"status":"PASS" if passed==len(checks) else "FAIL","passed":passed,"total":len(checks),"checks":checks}
