#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,pathlib,subprocess,sys
a=argparse.ArgumentParser();a.add_argument("--vault-root",required=True);a.add_argument("--patch-root",required=True);a.add_argument("--output",required=True);x=a.parse_args();r=pathlib.Path(x.vault_root);m=r/"91 Global Multi-Asset Coverage and Instrument Intelligence Engine"
def run(fn,args):
 p=subprocess.run([sys.executable,str(m/"tools"/fn)]+args,capture_output=True,text=True)
 try:d=json.loads(p.stdout)
 except:d={"status":"FAIL","errors":[p.stdout,p.stderr]}
 d["returncode"]=p.returncode;return d
files=["validate_v13_universal_schema.py","validate_instrument_resolution.py","validate_asset_adapter_selection.py","validate_fx_bilateral_synthesis.py","validate_fx_regime_handling.py","validate_commodity_contract_identity.py","validate_commodity_physical_balance.py","validate_index_methodology_and_constituents.py","validate_point_in_time_metadata.py","validate_universal_report_completeness.py","validate_large_universe_depth_control.py","validate_data_confidence_caps.py","validate_v11_v12_regression.py"];checks={f:run(f,["--vault-root",str(r)]) for f in files};checks["validate_patch_manifest.py"]=run("validate_patch_manifest.py",["--patch-root",x.patch_root])
sys.path.insert(0,str(m/"tools"));from _v13_common import ex,load,errors
bad=[p.name for p in ex(r,"invalid_") if not errors(load(p))];checks["invalid_fixtures"]={"status":"PASS" if not bad else "FAIL","count":len(ex(r,"invalid_")),"errors":bad};bench=list((m/"benchmarks").glob("B*.json"));checks["benchmarks"]={"status":"PASS" if len(bench)>=60 else "FAIL","count":len(bench),"errors":[]};status="PASS" if all(v.get("status")=="PASS" and v.get("returncode",0)==0 for v in checks.values()) else "FAIL";out={"status":status,"checks":checks,"certification_boundary":["architecture and deterministic QA only","no universal live-data completeness","no proprietary flow or inventory certification","no empirical alpha certification"]};pathlib.Path(x.output).write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8");print(json.dumps(out,indent=2));sys.exit(0 if status=="PASS" else 1)
