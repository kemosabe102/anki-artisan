# Backtest Workflow Phases

Detailed phase-by-phase documentation for the `/backtest` command.

---

## Phase 0: Argument Parsing

```text
PHASE 0: ARGUMENT PARSING
  |-- Parse algorithm name and tier from $ARGUMENTS
  |-- Check flags: --resume, --dry-run, --skip-git, --verbose, --strategy-type
  |-- Load tier config from TRENDY_TRADER_PATH/quantconnect/tier-config.json
  |-- Load periods from TRENDY_TRADER_PATH/quantconnect/backtest-periods.json
  |-- Validate algorithm exists in Algorithms/{algorithm}/
  |-- Output: {algorithm, tier, flags, tier_config, periods}
```

---

## Phase 1: Hypothesis Validation

**Purpose**: Ensure hypothesis exists and is in valid state for testing.
**Agent/Skill**: `hypothesis-tracking` skill
**Timeout**: 30000ms (30 sec)

```text
ACTIONS:
  |-- Load hypothesis from algorithm's strategy-spec.json
  |-- Verify hypothesis_id exists
  |-- Check hypothesis state == TESTING (not ARCHIVED or DEPLOYED)
  |-- Validate trial_number:
  |     IF trial_number >= 5: HALT with exhaustion notice
  |     IF trial_number == 3: WARN "Approaching trial limit (3/5)"
  |-- Verify params_locked unchanged from previous trial
  |-- Tier 4 ONLY: Validate git hash matches tier_3_completion

OUTPUTS:
  {hypothesis_id, trial_number, params_locked}
```

---

## Phase 1.5: Project Setup (Cloud Mode)

**Purpose**: Ensure algorithm exists in QuantConnect Cloud and is properly configured.
**Agent**: `strategy-builder` agent (MODE: project_setup)
**Timeout**: 60000ms (1 min)
**When**: Cloud mode only (skip for --local)

```text
ACTIONS:
  |-- Check algorithm exists locally (Algorithms/{algorithm}/main.py)
  |-- Check config.json exists and has "algorithm-language": "Python"
  |-- Check cloud project exists via `lean cloud status`
  |-- IF not in cloud: `lean cloud push --project Algorithms/{algorithm}`

OUTPUTS:
  {project_exists_local, project_exists_cloud, config_valid, push_succeeded}
```

---

## Phase 2: Pre-Flight Checks

**Purpose**: Validate strategy specification and build environment.
**Agent**: `strategy-builder` agent (MODE: validate)
**Timeout**: 60000ms (1 min)

```text
ACTIONS:
  |-- Validate strategy spec JSON exists and schema-valid
  |-- Parameter count check: BLOCK if params >= 10
  |-- Tier 4: Verify ALL params locked (no unlocked params)
  |-- Check LEAN CLI availability: `lean --version`
  |-- Verify algorithm compiles: `lean build Algorithms/{algorithm}`
  |-- Data Availability Check (CLOUD mode only):
  |     1. Extract symbols from strategy universe
  |     2. Query QC data catalog for each symbol/date range
  |     3. IF missing: HALT with list of unavailable symbols

OUTPUTS:
  {preflight_passed, warnings[], data_verification: {symbols_checked, missing[], verified[]}}
```

---

## Phase 3: Period Execution

**Purpose**: Execute backtest for each period in the tier configuration.
**Agent**: `backtester` agent (MODE: tier_test)
**Timeout**: 600000ms (10 min) per period

