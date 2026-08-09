import json, hashlib
from pathlib import Path

def canonical_json_bytes(obj):
    return (json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode("utf-8")

def sha256_bytes(b): return "sha256:"+hashlib.sha256(b).hexdigest()
def sha256_obj(obj): return sha256_bytes(canonical_json_bytes(obj))
def sha256_file(path): return sha256_bytes(Path(path).read_bytes())
def load_json(path):
    with open(path,"r",encoding="utf-8") as f: return json.load(f)
