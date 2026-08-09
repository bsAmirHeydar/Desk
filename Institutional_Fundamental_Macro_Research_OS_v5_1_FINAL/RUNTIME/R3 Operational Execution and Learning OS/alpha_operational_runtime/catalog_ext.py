DDL="""
CREATE TABLE IF NOT EXISTS r3_launches(
 launch_id TEXT PRIMARY KEY, mode TEXT NOT NULL, episode_id TEXT, status TEXT NOT NULL,
 created_at_utc TEXT NOT NULL, details_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS r3_model_invocations(
 invocation_id TEXT PRIMARY KEY, run_id TEXT NOT NULL, process_id TEXT NOT NULL,
 job_hash TEXT NOT NULL, adapter TEXT NOT NULL, provider TEXT, model TEXT, model_version TEXT,
 request_hash TEXT NOT NULL, response_hash TEXT, status TEXT NOT NULL, attempt INTEGER NOT NULL,
 started_at_utc TEXT NOT NULL, completed_at_utc TEXT, latency_ms REAL, receipt_artifact_hash TEXT
);
CREATE TABLE IF NOT EXISTS r3_retrieval_items(
 run_id TEXT NOT NULL, snapshot_id TEXT NOT NULL, requirement_id TEXT NOT NULL, source_id TEXT NOT NULL,
 evidence_role TEXT NOT NULL DEFAULT 'DIRECT', artifact_hash TEXT, vintage_integrity TEXT,
 first_available_time TEXT, retrieved_at TEXT, status TEXT NOT NULL, created_at_utc TEXT NOT NULL,
 PRIMARY KEY(run_id,snapshot_id)
);
CREATE TABLE IF NOT EXISTS r3_execution_handoffs(
 handoff_id TEXT PRIMARY KEY, run_id TEXT NOT NULL, scientific_permission TEXT NOT NULL,
 operational_status TEXT NOT NULL, execution_profile TEXT NOT NULL, artifact_hash TEXT NOT NULL,
 created_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS r3_execution_receipts(
 execution_id TEXT PRIMARY KEY, run_id TEXT NOT NULL, status TEXT NOT NULL, artifact_hash TEXT NOT NULL,
 received_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS r3_d4_ledger(
 sequence INTEGER PRIMARY KEY AUTOINCREMENT, record_id TEXT UNIQUE NOT NULL, record_type TEXT NOT NULL,
 record_hash TEXT UNIQUE NOT NULL, previous_record_hash TEXT NOT NULL, payload_hash TEXT NOT NULL,
 payload_json TEXT NOT NULL, run_id TEXT, created_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS r3_analytics_rows(
 run_id TEXT PRIMARY KEY, instrument TEXT NOT NULL, run_mode TEXT NOT NULL, analysis_cutoff_utc TEXT NOT NULL,
 analysis_date TEXT NOT NULL, decision_seal_hash TEXT NOT NULL, permission TEXT, fundamental_direction TEXT,
 edge_state TEXT, active_horizon TEXT, execution_profile TEXT, outcome_state TEXT, realized_r REAL,
 mfe_r REAL, mae_r REAL, cost_r REAL, regime_state TEXT, complexity_class TEXT, unmodeled_driver_risk TEXT,
 independent_root_ids_json TEXT NOT NULL, abstention_reason_codes_json TEXT NOT NULL, updated_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS r3_counterfactuals(
 counterfactual_id TEXT PRIMARY KEY, run_id TEXT NOT NULL, branch TEXT NOT NULL, score_state TEXT NOT NULL,
 hypothetical_permission TEXT, realized_r REAL, mfe_r REAL, mae_r REAL,
 artifact_hash TEXT NOT NULL, created_at_utc TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_r3_analytics_instr_date ON r3_analytics_rows(instrument,analysis_date);
CREATE INDEX IF NOT EXISTS idx_r3_ledger_type ON r3_d4_ledger(record_type);
CREATE INDEX IF NOT EXISTS idx_r3_cf_run_branch ON r3_counterfactuals(run_id,branch);
"""
def _cols(c,table):
    return {r[1] for r in c.execute('PRAGMA table_info('+table+')').fetchall()}
def init_r3(catalog):
    with catalog.connect() as c:
        c.executescript(DDL)
        # Idempotent forward migrations for any interrupted/pre-release R3 database.
        migrations={
          'r3_retrieval_items': [('evidence_role',"TEXT NOT NULL DEFAULT 'DIRECT'"),('retrieved_at','TEXT')],
          'r3_d4_ledger': [('payload_json',"TEXT NOT NULL DEFAULT '{}'")],
          'r3_counterfactuals': [('hypothetical_permission','TEXT'),('realized_r','REAL'),('mfe_r','REAL'),('mae_r','REAL')]
        }
        for table,items in migrations.items():
            existing=_cols(c,table)
            for name,decl in items:
                if name not in existing:c.execute(f'ALTER TABLE {table} ADD COLUMN {name} {decl}')