```text
ACTIONS:
  FOR each period in tier_config.tiers[tier].periods:
    1. Display: "[{N}/{total}] Testing: {period_name}..."
    2. Inject dates into algorithm Initialize():
       SetStartDate({period.start_date})
       SetEndDate({period.end_date})
    3. Execute backtest:
       CLOUD (default):
         a. Push to cloud: `lean cloud push --project Algorithms/{algorithm}`
         b. Execute: `lean cloud backtest Algorithms/{algorithm}`
         c. Parse results from cloud response
       LOCAL (--local flag):
         a. Execute: `lean backtest Algorithms/{algorithm}` from TRENDY_TRADER_PATH/quantconnect/
         b. Parse results from backtests/{id}/{id}-summary.json
    4. Wait for completion (timeout 10min per period)
    5. Extract metrics: Sharpe, MaxDrawdown, TotalTrades, WinRate
    6. Record period result: {period_id, sharpe, dd, trades, win_rate, status}
    7. Display: "OK Sharpe: {sharpe}" or "FAIL {reason}"
    8. Save checkpoint to run-manifest.json (see checkpoint-management.md)
    9. Continue to next period

ERROR HANDLING:
  |-- Retry 1x on timeout or transient error
  |-- Mark period FAILED after retry failure
  |-- Continue to next period (don't abort entire run)

OUTPUTS:
  period_results[]
```

### Atomic Checkpoint Writes (FM-003)

To prevent checkpoint corruption on interruption:

```text
CHECKPOINT WRITE PATTERN:
  1. Write to: {checkpoint_path}.tmp
  2. Validate JSON structure
  3. Rename: {checkpoint_path}.tmp -> {checkpoint_path}
  
This ensures checkpoint file is always complete or absent.
```

---

## Phase 4: Aggregation

**Purpose**: Calculate aggregate metrics across all periods.
**Agent**: `backtester` agent (MODE: aggregate)
**Timeout**: 60000ms (1 min)

```text
ACTIONS:
  |-- Calculate aggregate metrics:
  |     avg_sharpe = mean(period_sharpes)
  |     worst_dd = min(period_drawdowns)  # Most negative
  |     total_trades = sum(period_trades)
  |     avg_win_rate = mean(period_win_rates)
  |-- Calculate regime CV (Tier 2+):
  |     regime_cv = stdev(sharpe_by_regime) / mean(sharpe_by_regime)
  |-- Tier 4 ONLY: Apply deflated Sharpe ratio
  |     See gate-thresholds.md for DSR formula

OUTPUTS:
  {avg_sharpe, dsr, worst_dd, total_trades, avg_win_rate, regime_cv}
```

---

## Phase 4.5: Dashboard Generation (Optional)

**Purpose**: Generate performance dashboard with historical comparison.
**Agent**: `backtester` agent (MODE: dashboard)
**Timeout**: 120000ms (2 min)
**When**: `--dashboard` flag present

```text
ACTIONS:
  |-- Check --dashboard flag presence
  |-- Calculate 35 metrics from period_results:
  |     - 6 core dimensions: Returns, Risk, Efficiency, Consistency, Capacity, Regime
  |     - 5-6 metrics per dimension
  |-- IF --history N:
  |     |-- Fetch QC Cloud history via fetch_backtest_logs.py pattern
  |     |-- Retrieve last N runs for comparison
  |     |-- Calculate trend indicators (improving/declining/stable)
  |-- Render ASCII dashboard using performance-dashboard.md template
  |-- IF --export FORMAT:
  |     |-- Validate FORMAT in [json, csv, markdown]
  |     |-- Save to backtest-history/runs/{run_id}/dashboard.{format}

OUTPUTS:
  {dashboard_rendered, metrics_calculated, history_fetched, export_path}
```

### Flag Validation Matrix

| --dashboard | --history | --local | Valid? | Reason |
|-------------|-----------|---------|--------|--------|
| YES | NO | YES | Valid | Dashboard from local results |
| YES | NO | NO | Valid | Dashboard from cloud results |
| YES | YES | NO | Valid | Dashboard with cloud history comparison |
| NO | YES | NO | Valid | History comparison without dashboard |
| ANY | YES | YES | **INVALID** | --history requires cloud (QC API access) |
| NO | NO | ANY | Valid | Standard execution, no dashboard |

