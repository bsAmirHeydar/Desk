from pathlib import Path
import math,statistics,random,json
from .util import load_json,now,uid,sha256_obj,validate_scientific_schema
class CalibrationError(RuntimeError):pass
def _mean(xs):return sum(xs)/len(xs) if xs else None
def _median(xs):return statistics.median(xs) if xs else None
def _pf(xs):
    pos=sum(x for x in xs if x>0);neg=-sum(x for x in xs if x<0);return None if neg==0 else pos/neg
def _tail(xs,p=.05):
    if not xs:return None
    return _mean(sorted(xs)[:max(1,math.ceil(len(xs)*p))])
def _stats(xs):return {'n':len(xs),'mean_r':_mean(xs),'median_r':_median(xs),'profit_factor':_pf(xs),'positive_r_rate':(sum(1 for x in xs if x>0)/len(xs) if xs else None),'lower_tail_mean_r_5pct':_tail(xs)}
class Calibrator:
    def __init__(self,vault,rt):self.vault=Path(vault);self.rt=rt;self.cfg=load_json(self.vault/'RUNTIME'/'R3 Operational Execution and Learning OS'/'config'/'calibration_runtime_policy.json');self.sp=load_json(self.vault/'102 Forward Validation Calibration Promotion and Scientific Governance Engine'/'config'/'calibration_policy.json');self.pp=load_json(self.vault/'102 Forward Validation Calibration Promotion and Scientific Governance Engine'/'config'/'promotion_policy.json')
    def _rows(self,run_ids):
        if not run_ids:return []
        q='SELECT * FROM r3_analytics_rows WHERE run_id IN ('+','.join('?'*len(run_ids))+')'
        with self.rt.catalog.connect() as c:c.row_factory=__import__('sqlite3').Row;return [dict(x) for x in c.execute(q,run_ids).fetchall()]
    def _clusters(self,rows):
        usable=[r for r in rows if r.get('realized_r') is not None]
        roots=[]
        for r in usable:
            try:roots.append(set(json.loads(r.get('independent_root_ids_json') or '[]')))
            except Exception:roots.append(set())
        if any(roots):
            parent=list(range(len(usable)))
            def find(x):
                while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
                return x
            def union(a,b):
                a,b=find(a),find(b)
                if a!=b:parent[b]=a
            owner={}
            for i,rs in enumerate(roots):
                for root in rs:
                    if root in owner:union(i,owner[root])
                    else:owner[root]=i
            groups={}
            for i,r in enumerate(usable):groups.setdefault(find(i),[]).append(r)
            return 'independent_root_connected_component',list(groups.values())
        if any(r.get('analysis_date') for r in usable):
            groups={}
            for r in usable:groups.setdefault(r.get('analysis_date') or r['run_id'],[]).append(r)
            return 'trading_day',list(groups.values())
        return 'observation',[[r] for r in usable]
    def _bootstrap(self,rows,iterations):
        key,clusters=self._clusters(rows)
        if not clusters:return {'state':'INSUFFICIENT_EVIDENCE','iterations':0,'cluster_key':key,'cluster_count':0}
        vals=[_mean([r['realized_r'] for r in g if r.get('realized_r') is not None]) for g in clusters];vals=[x for x in vals if x is not None];seed=int(sha256_obj(sorted((r['run_id'],r.get('realized_r')) for r in rows)).split(':')[1][:16],16);rng=random.Random(seed);means=[]
        for _ in range(iterations):means.append(_mean([rng.choice(vals) for _ in vals]))
        means.sort();lo=means[int(.025*(len(means)-1))];hi=means[int(.975*(len(means)-1))]
        return {'state':'CLUSTER_AWARE' if key!='observation' else 'OBSERVATION_LEVEL_FALLBACK','iterations':iterations,'seed_basis':'SHA256_DATASET','cluster_key':key,'cluster_count':len(vals),'cluster_equal_weighting':True,'mean_ci95':[lo,hi]}
    def run(self,request):
        dev=self._rows(request['development_run_ids']);hold=self._rows(request['holdout_run_ids']);devr=[r['realized_r'] for r in dev if r.get('realized_r') is not None];holdr=[r['realized_r'] for r in hold if r.get('realized_r') is not None];db=self._bootstrap(dev,int(self.cfg['bootstrap_iterations']));hb=self._bootstrap(hold,int(self.cfg['bootstrap_iterations']));reasons=[];elig='NOT_ELIGIBLE'
        if not holdr:elig='INSUFFICIENT_EVIDENCE';reasons.append('NO_MATURE_HOLDOUT')
        else:
            ac=request.get('authority_class');floor_key='risk_reducing_or_constraint' if ac not in ('RESTORE_EXISTING_DIRECTION_PERMISSION','CREATE_PERMISSION_WITH_EXISTING_FUNDAMENTAL_DIRECTION') else ('positive_permission_restore' if ac=='RESTORE_EXISTING_DIRECTION_PERMISSION' else 'positive_permission_create');floor=self.pp['governance_floors'][floor_key];nroots=hb.get('cluster_count',0)
            if len(devr)+len(holdr)<floor['min_observations']:reasons.append('OBSERVATION_FLOOR_NOT_MET')
            if db.get('cluster_count',0)+hb.get('cluster_count',0)<floor['min_independent_roots']:reasons.append('INDEPENDENT_ROOT_FLOOR_NOT_MET')
            if nroots<floor['min_holdout_roots']:reasons.append('HOLDOUT_ROOT_FLOOR_NOT_MET')
            regimes={r.get('regime_state') for r in dev+hold if r.get('regime_state')}
            if len(regimes)<floor['min_distinct_regimes']:reasons.append('REGIME_FLOOR_NOT_MET')
            if _mean(holdr) is None or _mean(holdr)<=0:reasons.append('HOLDOUT_MEAN_NOT_POSITIVE')
            if not reasons:elig='ELIGIBLE_FOR_REVIEW';reasons=['INDEPENDENT_VALIDATOR_STILL_REQUIRED']
        rep={'record_type':'CALIBRATION_REPORT','calibration_id':uid('CAL'),'modifier_id':request['modifier_id'],'policy_version':'1.2.0','calibration_version':'R3_CALIBRATION_RUNTIME_1.1.0','created_at_utc':now(),'development':{**_stats(devr),'bootstrap':db},'holdout':{**_stats(holdr),'bootstrap':hb},'promotion_eligibility':elig,'dependence':{'preferred_cluster_key':'independent_root_id','fallback':'trading_day_then_labeled_observation','implemented_state':'CONNECTED_ROOT_CLUSTER_THEN_DAY_THEN_OBSERVATION'},'tail_risk':{'development_lower_tail_mean_r_5pct':_tail(devr),'holdout_lower_tail_mean_r_5pct':_tail(holdr)},'regime_stability':{'distinct_regimes':sorted({r.get('regime_state') for r in dev+hold if r.get('regime_state')}),'state':'DESCRIPTIVE_GOVERNANCE_CHECK'},'multiple_testing':{'state':'DISCLOSURE_REQUIRED_BEFORE_PROMOTION'},'chronological_split_attested':bool(request.get('holdout_run_ids')),'execution_profiles':sorted(set((r.get('execution_profile') or 'UNKNOWN') for r in dev+hold)),'hypothesis_family_ids':request.get('hypothesis_family_ids') or [],'reference_class_ids':request.get('reference_class_ids') or [],'promotion_eligibility_reason_codes':reasons,'note':'Eligibility is review-only. No registry write, numeric predictive probability, or automatic authority creation is authorized.'};validate_scientific_schema(self.vault,'102 Forward Validation Calibration Promotion and Scientific Governance Engine/schemas/AlphaLab_D4_Calibration_Report.schema.json',rep);return rep
