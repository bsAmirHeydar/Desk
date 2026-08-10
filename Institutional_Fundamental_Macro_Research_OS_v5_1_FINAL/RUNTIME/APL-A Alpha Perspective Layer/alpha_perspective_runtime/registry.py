from pathlib import Path
from .util import load_json,chash
class RegistryError(RuntimeError):pass
class APLRegistry:
 def __init__(self,vault):
  self.vault=Path(vault);self.root=self.vault/'RUNTIME'/'APL-A Alpha Perspective Layer';self.cfg=load_json(self.root/'config/prompt_registry.json');self.pack=load_json(self.root/'config/prompt_pack.json');self.graph=load_json(self.root/'config/process_graph.json');self._m={}
  for x in self.cfg['processes']:
   m=load_json(self.vault/x['manifest_path']);self._m[m['process_id']]=m
 def ids(self):return self.graph['order']
 def manifest(self,p):return self._m[p]
 def validate(self):
  e=[]
  if len(self._m)!=8:e.append('expected 8 APL-A processes')
  for pid in self.ids():
   if pid not in self._m:e.append('missing process '+pid);continue
   m=self._m[pid];pp=self.vault/m['prompt_path']
   if not pp.is_file():e.append(pid+': prompt missing')
   for c in m.get('canonical_dependencies',[]):
    if not (self.vault/c).is_file():e.append(pid+': canon missing '+c)
   for o in m['outputs']:
    if not (self.vault/o['schema_ref']).is_file():e.append(pid+': schema missing '+o['schema_ref'])
   bad=set(m['authority'].get('can_create',[])) & set(['fundamental_direction','final_permission','fact'])
   if bad:e.append(pid+': authority drift')
  return e
