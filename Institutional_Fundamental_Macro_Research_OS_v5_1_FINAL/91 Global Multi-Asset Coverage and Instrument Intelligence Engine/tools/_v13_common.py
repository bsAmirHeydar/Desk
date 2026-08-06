#!/usr/bin/env python3
from __future__ import annotations
import csv,json,pathlib
MOD="91 Global Multi-Asset Coverage and Instrument Intelligence Engine"
def load(p):return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
def registry(root):
 p=pathlib.Path(root)/MOD/"instrument_registry.csv"
 with p.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))
def adapters(root):return load(pathlib.Path(root)/MOD/"asset_adapters.json")
def ex(root,prefix="example_"):return sorted((pathlib.Path(root)/MOD/"examples").glob(prefix+"*.json"))
def errors(d):
 e=[]
 for k in ["methodology","instrument","coverage","shared_state","provenance","validation"]:
  if k not in d:e.append("missing "+k)
 if e:return e
 ins=d["instrument"];cov=d["coverage"];fam=ins.get("asset_family")
 if ins.get("resolution_status")=="UNRESOLVED" and d.get("shared_state",{}).get("direction") not in [None,"UNDETERMINED"]:e.append("unresolved has direction")
 if cov.get("status")=="FULLY_SUPPORTED" and cov.get("missing_inputs"):e.append("full support has missing inputs")
 key={"FX":"fx_state","COMMODITY":"commodity_state","INDEX":"index_state"}.get(fam)
 if key and key not in d:e.append("missing specialist state")
 if fam=="FX":
  x=d.get("fx_state") or {}
  if not x.get("base_currency_block") or not x.get("quote_currency_block"):e.append("FX missing leg")
 if fam=="COMMODITY":
  x=d.get("commodity_state") or {}
  if not all(k in x for k in ["physical_balance","curve","grade_location"]):e.append("commodity missing physical/curve/identity")
 if fam=="INDEX" and "CURRENT_USED_FOR_2010" in json.dumps(d.get("index_state")):e.append("constituent lookahead")
 if d.get("methodology",{}).get("scoring_mode")!="EMPIRICALLY_CALIBRATED" and "probability" in json.dumps(d).lower():e.append("false probability")
 return e
