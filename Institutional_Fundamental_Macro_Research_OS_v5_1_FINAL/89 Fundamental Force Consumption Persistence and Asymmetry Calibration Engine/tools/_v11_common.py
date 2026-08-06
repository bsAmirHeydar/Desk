#!/usr/bin/env python3
"""Shared V11 validator utilities. Standard library only."""
from __future__ import annotations
import argparse, hashlib, json, pathlib, re, sys
from typing import Any

HORIZONS = {"MICRO_0_15M","SHORT_15_60M","SESSION_1_6H","DAILY_OPEN_TO_CLOSE","MULTI_DAY_2_10D","CYCLICAL","STRUCTURAL"}
PROVENANCE = {"OBSERVED","OFFICIAL_FIRST_RELEASE","OFFICIAL_REVISION","DERIVED_DETERMINISTIC","MARKET_IMPLIED","EMPIRICALLY_CALIBRATED","MODEL_IMPLIED","PUBLIC_PROXY","LICENSED_DATA","PROPRIETARY_DATA","STRUCTURED_JUDGMENT","UNAVAILABLE"}

def load_json(path):
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))

def dump_report(report, output=None):
    text=json.dumps(report, indent=2, ensure_ascii=False)
    if output: pathlib.Path(output).write_text(text+"\n",encoding="utf-8")
    print(text)
    return 0 if report.get("status")=="PASS" else 1

def state(doc):
    if not isinstance(doc,dict) or "v11_fundamental_state" not in doc:
        raise ValueError("root key v11_fundamental_state is required")
    return doc["v11_fundamental_state"]

def get_path(obj: Any, path: str):
    cur=obj
    for part in path.split("."):
        if isinstance(cur,dict) and part in cur: cur=cur[part]
        else: return None
    return cur

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def markdown_files(root):
    root=pathlib.Path(root)
    return [p for p in root.rglob("*.md") if not any(part.startswith(".") for part in p.relative_to(root).parts)]

def parse_frontmatter(text):
    if not text.startswith("---\n"): return None
    end=text.find("\n---\n",4)
    if end<0: return None
    data={}
    for line in text[4:end].splitlines():
        if ":" in line:
            k,v=line.split(":",1); data[k.strip()]=v.strip().strip('"')
    return data

def wikilinks(text):
    return re.findall(r"\[\[([^\]|#]+)",text)

def title_index(root):
    idx={}
    for p in markdown_files(root):
        title=p.stem
        idx.setdefault(title,[]).append(p)
        fm=parse_frontmatter(p.read_text(encoding="utf-8",errors="replace"))
        if fm and fm.get("title"): idx.setdefault(fm["title"],[]).append(p)
    return idx
