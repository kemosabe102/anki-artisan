# Phase 2: ORIENT - Environment Verification and Config Loading

**OODA Stage**: ORIENT | **Time Allocation**: 15-20%

**Purpose**: Verify backtest environment, load tier configuration, validate algorithm paths

**Deliverable**: Verified environment with loaded configuration

---

## Environment Verification

### Step 2.1: Script-First Environment Check

**Input**: Validated request from Phase 1

**Process**:
```bash
uv run python scripts/verify_backtest_env.py
```

**Verification Checks**:
- Python environment configured correctly
- Required packages installed (quantconnect, pandas, numpy)
- Data directories accessible
- Lean CLI available and configured

**Expected Output**:
```json
{
  "status": "VERIFIED",
  "python_version": "3.11.x",
  "lean_version": "x.x.x",
  "data_path": "/path/to/data",
  "algorithms_path": "/path/to/algorithms"
}
```

**On Failure**: Return FAILURE with diagnostic output

---

### Step 2.2: Local Compilation Validation (MANDATORY)

**BEFORE any cloud operation**:
1. Verify algorithm file exists: `Algorithms/{name}/main.py`
2. Run syntax check: `python -m py_compile Algorithms/{name}/main.py`
3. Run local lean build: `lean build Algorithms/{name}` (if lean installed locally)
4. ONLY proceed to cloud if local validation passes

**Command Sequence**:
```bash
# Step 1: Verify file exists
ls Algorithms/{name}/main.py

# Step 2: Syntax check
python -m py_compile Algorithms/{name}/main.py

# Step 3: Local build (optional but recommended)
lean build Algorithms/{name}
```

**On Local Failure**:
- STOP immediately
- Report compilation errors with file:line references
- DO NOT push to cloud for "better error messages"

**Exit Criteria**: All local validations pass before any cloud operation

**Anti-Pattern**: Pushing uncompiled code to cloud for validation

---

### Step 2.3: Load Tier Configuration

**Input**: Tier number (if tier_test mode) or defaults

**Config Files**:
- `quantconnect/tier-config.json` - Gate thresholds per tier
- `quantconnect/backtest-periods.json` - Period definitions per tier

**Process**:
1. Read tier-config.json
2. Extract tier-specific gate thresholds
3. Read backtest-periods.json
4. Extract period list for specified tier

**tier-config.json Structure**:
```json
{
  "tiers": {
    "1": {
      "gates": {
        "sharpe_minimum": 0.20,
        "max_drawdown": 0.50,
        "trade_count_minimum": 20
      }
    }
  }
}
```

**Output**: Loaded configuration object

---

### Step 2.4: Validate Algorithm Path

**Input**: algorithm_path from request (if provided)

**Process**:
1. Verify algorithm folder exists
2. Check for required files (main.py or Algorithm.cs)
3. Validate Initialize() method exists
4. Check for config.json if required

**Path Validation**:
```
algorithm_path must:
- Be absolute path
- Use forward slashes
- Exist and be readable
- Contain valid algorithm structure
```

**Output**: Validated algorithm path or default

---

### Step 2.5: Load Regime Configuration (Optional)

**Input**: regime_config from request

**When**: `regime_config.enabled = true`

**Process**:
1. Validate regime_config structure
2. Load regime-classifier skill configuration
3. Prepare regime stratification parameters

**regime_config Structure**:
```json
{
  "enabled": true,
  "factors": ["volatility", "trend", "correlation"],
  "stratify_results": true,
  "source": "risk-management-specialist"
}
```

**Output**: Loaded regime configuration or null

---

## Exit Criteria

**All criteria must pass to proceed to DECIDE**:

| Criterion | Check | On Failure |
|-----------|-------|------------|
| Environment verified | Script returns VERIFIED | FAILURE with diagnostics |
| Config loaded | tier-config.json readable | FAILURE - config not found |
| Periods defined | backtest-periods.json valid | FAILURE - periods undefined |
| Algorithm path valid | Path exists and readable | FAILURE - algorithm not found |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping environment check | ALWAYS run verify script first |
| Hardcoding config values | Load from tier-config.json |
| Relative algorithm paths | Convert to absolute paths |
| Missing period definitions | Verify backtest-periods.json exists |

---

**Previous Phase**: [Phase 1: OBSERVE](phase-1-observe.md)
**Next Phase**: [Phase 3: DECIDE](phase-3-decide.md)
