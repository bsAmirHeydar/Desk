import json, hashlib

def canonical_json_bytes(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")

def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()

def sha256_obj(obj) -> str:
    return sha256_bytes(canonical_json_bytes(obj))

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def dump_json(path, obj):
    from pathlib import Path
    p=Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    tmp=p.with_name(p.name+".tmp")
    tmp.write_bytes(canonical_json_bytes(obj))
    tmp.replace(p)