**Invalid Combination Handling**:
```text
IF --history AND --local:
  HALT with error: "INVALID: --history requires cloud execution. Remove --local or --history."
```

---

## Phase 5: Gate Validation

**Purpose**: Apply tier-specific gates to determine pass/fail.
**Agent**: `backtester` agent (MODE: validate)
**Timeout**: 60000ms (1 min)

```text
ACTIONS:
  |-- Load tier-specific gates from tier-config.json
  |-- Apply gates in order (first failure = HALT):
  |     1. trade_count >= tier.gates.trade_count_minimum
  |     2. sharpe >= tier.gates.sharpe_minimum (DSR for Tier 4)
  |     3. drawdown >= tier.gates.max_drawdown (less negative)
  |     4. win_rate >= tier.gates.win_rate_minimum (Tier 2+)
  |     5. regime_cv < tier.gates.regime_consistency.threshold (Tier 2+)
  |     6. oos_is_ratio >= tier.gates.oos_is_ratio.threshold (Tier 4)
  |-- All gates are HARD: First failure = FAIL verdict

OUTPUTS:
  {gate_passed, failed_gate, gate_results[]}
```

**Gate Thresholds**: See `gate-thresholds.md` for tier-specific values.

---

## Phase 5.5: Skepticism Gates (Tier 3+)

**Purpose**: Apply skepticism-first validation to filter noise from signal.
**Agent**: `backtester` agent
**Timeout**: 120000ms (2 min)
**When**: After standard gate validation, before deployment approval

### Overview

Skepticism gates enforce the philosophy that patterns contain more noise than signal. These additional validations ensure statistical significance and scalability before deployment.

### Gate Sequence

```text
STANDARD GATES (Phases 1-5):
  |-- trade_count >= minimum
  |-- sharpe >= threshold (DSR at Tier 4)
  |-- drawdown <= maximum
  |-- win_rate >= minimum
  |-- regime_cv < threshold
  |-- oos_is_ratio >= threshold (Tier 4)

SKEPTICISM GATES (Phase 5.5):
  |
  |-- [Tier 3+] Capacity Scaling Test
  |     |-- Run capacity_test mode
  |     |-- Calculate capacity_score
  |     |-- IF score < 70%: WARN (Tier 3) or FAIL (Tier 4)
  |
  |-- [Tier 4] Monte Carlo Validation
  |     |-- Run monte_carlo mode
  |     |-- Validate p-value < 0.05
  |     |-- IF missing or p >= 0.05: FAIL
  |
  +-- RETURN: {skepticism_gates_passed, monte_carlo_passed, capacity_passed}
```

### Tier-Specific Requirements

| Tier | Monte Carlo | Capacity Test | Failure Mode |
|------|-------------|---------------|--------------|
| 1-2 | Not required | Not required | N/A |
| 3 | Optional | >= 70% (SOFT) | Warning only |
| 4 | p < 0.05 (HARD) | >= 75% (HARD) | Fail validation |

### Execution Example

```
Task(backtester, prompt="Run skepticism gates for Tier 4 validation
  hypothesis_id: H001
  tier: 4
  
  Execute:
  1. capacity_test mode with scale_factors [2, 5, 10]
  2. monte_carlo mode with 1000 simulations
  
  Return gate results for final verdict.")
```

### Output Schema

```json
{
  "skepticism_gates": {
    "tier": 4,
    "capacity_test": {
      "passed": true,
      "score": 78.5,
      "threshold": 75
    },
    "monte_carlo": {
      "passed": true,
      "p_value": 0.023,
      "threshold": 0.05,
      "percentile": 97.7
    },
    "all_passed": true,
    "verdict": "PASS"
  }
}
```

### Failure Handling

| Failure | Tier 3 Action | Tier 4 Action |
|---------|---------------|---------------|
| Capacity < threshold | WARN, continue | FAIL, halt |
| Monte Carlo missing | N/A | FAIL, halt |
| Monte Carlo p >= 0.05 | N/A | FAIL, halt |

