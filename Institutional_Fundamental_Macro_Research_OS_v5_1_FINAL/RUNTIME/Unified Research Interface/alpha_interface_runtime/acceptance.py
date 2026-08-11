from pathlib import Path
import json
from .selftest import run as selftest,_fixture
from .compiler import compile_request
from .render import explorer_html
from .simple_language import simplify_text,to_fa

def run(vault_root):
    v=Path(vault_root).resolve();checks=[]
    def ck(n,b,d=None):checks.append({'name':n,'pass':bool(b),'detail':d})
    st=selftest(v);ck('selftest',st['status']=='PASS',st.get('errors'))
    m=json.loads((v/'RUNTIME'/'Unified Research Interface'/'UNIFIED_INTERFACE_MANIFEST.json').read_text(encoding='utf-8'));ck('ux3_frozen',m['version']=='UX3.0.0' and m['interface_freeze'] is True and m['ux']['architecture']=='COMMAND_CENTER_MARKET_WORKSPACE_LENS_DEEP_DIVE')
    schema=json.loads((v/'RUNTIME'/'Unified Research Interface'/'schemas'/'AlphaLab_Report_Model.schema.json').read_text(encoding='utf-8'));ck('report_model_v2_ux3_view',schema['properties']['report_model_version']['const']=='2.0.0' and schema['properties']['interface_version']['const']=='UX3.0.0' and 'layer1' in schema['required'] and 'layer3' in schema['required'])
    c=compile_request(v,{'subject':'NASDAQ100','request_text':'نزدک امروز چرا ریخت و فشار فروش چقدر مونده؟','mode':'LIVE'});ck('multi_intent','CAUSAL_ATTRIBUTION' in c['research_classes'] and 'PERSISTENCE_REVERSAL' in c['research_classes'])
    ck('authority',m['authority']['request_compiler_direction']=='NONE' and m['authority']['report_composer_direction']=='NONE' and m['authority']['apl_a']=='SHADOW_ONLY' and m['authority']['broker_write']=='NONE')
    model=_fixture();h=explorer_html(model)
    ck('command_center_seconds_surface','تصویر فعلی بازار' in h and 'market-strip' in h and 'عامل اصلی' in h)
    ck('lens_index_complete','id="lens-index"' in h and all(x in h for x in ['وضعیت بنیادی','نقدینگی و تأمین مالی','ساختار، ظرفیت و نوسان بازار']))
    ck('single_deep_drawer','id="drawer"' in h and h.count('role="dialog"')==1 and '<dialog' not in h)
    ck('simple_language','convexity' not in simplify_text('duration convexity is high').lower() and to_fa('UNKNOWN')=='نامشخص')
    ck('scientific_fidelity','علت قطعی هنوز مشخص نیست' in h)
    ck('request_awareness','نرخ واقعی یکی از توضیح‌های اصلی است' in h)
    ck('pressure_surface',all(x in h for x in ['قدرت نیرو','مصرف','فشار باقی‌مانده','ریسک برگشت']))
    ck('quality_user_facing','کیفیت و محدودیت‌ها' in h and 'کیفیت فرایند تحلیل با قطعیت بازار یکی نیست' in h)
    ck('perspective_separation','دیدگاه فلسفی' in h and 'این بخش جهت بازار را تعیین نمی‌کند' in h)
    ck('no_debug_audit_surface','Scientific Audit' not in h and 'artifact_hash' not in h and 'technical_detail' not in h)
    ck('responsive_and_accessible','@media(max-width:900px)' in h and 'focus-visible' in h and 'prefers-reduced-motion' in h and 'aria-modal="true"' in h)
    ck('no_fake_precision','67/100' not in h and '67%' not in h)
    preg=json.loads((v/'RUNTIME'/'R2 Prompt Execution OS'/'config'/'prompt_registry.json').read_text(encoding='utf-8'));ids={x.get('process_id') or x.get('prompt_id') or x.get('id') for x in (preg.get('processes') or preg.get('prompts') or preg.get('registry') or [])};needed={'W30_TEMPORAL','W31_FUNDAMENTAL','W32_EXPECTATIONS_POLICY_REGIME','W33_NARRATIVE_REFLEXIVITY_CONSUMPTION','W34_POSITIONING','W35_ACTUAL_FLOW','W36_FUNDING_PLUMBING','W37_MECHANICS_CAPACITY_VOL'};ck('eight_clusters',needed.issubset(ids),sorted(needed-ids))
    ck('root_entrypoint',(v.parent/'AlphaLab.ps1').is_file() and not (v.parent/'AlphaLab_V14_Any_Symbol_Live_Launcher.md').exists())
    rp=json.loads((v/'RUNTIME'/'Unified Research Interface'/'config'/'run_command_policy.json').read_text(encoding='utf-8'))
    ck('one_command_human_surface',m.get('canonical_local_shortcut','').endswith('AlphaLab.ps1 run <subject>') and rp['command']=='run <subject>')
    ck('chat_native_defaults',rp['defaults']=={'mode':'LIVE','as_of':'NOW','horizon':'AUTO_INTRADAY_SESSION_WITH_DAILY_CONTEXT','depth':'DEEP','output_profile':'EXPLORER','locale':'fa-IR'})
    ck('chat_native_authority',rp['direction_authority']=='NONE' and rp['broker_write']=='NONE' and rp['research_orchestration']['perspective']=='APL-A_SHADOW_ONLY')
    ck('apl_b_not_implemented',not any(p.is_dir() and 'APL-B' in p.name for p in (v/'RUNTIME').iterdir()))
    q=json.loads((v/'RUNTIME'/'Unified Research Interface'/'config'/'run_quality_registry.json').read_text(encoding='utf-8'));ck('run2_mandatory_quality',q['gate_set_version']=='RUN2.0.0' and {x['gate_id'] for x in q['gates']}.issuperset({'PRE_RUN_INTEGRITY','EVIDENCE_INTEGRITY','EIGHT_CLUSTER_COVERAGE','M1_HARD_GATE','THESIS_DESTROYER','PREMORTEM','REPORT_FIDELITY','PERSISTENCE'}))
    mp=json.loads((v/'RUNTIME'/'Unified Research Interface'/'config'/'run_memory_policy.json').read_text(encoding='utf-8'));ck('run2_persistence_contract',mp['capsule_immutable'] is True and mp['source_fingerprint_includes_run_memory'] is False)
    ck('run2_one_command_persistence',rp.get('quality_gates')=='MANDATORY' and rp.get('persistence')=='ON' and rp.get('previous_run_compare')=='AUTO')
    ck('run2_chat_portable_memory',mp['chat_native']['portable_capsule_required'] is True and mp['chat_native']['mutate_uploaded_vault_in_place'] is False)
    ck('run2_direction_authority',mp['authority']['direction']=='NONE' and mp['authority']['broker_write']=='NONE')
    bad=[x for x in checks if not x['pass']]
    return {'schema_version':'1.0.0','status':'PASS' if not bad else 'FAIL','interface_version':'UX3.0.0','passed':len(checks)-len(bad),'total':len(checks),'checks':checks,'errors':[x['name'] for x in bad]}
