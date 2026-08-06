#!/usr/bin/env python3
"""Run the V11 validation suite in one process. Standard library only."""
from __future__ import annotations
import argparse, json, pathlib, sys, re
from _v11_common import *
from validate_v11_state_schema import validate as schema_validate

REQUIRED_PROV={"force.aggregate_value","consumption_v2.summary_state","remaining_pressure_v2.aggregate_class","asymmetry_v2.path_asymmetry_class"}

def semantic_record_checks(path):
    doc=load_json(path); s=state(doc); errors=[]
    errors += [f"schema:{x}" for x in schema_validate(doc)]
    rows=s.get("provenance",{}).get("field_level_ledger",[])
    present={r.get("field") for r in rows}
    errors += [f"provenance missing:{x}" for x in sorted(REQUIRED_PROV-present)]
    caps=s.get("provenance",{}).get("confidence_caps",[])
    for c in caps:
        target=get_path(s,c.get("field",""))
        actual=target.get("confidence") if isinstance(target,dict) else target
        if isinstance(actual,(int,float)) and actual>c.get("cap",100): errors.append(f"cap exceeded:{c['field']}")
    unavailable={x.get("input") for x in s.get("provenance",{}).get("unavailable_inputs",[])}
    flow=s.get("consumption_v2",{}).get("mechanical_flow_exhaustion",{})
    if "proprietary_flow_data" in unavailable and (flow.get("confidence") or 0)>65: errors.append("public flow confidence >65")
    m=s.get("methodology",{})
    if m.get("scoring_mode")=="EMPIRICALLY_CALIBRATED_MODE":
        if not m.get("estimand"): errors.append("calibrated mode missing estimand")
        if not m.get("calibration_evidence_locator"): errors.append("calibrated mode missing evidence")
        if s.get("validation",{}).get("calibration_status") not in {"OUT_OF_SAMPLE_PARTIAL","OUT_OF_SAMPLE_VALIDATED"}: errors.append("calibrated mode lacks OOS status")
    hs=s.get("horizon_states",[])
    names=[h.get("horizon") for h in hs]
    if len(names)!=len(set(names)): errors.append("duplicate horizons")
    return errors

