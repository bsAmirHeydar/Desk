from pathlib import Path
import platform,json,tempfile,os,sys
from .util import load_json
from .true_forward import selftest as tf_selftest
from .hostcert import certify as host_certify

def run(vault_root):
    v=Path(vault_root).resolve();c=v/'RUNTIME'/'Production Commissioning';checks=[];errors=[]
    def ck(n,b,d=None):checks.append({'name':n,'pass':bool(b),'detail':d});errors.extend([] if b else [n])
    tf=tf_selftest(v);ck('tf1_selftest',tf.get('status')=='PASS',{'passed':tf.get('passed'),'total':tf.get('total')})
    pol=load_json(c/'config'/'true_forward_policy.json');cp=load_json(c/'config'/'commissioning_policy.json');man=load_json(c/'TRUE_FORWARD_MANIFEST.json')
    ck('authoritative_universe_discovered_from_c1',pol.get('configured_market_universe_source','').endswith('commissioning_policy.json#shadow_instruments') and cp.get('shadow_instruments')==['XAUUSD','NASDAQ100','SP500','DJIA','EURUSD','USDJPY'],cp.get('shadow_instruments'))
    ck('authority_isolation',man.get('authority')=={'direction':'NONE','permission':'NONE','broker_write':'NONE','apl_a':'SHADOW_ONLY','m1_new_direction_authority':'NONE'})
    launch=(c/'alpha_commissioning'/'launcher.py').read_text(encoding='utf-8');shadow=(c/'alpha_commissioning'/'shadow.py').read_text(encoding='utf-8')
    ck('shadow_launcher_seals',"seal_truth_state" in launch and "seal_run" in launch)
    ck('six_market_shadow_observes_m1_apla_and_seal',all(x in shadow for x in ('method_plan','apl_a_shadow_bundle','forward_commitment_id','forward_seal_valid')))
    bp=load_json(v/'RUNTIME'/'R4 Scientific Certification and Reproducibility Hardening'/'config'/'certification_surface_baseline.json')
    bad=[k for k in bp.get('files',{}) if 'AlphaLab_Data' in k or '/forward/commitments/' in k or '/forward/outcomes/' in k or '/forward/reviews/' in k or '__pycache__' in k or k.endswith('.pyc')]
    ck('r4_excludes_mutable_forward_evidence_and_pyc',not bad,bad[:10])
    ck('apl_b_absent',not any(p.is_dir() and 'APL-B' in p.name for p in (v/'RUNTIME').iterdir()))
    h=host_certify(v)
    if platform.system()=='Windows': ck('host_truthful_on_windows',h.get('classification') in ('WINDOWS_HOST_PLATFORM_CERTIFIED','HOST_PLATFORM_NOT_CERTIFIED'),h.get('classification'))
    else: ck('nonwindows_cannot_fake_windows_cert',h.get('status')=='PENDING' and h.get('classification')=='HOST_CERTIFICATION_PENDING_REAL_WINDOWS_HOST_EXECUTION',h.get('classification'))
    ck('maturity_not_fabricated',man.get('true_forward_maturity','').startswith('INSUFFICIENT'))
    return {'schema_version':'1.0.0','status':'PASS' if not errors else 'FAIL','passed':sum(1 for x in checks if x['pass']),'total':len(checks),'checks':checks,'errors':errors}
