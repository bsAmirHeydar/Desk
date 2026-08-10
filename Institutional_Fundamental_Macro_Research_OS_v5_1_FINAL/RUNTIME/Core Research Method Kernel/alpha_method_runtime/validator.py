from .util import now, parse_utc
from .registry import MethodRegistry
from .evidence import dependency_graph,time_after_cutoff

SEV_RANK={'PASS':0,'INFO':0,'WARNING':1,'RESEARCH_REQUIRED':2,'METHOD_INVALID':3,'OUTPUT_QUARANTINED':4}

def finding(code,severity,message,hard=False,evidence_ids=None,claim_ids=None):
    return {'code':code,'severity':severity,'hard':bool(hard),'message':message,'evidence_ids':list(evidence_ids or []),'claim_ids':list(claim_ids or [])}

def _status(findings):
    if not findings: return 'PASS'
    # hard quarantine outranks hard invalid; soft findings never become METHOD_INVALID by aggregation alone
    if any(x['severity']=='OUTPUT_QUARANTINED' for x in findings): return 'OUTPUT_QUARANTINED'
    if any(x['severity']=='METHOD_INVALID' for x in findings): return 'METHOD_INVALID'
    if any(x['severity']=='RESEARCH_REQUIRED' for x in findings): return 'RESEARCH_REQUIRED'
    if any(x['severity']=='WARNING' for x in findings): return 'WARNING'
    return 'PASS'

