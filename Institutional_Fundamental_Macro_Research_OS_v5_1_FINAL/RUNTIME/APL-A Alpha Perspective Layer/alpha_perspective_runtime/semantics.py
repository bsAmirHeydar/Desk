class SemanticError(RuntimeError):pass
def require_scope(x):
 for k in ('system_boundary','stressor','horizon','welfare_metric'):
  if not x.get(k):raise SemanticError('scope missing '+k)
 return True
def direct_fact_satisfied(evidence):return any(x.get('epistemic_class') in ('OBSERVED_FACT','OFFICIAL_REPORTED_FACT','CONTRACTUAL_FACT','IDENTIFIED_FLOW_FACT','IDENTIFIED_POSITIONING_FACT') and x.get('direct',True) for x in evidence)
def independent_roots(items):return len({x.get('root_id') for x in items if x.get('root_id')})
def optionality_state(cost,expiry,exercise):
 if not exercise:return 'ILLUSORY_OPTIONALITY'
 if expiry in ('EXPIRED','IMMINENT_WITHOUT_EXERCISE') or cost=='PROHIBITIVE':return 'IMPAIRED_OPTIONALITY'
 return 'EXERCISABLE_OPTIONALITY'
def fragility_state(scope,geometry):
 require_scope(scope)
 return geometry if geometry in ('LOCALLY_CONVEX','LOCALLY_CONCAVE','APPROX_LINEAR','MIXED_CURVATURE','CURVATURE_REVERSAL_RISK','THRESHOLD_DOMINATED','DISCONTINUOUS','UNKNOWN_GEOMETRY') else 'UNKNOWN_GEOMETRY'
def invariant_survives(results,statement):return all(statement in (r.get('surviving') or []) for r in results) if results else False
