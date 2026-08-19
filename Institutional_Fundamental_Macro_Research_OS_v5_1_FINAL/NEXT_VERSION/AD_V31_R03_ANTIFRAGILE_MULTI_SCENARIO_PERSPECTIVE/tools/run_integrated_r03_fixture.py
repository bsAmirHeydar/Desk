#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,pathlib,sys,tempfile
HERE=pathlib.Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent;REPO=NEXT.parents[1];sys.path.insert(0,str(NEXT))
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.gold_orchestrator import run_gold

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def ck(n,o,d=None): return {'name':n,'status':'PASS' if o else 'FAIL','detail':d}
def main():
    checks=[]
    real_state=NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/artifacts/state/forward_state.json';before=sha(real_state)
    p02=NEXT/'AD_V3_PHASE_02_TOTAL_LIVE_DATA_OBSERVABILITY_FABRIC';fix=p02/'tests/fixtures/generated'
    with tempfile.TemporaryDirectory() as td:
        td=pathlib.Path(td);art=td/'art';p09=td/'p09'
        out=run_gold(REPO,'SESSION_1_6H','FIXTURE','NORMAL',p02_data_root_override=td/'data',artifact_root_override=art,kernel_fixture_dir=fix,kernel_output_root_override=td/'kernel',p09_state_root_override=p09,as_of_utc='2026-08-17T10:00:00Z',fixture_mode=True,update_latest=False,quiet=True)
        rd=next((art/'runs').iterdir());p08=load(rd/'p08_decision_calibration.json');r03=load(rd/'r03_perspective_state.json');pre=load(rd/'p09_forward_precommit.json');vm=load(rd/'control_room_view_model.json');html=(rd/'control_room.html').read_text(encoding='utf-8')
        order=[x['stage_id'] for x in out['stage_receipts']]
        checks.append(ck('R03 stage is canonical between P08 and P09',order.index('DECISION_CALIBRATION')<order.index('PERSPECTIVE_OVERLAY')<order.index('FORWARD_PRECOMMIT'),order))
        checks.append(ck('canonical direction is unchanged by R03',r03.get('canonical_direction')==p08.get('causal_direction')))
        rank={'NO_EDGE':0,'LOW_EDGE':1,'CONDITIONAL_EDGE':2,'ACTIONABLE_EDGE':3};checks.append(ck('R03 edge overlay is monotonic non-upgrading',rank.get(r03.get('final_edge'),0)<=rank.get(r03.get('pre_overlay_edge'),0),{'pre':r03.get('pre_overlay_edge'),'post':r03.get('final_edge')}))
        preperm=r03.get('pre_overlay_permission');post=r03.get('final_permission');checks.append(ck('R03 permission overlay never upgrades WAIT',not (preperm in {'WAIT','NO_AUTHORITY'} and post in {'BUY','SELL'}),{'pre':preperm,'post':post}))
        checks.append(ck('P09 snapshot persists R03 perspective fields',pre.get('r03_perspective_version')=='3.1.3-antifragile-perspective' and 'r03_scenario_set' in pre and 'r03_fragility_map' in pre and 'r03_final_permission' in pre))
        pv=vm.get('perspective') or {};checks.append(ck('P11 exposes bounded human scenario atlas',pv.get('scenario_count',0)<=6 and 'scenario_atlas' in pv and 'id="scenarios"' in html,pv.get('scenario_count')))
        checks.append(ck('scenario counts are not probabilities',(r03.get('scenario_packet') or {}).get('scenario_counts_are_not_probabilities') is True and 'scenario_probability' not in html.lower()))
        checks.append(ck('fixture does not update live latest',not (art/'latest/last_success.json').exists()))
    after=sha(real_state);checks.append(ck('integrated fixture preserves real P09 ledger',before==after,{'before':before,'after':after}))
    ok=all(x['status']=='PASS' for x in checks);result={'phase':'AD-V3.1-R03','fixture':'FULL_OFFLINE_INTEGRATED_R03','status':'PASS' if ok else 'FAIL_CLOSED','check_count':len(checks),'checks':checks,'real_p09_unchanged':before==after,'trade_execution_authority':'NONE'}
    print(json.dumps(result,ensure_ascii=False,indent=2));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
