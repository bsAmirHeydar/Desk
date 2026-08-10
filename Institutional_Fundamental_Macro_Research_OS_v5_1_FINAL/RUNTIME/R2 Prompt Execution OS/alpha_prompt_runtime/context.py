from pathlib import Path
from .util import sha256_obj, sha256_file

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
        # Commissioning C1: execute P11's dynamic full-vault retrieval plan, not merely record it.
        # Every selected path is resolved inside the vault and hash-pinned into the Context Bundle,
        # so downstream workers receive the exact canonical material P11 selected without drift.
        if pid not in ('P10_SCOPE','P11_EVIDENCE_PLAN') and 'retrieval_plan' in byname:
            try:
                plan=self.rt.store.load_artifact_json(run_id,'retrieval_plan')
                for rel in plan.get('selected_paths',[]) or []:
                    if not isinstance(rel,str) or not rel.strip(): continue
                    rel=rel.replace('\\','/').lstrip('/')
                    q=(self.vault/rel).resolve()
                    if self.vault not in q.parents and q!=self.vault: raise ContextError(f'{pid}: retrieval-plan path escaped vault: {rel}')
                    if not q.is_file(): raise ContextError(f'{pid}: retrieval-plan canonical path missing: {rel}')
                    if rel not in paths: paths.append(rel)
            except ContextError: raise
            except Exception as e: raise ContextError(f'{pid}: invalid retrieval-plan dynamic context: {e}') from e
        canon_paths=sorted(set(paths)); canon_hashes=[{'path':p,'sha256':sha256_file(self.vault/p)} for p in canon_paths]
        bundle={'schema_version':'1.0.0','run_id':run_id,'process_id':pid,'analysis_cutoff_utc':m['analysis_cutoff_utc'],'prompt_sha256':self.registry.prompt_hash(pid),'prompt_pack_version':self.registry.pack['version'],'input_artifacts':sorted(inputs,key=lambda x:x['logical_name']),'canonical_context_paths':canon_paths,'canonical_context_hashes':canon_hashes,'forbidden_context_check':'PASS'}
        bundle['bundle_hash']=sha256_obj({k:v for k,v in bundle.items() if k!='bundle_hash'})
        return bundle
