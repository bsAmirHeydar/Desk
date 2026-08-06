#!/usr/bin/env python3
"""Validate frontmatter/fences and report wikilink resolution. Existing-baseline issues can be supplied and are not counted as introduced."""
from __future__ import annotations
import argparse, pathlib, json
from _v11_common import *
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--vault-root",required=True); ap.add_argument("--baseline-report"); ap.add_argument("--output"); a=ap.parse_args()
    root=pathlib.Path(a.vault_root); idx=title_index(root); errors=[]; unresolved=[]; ambiguous=[]; malformed=[]; fences=[]
    for p in markdown_files(root):
        t=p.read_text(encoding="utf-8",errors="replace")
        if parse_frontmatter(t) is None: malformed.append(str(p.relative_to(root)))
        if t.count("```")%2: fences.append(str(p.relative_to(root)))
        for link in wikilinks(t):
            direct=(root/(link+".md"))
            if direct.is_file():
                continue
            c=idx.get(link,[])
            if not c: unresolved.append({"source":str(p.relative_to(root)),"target":link})
            elif len({str(x) for x in c})>1: ambiguous.append({"source":str(p.relative_to(root)),"target":link,"matches":sorted({str(x.relative_to(root)) for x in c})})
    baseline={"unresolved":[],"ambiguous":[],"malformed":[],"unbalanced_fences":[]}
    if a.baseline_report:
        baseline=load_json(a.baseline_report)
    def key(x): return (x.get("source"),x.get("target"))
    introduced_unresolved=[x for x in unresolved if key(x) not in {key(y) for y in baseline.get("unresolved",[])}]
    introduced_ambiguous=[x for x in ambiguous if key(x) not in {key(y) for y in baseline.get("ambiguous",[])}]
    introduced_malformed=sorted(set(malformed)-set(baseline.get("malformed",[])))
    introduced_fences=sorted(set(fences)-set(baseline.get("unbalanced_fences",[])))
    if introduced_unresolved: errors.append(f"{len(introduced_unresolved)} introduced unresolved wikilinks")
    if introduced_ambiguous: errors.append(f"{len(introduced_ambiguous)} introduced ambiguous wikilinks")
    if introduced_malformed: errors.append(f"{len(introduced_malformed)} introduced malformed frontmatter files")
    if introduced_fences: errors.append(f"{len(introduced_fences)} introduced unbalanced-fence files")
    report={"validator":"validate_vault_links_and_frontmatter","status":"PASS" if not errors else "FAIL","errors":errors,
      "unresolved":unresolved,"ambiguous":ambiguous,"malformed":malformed,"unbalanced_fences":fences,
      "introduced":{"unresolved":introduced_unresolved,"ambiguous":introduced_ambiguous,"malformed":introduced_malformed,"unbalanced_fences":introduced_fences},
      "totals":{"unresolved":len(unresolved),"ambiguous":len(ambiguous),"malformed":len(malformed),"unbalanced_fences":len(fences)}}
    return dump_report(report,a.output)
if __name__=="__main__": raise SystemExit(main())
