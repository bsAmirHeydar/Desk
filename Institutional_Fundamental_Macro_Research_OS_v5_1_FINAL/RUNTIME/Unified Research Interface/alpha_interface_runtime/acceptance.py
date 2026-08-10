from pathlib import Path
import json,re
from .selftest import run as selftest
from .compiler import compile_request

def run(vault_root):
    v=Path(vault_root).resolve();checks=[]
    def ck(n,b,d=None):checks.append({'name':n,'pass':bool(b),'detail':d})
    st=selftest(v);ck('selftest',st['status']=='PASS',st.get('errors'))
    m=json.loads((v/'RUNTIME'/'Unified Research Interface'/'UNIFIED_INTERFACE_MANIFEST.json').read_text(encoding='utf-8'));ck('one_interface',m['version']=='UI1.0.0' and m['interface_freeze'] is True)
    r3=json.loads((v/'RUNTIME'/'R3 Operational Execution and Learning OS'/'schemas'/'AlphaLab_R3_Launch_Request.schema.json').read_text(encoding='utf-8'));ck('r3_schema_universal','research_program_id' in r3['properties'] and 'strategy_id' in r3['properties'] and 'lookahead_policy' in r3['properties'])
    c=compile_request(v,{'subject':'NASDAQ100','request_text':'نزدک امروز چرا ریخت و فشار فروش چقدر مونده؟','mode':'LIVE'});ck('multi_intent','CAUSAL_ATTRIBUTION' in c['research_classes'] and 'PERSISTENCE_REVERSAL' in c['research_classes'])
    ck('certified_truth',c['execution_eligibility']=='CERTIFIED_RUNTIME')
    ck('authority',m['authority']['request_compiler_direction']=='NONE' and m['authority']['report_composer_direction']=='NONE' and m['authority']['apl_a']=='SHADOW_ONLY' and m['authority']['broker_write']=='NONE')
    # R2 eight clusters intact
    preg=json.loads((v/'RUNTIME'/'R2 Prompt Execution OS'/'config'/'prompt_registry.json').read_text(encoding='utf-8'));ids={x.get('process_id') or x.get('prompt_id') or x.get('id') for x in (preg.get('processes') or preg.get('prompts') or preg.get('registry') or [])};needed={'W30_TEMPORAL','W31_FUNDAMENTAL','W32_EXPECTATIONS_POLICY_REGIME','W33_NARRATIVE_REFLEXIVITY_CONSUMPTION','W34_POSITIONING','W35_ACTUAL_FLOW','W36_FUNDING_PLUMBING','W37_MECHANICS_CAPACITY_VOL'};ck('eight_clusters',needed.issubset(ids),sorted(needed-ids))
    # root human entrypoint uses UI, commission remains separate
    root=(v.parent/'AlphaLab.ps1').read_text(encoding='utf-8');ck('root_research_entrypoint','Unified Research Interface' in root and 'alpha_research.py' in root)
    ck('operations_separate',(v.parent/'AlphaLab_Commission.ps1').is_file())
    # no misleading active root any-symbol
    ck('legacy_root_removed',not (v.parent/'AlphaLab_V14_Any_Symbol_Live_Launcher.md').exists())
    bad=[x for x in checks if not x['pass']];return {'schema_version':'1.0.0','status':'PASS' if not bad else 'FAIL','interface_version':'UI1.0.0','passed':len(checks)-len(bad),'total':len(checks),'checks':checks,'errors':[x['name'] for x in bad]}
