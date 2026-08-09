import uuid
from .util import sha256_obj

def make_job(run_id,pid,registry,context):
    m=registry.manifest(pid)
    job={'schema_version':'1.0.0','job_id':'JOB_'+uuid.uuid4().hex[:16].upper(),'run_id':run_id,'process_id':pid,'process_version':m['version'],'stage':m['stage'],'prompt_path':m['prompt_path'],'prompt_sha256':registry.prompt_hash(pid),'model_profile':m['model_profile'],'context_bundle':context,'expected_outputs':m['outputs']}
    job['job_hash']=sha256_obj({k:v for k,v in job.items() if k not in ('job_id','job_hash')})
    return job
