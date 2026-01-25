# Checkpoint Management

Checkpoint schema, resume behavior, and cleanup rules for interrupted backtest runs.

---

## Checkpoint File

**Location**: `{backtest-history}/runs/{run_id}/.checkpoint.json`

### Schema

```json
{
  "schema_version": "1.0",
  "checksum": "sha256:...",
  "run_id": "20260103_001",
  "algorithm": "StageAnalysisTrendMomentum",
  "tier": 2,
  "hypothesis_id": "HYP-20260103-STAGE2-001",
  "trial_number": 2,
  "started_at": "2026-01-03T10:00:00Z",
  "total_periods": 6,
  "completed_periods": [
    {"id": "post_gfc_bull", "sharpe": 0.45, "dd": -22, "trades": 15, "status": "OK"},
    {"id": "gfc_bear", "sharpe": 0.22, "dd": -35, "trades": 8, "status": "OK"}
  ],
  "current_period": 3,
  "status": "IN_PROGRESS"
}
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | string | Checkpoint format version for compatibility |
| `checksum` | string | SHA256 hash for integrity validation |
| `run_id` | string | Unique run identifier (date_sequence) |
| `algorithm` | string | Algorithm name being tested |
| `tier` | number | Tier level (1-4) |
| `hypothesis_id` | string | Associated hypothesis identifier |
| `trial_number` | number | Current trial count for this hypothesis |
| `started_at` | string | ISO8601 timestamp of run start |
| `total_periods` | number | Total periods in this tier |
| `completed_periods` | array | Array of completed period results |
| `current_period` | number | Index of next period to execute |
| `status` | string | Current status: "IN_PROGRESS" |

---

## Resume Behavior

When `--resume` flag is provided or checkpoint exists:

```text
1. Load checkpoint file from run directory
2. Validate checksum for integrity
3. Skip periods in `completed_periods` array
4. Start execution from `current_period` index
5. Merge new results with existing `completed_periods`
6. Continue to aggregation with combined results
```

### Resume Decision Flow

```
IF --resume flag OR checkpoint exists:
  IF --no-resume flag:
    Delete checkpoint, start fresh
  ELSE:
    Load checkpoint
    IF checksum invalid:
      ERROR: "Checkpoint corrupted. Use --no-resume to restart fresh."
    ELSE:
      Resume from current_period
```

### Resume Display

```
Resuming from checkpoint...
Run ID: 20260103_001
Completed: 2/6 periods
Continuing from period 3: tech_boom
```

---

## Checkpoint Cleanup

### Automatic Cleanup

On successful completion (all periods tested + verdict generated):

```text
1. Generate final report (verdict.md)
2. Save run-manifest.json
3. Delete checkpoint file (.checkpoint.json)
4. Checkpoint presence indicates incomplete run
```

### Manual Cleanup

To force a fresh run when checkpoint exists:

```bash
/backtest StageAnalysisTrendMomentum 2 --no-resume
```

Or manually delete the checkpoint:

```bash
rm backtest-history/runs/{run_id}/.checkpoint.json
```

---

## Atomic Checkpoint Writes

To prevent corruption during interruption, checkpoints use atomic write pattern:

```text
WRITE SEQUENCE:
  1. Serialize checkpoint to JSON
  2. Write to: {checkpoint_path}.tmp
  3. Validate written JSON is parseable
  4. Rename: {checkpoint_path}.tmp -> {checkpoint_path}

RESULT:
  - Checkpoint file is always complete OR absent
  - Partial writes stay in .tmp file
  - System crash during write = no checkpoint (restart fresh)
```

---

## Checkpoint Presence Logic

| Checkpoint Exists | --resume Flag | --no-resume Flag | Behavior |
|-------------------|---------------|------------------|----------|
| No | - | - | Fresh run |
| Yes | No | No | Prompt user: resume or fresh? |
| Yes | Yes | No | Resume from checkpoint |
| Yes | No | Yes | Delete checkpoint, fresh run |
| Yes | Yes | Yes | Error: conflicting flags |
