#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json, hashlib, re, fnmatch

PHASE='AD-V3-P01'; VERSION='3.1.1-foundation'; DEPLOYMENT='SHADOW_ONLY'

class P01Error(ValueError): pass

def _phase_root(): return Path(__file__).resolve().parents[1]
def _vault_root(): return _phase_root().parent.parent
def _repo_root(): return _vault_root().parent

def _load(name): return json.loads((_phase_root()/'config'/name).read_text(encoding='utf-8'))
def _sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def validate_registry():
    reg=_load('gold_master_fact_registry.json'); const=_load('scientific_constitution.json'); causal=_load('causal_ontology.json'); role_cfg=_load('fact_role_registry.json'); horizon_cfg=_load('horizon_registry.json')
    facts=reg.get('facts') or []
    ids=[x.get('fact_id') for x in facts]
    errors=[]
    if len(ids)!=len(set(ids)): errors.append('DUPLICATE_FACT_ID')
    if len(facts)<100: errors.append('FACT_UNIVERSE_TOO_SMALL')
    planes={x['id'] for x in const['pressure_planes']}; roots={x['root_id'] for x in causal['canonical_root_families']}
    roles={x['role_id']:x for x in role_cfg.get('roles',[])}
    horizons={x['id'] if isinstance(x,dict) else x for x in horizon_cfg.get('horizons',[])}
    for f in facts:
        fid=f.get('fact_id')
        if not fid or not re.fullmatch(r'[A-Z0-9_]+',str(fid)): errors.append(f'INVALID_FACT_ID:{fid}')
        role=f.get('default_role')
        if role not in roles: errors.append(f'UNKNOWN_DEFAULT_ROLE:{fid}:{role}')
        if f.get('pressure_plane')!='NONE' and f.get('pressure_plane') not in planes: errors.append(f'INVALID_PLANE:{fid}')
        if role in roles and f.get('pressure_plane') not in roles[role]['allowed_pressure_planes']: errors.append(f'ROLE_PLANE_MISMATCH:{fid}:{role}:{f.get("pressure_plane")}')
        root=f.get('causal_root_family')
        if root and root not in roots: errors.append(f'UNKNOWN_ROOT:{fid}:{root}')
        if f.get('causal_root_eligible') and not root: errors.append(f'ROOT_ELIGIBLE_WITHOUT_ROOT:{fid}')
        for k in ('active_horizons','discovery_terms','source_hints','prohibited_interpretations'):
            vals=f.get(k)
            if vals is None: errors.append(f'MISSING_LIST:{fid}:{k}'); continue
            if len(vals)!=len(set(vals)): errors.append(f'DUPLICATE_LIST_VALUE:{fid}:{k}')
        ah=f.get('active_horizons') or []
        if not ah: errors.append(f'NO_HORIZON:{fid}')
        for h in ah:
            if h not in horizons: errors.append(f'UNKNOWN_HORIZON:{fid}:{h}')
        if not f.get('discovery_terms'): errors.append(f'NO_DISCOVERY_TERMS:{fid}')
        if 'notes' not in f: errors.append(f'NO_NOTES_FIELD:{fid}')
        if not f.get('default_materiality'): errors.append(f'NO_MATERIALITY:{fid}')
    by={f['fact_id']:f for f in facts}
    for fid in ['XAUUSD_SPOT_PRICE','GC_FUTURES_PRICE']:
        if by[fid]['causal_root_eligible']: errors.append(f'PRICE_ROOT_CONTAMINATION:{fid}')
    if 'VOLUME_NOT_FLOW' not in by['GC_VOLUME']['prohibited_interpretations']: errors.append('VOLUME_FLOW_BOUNDARY_MISSING')
    if 'OI_NOT_DIRECTION' not in by['GC_OPEN_INTEREST']['prohibited_interpretations']: errors.append('OI_DIRECTION_BOUNDARY_MISSING')
    if 'NOT_LIVE_FLOW' not in by['CFTC_MANAGED_MONEY']['prohibited_interpretations']: errors.append('COT_LIVE_BOUNDARY_MISSING')
    if 'CLEARING_NOT_DIRECTIONAL_FLOW' not in by['LBMA_CLEARING_ACTIVITY']['prohibited_interpretations']: errors.append('LBMA_CLEARING_BOUNDARY_MISSING')
    required=['UST_TERM_PREMIUM','FED_BROAD_DOLLAR','FED_AFE_DOLLAR','FED_EME_DOLLAR','USDCNH_CNH_STATE','GOLD_MINE_PRODUCTION','GOLD_RECYCLING_SUPPLY','GOLD_PRODUCER_HEDGING','CHINA_PHYSICAL_BALANCE','INDIA_PHYSICAL_BALANCE','LONDON_OTC_CLIENT_DEALER_FLOW','GOLD_LEASE_RATE','COMEX_LONDON_EFP','CFTC_PRODUCER_MERCHANT','CFTC_SWAP_DEALER','CFTC_MANAGED_MONEY','CFTC_OTHER_REPORTABLES','GC_OPTIONS_SKEW_RISK_REVERSAL','MODEL_COMPLETENESS_STATE','MISSING_DRIVER_RISK']
    for fid in required:
        if fid not in by: errors.append('REQUIRED_V3_FACT_MISSING:'+fid)
    if const.get('live_network_fetch')!='FORBIDDEN_IN_P01': errors.append('P01_NETWORK_BOUNDARY_BROKEN')
    if const.get('trade_permission_authority')!='NONE': errors.append('P01_PERMISSION_AUTHORITY_BROKEN')
    if const.get('precision_policy',{}).get('uncalibrated_user_scores')!='FORBIDDEN': errors.append('FAKE_PRECISION_POLICY_BROKEN')
    if len(const.get('pressure_planes') or [])!=4: errors.append('PRESSURE_PLANE_COUNT_NOT_FOUR')
    return {'status':'PASS' if not errors else 'FAIL_CLOSED','fact_count':len(facts),'errors':errors}