### Integration Notes

- Skepticism gates run AFTER standard gates pass
- Both capacity AND monte_carlo must pass at Tier 4
- Results feed into final DEPLOYABLE verdict
- Failures at Tier 4 require hypothesis revision or retirement

---

## Phase 5.5b: G_REVIEW - Human Review Gate

**Purpose**: Pause workflow for human decision when failure classification is UNDETERMINED.
**Agent**: AskUserQuestion (built-in)
**Timeout**: None (human decision)
**When**: After failure-analyzer returns UNDETERMINED classification with confidence < 0.70

```text
TRIGGER CONDITIONS (ANY of):
  |-- failure_classification.type == "UNDETERMINED"
  |-- failure_classification.confidence < 0.70
  |-- Evidence includes mixed signals:
  |     - Monte Carlo p-value: 0.01-0.05 (indeterminate range)
  |     - Sigma from mean: -1.0 to -2.0 (boundary zone)
  |     - Process followed correctly

ACTIONS:
  |-- Compile evidence package:
  |     - raw_sharpe, dsr, trial_number
  |     - regime_context, monte_carlo_pvalue
  |     - sigma_from_mean
  |     - parameter_changes_from_previous
  |     - Questions flagged by failure-analyzer
  |
  |-- Present human checkpoint:
  |
  |     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  |     G_REVIEW: HUMAN DECISION REQUIRED
  |     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  |
  |     Algorithm: {algorithm}
  |     Trial: {trial_number} of 5
  |     Classification: UNDETERMINED (confidence: {confidence})
  |
  |     Evidence:
  |     - Monte Carlo p-value: {pvalue}
  |     - Sigma from mean: {sigma}
  |     - Process followed correctly: YES
  |
  |     Questions:
  |     {human_questions from failure-analyzer}
  |
  |     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  |     [A] APPROVE - Treat as BAD_LUCK, proceed to next trial
  |     [R] REJECT - Treat as BAD_PROCESS, reformulate hypothesis
  |     [Q] QUERY - Show detailed evidence
  |     [S] SAVE - Pause workflow, resume later with --resume
  |     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  |
  |-- Process human decision:
  |     [A] → verdict = PASS (caveat), trial_number += 1, continue
  |     [R] → verdict = FAIL, trial_number += 1, route to reformulation
  |     [Q] → display detailed evidence, re-prompt
  |     [S] → save checkpoint, pause workflow

OUTPUTS:
  {human_decision, human_verdict, fate_override, checkpoint_saved}
```

**Decision Matrix**:

| Decision | Action | Trial Count | Next Step | Checkpoint |
|----------|--------|-------------|-----------|------------|
| [A] APPROVE | verdict = PASS (caveat) | +1 | Continue to next trial | No |
| [R] REJECT | verdict = FAIL | +1 | Route to reformulation | No |
| [Q] QUERY | Display evidence | unchanged | Re-prompt | No |
| [S] SAVE | Pause workflow | unchanged | Resume with --resume | Yes |

**Integration with Phase 6**:
- If G_REVIEW triggered and human provides verdict → Phase 6 uses `human_verdict`
- If G_REVIEW not triggered (clear PASS/FAIL) → Phase 6 uses normal `verdict`

---

## Phase 6: Verdict & Routing

**Purpose**: Determine final verdict and route failures for analysis.

```text
ACTIONS:
  IF all gates PASS:
    verdict = "PASS"
    IF tier < 4: suggest = "Proceed to Tier {tier+1}"
    IF tier == 4: suggest = "DEPLOYABLE - Ready for paper trading"
    Update hypothesis state via hypothesis-tracking skill

  IF any gate FAIL:
    verdict = "FAIL"
    Route to failure-analyzer skill:
      Task(failure-analyzer, "Classify: {failed_gate} with {metrics}")
    Receive: failure_mode, root_cause, remediation[]
    suggest = remediation[0]
    Update hypothesis state via hypothesis-tracking skill

  Increment trial_number via hypothesis-tracking skill

OUTPUTS:
  {verdict, suggest, failure_analysis}
```

