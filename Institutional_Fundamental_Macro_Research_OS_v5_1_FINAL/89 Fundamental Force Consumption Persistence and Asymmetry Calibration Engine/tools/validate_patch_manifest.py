#!/usr/bin/env python3
"""Validate patch paths, hashes and manifest consistency."""
from __future__ import annotations
import argparse, pathlib
from _v11_common import *
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--patch-root",required=True); ap.add_argument("--output"); a=ap.parse_args()
    root=pathlib.Path(a.patch_root); errors=[]; p=root/"PATCH_MANIFEST.json"
    if not p.exists(): errors.append("PATCH_MANIFEST.json missing"); manifest={}
    else:
        try: manifest=load_json(p)
        except Exception as e: errors.append(f"manifest invalid JSON: {e}"); manifest={}
    seen=set()
    for group in ["files_added","files_modified"]:
        for item in manifest.get(group,[]):
            rel=item.get("path","")
            pp=pathlib.PurePosixPath(rel)
            if pp.is_absolute() or ".." in pp.parts: errors.append(f"unsafe path: {rel}")
            if rel in seen: errors.append(f"duplicate path: {rel}")
            seen.add(rel)
            f=root/"payload"/rel
            if not f.is_file(): errors.append(f"payload missing: {rel}")
            elif item.get("sha256_after")!=sha256(f): errors.append(f"hash mismatch: {rel}")
    payload={str(x.relative_to(root/"payload")).replace("\\","/") for x in (root/"payload").rglob("*") if x.is_file()}
    extras=sorted(payload-seen)
    if extras: errors.append(f"unmanifested payload files: {len(extras)}")
    return dump_report({"validator":"validate_patch_manifest","status":"PASS" if not errors else "FAIL","errors":errors},a.output)
if __name__=="__main__": raise SystemExit(main())
