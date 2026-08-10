from pathlib import Path
import argparse,json
from .selftest import run as selftest
from .environment import doctor,certify as env_certify
from .shadow import certify as shadow_certify
from .readiness import evaluate as readiness
from .launcher import main as launch
from .hostcert import certify as host_certify
from .true_forward import initialize as forward_init,list_records,verify_commitment,link_outcome,add_review,selftest as tf_selftest
from .tf_acceptance import run as tf_acceptance
from .continuous_forward import status as tf3_status,cycle as tf3_cycle,mature_pending as tf3_mature,periodic_review as tf3_review,scheduler as tf3_scheduler,backup as tf3_backup,selftest as tf3_selftest,preflight as tf3_preflight
from .tf3_acceptance import run as tf3_acceptance

def _obj(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def main(argv=None):
    ap=argparse.ArgumentParser(prog='alpha-commission');ap.add_argument('--vault-root',required=True);sp=ap.add_subparsers(dest='cmd',required=True)
    sp.add_parser('selftest');sp.add_parser('doctor');sp.add_parser('environment');sp.add_parser('host-certify');sp.add_parser('forward-init');sp.add_parser('forward-status');sp.add_parser('true-forward-selftest');sp.add_parser('true-forward-acceptance');sp.add_parser('tf3-status');sp.add_parser('tf3-selftest');sp.add_parser('tf3-preflight');sp.add_parser('tf3-acceptance');sp.add_parser('tf3-backup')
    p=sp.add_parser('shadow');p.add_argument('--runs-per-instrument',type=int,default=None)
    p=sp.add_parser('readiness');p.add_argument('--signoff',action='store_true')
    p=sp.add_parser('launch');p.add_argument('launch_args',nargs=argparse.REMAINDER)
    p=sp.add_parser('forward-run');p.add_argument('subject')
    p=sp.add_parser('forward-verify');p.add_argument('--commitment-id',required=True)
    p=sp.add_parser('forward-link');p.add_argument('--commitment-id',required=True);p.add_argument('--outcome-json',required=True)
    p=sp.add_parser('forward-review');p.add_argument('--commitment-id',required=True);p.add_argument('--review-json',required=True)
    p=sp.add_parser('tf3-cycle');p.add_argument('--run-shadow',action='store_true');p.add_argument('--auto-link',action='store_true');p.add_argument('--review-if-due',action='store_true');p.add_argument('--force-review',action='store_true')
    p=sp.add_parser('tf3-mature');p.add_argument('--at-utc',default=None);p.add_argument('--auto-link',action='store_true')
    p=sp.add_parser('tf3-review');p.add_argument('--cutoff-utc',default=None);p.add_argument('--force',action='store_true')
    p=sp.add_parser('tf3-scheduler');p.add_argument('action',choices=['install','status','enable','disable','run-now','remove'])
    a=ap.parse_args(argv);v=Path(a.vault_root).resolve()
    if a.cmd=='selftest':out=selftest(v)
    elif a.cmd=='doctor':out=doctor(v)
    elif a.cmd=='environment':out=env_certify(v)
    elif a.cmd=='host-certify':out=host_certify(v)
    elif a.cmd=='shadow':out=shadow_certify(v,a.runs_per_instrument)
    elif a.cmd=='readiness':out=readiness(v,a.signoff)
    elif a.cmd=='launch':out=launch(v,a.launch_args)
    elif a.cmd=='forward-init':out=forward_init(v)
    elif a.cmd=='forward-status':out=list_records(v)
    elif a.cmd=='true-forward-selftest':out=tf_selftest(v)
    elif a.cmd=='true-forward-acceptance':out=tf_acceptance(v)
    elif a.cmd=='forward-run':out=launch(v,[a.subject,'SHADOW'],seal_truth_state='TRUE_FORWARD')
    elif a.cmd=='forward-verify':out=verify_commitment(v,a.commitment_id)
    elif a.cmd=='forward-link':out=link_outcome(v,a.commitment_id,_obj(a.outcome_json))
    elif a.cmd=='forward-review':out=add_review(v,a.commitment_id,_obj(a.review_json))
    elif a.cmd=='tf3-status':out=tf3_status(v)
    elif a.cmd=='tf3-selftest':out=tf3_selftest(v)
    elif a.cmd=='tf3-preflight':out=tf3_preflight(v)
    elif a.cmd=='tf3-acceptance':out=tf3_acceptance(v)
    elif a.cmd=='tf3-backup':out=tf3_backup(v)
    elif a.cmd=='tf3-cycle':out=tf3_cycle(v,a.run_shadow,a.auto_link,a.review_if_due,a.force_review)
    elif a.cmd=='tf3-mature':out=tf3_mature(v,a.at_utc,a.auto_link)
    elif a.cmd=='tf3-review':out=tf3_review(v,a.force,a.cutoff_utc)
    elif a.cmd=='tf3-scheduler':out=tf3_scheduler(v,a.action)
    print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if out.get('status') in ('PASS','PENDING','BLOCKED') else 2
if __name__=='__main__':raise SystemExit(main())
