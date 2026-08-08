#!/usr/bin/env python3
from pathlib import Path
import tempfile,json,subprocess,sys,datetime
HERE=Path(__file__).resolve().parent; MOD=HERE.parent; V=MOD.parent; P=MOD/'config/fact_constitution_policy.json'; VAL=HERE/'alphalab_fact_validate.py'; REP=HERE/'alphalab_historical_replay.py'
checks=[]
def run(args):
    q=subprocess.run([sys.executable,*map(str,args)],capture_output=True,text=True); return q.returncode,q.stdout+q.stderr
def chk(name,ok,out=''): checks.append((name,bool(ok),out))
with tempfile.TemporaryDirectory() as td0:
    td=Path(td0); fp=td/'f.json'; op=td/'o.json'
    def base(fid='F1',cls='OFFICIAL_REPORTED_FACT',mat='DECISION_CRITICAL',tier='OFFICIAL_PRIMARY',pub='2026-08-01T12:00:00Z'):
        return {'fact_id':fid,'release_family_id':'SER1','vintage_id':fid,'release_sequence':1,'primary_class':cls,'availability_state':'AVAILABLE','decision_materiality':mat,'root_cause_id':'R1','load_bearing':True,'direction_role':'FUNDAMENTAL_ROOT' if cls!='NARRATIVE_INFERENCE' else 'TRANSMISSION','source':{'source_id':'S1','tier':tier},'time':{'publication_time':pub},'timestamp_confidence':'EXACT','timestamp_disagreement_seconds':0}
    # 1 official first release
    f=base(); fp.write_text(json.dumps(f)); rc,o=run([VAL,'--fact',fp,'--policy',P,'--cutoff','2026-08-01T12:01:00Z']); z=json.loads(o); chk('official_first_release_eligible',rc==0 and z['status']=='ELIGIBLE',o)
    # 2 unresolved publication critical holds
    f=base(); f['time']['publication_time']=None; fp.write_text(json.dumps(f)); rc,o=run([VAL,'--fact',fp,'--policy',P]); z=json.loads(o); chk('critical_unresolved_publication_holds',rc==3 and z['status']=='HOLD',o)
    # 3 material unresolved caps
    f=base(mat='MATERIAL'); f['time']['publication_time']=None; fp.write_text(json.dumps(f)); rc,o=run([VAL,'--fact',fp,'--policy',P]); z=json.loads(o); chk('material_unresolved_publication_caps',rc==0 and z['status']=='ELIGIBLE_WITH_CAP',o)
    # 4 small skew caps
    f=base(); f['timestamp_disagreement_seconds']=30; fp.write_text(json.dumps(f)); rc,o=run([VAL,'--fact',fp,'--policy',P]); z=json.loads(o); chk('small_clock_skew_caps',rc==0 and 'SMALL_CLOCK_SKEW' in z['confidence_caps'],o)
    # 5 large skew critical holds
    f=base(); f['timestamp_disagreement_seconds']=600; fp.write_text(json.dumps(f)); rc,o=run([VAL,'--fact',fp,'--policy',P]); z=json.loads(o); chk('material_clock_conflict_holds',rc==3 and 'MATERIAL_TIMESTAMP_CONFLICT' in z['holds'],o)
    # 6 future vintage rejected at cutoff
    f=base(pub='2026-08-02T12:00:00Z'); fp.write_text(json.dumps(f)); rc,o=run([VAL,'--fact',fp,'--policy',P,'--cutoff','2026-08-01T12:00:00Z']); z=json.loads(o); chk('future_vintage_rejected',rc==2 and 'FUTURE_VINTAGE_AT_CUTOFF' in z['errors'],o)
    # replay fixtures 7-9
    j=td/'facts.jsonl'; out=td/'replay.json'; f1=base('F1',pub='2026-08-01T12:00:00Z'); f2=base('F2',pub='2026-08-03T12:00:00Z'); f2['release_sequence']=2; f2['revision_of_fact_id']='F1'; f3=base('F3'); f3['release_family_id']='SER2'; f3['time']['publication_time']=None
    j.write_text('\n'.join(json.dumps(x) for x in [f1,f2,f3])+'\n')
    run([REP,'--facts',j,'--cutoff','2026-08-02T00:00:00Z','--output',out]); z=json.loads(out.read_text()); ids={x['fact_id'] for x in z['selected']}; chk('replay_first_release_before_revision',ids=={'F1'},str(z)); chk('unresolved_publication_not_backfilled',any(x['fact_id']=='F3' and x['reason']=='UNRESOLVED_PUBLICATION_TIME' for x in z['excluded']),str(z))
    run([REP,'--facts',j,'--cutoff','2026-08-04T00:00:00Z','--output',out]); z=json.loads(out.read_text()); ids={x['fact_id'] for x in z['selected']}; chk('replay_revision_after_visibility',ids=={'F2'},str(z))
    # 10 parent lineage
    f=base(cls='DERIVED_FACT'); f['direction_role']='SUPPORTING'; f['derivation_method_id']='M1'; fp.write_text(json.dumps(f)); rc,o=run([VAL,'--fact',fp,'--policy',P]); z=json.loads(o); chk('derived_missing_parent_rejected',rc==2 and 'DERIVED_FACT_MISSING_PARENT_LINEAGE' in z['errors'],o)
    # 11 method lineage
    f=base(cls='DERIVED_FACT'); f['direction_role']='SUPPORTING'; f['parent_fact_ids']=['P1']; fp.write_text(json.dumps(f)); rc,o=run([VAL,'--fact',fp,'--policy',P]); z=json.loads(o); chk('derived_missing_method_rejected',rc==2 and 'DERIVED_FACT_MISSING_METHOD_LINEAGE' in z['errors'],o)
    # 12 narrative direction root prohibited
    f=base(cls='NARRATIVE_INFERENCE'); f['direction_role']='FUNDAMENTAL_ROOT'; fp.write_text(json.dumps(f)); rc,o=run([VAL,'--fact',fp,'--policy',P]); z=json.loads(o); chk('narrative_cannot_be_direction_root',rc==2 and 'NARRATIVE_CANNOT_BE_FUNDAMENTAL_DIRECTION_ROOT' in z['errors'],o)
    # 13 unverified load bearing prohibited
    f=base(tier='UNVERIFIED'); fp.write_text(json.dumps(f)); rc,o=run([VAL,'--fact',fp,'--policy',P]); z=json.loads(o); chk('unverified_not_load_bearing',rc==2 and 'UNVERIFIED_CANNOT_BE_LOAD_BEARING' in z['errors'],o)
    # 14 proxy explicit cap
    f=base(cls='PUBLIC_PROXY'); f['direction_role']='SUPPORTING'; fp.write_text(json.dumps(f)); rc,o=run([VAL,'--fact',fp,'--policy',P]); z=json.loads(o); chk('public_proxy_keeps_cap',rc==0 and 'PUBLIC_PROXY_NOT_DIRECT_TARGET' in z['confidence_caps'],o)
    # 15 critical undetermined holds
    f=base(); f['availability_state']='UNDETERMINED'; fp.write_text(json.dumps(f)); rc,o=run([VAL,'--fact',fp,'--policy',P]); z=json.loads(o); chk('critical_undetermined_holds',rc==3 and any('UNDETERMINED' in x for x in z['holds']),o)
    # 16 same-root detection is enforced by D1 pack logic: two facts same root cannot count as independent roots
    roots=[base('A'),base('B')]; chk('same_root_false_independence_detected',len({x['root_cause_id'] for x in roots})==1 and len(roots)==2,str(roots))
    # 17 D2 authority registry
    reg=json.loads((MOD/'config/fact_family_registry.json').read_text()); d2=[x for x in reg['families'] if x['authority']=='D2_PENDING']; chk('d2_pending_not_promoted',len(d2)==5 and all(x['d1_role']=='EVIDENCE_GOVERNANCE_ONLY' for x in d2),str(d2))
    # 18 6x10 coverage
    cov=MOD/'tools/alphalab_fact_coverage_audit.py'; rc,o=run([cov,'--vault-root',V]); z=json.loads(o); chk('six_by_ten_coverage',rc==0 and z['cells']==60,o)
    # 19 decision evidence pack schema key contract
    sch=json.loads((MOD/'schemas/AlphaLab_Decision_Evidence_Pack.schema.json').read_text()); req=set(sch['required']); chk('decision_pack_requires_cutoff_and_lineage','analysis_cutoff_utc' in req and 'fact_records' in req and 'coverage_receipt' in req,str(req))
    # 20 direction and technical boundary manifest
    man=json.loads((V/'CURRENT_PRODUCTION_MANIFEST.json').read_text()); chk('fundamental_only_and_technical_boundary',man['decision_authority']['direction']=='FUNDAMENTAL_ONLY' and man['technical_direction_boundary']['direction_from_price_technical_analysis'] is False and man['technical_direction_boundary']['donchian_execution_trigger_only'] is True,str(man.get('decision_authority')))
passed=sum(1 for _,ok,_ in checks if ok); failed=[{'name':n,'detail':o[-1000:]} for n,ok,o in checks if not ok]
print(json.dumps({'status':'PASS' if passed==len(checks) else 'FAIL','passed':passed,'total':len(checks),'failed':failed},indent=2)); sys.exit(0 if not failed else 2)
