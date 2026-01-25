# Backtester Scripts

> **Script-First Protocol**: Always use these scripts for environment setup, backtest execution, and result retrieval. Direct API calls or manual operations are discouraged.

---

## Available Scripts

| Script | Purpose | Required Env Vars |
|--------|---------|-------------------|
| `verify_backtest_env.py` | Validate environment before backtest execution | `TRENDY_TRADER_PATH`, optionally `QC_API_USER_ID`, `QC_API_TOKEN` |
| `fetch_backtest_logs.py` | Retrieve backtest logs and results from QuantConnect cloud | `QC_API_USER_ID`, `QC_API_TOKEN` |
| `init_qc_project.py` | Initialize or sync a QuantConnect project | `TRENDY_TRADER_PATH` |
| `run_tier_backtest.py` | Execute tier-based progressive backtests | `TRENDY_TRADER_PATH` |

---

## Environment Variables

### Required for All Operations

| Variable | Description | Example |
|----------|-------------|---------|
| `TRENDY_TRADER_PATH` | Absolute path to trendy-trader repository | `C:/Users/kemos/Repos/trendy-trader` |

### Required for Cloud Operations

| Variable | Description | Source |
|----------|-------------|--------|
| `QC_API_USER_ID` | QuantConnect API User ID | QuantConnect Account Settings |
| `QC_API_TOKEN` | QuantConnect API Token | QuantConnect Account Settings |

### Setting Environment Variables

**Windows (PowerShell)**:
```powershell
$env:TRENDY_TRADER_PATH = "C:/Users/kemos/Repos/trendy-trader"
$env:QC_API_USER_ID = "your-user-id"
$env:QC_API_TOKEN = "your-api-token"
```

**Windows (Command Prompt)**:
```cmd
set TRENDY_TRADER_PATH=C:/Users/kemos/Repos/trendy-trader
set QC_API_USER_ID=your-user-id
set QC_API_TOKEN=your-api-token
```

**Linux/macOS**:
```bash
export TRENDY_TRADER_PATH="/home/user/repos/trendy-trader"
export QC_API_USER_ID="your-user-id"
export QC_API_TOKEN="your-api-token"
```

---

## Usage Examples

### 1. Verify Environment (Run First)

```bash
# Check local backtest environment
uv run python .claude/agents/investing/backtester/scripts/verify_backtest_env.py --mode local

# Check cloud backtest environment (includes API credential verification)
uv run python .claude/agents/investing/backtester/scripts/verify_backtest_env.py --mode cloud
```

**Exit Codes**:
- `0`: All checks passed
- `1`: TRENDY_TRADER_PATH not set or invalid
- `2`: Configuration files missing (tier-config.json or backtest-periods.json)
- `3`: Lean CLI not installed or not in PATH
- `4`: Cloud credentials missing (cloud mode only)

### 2. Initialize QuantConnect Project

```bash
# Initialize a new algorithm project
uv run python .claude/agents/investing/backtester/scripts/init_qc_project.py \
    --algorithm StageAnalysisTrendMomentum

# Sync existing project to cloud
uv run python .claude/agents/investing/backtester/scripts/init_qc_project.py \
    --algorithm StageAnalysisTrendMomentum \
    --cloud-sync
```

### 3. Fetch Backtest Logs

```bash
# List recent backtests for a project
uv run python .claude/agents/investing/backtester/scripts/fetch_backtest_logs.py \
    --project-id 27218459 \
    --list

# Fetch specific backtest results
uv run python .claude/agents/investing/backtester/scripts/fetch_backtest_logs.py \
    --project-id 27218459 \
    --backtest-id 40764ce7389439d01b5c00efd827d9e7

# Save results to output directory
uv run python .claude/agents/investing/backtester/scripts/fetch_backtest_logs.py \
    --project-id 27218459 \
    --backtest-id 40764ce7389439d01b5c00efd827d9e7 \
    --output-dir ./backtest-results/
```


### 4. Run Tier-Based Backtest

```bash
# Run Tier 1 backtest (sanity check)
uv run python .claude/agents/investing/backtester/scripts/run_tier_backtest.py \
    --algorithm StageAnalysisTrendMomentum \
    --tier 1 \
    --hypothesis-id HYP-20260115-STAGE2-001

# Run Tier 2 with checkpoint resume
uv run python .claude/agents/investing/backtester/scripts/run_tier_backtest.py \
    --algorithm StageAnalysisTrendMomentum \
    --tier 2 \
    --hypothesis-id HYP-20260115-STAGE2-001 \
    --resume

# Run all periods in Tier 3
uv run python .claude/agents/investing/backtester/scripts/run_tier_backtest.py \
    --algorithm StageAnalysisTrendMomentum \
    --tier 3 \
    --hypothesis-id HYP-20260115-STAGE2-001 \
    --output-dir ./backtest-history/runs/
```

---

## Script Integration with Backtester Agent

The backtester agent delegates to these scripts via the script-first protocol:

```
Agent Request -> Script Execution -> Result Parsing -> Verdict Generation
```

### Delegation Pattern

```python
# Agent delegates environment verification
Task(verify_backtest_env, "--mode cloud")

# Agent delegates tier execution
Task(run_tier_backtest, "--algorithm {algo} --tier {tier} --hypothesis-id {hyp_id}")

# Agent parses results for gate evaluation
```

---

## File Dependencies

These scripts expect the following files in `$TRENDY_TRADER_PATH/quantconnect/`:

| File | Purpose |
|------|---------|
| `tier-config.json` | Tier gate thresholds, period mappings |
| `backtest-periods.json` | Historical period definitions by regime |
| `Algorithms/{name}/` | Algorithm source code directory |
| `Algorithms/{name}/config.json` | Algorithm cloud project configuration |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "TRENDY_TRADER_PATH not set" | Set environment variable (see above) |
| "lean: command not found" | Install Lean CLI: `pip install lean` |
| "API authentication failed" | Verify QC_API_USER_ID and QC_API_TOKEN |
| "tier-config.json not found" | Ensure TRENDY_TRADER_PATH points to trendy-trader repo |
| "Algorithm directory not found" | Check algorithm name spelling |