def verify_v2_freeze():
    m=json.loads((_phase_root()/'baseline/v2_frozen_surface_manifest.json').read_text(encoding='utf-8'))
    rows=[]; ok=True
    for s in m.get('surfaces',[]):
        p=_repo_root()/s['rel']; exists=p.exists(); actual=_sha(p) if exists and p.is_file() else None; same=exists and actual==s['sha256']; ok=ok and same
        rows.append({'rel':s['rel'],'exists':exists,'expected_sha256':s['sha256'],'actual_sha256':actual,'unchanged':same})
    return {'status':'PASS' if ok else 'FAIL_CLOSED','surface_count':len(rows),'surfaces':rows}

def _matches_discovery_filename(filename:str, pattern:str)->bool:
    # Current discovery contracts are filename patterns under **/.  Matching the
    # basename explicitly makes behavior identical on Windows and POSIX.
    pat=pattern.replace('\\','/').split('/')[-1]
    return fnmatch.fnmatchcase(filename.lower(), pat.lower())

def discover_surfaces():
    cfg=_load('gold_knowledge_surface_registry.json'); vault=_vault_root(); found={}
    for x in cfg.get('explicit_authority_surfaces',[]):
        rel=x['rel']; p=vault/rel; found[rel]={'rel':rel,'path':p,'explicit':True,'required':bool(x.get('required',True)),'kind':x.get('kind')}
    excludes=[str(x).lower() for x in cfg.get('discovery_exclude_contains',[])]
    patterns=cfg.get('discovery_globs',[])
    # Platform-invariant case-insensitive scan. Do not delegate case semantics to Path.glob().
    for p in vault.rglob('*'):
        if not p.is_file(): continue
        rel=p.relative_to(vault).as_posix(); key='/'+rel.lower()+'/'
        if any(e.lower() in key for e in excludes): continue
        if not any(_matches_discovery_filename(p.name,pat) for pat in patterns): continue
        found.setdefault(rel,{'rel':rel,'path':p,'explicit':False,'required':False,'kind':'DISCOVERED_GOLD_SURFACE'})
    return cfg, list(found.values())

def _safe_text(p):
    try: return p.read_text(encoding='utf-8',errors='ignore')
    except Exception: return ''

def _interface_registry():
    return _load('gold_interface_contract_registry.json')

