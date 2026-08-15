#!/usr/bin/env python3
"""Alpha Desk V2 P01 shadow semantic lifecycle adapter.

Reads closed V1 artifacts. Writes no V1 state. Uses explicit semantic owners only.
"""
from __future__ import annotations
from copy import deepcopy

CONTRACT_VERSION = "AD-V2-P01.0"
DEPLOYMENT = "SHADOW_ONLY"


def _owned(value, owner, artifact, source_path, *, horizon=None, missing=None):
    status = "PRESENT" if value not in (None, "") else "MISSING"
    if status == "MISSING" and missing is not None:
        missing.append(source_path)
    out = {"status": status, "owner": owner, "artifact": artifact, "source_path": source_path, "value": deepcopy(value)}
    if horizon is not None:
        out["horizon"] = horizon
    return out


def _v11(artifacts, missing, diagnostics):
    raw = artifacts.get("fundamental_state")
    if not isinstance(raw, dict):
        missing.append("fundamental_state")
        diagnostics.append("AUTHORITATIVE_FUNDAMENTAL_STATE_MISSING")
        return {}
    v11 = raw.get("v11_fundamental_state")
    if not isinstance(v11, dict):
        missing.append("fundamental_state.v11_fundamental_state")
        diagnostics.append("V11_FUNDAMENTAL_ENVELOPE_MISSING")
        return {}
    return v11


def _active_row(v11, active_horizon, missing, diagnostics):
    rows = v11.get("horizon_states") if isinstance(v11, dict) else None
    if not isinstance(rows, list):
        missing.append("fundamental_state.v11_fundamental_state.horizon_states")
        diagnostics.append("HORIZON_STATES_MISSING")
        return {}
    exact = [x for x in rows if isinstance(x, dict) and x.get("horizon") == active_horizon]
    if len(exact) != 1:
        missing.append(f"fundamental_state.v11_fundamental_state.horizon_states[{active_horizon}]")
        diagnostics.append("ACTIVE_HORIZON_EXACT_MATCH_REQUIRED")
        return {}
    return exact[0]


