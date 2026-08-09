from pathlib import Path
from .util import load_json, sha256_file, sha256_obj

class RegistryError(RuntimeError): pass

class PromptRegistry:
    def __init__(self,vault_root):
        self.vault=Path(vault_root).resolve(); self.r2=self.vault/'RUNTIME'/'R2 Prompt Execution OS'
        self.registry=load_json(self.r2/'config'/'prompt_registry.json')
        self.pack=load_json(self.r2/'config'/'prompt_pack.json')
        self.graph=load_json(self.r2/'config'/'process_graph.json')
        self.models=load_json(self.r2/'config'/'model_profiles.json')
        self.context_policy=load_json(self.r2/'config'/'context_policy.json')
        self.completion=load_json(self.r2/'config'/'completion_policy.json')
        self._manifests={}
        for x in self.registry['processes']:
            m=load_json(self.vault/x['manifest_path']); self._manifests[m['process_id']]=m
    def process_ids(self): return list(self._manifests)
    def manifest(self,pid):
        if pid not in self._manifests: raise RegistryError('unknown process '+pid)
        return self._manifests[pid]
    def prompt_path(self,pid): return self.vault/self.manifest(pid)['prompt_path']
    def prompt_hash(self,pid): return sha256_file(self.prompt_path(pid))
    def validate(self):
        errs=[]; ids=self.process_ids()
        if len(ids)!=len(set(ids)): errs.append('duplicate process id')
        if len(ids)!=25: errs.append(f'expected 25 processes, found {len(ids)}')
        profiles=set(self.models['profiles'])
        for pid in ids:
            m=self.manifest(pid)
            if not self.prompt_path(pid).is_file(): errs.append(pid+': prompt missing')
            if m['model_profile'] not in profiles: errs.append(pid+': model profile missing')
            for d in m['dependencies']:
                if d not in ids: errs.append(pid+': unknown dependency '+d)
            for c in m.get('canonical_dependencies',[]):
                if not (self.vault/c).exists(): errs.append(pid+': canonical dependency missing '+c)
            for o in m['outputs']:
                if not (self.vault/o['schema_ref']).exists(): errs.append(pid+': output schema missing '+o['schema_ref'])
        # independent worker isolation
        ig=[p for p in ids if self.manifest(p).get('independence_group')=='INDEPENDENT_STATE_CONSTRUCTION']
        for pid in ig:
            if any(d in ig for d in self.manifest(pid)['dependencies']): errs.append(pid+': independent worker depends on peer')
        # authority boundary
        permission_creators=[p for p in ids if 'final_permission' in self.manifest(p)['authority'].get('can_create',[])]
        if permission_creators!=['P63_FINAL_DECISION']: errs.append('final permission authority drift: '+repr(permission_creators))
        direction_creators=[p for p in ids if 'fundamental_direction' in self.manifest(p)['authority'].get('can_create',[])]
        if direction_creators!=['W31_FUNDAMENTAL']: errs.append('direction authority drift: '+repr(direction_creators))
        return errs
