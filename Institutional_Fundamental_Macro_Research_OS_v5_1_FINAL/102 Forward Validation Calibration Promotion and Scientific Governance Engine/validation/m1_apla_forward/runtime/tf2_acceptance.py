from pathlib import Path
import os,tempfile,shutil,json,hashlib
from .tf2_review import build_snapshot,selftest,_seal,_sha,_canon

def _write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
def _commit(cid,version='TF1.0.1',sealed='2026-08-10T08:01:00Z',subject='XAUUSD',rc='DIRECTIONAL_FORECAST',h='DAILY',mfind=None,lenses=None):
    x={'schema_version':'1.0.0','true_forward_version':version,'commitment_id':cid,'run_id':cid[4:],'truth_state':'TRUE_FORWARD','state':'SEALED_PRE_OUTCOME','reviewability':'FULL_M1_APL_SNAPSHOT' if version=='TF1.0.1' else 'LIMITED_REVIEWABILITY','subject':subject,'research_class':rc,'horizon':h,'analysis_cutoff_utc':'2026-08-10T08:00:00Z','evidence_cutoff_utc':'2026-08-10T08:00:00Z','sealed_at_utc':sealed,'decision_seal_hash':'sha256:'+'1'*64,'method':{'version':'M1.0.1','protocol_id':'P','findings_snapshot':mfind or []},'apl_a':{'version':'APL-A 1.0.0','mode':'SHADOW_ONLY','active_lenses':lenses or [],'artifact_payloads':{}},'science':{},'uncertainty':None,'expected_outcome_contract':{'type':'DIRECTIONAL_OR_RELATIVE_OUTCOME','horizon':h,'price_only_evaluation_forbidden':True},'authority':{'direction_mutated':False,'permission_mutated':False,'broker_write':'NONE','apl_a':'SHADOW_ONLY','m1_new_direction_authority':'NONE'},'source_surface_hash':'sha256:'+'2'*64}
    x['payload_hash']=_sha({k:x[k] for k in x if k not in ('payload_hash','seal')});x['seal']=_seal(x);return x
def _out(c,linked='2026-08-10T09:02:00Z',obs='2026-08-10T09:00:00Z'):
    x={'schema_version':'1.0.0','true_forward_version':c['true_forward_version'],'outcome_link_id':'OUT_'+c['commitment_id'],'commitment_id':c['commitment_id'],'commitment_seal':c['seal'],'observed_at_utc':obs,'linked_at_utc':linked,'observation_state':'OBSERVABLE','outcome':{'direction':'UP'},'evaluation':{}};x['seal']=_seal(x);return x
def _review(c,classification,target_type,target):
    x={'schema_version':'1.0.0','true_forward_version':c['true_forward_version'],'review_id':'REV_'+c['commitment_id']+'_1','commitment_id':c['commitment_id'],'commitment_seal':c['seal'],'reviewed_at_utc':'2026-08-10T09:10:00Z','reviewer':'TEST','assessment':{'target_type':target_type,('capability' if target_type=='M1_CAPABILITY' else 'lens_id'):target},'evidence':{},'classification':classification};x['seal']=_seal(x);return x

