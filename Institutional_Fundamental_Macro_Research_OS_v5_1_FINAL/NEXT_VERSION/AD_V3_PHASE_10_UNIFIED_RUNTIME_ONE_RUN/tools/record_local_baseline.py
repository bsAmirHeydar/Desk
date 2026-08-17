from __future__ import annotations
import argparse,json,pathlib
HERE=pathlib.Path(__file__).resolve(); PH=HERE.parents[1]
def load(p): return json.loads(p.read_text(encoding='utf-8-sig')) if p.exists() else {}
def save(p,o): p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--commit',required=True);a=ap.parse_args();commit=a.commit.strip()
 if not commit: raise SystemExit('EMPTY_BASELINE_COMMIT')
 for name in ['DEVELOPMENT_MANIFEST.json','PHASE_10_HANDOFF.json']:
  p=PH/name;o=load(p);o['baseline_commit']=commit;save(p,o)
 receipt=PH/'baseline/LOCAL_INSTALL_BASELINE.json'
 save(receipt,{'record_type':'AD_V3_P10_LOCAL_INSTALL_BASELINE','baseline_commit':commit,'source':'operator_git_before_p10_install'})
 print(json.dumps({'status':'PASS','baseline_commit':commit,'updated':['DEVELOPMENT_MANIFEST.json','PHASE_10_HANDOFF.json','baseline/LOCAL_INSTALL_BASELINE.json']},indent=2))
if __name__=='__main__': main()