def link_delta(root, baseline_path):
    idx=title_index(root); unresolved=[]; ambiguous=[]; malformed=[]; fences=[]
    relpaths={str(p.relative_to(root)).replace("\\","/") for p in markdown_files(root)}
    for p in markdown_files(root):
        t=p.read_text(encoding="utf-8",errors="replace")
        rel=str(p.relative_to(root)).replace("\\","/")
        if parse_frontmatter(t) is None: malformed.append(rel)
        if t.count("```")%2: fences.append(rel)
        for link in wikilinks(t):
            if link+".md" in relpaths: continue
            c=idx.get(link,[])
            if not c: unresolved.append({"source":rel,"target":link})
            elif len({str(x) for x in c})>1: ambiguous.append({"source":rel,"target":link})
    base=load_json(baseline_path)
    def key(x): return (x.get("source"),x.get("target"))
    errors=[]
    if [x for x in unresolved if key(x) not in {key(y) for y in base.get("unresolved",[])}]: errors.append("introduced unresolved links")
    if [x for x in ambiguous if key(x) not in {key(y) for y in base.get("ambiguous",[])}]: errors.append("introduced ambiguous links")
    if set(malformed)-set(base.get("malformed",[])): errors.append("introduced malformed frontmatter")
    if set(fences)-set(base.get("unbalanced_fences",[])): errors.append("introduced unbalanced fences")
    return errors, {"unresolved":len(unresolved),"ambiguous":len(ambiguous),"malformed":len(malformed),"unbalanced_fences":len(fences)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--vault-root",required=True)
    ap.add_argument("--patch-root",required=True)
    ap.add_argument("--baseline-link-report",required=True)
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    root=pathlib.Path(a.vault_root); patch=pathlib.Path(a.patch_root); module=root/"89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine"
    checks={}; errors=[]
    for p in sorted((module/"examples").glob("example_*.json")):
        e=semantic_record_checks(p); checks[f"example:{p.name}"]={"status":"PASS" if not e else "FAIL","errors":e}; errors += [f"{p.name}:{x}" for x in e]
    invalid=module/"examples"/"invalid_false_calibration_and_cap.json"
    neg=semantic_record_checks(invalid)
    checks["negative_fixture"]={"status":"PASS" if neg else "FAIL","detected_errors":neg}
    if not neg: errors.append("negative fixture unexpectedly passed")
    # Required paths / regression.
    req=[
      "00 HOME.md","01 COVERAGE MATRIX.md",
      "88 Hybrid Daily Session Event Fundamental State Engine/14 Hybrid Fundamental State Schema.md",
      "89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/00 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine MOC.md",
      "89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/38 Alpha Lab V11 Full-Spectrum Fundamental State Analysis Prompt.md",
      "V11_CANONICAL_AUTHORITY_MAP.yaml"
    ]
    missing=[x for x in req if not (root/x).is_file()]
    checks["regression_required_paths"]={"status":"PASS" if not missing else "FAIL","missing":missing}; errors += [f"missing:{x}" for x in missing]
    schema_text=(root/"88 Hybrid Daily Session Event Fundamental State Engine/14 Hybrid Fundamental State Schema.md").read_text(encoding="utf-8")
    markers=["direction","intensity","confidence","consumption","remaining_pressure","25"]
    absent=[x for x in markers if x.lower() not in schema_text.lower()]
    checks["v10_schema_markers"]={"status":"PASS" if not absent else "FAIL","absent":absent}; errors += [f"v10 marker missing:{x}" for x in absent]
    # Authority.
    auth=(root/"V11_CANONICAL_AUTHORITY_MAP.yaml").read_text(encoding="utf-8")
    concepts=["force","consumption","remaining_pressure","persistence","reversal_risk","fundamental_asymmetry","confidence_caps","calibration"]
    absent=[x for x in concepts if re.search(rf"(?m)^\s*{re.escape(x)}\s*:",auth) is None]
    checks["authority_map"]={"status":"PASS" if not absent else "FAIL","absent":absent}; errors += [f"authority missing:{x}" for x in absent]
    # Links.
    le, totals=link_delta(root,a.baseline_link_report)
    checks["link_frontmatter_delta"]={"status":"PASS" if not le else "FAIL","errors":le,"totals":totals}; errors += le
    # Benchmarks.
    benches=list((module/"benchmarks").glob("B*.json")); bad=[]
    for p in benches:
        d=load_json(p)
        for k in ["benchmark_id","frozen_cutoff_utc","allowed_evidence","prohibited_evidence","core_acceptance_condition"]:
            if k not in d: bad.append(f"{p.name}:{k}")
    checks["benchmarks"]={"status":"PASS" if len(benches)==25 and not bad else "FAIL","count":len(benches),"errors":bad}
    if len(benches)!=25: errors.append(f"benchmark count {len(benches)}")
    errors += bad
    # Patch manifest.
    man=load_json(patch/"PATCH_MANIFEST.json"); p_errors=[]; seen=set()
    for group in ["files_added","files_modified"]:
        for item in man.get(group,[]):
            rel=item["path"]; f=patch/"payload"/rel
            if rel in seen: p_errors.append(f"duplicate:{rel}")
            seen.add(rel)
            if not f.is_file(): p_errors.append(f"missing:{rel}")
            elif sha256(f)!=item["sha256_after"]: p_errors.append(f"hash:{rel}")
    payload={str(x.relative_to(patch/"payload")).replace("\\","/") for x in (patch/"payload").rglob("*") if x.is_file()}
    if payload-seen: p_errors.append(f"unmanifested:{len(payload-seen)}")
    checks["patch_manifest"]={"status":"PASS" if not p_errors else "FAIL","errors":p_errors}; errors += p_errors
    report={"validator":"run_v11_validation_suite","status":"PASS" if not errors else "FAIL","generated_at_utc":__import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),"checks":checks,"errors":errors,
      "certification_boundary":["No empirical market calibration executed","No proprietary flow dataset supplied","Internal validation only"]}
    pathlib.Path(a.output).write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],"checks":len(checks),"errors":len(errors)},indent=2))
    return 0 if not errors else 1
if __name__=="__main__": raise SystemExit(main())
