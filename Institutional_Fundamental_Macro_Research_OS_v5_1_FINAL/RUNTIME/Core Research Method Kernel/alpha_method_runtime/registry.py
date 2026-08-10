from pathlib import Path
from .util import load_json

class MethodRegistry:
    def __init__(self,vault_root):
        self.vault=Path(vault_root).resolve(); self.root=self.vault/'RUNTIME'/'Core Research Method Kernel'
        self.manifest=load_json(self.root/'METHOD_KERNEL_MANIFEST.json')
        self.constitution=load_json(self.root/'config'/'research_constitution.json')
        self.protocols=load_json(self.root/'config'/'protocol_registry.json')
        self.router=load_json(self.root/'config'/'router_policy.json')
        self.authority=load_json(self.root/'config'/'authority_policy.json')
        self.validation=load_json(self.root/'config'/'validation_policy.json')
        self.by_class={x['research_class']:x for x in self.protocols['protocols']}
    def protocol(self,research_class): return self.by_class[research_class]
    def schema_ref(self,name): return f'RUNTIME/Core Research Method Kernel/schemas/{name}'
    def validate(self):
        errs=[]
        if self.manifest.get('method_version')!='M1.0.0': errs.append('method version')
        if self.manifest.get('authority',{}).get('direction')!='NONE': errs.append('direction authority')
        if self.manifest.get('authority',{}).get('permission')!='NONE': errs.append('permission authority')
        if self.manifest.get('apl_b')!='NOT_IMPLEMENTED': errs.append('APL-B boundary')
        classes=set(self.protocols.get('research_classes',[])); mapped=set(self.by_class)
        if classes!=mapped: errs.append('protocol coverage')
        ids=[x['protocol_id'] for x in self.protocols['protocols']]
        if len(ids)!=len(set(ids)): errs.append('duplicate protocol id')
        for rel in ['AlphaLab_Method_Plan.schema.json','AlphaLab_Method_Claim.schema.json','AlphaLab_Method_Evidence_Item.schema.json','AlphaLab_Method_Uncertainty_Register.schema.json','AlphaLab_Method_Source_Dependency_Graph.schema.json','AlphaLab_Method_Receipt.schema.json','AlphaLab_Method_Exception.schema.json','AlphaLab_Method_Quarantine_Receipt.schema.json','AlphaLab_Proxy_Contract.schema.json','AlphaLab_Model_Method_Card.schema.json']:
            if not (self.root/'schemas'/rel).is_file(): errs.append('missing schema '+rel)
        return errs
