from pathlib import Path
from .util import load

def run(vault_root):
    v=Path(vault_root).resolve(); root=v/'102 Forward Validation Calibration Promotion and Scientific Governance Engine'/'validation'/'m1_apla_forward'; checks=[]
    def ck(n,x,d=None):checks.append({'name':n,'pass':bool(x),'detail':d})
    try:m=load(v/'RUNTIME'/'Core Research Method Kernel'/'METHOD_KERNEL_MANIFEST.json');ck('m1_installed',m.get('method_version')=='M1.0.1');ck('m1_no_direction_authority',m.get('authority',{}).get('direction')=='NONE')
    except Exception as e:ck('m1_installed',False,str(e))
    try:a=load(v/'RUNTIME'/'APL-A Alpha Perspective Layer'/'APL_A_MANIFEST.json');ck('apl_shadow_only',a.get('mode')=='SHADOW_ONLY' and a.get('authority',{}).get('direction')=='NONE')
    except Exception as e:ck('apl_shadow_only',False,str(e))
    aplb=list((v/'RUNTIME').glob('APL-B*'))+list((v/'RUNTIME').glob('**/APL_B_MANIFEST.json'));ck('no_apl_b',not aplb,[str(x) for x in aplb])
    cp=load(v/'CURRENT_PRODUCTION_MANIFEST.json');ck('direction_fundamental_only',cp.get('decision_authority',{}).get('direction')=='FUNDAMENTAL_ONLY')
    fv=load(root/'M1_APLA_FORWARD_VALIDATION_MANIFEST.json');ck('truthful_forward_state',fv.get('true_forward_status')=='TRUE_FORWARD_EVIDENCE_INSUFFICIENT');ck('no_promotion',fv.get('promotion')=='FORBIDDEN_IN_THIS_PHASE')
    needed=['AlphaLab_D4_M1_APLA_Validation_Record.schema.json','AlphaLab_D4_M1_APLA_Readiness_Matrix.schema.json','AlphaLab_D4_M1_APLA_Interaction_Matrix.schema.json','AlphaLab_D4_M1_APLA_Postmortem.schema.json','AlphaLab_D4_M1_APLA_Forward_Commitment.schema.json']
    ck('schemas_present',all((root/'schemas'/x).is_file() for x in needed))
    rb=load(v/'RUNTIME'/'R4 Scientific Certification and Reproducibility Hardening'/'config'/'certification_surface_baseline.json'); volatile=[k for k in rb.get('files',{}) if '__pycache__' in k or k.endswith('.pyc')];ck('r4_surface_source_only',not volatile,volatile)
    bad=[x for x in checks if not x['pass']];return {'status':'PASS' if not bad else 'FAIL','validation_version':'FV1.0.0','checks':checks,'errors':[x['name'] for x in bad]}
