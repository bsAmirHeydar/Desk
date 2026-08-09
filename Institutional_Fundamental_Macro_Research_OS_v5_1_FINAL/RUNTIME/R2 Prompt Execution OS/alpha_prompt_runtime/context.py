from pathlib import Path
from .util import sha256_obj

FORBIDDEN_NAMES={'outcome','path_metrics','counterfactuals','realized_r','future_price_path'}

class ContextError(RuntimeError): pass

class ContextCompiler:
    def __init__(self,vault,rt,registry): self.vault=Path(vault); self.rt=rt; self.registry=registry
    def compile(self,run_id,pid):
        m=self.rt.store.load_manifest(run_id); pm=self.registry.manifest(pid); rows=self.rt.catalog.list_artifacts(run_id)
        byname={r['logical_name']:r for r in rows}
        inputs=[]
        for name in pm.get('required_inputs',[]):
            if name not in byname: raise ContextError(f'{pid}: required artifact missing: {name}')
            r=byname[name]
            if r['world'] in ('OUTCOME','LEARNING'): raise ContextError(f'{pid}: forbidden future-world input: {name}')
            inputs.append({'logical_name':name,'artifact_hash':r['artifact_hash'],'world':r['world'],'stage':r['stage']})
        # optional only if present and decision/meta
        for name in pm.get('optional_inputs',[]):
            if name in byname and name not in {x['logical_name'] for x in inputs}:
                r=byname[name]
                if r['world'] in ('OUTCOME','LEARNING'): raise ContextError(f'{pid}: forbidden optional future-world input: {name}')
                inputs.append({'logical_name':name,'artifact_hash':r['artifact_hash'],'world':r['world'],'stage':r['stage']})
        paths=[]
        for p in pm.get('canonical_dependencies',[]):
            q=self.vault/p
            if not q.exists(): raise ContextError(f'{pid}: canonical dependency missing: {p}')
            paths.append(p)
        # include asset books for exact instrument if production manifest defines them
        try:
            import json
            prod=json.loads((self.vault/'CURRENT_PRODUCTION_MANIFEST.json').read_text(encoding='utf-8'))
            subj=m['subject']
            for p in prod.get('asset_books',{}).get(subj,[]):
                if p not in paths and (self.vault/p).exists(): paths.append(p)
        except Exception: pass
        bundle={'schema_version':'1.0.0','run_id':run_id,'process_id':pid,'analysis_cutoff_utc':m['analysis_cutoff_utc'],'prompt_sha256':self.registry.prompt_hash(pid),'prompt_pack_version':self.registry.pack['version'],'input_artifacts':sorted(inputs,key=lambda x:x['logical_name']),'canonical_context_paths':sorted(set(paths)),'forbidden_context_check':'PASS'}
        bundle['bundle_hash']=sha256_obj({k:v for k,v in bundle.items() if k!='bundle_hash'})
        return bundle