def _validate_interface_surface(surface):
    reg=_interface_registry(); by={x['rel']:x for x in reg.get('contracts',[])}
    rel=surface['rel']; p=surface['path']; c=by.get(rel)
    errors=[]
    if c is None:
        return {'status':'FAIL_CLOSED','errors':['INTERFACE_CONTRACT_NOT_REGISTERED:'+rel]}
    if not p.exists():
        return {'status':'FAIL_CLOSED','errors':['INTERFACE_CONTRACT_MISSING:'+rel]}
    actual_sha=_sha(p)
    if actual_sha!=c.get('sha256'):
        errors.append(f'INTERFACE_CONTRACT_HASH_DRIFT:{rel}:{actual_sha}')
    try:
        obj=json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:
        errors.append(f'INTERFACE_CONTRACT_JSON_INVALID:{rel}:{e}')
        obj={}
    actual_required=list(obj.get('required') or [])
    actual_props=list((obj.get('properties') or {}).keys())
    expected_required=list(c.get('required_top_level_fields') or [])
    expected_props=list(c.get('declared_property_names') or [])
    if set(actual_required)!=set(expected_required):
        errors.append(f'INTERFACE_REQUIRED_FIELD_DRIFT:{rel}:expected={sorted(expected_required)}:actual={sorted(actual_required)}')
    if set(actual_props)!=set(expected_props):
        errors.append(f'INTERFACE_PROPERTY_FIELD_DRIFT:{rel}:expected={sorted(expected_props)}:actual={sorted(actual_props)}')
    actual_addl=obj.get('additionalProperties',True)
    if actual_addl!=c.get('additional_properties_expected'):
        errors.append(f'INTERFACE_ADDITIONAL_PROPERTIES_DRIFT:{rel}:expected={c.get("additional_properties_expected")}:actual={actual_addl}')
    bindings=c.get('field_bindings') or {}
    union=set(actual_required)|set(actual_props)
    if set(bindings.keys())!=union:
        errors.append(f'INTERFACE_BINDING_COVERAGE_DRIFT:{rel}:unbound={sorted(union-set(bindings))}:extra={sorted(set(bindings)-union)}')
    return {
      'status':'PASS' if not errors else 'FAIL_CLOSED',
      'errors':errors,
      'semantic_role':c.get('semantic_role'),
      'market_fact_authority':c.get('market_fact_authority'),
      'audit_conclusion':c.get('audit_conclusion'),
      'expected_sha256':c.get('sha256'),
      'actual_sha256':actual_sha,
      'required_top_level_fields':actual_required,
      'declared_property_names':actual_props
    }

def validate_interface_registry():
    reg=_interface_registry(); errors=[]
    contracts=reg.get('contracts') or []
    rels=[x.get('rel') for x in contracts]
    if len(rels)!=len(set(rels)): errors.append('DUPLICATE_INTERFACE_CONTRACT_REL')
    if len(contracts)!=5: errors.append(f'EXPECTED_FIVE_AUDITED_INTERFACE_CONTRACTS:{len(contracts)}')
    for c in contracts:
        if c.get('classification')!='INTERFACE_CONTRACT_ONLY': errors.append('INVALID_INTERFACE_CLASS:'+str(c.get('rel')))
        if c.get('market_fact_authority')!='NONE': errors.append('INTERFACE_HAS_MARKET_FACT_AUTHORITY:'+str(c.get('rel')))
        if c.get('audit_conclusion')!='NO_NEW_GOLD_MARKET_FACT_DEFINITION': errors.append('INTERFACE_AUDIT_CONCLUSION_MISSING:'+str(c.get('rel')))
        if not re.fullmatch(r'[0-9a-f]{64}',str(c.get('sha256',''))): errors.append('INVALID_INTERFACE_SHA:'+str(c.get('rel')))
    return {'status':'PASS' if not errors else 'FAIL_CLOSED','contract_count':len(contracts),'errors':errors}

