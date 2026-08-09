from pathlib import Path
import os,json
from .util import now

def inspect(vault_root):
    v=Path(vault_root);hp=json.loads((v/'RUNTIME'/'R3 Operational Execution and Learning OS'/'config'/'host_policy.json').read_text(encoding='utf-8'));default=hp['default_binding'];b=hp['bindings'][default]
    if b['adapter']=='COMMAND':configured=bool(os.environ.get(b.get('command_env','')))
    elif b['adapter']=='HTTP_JSON':configured=bool(os.environ.get(b.get('endpoint_env','')))
    else:configured=False
    return {'schema_version':'1.0.0','host_binding':default,'provider_attested':False,'host_configured':configured,'source_binding_state':'REQUIRES_ACTUAL_ENVIRONMENT_AUDIT','secrets_policy':hp.get('secret_policy'),'status':'PENDING_ATTESTATION','created_at_utc':now()}
