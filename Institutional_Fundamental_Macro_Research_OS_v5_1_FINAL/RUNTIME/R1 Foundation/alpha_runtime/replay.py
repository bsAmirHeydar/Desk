from .visibility import build_receipt
from .canonical import sha256_obj
from .timeutil import utc_now

def reproduce_visibility(source_manifest,source_snapshot_manifest,source_visibility_receipt,replay_run_id,requirements):
    cutoff=source_manifest['analysis_cutoff_utc']
    snapshots=source_snapshot_manifest['snapshots']
    # Reproduction uses the original run's visibility semantics over its frozen snapshots.
    # It does not query future sources and it does not reinterpret an original live capture as a later historical reconstruction.
    receipt=build_receipt(replay_run_id,cutoff,source_manifest.get('run_mode','LIVE'),requirements,snapshots)
    def normalized(r):
        x={k:v for k,v in r.items() if k not in ('run_id','created_at_utc','receipt_hash')}; return sha256_obj(x)
    parity=normalized(source_visibility_receipt)==normalized(receipt)
    return receipt,{"schema_version":"1.0.0","source_run_id":source_manifest['run_id'],"replay_run_id":replay_run_id,"analysis_cutoff_utc":cutoff,"source_snapshot_manifest_hash":source_manifest.get('snapshot_manifest_hash') or sha256_obj(source_snapshot_manifest),"source_visibility_receipt_hash":source_visibility_receipt.get('receipt_hash') or sha256_obj(source_visibility_receipt),"replay_visibility_receipt_hash":receipt['receipt_hash'],"visibility_parity":parity,"limitations":["R1 certifies frozen-snapshot evidence visibility parity; full cognitive reproduction requires R2 prompt/runtime pins."],"created_at_utc":utc_now()}