def normalize_v1_artifacts(artifacts: dict, active_horizon: str) -> dict:
    """Normalize V1 artifacts into the P01 V2 shadow semantic contract.

    No semantic substitution is permitted. Missing authoritative data fails closed.
    """
    artifacts = artifacts if isinstance(artifacts, dict) else {}
    missing = []
    diagnostics = []
    illegal = []
    substitutions = []  # Constitutionally must stay empty in P01.

    v11 = _v11(artifacts, missing, diagnostics)
    row = _active_row(v11, active_horizon, missing, diagnostics) if v11 else {}

    force = v11.get("force") if isinstance(v11.get("force"), dict) else {}
    cons89 = v11.get("consumption_v2") if isinstance(v11.get("consumption_v2"), dict) else {}
    rem = v11.get("remaining_pressure_v2") if isinstance(v11.get("remaining_pressure_v2"), dict) else {}
    pers = v11.get("persistence_v2") if isinstance(v11.get("persistence_v2"), dict) else {}
    cons103 = artifacts.get("consumption_state") if isinstance(artifacts.get("consumption_state"), dict) else {}
    ri = artifacts.get("research_intent") if isinstance(artifacts.get("research_intent"), dict) else {}
    dt = artifacts.get("driver_transition") if isinstance(artifacts.get("driver_transition"), dict) else {}

    # Exact owner-bound reads. There are intentionally no fallback chains.
    direction = _owned(row.get("direction"), "MODULE_89", "fundamental_state",
        f"v11_fundamental_state.horizon_states[{active_horizon}].direction", horizon=active_horizon, missing=missing)

    active_force_range = deepcopy(row.get("force_range"))
    if active_force_range in (None, "", {}):
        missing.append(f"v11_fundamental_state.horizon_states[{active_horizon}].force_range")
    force_status = "PRESENT" if active_force_range not in (None, "", {}) and force else "MISSING"
    fundamental_force = {
        "status": force_status,
        "owner": "MODULE_89",
        "artifact": "fundamental_state",
        "active_horizon_range": active_force_range,
        "aggregate_value": deepcopy(force.get("aggregate_value")),
        "aggregate_range": deepcopy(force.get("aggregate_range")),
        "aggregate_provenance": deepcopy(force.get("aggregate_provenance")),
        "force_class": "UNMAPPED_IN_P01",
        "source_paths": [
            f"v11_fundamental_state.horizon_states[{active_horizon}].force_range",
            "v11_fundamental_state.force.aggregate_value",
            "v11_fundamental_state.force.aggregate_range",
            "v11_fundamental_state.force.aggregate_provenance",
        ],
    }
    if force_status != "PRESENT": diagnostics.append("FUNDAMENTAL_FORCE_INCOMPLETE")

    fundamental_consumption = _owned(cons89.get("summary_state"), "MODULE_89", "fundamental_state",
        "v11_fundamental_state.consumption_v2.summary_state", missing=missing)
    cognitive_consumption = _owned(cons103.get("lifecycle_state"), "MODULE_103", "consumption_state",
        "lifecycle_state", missing=missing)

    rem_value = deepcopy(rem.get("aggregate_class")); rem_range = deepcopy(rem.get("aggregate_range"))
    if rem_value in (None, ""):
        missing.append("v11_fundamental_state.remaining_pressure_v2.aggregate_class")
    if rem_range in (None, "", {}):
        missing.append("v11_fundamental_state.remaining_pressure_v2.aggregate_range")
    remaining = {
        "status": "PRESENT" if rem_value not in (None, "") and rem_range not in (None, "", {}) else "MISSING",
        "owner": "MODULE_89", "artifact": "fundamental_state", "value": rem_value, "range": rem_range,
        "source_paths": ["v11_fundamental_state.remaining_pressure_v2.aggregate_class","v11_fundamental_state.remaining_pressure_v2.aggregate_range"],
    }

    ri_asym = _owned(ri.get("remaining_asymmetry"), "MODULE_103_FINAL_SYNTHESIS", "research_intent",
        "remaining_asymmetry", missing=missing)
    cog_asym = _owned(cons103.get("remaining_asymmetry"), "MODULE_103", "consumption_state",
        "remaining_asymmetry", missing=missing)

    pers_value = deepcopy(row.get("persistence_class"))
    if pers_value in (None, ""):
        missing.append(f"v11_fundamental_state.horizon_states[{active_horizon}].persistence_class")
    persistence = {
        "status": "PRESENT" if pers_value not in (None, "") and pers else "MISSING",
        "owner": "MODULE_89", "artifact": "fundamental_state", "value": pers_value, "horizon": active_horizon,
        "survival_metadata": deepcopy(pers),
        "source_paths": [f"v11_fundamental_state.horizon_states[{active_horizon}].persistence_class","v11_fundamental_state.persistence_v2"],
    }
    if persistence["status"] != "PRESENT": diagnostics.append("PERSISTENCE_INCOMPLETE")

    reversal = _owned(row.get("reversal_risk"), "MODULE_89", "fundamental_state",
        f"v11_fundamental_state.horizon_states[{active_horizon}].reversal_risk", horizon=active_horizon, missing=missing)

    pressure_update = _owned(row.get("next_update_trigger"), "MODULE_89", "fundamental_state",
        f"v11_fundamental_state.horizon_states[{active_horizon}].next_update_trigger", horizon=active_horizon, missing=missing)
    review = _owned(ri.get("review_trigger"), "MODULE_103_FINAL_SYNTHESIS", "research_intent", "review_trigger", missing=missing)
    invalidation = _owned(ri.get("invalidation_triggers"), "MODULE_103_FINAL_SYNTHESIS", "research_intent", "invalidation_triggers", missing=missing)

    driver_transition = {
        "owner": "MODULE_103", "artifact": "driver_transition", "state": deepcopy(dt.get("state")),
        "current_driver": deepcopy(dt.get("current_driver")), "strongest_challenger": deepcopy(dt.get("strongest_challenger")),
        "source_path": "state", "semantic_role": "DRIVER_IDENTITY_TRANSITION_ONLY",
        "excluded_from": ["fundamental_force","remaining_fundamental_pressure","persistence"],
    }

    # Defensive illegal-substitution detector: values can coincide lexically, but source paths may not.
    forbidden_sources = {
        "fundamental_force": ["driver_transition", "remaining_asymmetry", "target_price"],
        "remaining_fundamental_pressure": ["remaining_asymmetry", "target_price"],
        "persistence": ["driver_transition", "review_trigger", "target_price"],
    }
    source_index = {
        "fundamental_force": fundamental_force.get("source_paths", []),
        "remaining_fundamental_pressure": remaining.get("source_paths", []),
        "persistence": persistence.get("source_paths", []),
    }
    for field, bad_tokens in forbidden_sources.items():
        for path in source_index[field]:
            lp = str(path).lower()
            for tok in bad_tokens:
                if tok in lp:
                    illegal.append({"field": field, "source_path": path, "forbidden_token": tok})

    # Load-bearing Module 89 fields define semantic completeness. Optional cognitive fields may be missing without
    # converting valid fundamental lifecycle science into a false fallback.
    load_bearing = [
        direction["status"], fundamental_force["status"], fundamental_consumption["status"],
        remaining["status"], persistence["status"], reversal["status"], pressure_update["status"],
    ]
    integrity = "PASS" if all(x == "PRESENT" for x in load_bearing) and not illegal and not substitutions else "FAIL_CLOSED"

    return {
        "schema_version": "1.0.0", "contract_version": CONTRACT_VERSION, "deployment": DEPLOYMENT,
        "active_horizon": active_horizon,
        "fundamental_direction": direction,
        "fundamental_force": fundamental_force,
        "fundamental_consumption": fundamental_consumption,
        "cognitive_consumption": cognitive_consumption,
        "remaining_fundamental_pressure": remaining,
        "remaining_asymmetry": {"research_intent": ri_asym, "cognitive_consumption": cog_asym},
        "persistence": persistence,
        "reversal_risk": reversal,
        "driver_transition": driver_transition,
        "timing": {"pressure_next_update_trigger": pressure_update, "decision_review_trigger": review, "decision_invalidation_triggers": invalidation},
        "semantic_integrity": {"status": integrity, "substitutions_used": substitutions, "illegal_substitutions_detected": illegal,
            "missing_authoritative_fields": sorted(set(missing)), "diagnostics": diagnostics},
    }


def compatibility_summary(normalized: dict) -> dict:
    """Human-readable V1-compatible *read* view without reviving forbidden fallbacks.

    Force is intentionally not converted to HIGH/MEDIUM/LOW in P01 because V1 provides no canonical band mapping.
    """
    n = normalized if isinstance(normalized, dict) else {}
    return {
        "direction": (n.get("fundamental_direction") or {}).get("value"),
        "force": "UNMAPPED_IN_P01",
        "force_range": (n.get("fundamental_force") or {}).get("active_horizon_range"),
        "consumption": (n.get("fundamental_consumption") or {}).get("value"),
        "cognitive_consumption": (n.get("cognitive_consumption") or {}).get("value"),
        "remaining_pressure": (n.get("remaining_fundamental_pressure") or {}).get("value"),
        "remaining_asymmetry": ((n.get("remaining_asymmetry") or {}).get("research_intent") or {}).get("value"),
        "persistence": (n.get("persistence") or {}).get("value"),
        "reversal": (n.get("reversal_risk") or {}).get("value"),
        "semantic_integrity": (n.get("semantic_integrity") or {}).get("status"),
    }
