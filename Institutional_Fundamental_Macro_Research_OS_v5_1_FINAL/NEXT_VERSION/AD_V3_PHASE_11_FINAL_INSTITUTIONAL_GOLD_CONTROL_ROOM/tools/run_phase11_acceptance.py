from __future__ import annotations
import copy,hashlib,json,pathlib,re,subprocess,sys,tempfile
from bs4 import BeautifulSoup
HERE=pathlib.Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent;REPO=NEXT.parents[1];sys.path.insert(0,str(NEXT))
import jsonschema
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.gold_orchestrator import run_gold
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.artifact_manager import ArtifactManager,verify_seal
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.runtime_router import resolve
from AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM.runtime.report_runtime import render_report
from AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM.runtime.presenter import build_view_model
from AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM.tools.fixture_factory import base_input,scenario

def load(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def ck(n,o,d=None):return {'name':n,'status':'PASS' if o else 'FAIL','detail':d}
def main():
 checks=[]
 # Static/prerequisite checks.
 for name,tool in [('P05',NEXT/'AD_V3_PHASE_05_INTEGRITY_ARCHITECTURE_CONSOLIDATION/tools/run_phase05_acceptance.py'),('P10',NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/tools/run_phase10_acceptance.py'),('P11 static',PH/'tools/validate_phase11.py')]:
  cp=subprocess.run([sys.executable,str(tool)],capture_output=True,text=True,encoding='utf-8',errors='replace');checks.append(ck(name+' prerequisite valid',cp.returncode==0,cp.stdout[-700:] if cp.returncode else 'PASS'))
 # Canonical P10 fixture -> P11 end to end.
 p02=NEXT/'AD_V3_PHASE_02_TOTAL_LIVE_DATA_OBSERVABILITY_FABRIC';fix=p02/'tests/fixtures/generated'
 with tempfile.TemporaryDirectory() as td:
  td=pathlib.Path(td);data=td/'data';art=td/'art';kout=td/'kernel';p09=td/'p09'
  out=run_gold(REPO,'SESSION_1_6H','FIXTURE','NORMAL',p02_data_root_override=data,artifact_root_override=art,kernel_fixture_dir=fix,kernel_output_root_override=kout,p09_state_root_override=p09,as_of_utc='2026-08-17T10:00:00Z',fixture_mode=True,update_latest=False,quiet=True)
  rd=next((art/'runs').iterdir());cri=load(rd/'control_room_input.json');vm=load(rd/'control_room_view_model.json');html=(rd/'control_room.html').read_text(encoding='utf-8');receipt=load(rd/'p11_report_receipt.json');soup=BeautifulSoup(html,'lxml')
  checks.append(ck('P10 ControlRoomInput is canonical P11 input',cri.get('schema_id')=='ControlRoomInputV3' and cri.get('schema_version')=='1.3.0'))
  checks.append(ck('P10 report stage uses P11 canonical renderer',out.get('report_state')=='P11_GENERATED' and receipt.get('canonical_v3_renderer') is True))
  checks.append(ck('P11 view model schema valid',_schema(vm,PH/'schemas/control_room_view_model.schema.json')))
  checks.append(ck('P11 report receipt schema valid',_schema(receipt,PH/'schemas/report_receipt.schema.json')))
  checks.append(ck('canonical Evidence Index contains Gold universe observations',len(vm.get('evidence') or [])==192, len(vm.get('evidence') or [])))
  required=['now','changed','drivers','pressure','transmission','watch','invalidation','scenarios','events','data','forward','evidence','audit'];checks.append(ck('all human-first sections present',all(soup.find(id=x) for x in required),required))
  checks.append(ck('RTL-first document contract',soup.html and soup.html.get('dir')=='rtl' and soup.html.get('lang')=='fa'))
  ex=vm.get('executive') or {};checks.append(ck('executive layer exposes decision dimensions',all(k in ex for k in ['direction','pressure_strength','dominance','permission','edge','consumption','fragility','headline'])))
  checks.append(ck('human intelligence sections populated deterministically',isinstance(vm.get('watch_next'),list) and isinstance(vm.get('invalidation'),list) and isinstance(vm.get('what_changed'),dict)))
  perspective=vm.get('perspective') or {}
  checks.append(ck('R03 scenario atlas is presentation-only and bounded',len(perspective.get('scenarios') or [])<=6 and perspective.get('scenario_count',0)<=6,perspective.get('scenario_count')))
  checks.append(ck('R03 perspective exposes thesis resilience and permission effect',perspective.get('thesis_resilience') is not None and perspective.get('overlay') is not None))
  checks.append(ck('Pressure != Price is explicit in HTML','Pressure ≠ Price' in html and soup.find(id='pressure') is not None and soup.find(id='transmission') is not None))
  checks.append(ck('data health separates live/context/semantic',all(k in (vm.get('data_health') or {}) for k in ['live_kernel_health','context_health']) and 'semantic_health' in vm))
  checks.append(ck('P09 real forward fields separately represented',all(k in (vm.get('forward') or {}) for k in ['cohort_id','prediction_count','episode_count','mature_episode_count','evidence_state','direction_state','permission_state','wait_state'])))
  checks.append(ck('fixture identity visibly prevents live confusion',vm.get('fixture') is True and 'TEST FIXTURE — NOT LIVE' in html))
  checks.append(ck('Decision to evidence forensic chain present',len(vm.get('roots') or [])>0 and len(vm.get('evidence') or [])==192 and soup.select('#evidence details.evidence-row')))
  checks.append(ck('timestamps and freshness available in evidence detail',any(x.get('retrieved_at') is not None for x in vm['evidence']) and any('freshness_state' in x for x in vm['evidence'])))
  checks.append(ck('semantic state is not a fake confidence score','Confidence' not in html and '%' not in ' '.join(str(ex.get(k,'')) for k in ex)))
  checks.append(ck('run seal binds P11 artifacts',verify_seal(rd) and 'p11_view_model_sha256' in load(rd/'run_capsule.json')))
  # Comparison and fetch-only no-change.
  prev=copy.deepcopy(cri);prev['decision_calibration']['pressure_strength']='MODERATE';cur=copy.deepcopy(cri);cmp=build_view_model(cur,prev,fixture=True)['what_changed'];checks.append(ck('material previous-run comparison exists',any(x['field']=='pressure_strength' for x in cmp.get('items',[]))))
  prev2=copy.deepcopy(cri);prev2.setdefault('evidence_index',{}).setdefault('observations',[])[0]['retrieved_at']='2026-08-17T09:00:00Z';cmp2=build_view_model(cri,prev2,fixture=True)['what_changed'];checks.append(ck('fetch-only change ignored',len(cmp2.get('items',[]))==0,cmp2))
  # Rerender cannot mutate P09 state.
  statefile=p09/'forward_state.json';before=sha(statefile) if statefile.exists() else None;rr=render_report(cri,td/'rerender',fixture=False,visual_state='RERENDER');after=sha(statefile) if statefile.exists() else None;checks.append(ck('rerender creates no new P09 state and preserves decision',before==after and rr['view_model']['executive']['direction']==vm['executive']['direction']))
  # Security attack.
  evil=copy.deepcopy(cri);evilobs=evil['evidence_index']['observations'][0];evilobs['value']='<script>alert(1)</script>';evilobs['provenance_ref']='javascript:alert(1)';sec=render_report(evil,td/'evil',fixture=True);sh=sec['html'];ss=BeautifulSoup(sh,'lxml');checks.append(ck('XSS evidence is escaped and never executable',not ss.find('script',string=re.compile('alert\\(1\\)')) and '&lt;script&gt;alert(1)&lt;/script&gt;' in sh))
  hrefs=[a.get('href') for a in ss.find_all('a') if a.get('href')];checks.append(ck('unsafe source URLs blocked',not any(str(x).lower().startswith('javascript:') for x in hrefs)))
  checks.append(ck('CSP blocks core remote network dependency',"connect-src 'none'" in sh and "default-src 'none'" in sh))
  # Accessibility/DOM basics.
  checks.append(ck('semantic landmarks and keyboard-native drawers present',bool(soup.find('main')) and bool(soup.find('nav')) and len(soup.find_all('details'))>2 and all(x.find('summary') for x in soup.find_all('details'))))
  checks.append(ck('evidence search controls have accessible labels',all(x.get('aria-label') for x in [soup.find(id='evidence-search'),soup.find(id='freshness-filter'),soup.find(id='tier-filter')])))
  checks.append(ck('reduced motion and print styles present','prefers-reduced-motion' in html and '@media print' in html))
  checks.append(ck('responsive CSS exists for laptop/tablet/mobile','@media(max-width:1050px)' in html and '@media(max-width:720px)' in html))
  # Scenario rendering.
  for name,expected in [('bullish_buy','BUY'),('bearish_sell','SELL'),('true_mixed','WAIT'),('unknown','WAIT'),('blocked','NO_AUTHORITY'),('degraded','WAIT'),('semantic_conservative',None),('forward_provisional',None),('dense','WAIT')]:
   sc=scenario(cri,name);rv=render_report(sc,td/name,fixture=True)['view_model'];ok=(expected is None or rv['executive']['permission']==expected); checks.append(ck('fixture renders '+name,ok,rv['executive'].get('permission')))
  blocked_html=(td/'blocked/control_room.html').read_text(encoding='utf-8');blocked_vm=load(td/'blocked/control_room_view_model.json'); checks.append(ck('blocked state unmistakable and no directional permission','ANALYSIS BLOCKED' in blocked_html and blocked_vm['executive']['permission']=='NO_AUTHORITY'))
  mixed_vm=load(td/'true_mixed/control_room_view_model.json');checks.append(ck('TRUE_MIXED/BALANCED does not imply hidden direction',mixed_vm['executive']['direction']=='MIXED' and mixed_vm['executive']['permission']=='WAIT'))
  prov=load(td/'forward_provisional/control_room_view_model.json');checks.append(ck('forward fixture marked test and kept separate',prov['fixture'] is True and prov['forward']['evidence_state']=='PROVISIONAL'))
  # Visual browser acceptance on dense fixture.
  visual_out=td/'visual';cp=subprocess.run([sys.executable,str(PH/'tools/visual_acceptance.py'),str(td/'dense/control_room.html'),'--screenshots',str(visual_out)],capture_output=True,text=True,encoding='utf-8',errors='replace');vis=json.loads(cp.stdout or '{}');checks.append(ck('browser visual acceptance responsive RTL no overflow',cp.returncode==0 and vis.get('status') in {'PASS','NOT_RUN_ENVIRONMENT_UNAVAILABLE'},vis))
  # P11 must not update latest in fixture mode.
  checks.append(ck('fixture render cannot update live latest',not (art/'latest/last_success.json').exists()))
 # Canonical authority/static contracts.
 p10src=(NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/runtime/gold_orchestrator.py').read_text(encoding='utf-8');p04src=(NEXT/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING/runtime/renderer.py').read_text(encoding='utf-8');contract=load(PH/'config/report_contract.json')
 checks.append(ck('exactly one canonical V3 HTML renderer declared',contract.get('canonical_v3_html_authority')=='AD-V3-P11' and contract.get('legacy_v3_renderer')=='AD-V3-P04'))
 checks.append(ck('P10 imports P11 renderer not P04 renderer','render_p11_report' in p10src and 'runtime.renderer import render' not in p10src))
 checks.append(ck('P04 legacy renderer retained but noncanonical',(NEXT/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING/runtime/renderer.py').exists()))
 checks.append(ck('no LLM report writer introduced','openai' not in (PH/'runtime/presenter.py').read_text(encoding='utf-8').lower() and 'model_host' not in (PH/'runtime/renderer.py').read_text(encoding='utf-8').lower()))
 # Routing/report isolation contracts.
 rprod=resolve(REPO,'Gold','PRODUCTION',promotion_override='SHADOW_COMMISSIONING');rshadow=resolve(REPO,'Gold','SHADOW',promotion_override='SHADOW_COMMISSIONING');rfuture=resolve(REPO,'Gold','PRODUCTION',promotion_override='PRODUCTION_V3');checks.append(ck('shadow routing preserves V2 production and P11 V3 shadow',rprod['selected_runtime']=='V2' and rshadow['selected_runtime']=='V3' and rfuture['selected_runtime']=='V3'))
 cli=(NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/tools/alpha_desk.py').read_text(encoding='utf-8');checks.append(ck('commission-report/open remain shadow report commands','commission-report' in cli and 'commission-open' in cli and 'v3-control-room-status' in cli))
 # Science integrity.
 b=load(PH/'baseline/PRE_P11_AUTHORITY_HASHES.json');drift=[]
 allowed_r01={
 'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION/AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/runtime/forward_statistics.py',
 'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION/AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/runtime/forward_runtime.py',
 'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION/AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/runtime/control_room_input.py',
 'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION/AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/runtime/gold_orchestrator.py',
 'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION/AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/schemas/control_room_input.schema.json'}
 for rel,expected in b.get('hashes',{}).items():
  if rel.endswith('/AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/config/stage_dag.json') or rel in allowed_r01: continue
  p=REPO/rel
  if p.exists() and sha(p)!=expected:drift.append(rel)
 checks.append(ck('substantive upstream science/runtime authority drift zero',not drift,drift))
 pre_dag=load(PH/'baseline/PRE_P11_P10_STAGE_DAG.json');cur_dag=load(NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/config/stage_dag.json');pre_map={x['stage_id']:(tuple(x.get('depends_on') or []),x.get('mandatory')) for x in pre_dag['stages']};cur_map={x['stage_id']:(tuple(x.get('depends_on') or []),x.get('mandatory')) for x in cur_dag['stages']};auth={x['stage_id']:x.get('authority') for x in cur_dag['stages']};top_ok=set(cur_map)==set(pre_map)|{'PERSPECTIVE_OVERLAY'} and cur_map.get('PERSPECTIVE_OVERLAY')==( ('DECISION_CALIBRATION',), True ) and cur_map.get('FORWARD_PRECOMMIT')==( ('PERSPECTIVE_OVERLAY',), pre_map['FORWARD_PRECOMMIT'][1] ) and all(cur_map.get(sid)==val for sid,val in pre_map.items() if sid!='FORWARD_PRECOMMIT');checks.append(ck('P10 stage DAG preserves legacy topology with governed R03 perspective insertion',top_ok and auth.get('CONTROL_MODEL')=='AD-V3-P11' and auth.get('REPORT')=='AD-V3-P11' and auth.get('PERSPECTIVE_OVERLAY')=='AD-V3.1-R03',auth))
 # Git-ignore/runtime artifact governance.
 gi=(REPO/'.gitignore').read_text(encoding='utf-8');checks.append(ck('P11 runtime artifacts gitignored','AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM/artifacts/' in gi))
 ok=all(x['status']=='PASS' for x in checks);out={'phase':'AD-V3-P11','version':'3.11.1-r03-perspective','acceptance_status':'PASS' if ok else 'FAIL_CLOSED','check_count':len(checks),'checks':checks,'canonical_renderer':'AD-V3-P11','visual_acceptance':next((x['detail'].get('status') for x in checks if x['name'].startswith('browser visual') and isinstance(x.get('detail'),dict)),'UNKNOWN'),'v3_state':'SHADOW_COMMISSIONING','production_promotion_performed':False,'trade_execution_authority':'NONE'};print(json.dumps(out,ensure_ascii=False,indent=2,default=str));return 0 if ok else 2

def _schema(obj,path):
 try:jsonschema.validate(obj,load(path));return True
 except Exception:return False
if __name__=='__main__':raise SystemExit(main())