---

## Phase 7: Persistence & Reporting

**Purpose**: Save results and generate reports.

```text
ACTIONS:
  |-- Create run directory: backtest-history/runs/{date}_{seq}/
  |-- Save run-manifest.json:
  |     {
  |       "run_id": "{date}_{seq}",
  |       "algorithm": "{algorithm}",
  |       "tier": {tier},
  |       "hypothesis_id": "{hypothesis_id}",
  |       "trial_number": {trial_number},
  |       "started_at": "{timestamp}",
  |       "completed_at": "{timestamp}",
  |       "verdict": "{verdict}",
  |       "metrics": {aggregated_metrics},
  |       "period_results": [{period_results}],
  |       "gate_results": [{gate_results}],
  |       "trial_audit": {
  |         "parameter_hash": "sha256:abc123def456...",
  |         "parameter_changes_from_previous": [
  |           "stop_loss: 0.02 -> 0.025",
  |           "position_size: 0.10 -> 0.08"
  |         ],
  |         "regime_at_test_time": "HIGH_RISK",
  |         "luck_vs_process": {
  |           "classification": "BAD_LUCK",
  |           "confidence": 0.78,
  |           "evidence": [
  |             "Monte Carlo p-value: 0.12 (> 0.05 threshold)",
  |             "Performance within 1 sigma of HIGH_RISK regime mean",
  |             "No parameter anomalies detected"
  |           ],
  |           "monte_carlo_pvalue": 0.12,
  |           "sigma_from_mean": 0.8
  |         }
  |       }
  |     }
  |-- Generate verdict.md (human-readable report)
  |-- Update backtest-history/README.md with heatmap row
  |-- Delete checkpoint (run complete)
  |-- UNLESS --skip-git:
  |     Task(git-github, "commit: chore(backtest): {algorithm} Tier {tier} - {verdict}")

DISPLAY:
  "Gate: {verdict}"
  "Action: {suggest}"
  "Report: backtest-history/runs/{run_id}/verdict.md"
```

**Trial Audit Fields** (new in Varma compliance update):
- `parameter_hash`: SHA256 hash of all parameters for reproducibility verification
- `parameter_changes_from_previous`: Human-readable list of what changed
- `regime_at_test_time`: Market regime during the test period
- `luck_vs_process`: Classification distinguishing bad luck from bad process
  - BAD_LUCK: Performance within normal variance, may retry
  - BAD_PROCESS: Systematic issues, requires hypothesis revision
  - UNDETERMINED: Mixed signals, needs human review

---

## Phase Summary Table

| Phase | Name | Agent/Skill | Timeout | Key Output |
|-------|------|-------------|---------|------------|
| 0 | Argument Parsing | - | - | {algorithm, tier, flags} |
| 1 | Hypothesis Validation | hypothesis-tracking | 30s | {hypothesis_id, trial_number} |
| 1.5 | Project Setup | strategy-builder | 60s | {project_exists_cloud, push_succeeded} |
| 2 | Pre-Flight Checks | strategy-builder | 60s | {preflight_passed, data_verification} |
| 3 | Period Execution | backtester | 10min/period | period_results[] |
| 4 | Aggregation | backtester | 60s | {avg_sharpe, dsr, regime_cv} |
| 4.5 | Dashboard Generation | backtester | 120s | {dashboard_rendered, metrics_calculated} |
| 5 | Gate Validation | backtester | 60s | {gate_passed, failed_gate} |
| 5.5 | Skepticism Gates | backtester | 120s | {skepticism_gates_passed} |
| 6 | Verdict & Routing | failure-analyzer | 60s | {verdict, suggest} |
| 7 | Persistence | git-github | 30s | run-manifest.json |