def compile_knowledge_coverage():
    vr=validate_registry(); freeze=verify_v2_freeze(); ir=validate_interface_registry(); cfg,surfaces=discover_surfaces(); reg=_load('gold_master_fact_registry.json'); facts=reg['facts']
    terms=[]
    for f in facts:
        for t in f.get('discovery_terms',[]):
            t=str(t).strip().lower()
            if len(t)>=3: terms.append((t,f['fact_id']))
    rows=[]; missing=[]; matched_fact_ids=set(); interface_errors=[]
    for s in surfaces:
        p=s['path']; exists=p.exists()
        if s.get('required') and not exists: missing.append(s['rel'])
        text=_safe_text(p).lower() if exists else ''
        fids=[]
        if text:
            for t,fid in terms:
                if t in text: fids.append(fid)
        fids=sorted(set(fids)); matched_fact_ids.update(fids)
        interface_audit=None
        if s.get('kind')=='GOVERNANCE_ONLY':
            classification='GOVERNANCE_OR_VALIDATION_SURFACE'
        elif s.get('kind')=='INTERFACE_CONTRACT_ONLY':
            interface_audit=_validate_interface_surface(s)
            if interface_audit['status']=='PASS':
                classification='INTERFACE_CONTRACT_SURFACE'
            else:
                classification='INTERFACE_CONTRACT_DRIFT'
                interface_errors.extend(interface_audit['errors'])
        elif fids:
            classification='FACT_SURFACE'
        else:
            classification='UNACCOUNTED_DISCOVERED_GOLD_SURFACE'
        rows.append({'rel':s['rel'],'explicit':s['explicit'],'required':s['required'],'kind':s.get('kind'),'exists':exists,'classification':classification,'matched_fact_ids':fids,'matched_fact_count':len(fids),'sha256':_sha(p) if exists else None,'interface_audit':interface_audit})
    reg_ids={f['fact_id'] for f in facts}
    unclassified=[r['rel'] for r in rows if r.get('classification')=='UNACCOUNTED_DISCOVERED_GOLD_SURFACE']
    drifted=[r['rel'] for r in rows if r.get('classification')=='INTERFACE_CONTRACT_DRIFT']
    status='PASS' if vr['status']=='PASS' and freeze['status']=='PASS' and ir['status']=='PASS' and not missing and not unclassified and not drifted and not interface_errors else 'FAIL_CLOSED'
    return {
      'schema_version':'1.1.0','phase':PHASE,'version':VERSION,'deployment':DEPLOYMENT,'status':status,
      'registry':{**vr,'registered_fact_ids':len(reg_ids),'fact_families':len({f['family'] for f in facts}),'causal_root_eligible_facts':sum(1 for f in facts if f['causal_root_eligible']),'private_or_paid_gap_facts':sum(1 for f in facts if 'PRIVATE' in f['observability_class'] or 'PAID' in f['observability_class'])},
      'discovery':{'case_policy':'CASE_INSENSITIVE_PLATFORM_INVARIANT','engine':'RGlobAllFiles + casefolded basename pattern match','patterns':cfg.get('discovery_globs',[])},
      'interface_contract_registry':ir,
      'surface_coverage':{'discovered_surface_count':len(rows),'required_missing':missing,'unaccounted_surfaces':unclassified,'unclassified_surfaces':unclassified,'interface_contract_drift_surfaces':drifted,'interface_contract_errors':interface_errors,'fact_surfaces':sum(1 for r in rows if r['classification']=='FACT_SURFACE'),'governance_or_validation_surfaces':sum(1 for r in rows if r['classification']=='GOVERNANCE_OR_VALIDATION_SURFACE'),'interface_contract_surfaces':sum(1 for r in rows if r['classification']=='INTERFACE_CONTRACT_SURFACE'),'matched_registry_fact_count':len(matched_fact_ids),'registry_entries_without_surface_term_match':len(reg_ids-matched_fact_ids),'term_match_is_diagnostic_only':True,'rows':rows},
      'v2_freeze':freeze,
      'integrity':{'live_network_fetch_performed':False,'v2_mutated':False,'direction_authority_granted':False,'permission_authority_granted':False,'target_price_causal_root':False,'platform_invariant_discovery':True,'interface_contracts_semantically_audited':ir['status']=='PASS' and not interface_errors and not drifted,'zero_unaccounted_gold_knowledge':status=='PASS'},
      'p02_handoff':{'ready':status=='PASS','next_phase':'AD-V3-P02_TOTAL_LIVE_DATA_OBSERVABILITY_FABRIC','required_inputs':['gold_master_fact_registry.json','epistemic_state_registry.json','causal_ontology.json'],'network_acquisition_still_forbidden_in_p01':True}
    }

def write_receipt(path=None):
    r=compile_knowledge_coverage(); p=Path(path) if path else (_phase_root()/'artifacts/P01_KNOWLEDGE_COVERAGE_RECEIPT.json'); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); return r,p
