from .registry import MethodRegistry

class RouteError(RuntimeError): pass

def _tag_map(tags):
    out={}
    for raw in tags or []:
        s=str(raw); low=s.lower()
        if ':' in s:
            k,v=s.split(':',1); out[k.strip().lower()]=v.strip()
        out[low]=True
    return out

def route(vault_root, run_request):
    reg=MethodRegistry(vault_root); tags=list(run_request.get('tags') or []); tmap=_tag_map(tags); reasons=[]
    explicit=None
    for prefix in reg.router.get('explicit_tag_prefixes',[]):
        key=prefix.rstrip(':').lower()
        if key in tmap: explicit=str(tmap[key]).upper().replace('-','_').replace(' ','_')
    if explicit:
        if explicit not in reg.by_class: raise RouteError('unknown explicit research class: '+explicit)
        rc=explicit; reasons.append('explicit research class tag')
    else:
        rc=None
        coverage=run_request.get('coverage_mode')
        if coverage in reg.router.get('coverage_rules',{}):
            rc=reg.router['coverage_rules'][coverage]; reasons.append('coverage mode '+str(coverage))
        if rc is None:
            lowtags=[str(x).lower() for x in tags]
            for rule in reg.router.get('tag_rules',[]):
                if any(rule['contains'].lower() in x for x in lowtags): rc=rule['class']; reasons.append('tag rule '+rule['contains']); break
        if rc is None:
            rc=reg.router['default_research_class']; reasons.append('production/default research class')
    proto=reg.protocol(rc)
    depth=str(run_request.get('research_depth') or 'AUTO').upper(); rigor=proto['default_rigor']
    if depth=='DEEP': rigor='DEEP'; reasons.append('explicit deep research depth')
    for raw in tags:
        s=str(raw)
        if s.lower().startswith('method_rigor:'):
            r=s.split(':',1)[1].upper()
            if r not in reg.router['rigor_levels']: raise RouteError('invalid method rigor '+r)
            rigor=r; reasons.append('explicit method rigor')
        if s.lower() in ('materiality:critical','critical-materiality','tail-exposure','novel-regime'):
            rigor='CRITICAL'; reasons.append('critical escalation tag')
    if rc in ('NEW_ASSET_RESEARCH',): rigor='CRITICAL'
    if rc in ('CAUSAL_ATTRIBUTION','MODEL_VALIDATION') and rigor in ('LIGHT','STANDARD'): rigor='DEEP'
    inst=run_request.get('instrument') or run_request.get('subject') or 'UNRESOLVED'
    family=reg.router.get('asset_family_map',{}).get(str(inst).upper(),'UNRESOLVED_OR_MULTI_ASSET')
    alternatives=[x['protocol_id'] for x in reg.protocols['protocols'] if x['research_class']!=rc][:2]
    return {'research_class':rc,'protocol':proto,'rigor_tier':rigor,'asset_family':family,'selection_basis':reasons,'alternative_protocols':alternatives}