def assess(vault_root, run_id, plan, bundle, phase='AD_HOC'):
    reg=MethodRegistry(vault_root); findings=[]; req=bundle.get('run_request') or {}; cutoff=req.get('analysis_cutoff_utc') or req.get('analysis_cutoff') or plan.get('analysis_cutoff_utc')
    if not cutoff or parse_utc(cutoff) is None:
        findings.append(finding('M001_MISSING_OR_INVALID_CUTOFF','OUTPUT_QUARANTINED','Research requires a valid timezone-aware decision cutoff.',True))
    if req and req.get('lookahead_policy') not in (None,'STRICT_POINT_IN_TIME'):
        findings.append(finding('M002_LOOKAHEAD_POLICY','OUTPUT_QUARANTINED','Lookahead policy is not STRICT_POINT_IN_TIME.',True))
    evidence=list(bundle.get('evidence') or []); by_id={e.get('evidence_id'):e for e in evidence}
    for e in evidence:
        eid=e.get('evidence_id')
        bad=time_after_cutoff(e,cutoff) if cutoff else ['INVALID_CUTOFF']
        if bad and bad!=['INVALID_CUTOFF']:
            findings.append(finding('M010_FUTURE_INFORMATION','OUTPUT_QUARANTINED','Evidence contains post-cutoff availability/publication/ingestion time: '+','.join(bad),True,[eid]))
        if e.get('materiality') in ('DECISION_CRITICAL','MATERIAL') and e.get('availability_state')=='AVAILABLE' and not (e.get('source_id') or e.get('root_source_id')):
            sev='METHOD_INVALID' if e.get('materiality')=='DECISION_CRITICAL' else 'RESEARCH_REQUIRED'
            findings.append(finding('M011_PROVENANCE_GAP',sev,'Decision-material available evidence lacks reconstructable source/root provenance.',sev=='METHOD_INVALID',[eid]))
        if e.get('availability_state') in ('UNAVAILABLE','UNDETERMINED','UNKNOWN','NOT_AVAILABLE','NOT_MEASURED') and e.get('value') in (0,0.0,'0'):
            findings.append(finding('M012_UNKNOWN_TO_ZERO','OUTPUT_QUARANTINED','Unavailable/unknown evidence collapsed to zero.',True,[eid]))
        if e.get('evidence_class')=='PROXY' and not e.get('proxy_contract_id'):
            findings.append(finding('M013_PROXY_CONTRACT_GAP','WARNING','Proxy evidence lacks an explicit method proxy contract; legacy evidence remains admissible but cannot be reified as the latent target.',False,[eid]))
        if e.get('evidence_class')=='MODEL_OUTPUT' and not e.get('model_version'):
            findings.append(finding('M014_MODEL_VERSION_GAP','WARNING','Model-derived evidence lacks explicit model/derivation version metadata.',False,[eid]))
    dg=dependency_graph(run_id,evidence)
    if dg['pseudo_independence_found']:
        findings.append(finding('M020_PSEUDO_INDEPENDENCE','RESEARCH_REQUIRED','Multiple evidence items share an underlying root; independence must not be counted nominally.',False,[i for g in dg['groups'] if len(g['evidence_ids'])>1 for i in g['evidence_ids']]))
    claims=list(bundle.get('claims') or [])
    for c in claims:
        cid=c.get('claim_id','?'); ctype=c.get('claim_type')
        if ctype in ('CAUSAL_HYPOTHESIS','MECHANISM_CLAIM'):
            if not c.get('mechanism'):
                findings.append(finding('M030_CAUSAL_NO_MECHANISM','METHOD_INVALID','Causal claim lacks an explicit mechanism.',True,claim_ids=[cid]))
            if c.get('identification_state')=='NOT_IDENTIFIED' and c.get('assertion_strength','').upper() in ('CAUSAL_ESTABLISHED','PROVEN','CONFIRMED_CAUSAL'):
                findings.append(finding('M031_CAUSAL_NOT_IDENTIFIED','METHOD_INVALID','Claim asserts causal certainty while causal effect is NOT_IDENTIFIED.',True,claim_ids=[cid]))
        p=c.get('probability')
        if p is not None:
            pt=c.get('probability_type')
            if not pt:
                findings.append(finding('M040_FAKE_PRECISION','METHOD_INVALID','Numeric probability lacks an epistemic probability type.',True,claim_ids=[cid]))
            elif pt=='CALIBRATED_PROBABILITY' and not c.get('calibration_id'):
                findings.append(finding('M041_UNCALIBRATED_CALIBRATED_CLAIM','METHOD_INVALID','Calibrated probability claim lacks calibration identifier.',True,claim_ids=[cid]))
        if c.get('regime_label_available_at_cutoff') is False:
            findings.append(finding('M050_RETROSPECTIVE_REGIME_LEAKAGE','OUTPUT_QUARANTINED','Contemporaneous research uses a regime label unavailable at the cutoff.',True,claim_ids=[cid]))
        if c.get('circular_validation') is True:
            findings.append(finding('M051_CIRCULAR_VALIDATION','RESEARCH_REQUIRED','Claim is validated by an outcome/price reaction that is not independent evidence of the claim.',False,claim_ids=[cid]))
        if c.get('research_mode')=='CONFIRMATORY' and (c.get('discovered_post_search') is True or int(c.get('search_space_size') or 1)>1 and c.get('specification_pre_registered') is False):
            findings.append(finding('M060_EXPLORATORY_MISLABELED','RESEARCH_REQUIRED','Search-discovered specification is labeled confirmatory.',False,claim_ids=[cid]))
        evid=c.get('evidence_ids') or []
        if c.get('directness')=='DIRECT' and any(by_id.get(x,{}).get('evidence_class') in ('PROXY','MODEL_OUTPUT','NARRATIVE') for x in evid):
            findings.append(finding('M061_INDIRECT_AS_DIRECT','RESEARCH_REQUIRED','Claim presents proxy/model/narrative evidence as direct observation.',False,evid,[cid]))
        contradict=[e['evidence_id'] for e in evidence if e.get('relation')=='CONTRADICTING' and (not e.get('claim_id') or e.get('claim_id')==cid)]
        disclosed=set(c.get('contradictory_evidence_ids') or [])
        omitted=[x for x in contradict if x not in disclosed]
        if omitted:
            findings.append(finding('M062_CONTRADICTION_SUPPRESSED','METHOD_INVALID','Material contradictory evidence is omitted from the claim record.',True,omitted,[cid]))
    integ=bundle.get('evidence_integrity_receipt') or {}
    if integ.get('same_root_double_count_found') is True and not any(x['code']=='M020_PSEUDO_INDEPENDENCE' for x in findings):
        findings.append(finding('M020_PSEUDO_INDEPENDENCE','RESEARCH_REQUIRED','Existing evidence integrity receipt reports same-root double counting.',False))
    # Existing V21 hypothesis discipline: missing alternatives becomes a research warning, not a hard rewrite.
    hs=bundle.get('hypothesis_set') or {}
    if hs:
        hy=hs.get('hypotheses') or []
        if len(hy)==1 and not hs.get('single_hypothesis_justification'):
            findings.append(finding('M070_SINGLE_HYPOTHESIS_WITHOUT_JUSTIFICATION','RESEARCH_REQUIRED','One-hypothesis state lacks explicit justification.',False))
        for h in hy:
            if not h.get('invalidation_triggers'):
                findings.append(finding('M071_NO_INVALIDATION_TRIGGER','RESEARCH_REQUIRED','Material hypothesis lacks an operational invalidation trigger.',False,claim_ids=[h.get('hypothesis_id','?')]))
    status=_status(findings); hard=sum(1 for x in findings if x['hard'])
    return {'schema_version':'1.0.0','method_version':'M1.0.0','run_id':run_id,'phase':phase,'status':status,'research_class':plan.get('research_class','UNRESOLVED'),'protocol_id':plan.get('protocol_id','UNRESOLVED'),'findings':findings,'hard_failure_count':hard,'source_dependency_graph':dg,'uncertainty_summary':list(bundle.get('uncertainty_summary') or []),'decision_authority':'NONE','decision_world_mutated':False,'created_at_utc':now()}