def run(vault_root):
    v=Path(vault_root).resolve();checks=[]
    def ck(n,b,d=None):checks.append({'name':n,'pass':bool(b),'detail':d})
    ck('selftest',selftest(v)['status']=='PASS')
    td=Path(tempfile.mkdtemp(prefix='alphalab_tf2_acc_'));old=os.environ.get('ALPHALAB_DATA_ROOT');os.environ['ALPHALAB_DATA_ROOT']=str(td);root=td/'forward';
    for n in ('commitments','outcomes','reviews','locks'):(root/n).mkdir(parents=True,exist_ok=True)
    try:
        c=_commit('TF1_GOOD',mfind=[{'code':'M020_PSEUDO_INDEPENDENCE','severity':'RESEARCH_REQUIRED','hard':False}],lenses=['V02_EPISTEMIC_FRAGILITY_AUDITOR']);_write(root/'commitments'/'TF1_GOOD.json',c);_write(root/'outcomes'/'OUT_TF1_GOOD.json',_out(c));_write(root/'reviews'/'REV_TF1_GOOD_1.json',_review(c,'TRUE_POSITIVE','M1_CAPABILITY','SOURCE_DEPENDENCY'))
        s=build_snapshot(v,'2026-08-10T10:00:00Z',store=False)['review'];ck('valid_true_forward_included',s['coverage']['valid_true_forward_count']==1 and s['coverage']['mature_true_forward_count']==1);ck('version_aware',s['coverage']['tf_versions']==['TF1.0.1']);ck('m1_review_operational',next(x for x in s['m1_readiness']['records'] if x['subject']=='SOURCE_DEPENDENCY')['review_labels']==['TRUE_POSITIVE']);ck('apl_lens_review_operational',next(x for x in s['apl_a_readiness']['records'] if x['subject']=='V02_EPISTEMIC_FRAGILITY_AUDITOR')['invocation_count']==1);ck('interaction_operational',s['interaction']['records'][0]['relation'] in ('BOTH_SAME','BOTH_COMPLEMENTARY'))
        # legacy record is valid but explicitly limited reviewability
        c2=_commit('TF1_OLD','TF1.0.0',subject='EURUSD');c2.pop('reviewability',None);c2['method'].pop('findings_snapshot',None);c2['apl_a'].pop('artifact_payloads',None);c2['payload_hash']=_sha({k:c2[k] for k in c2 if k not in ('payload_hash','seal')});c2['seal']=_seal(c2);_write(root/'commitments'/'TF1_OLD.json',c2);_write(root/'outcomes'/'OUT_TF1_OLD.json',_out(c2,obs='2026-08-10T09:01:00Z',linked='2026-08-10T09:03:00Z'))
        s=build_snapshot(v,'2026-08-10T10:00:00Z',store=False)['review'];ck('legacy_preserved_limited',s['coverage']['valid_true_forward_count']==2 and s['coverage']['limited_reviewability_count']==1)
        # tampered record excluded
        bad=_commit('TF1_BAD');bad['subject']='TAMPER';_write(root/'commitments'/'TF1_BAD.json',bad);s=build_snapshot(v,'2026-08-10T10:00:00Z',store=False)['review'];ck('tamper_excluded',any(x['record_id']=='TF1_BAD' and x['classification']=='INVALID_SEAL' for x in s['record_forensics']['excluded_records']))
        # after-cutoff record excluded
        late=_commit('TF1_LATE',sealed='2026-08-10T11:00:00Z');late['analysis_cutoff_utc']='2026-08-10T10:59:00Z';late['evidence_cutoff_utc']=late['analysis_cutoff_utc'];late['payload_hash']=_sha({k:late[k] for k in late if k not in ('payload_hash','seal')});late['seal']=_seal(late);_write(root/'commitments'/'TF1_LATE.json',late);s=build_snapshot(v,'2026-08-10T10:00:00Z',store=False)['review'];ck('moving_cutoff_blocked',any(x['record_id']=='TF1_LATE' and x['classification']=='AFTER_REVIEW_CUTOFF' for x in s['record_forensics']['excluded_records']))
        # outcome linked after cutoff is not matured in that review
        p=_commit('TF1_PENDING',subject='NASDAQ100');_write(root/'commitments'/'TF1_PENDING.json',p);_write(root/'outcomes'/'OUT_TF1_PENDING.json',_out(p,obs='2026-08-10T09:00:00Z',linked='2026-08-10T10:30:00Z'));s=build_snapshot(v,'2026-08-10T10:00:00Z',store=False)['review'];ck('future_link_not_credited',any(x['record_id']=='TF1_PENDING' and x['classification']=='OUTCOME_PENDING' for x in s['record_forensics']['excluded_records']))
        ck('authority_isolated',s['authority']['broker_write']=='NONE' and s['authority']['apl_a']=='SHADOW_ONLY' and s['authority']['auto_promotion'] is False);ck('no_apl_b',s['apl_b']=='NOT_IMPLEMENTED');ck('maturity_not_score','score' not in json.dumps(s).lower());ck('continued_collection_next_gate',s['next_gate'] in ('CONTINUE_TF1_TRUE_FORWARD_ACCUMULATION','REPAIR_FORWARD_INTEGRITY'))
    finally:
        if old is None:os.environ.pop('ALPHALAB_DATA_ROOT',None)
        else:os.environ['ALPHALAB_DATA_ROOT']=old
        shutil.rmtree(td,ignore_errors=True)
    bad=[x for x in checks if not x['pass']];return {'status':'PASS' if not bad else 'FAIL','review_version':'TF2.0.0','passed':len(checks)-len(bad),'total':len(checks),'checks':checks,'errors':[x['name'] for x in bad]}
