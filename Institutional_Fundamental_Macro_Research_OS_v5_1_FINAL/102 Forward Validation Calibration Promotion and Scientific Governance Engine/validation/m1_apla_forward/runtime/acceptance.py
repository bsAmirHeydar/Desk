from pathlib import Path
from .util import add_paths,load
from .engine import run_suite

def run(vault_root):
    v=Path(vault_root).resolve();add_paths(v)
    from alpha_method_runtime.selftest import run as mself
    from alpha_method_runtime.parity import run as mpar
    from alpha_perspective_runtime.selftest import run as aself
    from alpha_perspective_runtime.parity import run as apar
    from alpha_perspective_runtime.acceptance import run as aacc
    # alpha_certification path
    import sys
    r4p=str(v/'RUNTIME'/'R4 Scientific Certification and Reproducibility Hardening')
    if r4p not in sys.path:sys.path.insert(0,r4p)
    from alpha_certification.fingerprint import verify as r4verify
    s=run_suite(v); checks=[]
    def ck(n,x,d=None):checks.append({'gate':n,'pass':bool(x),'detail':d})
    ms=mself(v);mp=mpar(v);aps=aself(v);app=apar(v);apa=aacc(v,app)
    ck('A_BASELINE_HEALTH',ms['status']=='PASS' and aps['status']=='PASS')
    ck('B_M1_REGRESSION',ms['status']=='PASS',{'passed':ms.get('passed'),'total':ms.get('total')})
    ck('C_APL_A_REGRESSION',aps['status']=='PASS' and apa['status']=='PASS',{'selftest':aps.get('status'),'acceptance':apa.get('status')})
    ck('D_DECISION_PARITY',mp['status']=='PASS' and app['status']=='PASS')
    fv=load(v/'102 Forward Validation Calibration Promotion and Scientific Governance Engine'/'validation'/'m1_apla_forward'/'M1_APLA_FORWARD_VALIDATION_MANIFEST.json')
    ck('E_AUTHORITY_ISOLATION',fv['authority']['direction']=='NONE' and fv['authority']['apl_a']=='SHADOW_ONLY')
    ck('F_ROUTER_VALIDATION',s['router']['paraphrase_stable'] and all(s['router']['proportional'].values()),s['router'])
    a=next(r for r in s['records'] if r['case_id']=='FV1-A');ck('G_NEGATIVE_CONTROLS',a['m1']['status']=='PASS' and not a['apl_a']['findings'])
    c=next(r for r in s['records'] if r['case_id']=='FV1-C');ck('H_SOURCE_DEPENDENCY',c['m1']['status']=='RESEARCH_REQUIRED')
    p=next(r for r in s['records'] if r['case_id']=='FV1-P');ck('I_UNKNOWN_PRESERVATION',p['m1']['status']=='PASS')
    d=next(r for r in s['records'] if r['case_id']=='FV1-D');ck('J_CAUSAL_GOVERNANCE',d['m1']['status']=='METHOD_INVALID')
    lenses={f['lens'] for r in s['records'] for f in r['apl_a']['findings']};ck('K_APL_A_LENS_EXECUTION',len(lenses)==8,sorted(lenses))
    ints={r['interaction'] for r in s['records']};ck('L_INTERACTION_MATRIX',{'M1_ONLY','APL_A_ONLY','BOTH_SAME_ISSUE','BOTH_DIFFERENT_DIMENSIONS','CONFLICT'}.issubset(ints),sorted(ints))
    l=next(r for r in s['records'] if r['case_id']=='FV1-L');ck('M_FALSE_POSITIVE_TRACKING',any(x.get('classified_false_positive') for x in l['apl_a']['findings']))
    ck('N_PERFORMANCE',s['performance']['m1_ms']['p95']<50 and s['performance']['apl_harness_ms']['p95']<10,s['performance'])
    ck('O_NO_APL_B',fv.get('apl_b')=='NOT_IMPLEMENTED')
    ck('P_NO_UNAUTHORIZED_PROMOTION',fv.get('promotion')=='FORBIDDEN_IN_THIS_PHASE' and s['authority_unchanged'])
    ck('Q_VALIDATION_TRUTH_LABELING',s['truth_states_observed']==['SYNTHETIC_VALIDATION'] and s['true_forward_status']=='TRUE_FORWARD_EVIDENCE_INSUFFICIENT')
    rv=r4verify(v); c1=load(v/'RUNTIME'/'Production Commissioning'/'COMMISSIONING_MANIFEST.json');ck('R_R4_C1_COMPATIBILITY',rv['pass'] and c1.get('commissioning_version')=='C1.0.0',{'r4':rv,'c1':c1.get('commissioning_version')})
    bad=[x for x in checks if not x['pass']];return {'status':'PASS' if not bad and s['status']=='PASS' else 'FAIL','validation_version':'FV1.0.0','passed':len(checks)-len(bad),'total':len(checks),'gates':checks,'suite_status':s['status'],'true_forward_status':s['true_forward_status'],'authority_unchanged':True,'errors':[x['gate'] for x in bad]}
