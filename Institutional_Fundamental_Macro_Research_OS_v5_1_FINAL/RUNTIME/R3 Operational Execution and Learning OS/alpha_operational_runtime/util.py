from pathlib import Path
import json,hashlib,base64,uuid
from datetime import datetime,timezone

def now(): return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def sha256_bytes(b): return 'sha256:'+hashlib.sha256(b).hexdigest()
def canonical_bytes(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def sha256_obj(x): return sha256_bytes(canonical_bytes(x))
def load_json(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def dump_json(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
def uid(prefix): return prefix+'_'+uuid.uuid4().hex[:20].upper()
def decode_content(item):
    enc=item.get('content_encoding','UTF8_TEXT'); c=item.get('content','')
    if enc=='BASE64': return base64.b64decode(c)
    return c.encode('utf-8')
def safe_subject(s): return ''.join(c if c.isalnum() or c in '._-' else '_' for c in str(s))


def validate_scientific_schema(vault_root,schema_ref,payload):
    """Validate an R3 D4 artifact with the same strict Draft 2020-12 validator used by R2."""
    import sys
    v=Path(vault_root).resolve(); p=str(v/'RUNTIME'/'R2 Prompt Execution OS')
    if p not in sys.path: sys.path.insert(0,p)
    from alpha_prompt_runtime.validation import validate_json_schema
    return validate_json_schema(v,schema_ref,payload)
