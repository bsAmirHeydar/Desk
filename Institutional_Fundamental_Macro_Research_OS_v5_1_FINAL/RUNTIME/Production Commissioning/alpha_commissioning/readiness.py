from pathlib import Path
from .util import load_json,dump_json,now,data_root,add_runtime_paths,current_certification_surface,repo_git_state

def evaluate(vault_root,signoff=False):
    v=Path(vault_root).resolve();dr=data_root(v);pol=load_json(v/'RUNTIME'/'Production Commissioning'/'config'/'commissioning_policy.json');checks=[];errors=[]
    add_runtime_paths(v)
    try:
        from alpha_certification.preflight import run as r4run;r4=r4run(v);ok=r4.get('status')=='PASS';surface=current_certification_surface(v)
    except Exception as e:r4={};surface=None;ok=False;errors.append('r4: '+str(e))
    checks.append({'name':'r4_full_offline_certified','pass':ok})
    receipts={}
    for name,file,cls in [('environment','environment_receipt.json','ENVIRONMENT_CERTIFIED'),('shadow','shadow_receipt.json','SHADOW_PRODUCTION_CERTIFIED')]:
        p=dr/'commissioning'/file
        try:r=load_json(p);ok=r.get('status')=='PASS' and r.get('classification')==cls
        except Exception as e:r={};ok=False;errors.append(name+': '+str(e))
        receipts[name]=r;checks.append({'name':name+'_certified','pass':ok})
        same=bool(surface) and r.get('certification_surface_fingerprint')==surface;checks.append({'name':name+'_surface_current','pass':same})
        if name=='shadow':
            dc=int(r.get('decision_critical_gap_total') or 0);sok=(dc==0) if pol.get('readiness_requires_zero_decision_critical_gaps_in_shadow_basket') else True;checks.append({'name':'shadow_decision_critical_source_sufficiency','pass':sok,'detail':{'decision_critical_gap_total':dc}})
    try:gs=repo_git_state(v);checks.append({'name':'tracked_working_tree_clean','pass':gs['tracked_clean']})
    except Exception as e:gs={'head':None,'tracked_clean':False};checks.append({'name':'tracked_working_tree_clean','pass':False});errors.append('git: '+str(e))
    checks.append({'name':'operator_signoff','pass':bool(signoff)})
    hard_without_signoff=all(x['pass'] for x in checks if x['name']!='operator_signoff')
    if not hard_without_signoff:status='FAIL';classification='NOT_READY'
    elif not signoff:status='PENDING';classification='READY_FOR_OPERATOR_SIGNOFF'
    else:status='PASS';classification='PRODUCTION_READY_PERMISSION_ONLY'
    out={'schema_version':'1.0.0','status':status,'classification':classification,'operator_signoff':bool(signoff),'checks':checks,'broker_write_authority':'NONE','order_creation':False,'scientific_permission_authority':'P63_ONLY','operational_override':'BLOCK_ONLY','certification_surface_fingerprint':surface,'git_commit':gs.get('head'),'created_at_utc':now(),'errors':errors};dump_json(dr/'commissioning'/'readiness_receipt.json',out);return out
