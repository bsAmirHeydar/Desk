from __future__ import annotations
import hashlib,json,html,urllib.parse
from pathlib import Path
PHASE=Path(__file__).resolve().parents[1]
def load(path,default=None):
 p=Path(path);return json.loads(p.read_text(encoding='utf-8-sig')) if p.exists() else default
def cfg(name,default=None):return load(PHASE/'config'/name,default)
def canonical_bytes(o):return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False,default=str).encode('utf-8')
def sha_obj(o):return hashlib.sha256(canonical_bytes(o)).hexdigest()
def sha_file(p):
 h=hashlib.sha256();h.update(Path(p).read_bytes());return h.hexdigest()
def esc(x):return html.escape(str('—' if x is None else x),quote=True)
def safe_url(x):
 if not x:return None
 try:
  u=urllib.parse.urlparse(str(x));return str(x) if u.scheme.lower() in set((cfg('security_policy.json') or {}).get('safe_url_schemes',['http','https'])) else None
 except Exception:return None
def label(v,kind=None):
 r=cfg('label_registry.json',{}) or {};v='UNKNOWN' if v is None else str(v)
 if kind=='root':return (r.get('roots') or {}).get(v,v)
 if kind=='plane':return (r.get('planes') or {}).get(v,v)
 return (r.get('states') or {}).get(v,v)
def term(k):return (cfg('label_registry.json',{}).get('terms') or {}).get(k,k)
def uniq(xs):
 out=[]
 for x in xs:
  if x not in out:out.append(x)
 return out
