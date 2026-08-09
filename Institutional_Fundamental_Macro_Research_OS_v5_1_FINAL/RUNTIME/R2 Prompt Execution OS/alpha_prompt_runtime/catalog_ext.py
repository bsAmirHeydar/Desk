DDL="""
CREATE TABLE IF NOT EXISTS r2_process_runs(
 run_id TEXT PRIMARY KEY,
 prompt_pack_version TEXT NOT NULL,
 process_graph_version TEXT NOT NULL,
 model_profile_set TEXT NOT NULL,
 coverage_mode TEXT NOT NULL,
 research_depth TEXT NOT NULL,
 status TEXT NOT NULL,
 created_at_utc TEXT NOT NULL,
 updated_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS r2_process_state(
 run_id TEXT NOT NULL,
 process_id TEXT NOT NULL,
 process_version TEXT NOT NULL,
 stage TEXT NOT NULL,
 status TEXT NOT NULL,
 attempt_count INTEGER NOT NULL DEFAULT 0,
 output_status TEXT,
 output_reason TEXT,
 last_job_hash TEXT,
 completed_at_utc TEXT,
 PRIMARY KEY(run_id,process_id)
);
CREATE TABLE IF NOT EXISTS r2_stage_gates(
 run_id TEXT NOT NULL,
 gate_id TEXT NOT NULL,
 status TEXT NOT NULL,
 receipt_hash TEXT,
 created_at_utc TEXT NOT NULL,
 PRIMARY KEY(run_id,gate_id)
);
CREATE TABLE IF NOT EXISTS r2_prompt_pins(
 run_id TEXT NOT NULL,
 process_id TEXT NOT NULL,
 process_version TEXT NOT NULL,
 prompt_hash TEXT NOT NULL,
 model_profile TEXT NOT NULL,
 PRIMARY KEY(run_id,process_id)
);
"""

def init_r2(catalog):
    with catalog.connect() as c: c.executescript(DDL)
