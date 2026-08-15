from __future__ import annotations
from pathlib import Path
import hashlib,json

def canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,default=str)
def hsh(x): return 'sha256:'+hashlib.sha256(canon(x).encode()).hexdigest()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write_json(p,obj):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');return str(p)
