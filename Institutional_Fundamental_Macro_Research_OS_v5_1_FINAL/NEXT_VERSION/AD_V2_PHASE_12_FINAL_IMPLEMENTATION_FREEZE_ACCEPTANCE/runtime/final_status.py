from pathlib import Path
import json,hashlib,os
from .freeze import verify,load,v1_binding
def status(repo,data_root,phase_root):
 f=verify(repo,phase_root);auth=load(Path(phase_root)/'config/final_authority_manifest.json');handoff=load(Path(phase_root)/'FINAL_V2_HANDOFF.json');dr=Path(data_root);receipt=dr/'alpha_desk_v2'/'p12_finalization'/'final_implementation_receipt.json';rec=None
 if receipt.is_file():
  try:rec=json.loads(receipt.read_text(encoding='utf-8'))
  except:rec={'status':'INVALID'}
 binding_status='UNSEALED';current_binding=None
 if rec and rec.get('v1_launcher_binding'):
  try:
   current_binding=v1_binding(repo);stored=rec['v1_launcher_binding'];binding_status='PASS' if stored.get('canonical_sha256')==current_binding.get('canonical_sha256') and stored.get('git_blob')==current_binding.get('git_blob') else 'FAIL_CLOSED'
  except Exception as e:binding_status='FAIL_CLOSED';current_binding={'error':str(e)}
 overall='PASS' if f['status']=='PASS' and binding_status!='FAIL_CLOSED' else 'FAIL_CLOSED'
 return {'schema_version':'1.0.0','phase':'AD-V2-P12','status':overall,'implementation':handoff['implementation'],'implementation_version':handoff['implementation_version'],'freeze':{'status':f['status'],'failed_count':f['failed_count']},'v1_launcher_binding_status':binding_status,'current_v1_launcher_binding':current_binding,'empirical_validation':handoff['empirical_validation'],'production_promotion':handoff['production_promotion'],'normal_command':handoff['normal_command'],'receipt':rec,'authority':auth,'fixed_roadmap_closed':True,'default_next_phase':None}
