#!/usr/bin/env python3
from pathlib import Path
import argparse,sys,json,tempfile,copy,hashlib
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE))
from runtime.common import load_json,hobj
from runtime.model import build_control_room
from runtime.render_html import render
from runtime.governance import verify_p12_authorized_delta
from runtime.environment_gate import reconcile_doctor, environment_status

def run_p10(repo,pack):
    pp=Path(repo)/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION';sys.path.insert(0,str(pp))
    from AD_V2_PHASE_10_INTEGRATED_SHADOW_COMMISSIONING_RC.runtime.shadow_pipeline import run
    return run(pack,phase_parent=pp,data_root=Path(tempfile.mkdtemp())/'data',output_dir=Path(tempfile.mkdtemp())/'out',persist_state=False)

def receipt(p10,mode='TEST'):
    return {'schema_version':'1.0.0','phase':'AD-V2-P11','status':'PASS','mode':mode,'p10_receipt':p10,'authority':{'v1':'AUTHORITATIVE','v2':'SHADOW','permission':'V1_INHERITED','broker':'NONE'}}

def check(name,ok,detail=None):return {'name':name,'status':'PASS' if ok else 'FAIL','detail':detail}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo-root',required=True);a=ap.parse_args();repo=Path(a.repo_root).resolve();pp=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION';fixture=load_json(pp/'AD_V2_PHASE_10_INTEGRATED_SHADOW_COMMISSIONING_RC/tests/fixtures/integrated_gold_shadow_input.json');checks=[]
    p10=run_p10(repo,fixture);m=build_control_room(repo,receipt(p10),input_pack=fixture,data_root=Path(tempfile.mkdtemp()))
    checks.append(check('schema_contract',m.get('schema_id')=='alpha_desk_v2.gold_control_room.v1' and m.get('contract')=='ALPHA_DESK_V2_GOLD_CONTROL_ROOM_V1'))
    checks.append(check('gold_only',m.get('identity',{}).get('subject')=='XAUUSD' and m.get('identity',{}).get('gold_only') is True))
    checks.append(check('eight_layers', [x.get('id') for x in m.get('layers',[])]==['timing','fundamental','expectations_policy','narrative_consumption','positioning','flow','funding','mechanics']))
    checks.append(check('permission_visible',m.get('overview',{}).get('trade_permission')=='NO_TRADE'))
    checks.append(check('same_owner_integrity',m.get('audit',{}).get('science_owner_integrity')=='PASS'))
    # Price contamination attack: pressure_input unchanged, target response altered materially.
    flip=copy.deepcopy(fixture);flip['actual_response']['target']['observed_response']=0.8
    for o in flip['gold_observations']:
        if o.get('metric_id')=='XAUUSD_RETURN':o['value']=0.8
    p10b=run_p10(repo,flip);mb=build_control_room(repo,receipt(p10b),input_pack=flip,data_root=Path(tempfile.mkdtemp()))
    checks.append(check('price_does_not_change_pressure',m['pressure']['source_state_hash']==mb['pressure']['source_state_hash'],{'a':m['overview']['directional_pressure'],'b':mb['overview']['directional_pressure']}))
    checks.append(check('negative_transmission_not_sell',m['overview']['price_transmission']=='NEGATIVE_TRANSMISSION' and m['overview']['pressure_sign']=='BUY'))
    # High readiness never changes permission at presentation time.
    altered=copy.deepcopy(p10);altered['p04']['release_readiness']={'state':'HIGH_READINESS','trade_permission_granted':False};altered['p06']['state']['science_v2']['latent_release']['release_readiness']={'state':'HIGH_READINESS','trade_permission_granted':False}
    mh=build_control_room(repo,receipt(altered),input_pack=fixture,data_root=Path(tempfile.mkdtemp()))
    checks.append(check('readiness_not_permission',mh['overview']['release_readiness']=='HIGH_READINESS' and mh['overview']['trade_permission']=='NO_TRADE'))
    # Missing true flow must remain disclosed.
    noflow=copy.deepcopy(fixture);noflow['gold_observations']=[x for x in noflow['gold_observations'] if x.get('metric_id') not in {'GC_SIGNED_TRADE_IMBALANCE','GC_DEPTH_RESILIENCY'}]
    p10c=run_p10(repo,noflow);mc=build_control_room(repo,receipt(p10c),input_pack=noflow,data_root=Path(tempfile.mkdtemp()));flow=next(x for x in mc['layers'] if x['id']=='flow')
    checks.append(check('missing_flow_partial_unknown',flow['coverage'] in {'PARTIAL','UNKNOWN'} and 'TRUE_ORDER_FLOW_NOT_OBSERVED' in flow['missing_data']))
    # Volume-only evidence may be displayed but never called true flow.
    vol=copy.deepcopy(noflow);vol['gold_observations'].append({'observation_id':'vol','metric_id':'GC_VOLUME','source_id':'CME_VOLUME_OI','observed_at_utc':'2026-08-15T10:20:00Z','status':'AVAILABLE','value':12345,'provenance_ref':'TEST:VOL'})
    p10d=run_p10(repo,vol);md=build_control_room(repo,receipt(p10d),input_pack=vol,data_root=Path(tempfile.mkdtemp()));fd=next(x for x in md['layers'] if x['id']=='flow')
    checks.append(check('volume_not_flow',fd['current_signal']!='OBSERVED_TRUE_FLOW' and md['audit']['volume_flow_substitution_detected'] is False))
    # OI-only evidence cannot alter pressure because it enters P05 only.
    oi=copy.deepcopy(noflow);oi['gold_observations'].append({'observation_id':'oi','metric_id':'GC_OPEN_INTEREST','source_id':'CME_VOLUME_OI','observed_at_utc':'2026-08-15T10:20:00Z','status':'AVAILABLE','value':999999,'provenance_ref':'TEST:OI'})
    p10e=run_p10(repo,oi);me=build_control_room(repo,receipt(p10e),input_pack=oi,data_root=Path(tempfile.mkdtemp()))
    checks.append(check('oi_not_direction',me['pressure']['source_state_hash']==m['pressure']['source_state_hash'] and me['audit']['oi_direction_substitution_detected'] is False))
    # UNKNOWN must survive missing fields.
    missing=copy.deepcopy(p10);missing['p04'].pop('latent_causal_reserve',None);missing['p06']['state']['science_v2']['latent_release'].pop('latent_causal_reserve',None);mm=build_control_room(repo,receipt(missing),input_pack=fixture,data_root=Path(tempfile.mkdtemp()))
    checks.append(check('unknown_remains_unknown',mm['release']['latent_causal_reserve']=='UNKNOWN' or mm['release']['latent_causal_reserve']=={}))
    # Renderer deterministic for same model.
    with tempfile.TemporaryDirectory() as td:
        p1=Path(td)/'a.html';p2=Path(td)/'b.html';render(m,p1);render(m,p2);checks.append(check('rtl_renderer_deterministic',p1.read_bytes()==p2.read_bytes() and 'dir="rtl"' in p1.read_text(encoding='utf-8')))
    checks.append(check('section_order',load_json(BASE/'config/output_contract.json')['section_order']==['overview','pressure','transmission_release','eight_layers','events_timing','runs_memory','report_audit','data_health']))
    # Windows PowerShell 5.1 reads UTF-8-without-BOM scripts through the active ANSI code page.
    # Keep the root launcher ASCII-only so UTF-8 punctuation can never be mis-decoded as smart quote delimiters.
    launcher_bytes=(repo/'AlphaDesk.ps1').read_bytes()
    checks.append(check('windows_powershell51_launcher_encoding_safe',all(b < 128 for b in launcher_bytes),{'non_ascii_bytes':sum(1 for b in launcher_bytes if b >= 128)}))
    # The legacy C1 doctor still expects root AlphaLab wrappers, but P11/P12 govern a direct V1 runtime bridge.
    synthetic_doctor={'status':'FAIL','checks':[{'name':'scientific_v213','pass':True},{'name':'root_launchers_match_certified_templates','pass':False},{'name':'r4_full_preflight','pass':True}],'errors':['root_launchers_match_certified_templates']}
    compat=reconcile_doctor(repo,repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL',synthetic_doctor)
    checks.append(check('environment_legacy_wrapper_reconciled_only_by_p11_direct_binding',compat.get('status')=='PASS' and compat.get('legacy_root_launcher_reconciled') is True and (compat.get('v1_direct_binding') or {}).get('bridge_mode')=='DIRECT_V1_RUNTIME_SURFACE'))
    with tempfile.TemporaryDirectory() as td:
        es=environment_status(repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL',Path(td))
        checks.append(check('environment_missing_receipt_remains_blocked',es.get('status')=='MISSING'))
    gov=verify_p12_authorized_delta(repo,BASE);checks.append(check('p12_governance_authorized_delta',gov['status']=='PASS',gov.get('failed')))
    bad=[x for x in checks if x['status']!='PASS'];out={'schema_version':'1.0.0','phase':'AD-V2-P13','status':'PASS' if not bad else 'FAIL','passed':len(checks)-len(bad),'failed':len(bad),'checks':checks};print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if not bad else 1
if __name__=='__main__':raise SystemExit(main())
