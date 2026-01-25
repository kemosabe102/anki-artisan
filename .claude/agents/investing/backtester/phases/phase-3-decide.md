# Phase 3: DECIDE - Mode Selection and Configuration

**OODA Stage**: DECIDE | **Time Allocation**: 10-15%

**Purpose**: Auto-detect operation mode, configure timeouts, set up gate thresholds

**Deliverable**: Selected mode with configured gates and timeout

---

## Mode Detection

### Step 3.1: Auto-Detect Mode from Request

**Input**: User request or orchestrator delegation

**Mode Detection Table**:

| User Says | Mode | Description |
|-----------|------|-------------|
| "backtest this", "run backtest" | `single_run` | Execute ONE backtest per hypothesis |
| "test across regimes", "regime test" | `regime_test` | Execute across volatility regimes |
| "walk-forward", "rolling validation" | `walk_forward` | Rolling window OOS validation |
| "final test", "holdout validation" | `final_validation` | Holdout test before deployment |
| "tier test", "run tier", "progressive" | `tier_test` | Multi-period tier execution |
| "capacity test", "scale test" | `capacity_test` | Test Sharpe degradation at scale |
| "generate dashboard", "6D dashboard" | `dashboard` | Generate metrics dashboard |
| "validate results", "check gates" | `validate` | Apply gates to aggregated metrics |
| "aggregate metrics", "combine results" | `aggregate` | Aggregate period results |

**Default**: `single_run` if mode cannot be determined

**Output**: Detected mode with confidence score

---

### Step 3.2: Configure Timeout

**Input**: Detected mode from Step 3.1

**Mode Timeout Table**:

| Mode | Timeout (ms) | Timeout (min) | Rationale |
|------|--------------|---------------|-----------|
| `single_run` | 300,000 | 5 | Single backtest execution |
| `regime_test` | 600,000 | 10 | 4 regime backtests |
| `walk_forward` | 900,000 | 15 | 3-5 rolling windows |
| `final_validation` | 300,000 | 5 | Single holdout test |
| `tier_test` | 600,000 | 10 | Multi-period execution |
| `capacity_test` | 1,200,000 | 20 | Multi-scale testing |
| `aggregate` | 60,000 | 1 | Metric aggregation |
| `validate` | 60,000 | 1 | Gate evaluation |
| `dashboard` | 120,000 | 2 | Report generation |

**Output**: Configured timeout for Bash operations

---

### Step 3.3: Configure Gate Thresholds

**Input**: Mode and tier from request, loaded configuration from Phase 2

**Reference**: See [gate-thresholds.md](../docs/gate-thresholds.md) for complete threshold definitions.

**Gate Configuration by Tier**:

| Gate | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|------|--------|--------|--------|--------|
| Sharpe min | >= 0.20 | >= 0.30 | >= 0.50 | >= 0.35 (DSR) |
| Max DD | <= 50% | <= 35% | <= 30% | <= 25% |
| Trade count | >= 20 | >= 50 | >= 100 | >= 150 |
| Win rate | - | >= 35% | >= 40% | >= 42% |
| Regime CV | - | < 0.5 | < 0.4 | < 0.7 |
| OOS/IS ratio | - | - | - | >= 0.5 |

**Regime-Adjusted Thresholds**:
Apply multipliers based on detected regime (from regime-classifier):

| Regime | Sharpe Mult | DD Mult | Trades Mult |
|--------|-------------|---------|-------------|
| HIGH_RISK | x 0.67 | x 1.40 | x 0.60 |
| ELEVATED | x 0.83 | x 1.20 | x 0.80 |
| NORMAL | x 1.00 | x 1.00 | x 1.00 |
| LOW_RISK | x 1.17 | x 0.80 | x 1.00 |

**Output**: Configured gate thresholds for ACT phase

---

### Step 3.4: Prepare Execution Plan

**Input**: Mode, timeout, gate configuration

**Process**:
1. Define execution steps for selected mode
2. Map mode-specific validation gates
3. Configure failure routing (failure-analyzer skill)
4. Set checkpoint intervals for long-running modes

**Execution Plan Structure**:
```json
{
  "mode": "tier_test",
  "timeout_ms": 600000,
  "gates": { ... },
  "steps": ["load_periods", "execute_backtests", "aggregate", "validate"],
  "checkpoint_interval": "per_period",
  "failure_routing": "failure-analyzer"
}
```

**Output**: Structured execution plan

---

## Exit Criteria

**All criteria must pass to proceed to ACT**:

| Criterion | Check | On Failure |
|-----------|-------|------------|
| Mode detected | Valid mode selected | Default to single_run |
| Timeout configured | Positive timeout value | Use mode default |
| Gates configured | All required gates set | Load from tier-config |
| Plan structured | Execution steps defined | FAILURE |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Hardcoding thresholds | Reference gate-thresholds.md |
| Ignoring regime adjustment | Apply multipliers from table |
| Wrong timeout for mode | Match timeout to mode complexity |
| Missing DSR for Tier 4 | Tier 4 uses Deflated Sharpe, not raw |

---

**Previous Phase**: [Phase 2: ORIENT](phase-2-orient.md)
**Next Phase**: [Phase 4: ACT](phase-4-act.md)
