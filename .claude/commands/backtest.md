---
argument-hint: '<algorithm> <tier> [--local] [--strategy-type TYPE] [--dry-run] [--resume] [--skip-git] [--verbose] [--dashboard] [--history N] [--export FORMAT]'
description: 'Progressive tier-based backtesting with HDD compliance. Orchestrates LEAN CLI execution across 4 tiers with anti-overfit gates and hypothesis validation.'
allowed-tools: [Task, Bash, Read, Write, Glob, Grep, TodoRead, TodoWrite]
model: opus
---

# Backtest Command

*Progressive tier-based backtesting orchestrator with HDD (Hypothesis-Driven Development) compliance*

---

## Core Behavior

YOU ARE A BACKTEST ORCHESTRATOR.

---

## Philosophy: Why These Gates Exist

> "Markets are computationally irreducible. We cannot predict outcomes, 
> only build reactive systems that survive regime changes." - Varma

### Core Principles

1. **Process Over Outcome**: A strategy that loses money following good process 
   is better than one that makes money through luck
2. **Deflated Sharpe**: Multiple trials inflate apparent performance. DSR penalizes 
   trial count to reveal true edge
3. **Regime Awareness**: Single-regime success means nothing. Test across volatility, 
   correlation, and trend regimes
4. **Single Hypothesis Rule**: One change per trial prevents confounding variables

### How to Start
Parse $ARGUMENTS -> Validate hypothesis -> Pre-flight checks -> Execute periods -> Aggregate -> Gate validation -> Verdict & routing

### The Flow
```
/backtest <algorithm> <tier> [options] -> Hypothesis Check -> Pre-Flight -> Period Loop -> Aggregate -> Gate -> Verdict -> Persist
```

### Anti-Patterns (NEVER DO)
- Run backtests without hypothesis validation
- Modify algorithm parameters during Tier 4
- Skip checkpoint saves (interruption loses progress)
- Proceed after HARD gate failure
- Report Sharpe without deflation at Tier 4

### Good Patterns (ALWAYS DO)
- Validate hypothesis state before ANY backtest
- Save checkpoint after EACH period completion
- Display progress: `[N/total] Testing: {period_name}... OK/FAIL`
- Apply deflated Sharpe ratio (DSR) at Tier 4
- Route failures to failure-analyzer skill

### Process Over Outcome Examples

Understanding the distinction between process quality and outcome is critical for HDD compliance.

**Example 1: GOOD Process, BAD Outcome** ✓ (Acceptable)

```
Scenario: Strategy follows all HDD rules, loses 5% in HIGH_RISK regime

Metrics:
- Raw Sharpe: 0.22
- DSR: 0.17 (below 0.30 threshold)
- Trial: 3 of 5
- Regime: HIGH_RISK (4/5 factors RED)
- Parameter changes: Single variable (stop_loss: 0.02 → 0.025)

Classification: BAD_LUCK
Evidence:
- Performance within 1 sigma of HIGH_RISK historical mean (-0.8 sigma)
- Monte Carlo p-value: 0.15 (not statistically anomalous)
- Single-variable change verified

Action: Document in trial audit, proceed to trial 4
Why acceptable: Process was followed correctly; outcome reflects market conditions
```

**Example 2: BAD Process, GOOD Outcome** ✗ (Reject)

```
Scenario: Strategy makes 15% return but violated HDD rules

Metrics:
- Raw Sharpe: 0.85
- DSR: 0.66 (above threshold)
- Trial: 2 of 5

Process Violations:
- Multiple parameters changed simultaneously (3 variables modified)
- No rationale documented for changes
- Skipped Tier 2 validation

Action: REJECT regardless of returns
Why rejected: Good outcome doesn't validate bad process
             Cannot attribute success to any specific change
             Reproducibility compromised

Next step: Revert to trial 1 parameters, restart with proper process
```

**Example 3: Indeterminate Case** ⚠️ (Human Review)

```
Scenario: Marginal failure with mixed signals

Metrics:
- Raw Sharpe: 0.38
- DSR: 0.29 (just below 0.30 threshold)
- Trial: 4 of 5
- Regime: ELEVATED (2/5 factors RED)

Classification: UNDETERMINED
Evidence:
- Performance at -1.2 sigma (between 1-2 sigma boundary)
- Monte Carlo p-value: 0.07 (between 0.05-0.10)
- Process followed correctly

Action: Flag for human review
Questions to resolve:
- Is the threshold appropriate for this strategy type?
- Should we use remaining trial budget?
- Is the regime classification accurate?
```

---

## Delegation Model

**Agents**: `strategy-builder` (pre-flight), `backtester` (execution/aggregation/gates), `git-github` (commit)

**Skills**: `hypothesis-tracking` (state management, trial tracking), `failure-analyzer` (failure classification)

---

## Modes

| Flag | Mode | Action |
|------|------|--------|
| (none) | Cloud (DEFAULT) | Execute via QuantConnect Cloud |
| `--local` | Local | Execute via local LEAN CLI |
| `--resume` | Resume | Load checkpoint, continue from last period |
| `--dry-run` | Validate | Pre-flight checks only, no LEAN CLI execution |
| `--skip-git` | No commit | Skip auto-commit of results |
| `--verbose` | Debug | Show LEAN CLI output |
| `--dashboard` | Dashboard | Generate 6-dimension metrics dashboard after aggregation |
| `--history N` | Historical | Compare against last N cloud runs (requires QC credentials) |
| `--export FORMAT` | Export | Export results as json, csv, or markdown |
| `--skip-memory-check` | Skip memory | Skip Phase 2.5 memory advisory |

### Flag Compatibility

| --dashboard | --history | --local | Valid? | Notes |
|-------------|-----------|---------|--------|-------|
| YES | NO | ANY | ✓ | Dashboard generation only |
| NO | YES | NO | ✓ | Historical comparison (cloud required) |
| ANY | YES | YES | ✗ | INVALID: --history requires cloud execution |
| YES | YES | NO | ✓ | Full dashboard with historical comparison |
| ANY | ANY | --dry-run | ✓ | Pre-flight only, no execution |

**Tier Argument**: `1` (2 periods), `2` (6 periods), `3` (15 periods), `4` (10 periods, locked params)

---

## Workflow Phases

For detailed phase documentation, see [workflow-phases.md](./../docs/command-docs/backtest/docs/workflow-phases.md).

| Phase | Name | Agent/Skill | Key Action |
|-------|------|-------------|------------|
| 0 | Argument Parsing | - | Parse args, load config |
| 1 | Hypothesis Validation | hypothesis-tracking | Validate state, trial count |
| 1.5 | Project Setup | strategy-builder | Cloud project sync (cloud mode only) |
| 2 | Pre-Flight Checks | strategy-builder | Spec validation, LEAN check |
| 2.5 | Memory Advisory | qc-memory-profiling skill | Memory estimation, node recommendation |
| 3 | Period Execution | backtester | Execute each period |
| 4 | Aggregation | backtester | Calculate metrics, DSR |
| 4.5 | Dashboard Generation | backtester | Render metrics dashboard (--dashboard) |
| 5 | Gate Validation | backtester | Apply tier thresholds |
| 5.5b | Human Review (conditional) | AskUserQuestion | G_REVIEW for UNDETERMINED |
| 6 | Verdict & Routing | failure-analyzer | PASS/FAIL routing |
| 7 | Persistence | git-github | Save results, commit |

### Phase 5.5b: G_REVIEW - Human Review Gate

**Trigger Conditions** (ANY of):
- `failure_classification.type == "UNDETERMINED"`
- `failure_classification.confidence < 0.70`
- Evidence includes mixed signals (p-value 0.01-0.05, sigma -1 to -2)

**Checkpoint Format**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
G_REVIEW: HUMAN DECISION REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Algorithm: {algorithm}
Trial: {trial_number} of 5
Classification: UNDETERMINED (confidence: {confidence})

Evidence:
- Monte Carlo p-value: {pvalue} (0.01-0.05 range)
- Sigma from mean: {sigma} (1-2 sigma boundary)
- Process followed correctly: YES

Questions:
{human_questions from failure-analyzer}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[A] APPROVE - Treat as BAD_LUCK, proceed to next trial
[R] REJECT - Treat as BAD_PROCESS, reformulate hypothesis
[Q] QUERY - Show detailed evidence
[S] SAVE - Pause workflow, resume later with --resume
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Decision Processing**:
| Decision | Action | Trial Count | Next Step |
|----------|--------|-------------|-----------|
| [A] APPROVE | verdict = PASS (caveat) | +1 | Continue |
| [R] REJECT | verdict = FAIL | +1 | Reformulate |
| [Q] QUERY | Display evidence | unchanged | Re-prompt |
| [S] SAVE | Checkpoint | unchanged | Pause |

### Phase 2.5: Memory Advisory (Optional)

**Trigger**: After Phase 2 passes, before Phase 3 execution
**Blocking**: NO (advisory only - warnings don't halt execution)
**Timeout**: 30s
**Skip flag**: `--skip-memory-check`

**Invocation**:
```
Skill(qc-memory-profiling, "algorithm: {algo}, tier: {tier}")
```

**Output Format**:
```
Memory Check: {algorithm}
━━━━━━━━━━━━━━━━━━━━━━━━
Estimated: {X} GB | Node: {current} ({Y} GB)
Status: {OK|WARN_MEDIUM|WARN_HIGH|WARN_CRITICAL}
{Recommendations if any}
━━━━━━━━━━━━━━━━━━━━━━━━
```

**Status Actions**:
| Status | Action |
|--------|--------|
| PROCEED | Continue to Phase 3 |
| WARN_MEDIUM | Log warning, continue |
| WARN_HIGH | Log warning, suggest node upgrade, continue |
| WARN_CRITICAL | Log critical warning, recommend optimization before proceeding |

---

## Agent Delegation

| Phase | Agent/Skill | Timeout |
|-------|-------------|---------|
| 1 | hypothesis-tracking | 30s |
| 1.5 | strategy-builder (MODE: project_setup) | 60s |
| 2 | strategy-builder (MODE: validate) | 60s |
| 2.5 | Skill(qc-memory-profiling) | 30s |
| 3 | backtester (MODE: tier_test) | 10min/period |
| 4 | backtester (MODE: aggregate) | 60s |
| 4.5 | backtester (MODE: dashboard) | 120s |
| 5 | backtester (MODE: validate) | 60s |
| 5.5b | AskUserQuestion (built-in) | No timeout (human) |
| 6 | Skill(failure-analyzer) | 60s | On timeout: rule-based fallback |
| 7 | git-github | 30s |

### Task Invocation Examples

```
Task(strategy-builder, prompt="MODE: validate\nAlgorithm: {algo}\nTier: 2\nCheck: param_count < 10, spec valid", timeout_ms=60000)

# Cloud execution (default)
Task(backtester, prompt="MODE: tier_test\nExecution: cloud\nAlgorithm: {algo}\nPeriod: post_gfc_bull\nStart: 2009-03-09\nEnd: 2020-02-19\nCommands:\n  lean cloud push --project Algorithms/{algo}\n  lean cloud backtest Algorithms/{algo}", timeout_ms=600000)

# Local execution (--local flag)
Task(backtester, prompt="MODE: tier_test\nExecution: local\nAlgorithm: {algo}\nPeriod: post_gfc_bull\nStart: 2009-03-09\nEnd: 2020-02-19\nCommand: lean backtest Algorithms/{algo}", timeout_ms=600000)

Task(backtester, prompt="MODE: aggregate\nPeriod results: [{...}]\nTier: 2\nCalculate: avg_sharpe, worst_dd", timeout_ms=60000)

# Skill invocation for failure classification
Skill(failure-analyzer, "Classify failure for hypothesis {hypothesis_id}. Mode: {failure_mode}. Metrics: sharpe_raw={sharpe}, oos_ratio={oos_ratio}. Determine: ARCHIVE or NEW_HYPOTHESIS with requirements.")
```

---

## Checkpoint Management

See [checkpoint-management.md](./../docs/command-docs/backtest/docs/checkpoint-management.md).

- **Location**: `{backtest-history}/runs/{run_id}/.checkpoint.json`
- **Resume**: `--resume` flag loads checkpoint and continues
- **Cleanup**: Deleted on successful completion

---

## Gate Thresholds

See [gate-thresholds.md](./../docs/command-docs/backtest/docs/gate-thresholds.md) for tier-specific thresholds.

**Runtime Source**: `$TRENDY_TRADER_PATH/quantconnect/tier-config.json`

---

## Error Recovery

| Code | Error | Recovery |
|------|-------|----------|
| BACKTEST_ERR_001 | Algorithm not found | Check path spelling |
| BACKTEST_ERR_002 | Hypothesis missing | Run /algo-strategy first |
| BACKTEST_ERR_003 | Trial exhausted (>5) | Create new hypothesis |
| BACKTEST_ERR_004 | Param count >= 10 | Reduce parameters |
| BACKTEST_ERR_005 | Params unlocked (Tier 4) | Lock params first |
| BACKTEST_ERR_006 | LEAN timeout/error | Retry 1x, then mark FAILED |
| BACKTEST_ERR_007 | Gate failure | Route to failure-analyzer |
| BACKTEST_ERR_008 | Project not in cloud | Run `lean cloud push --project Algorithms/{algo}` |
| BACKTEST_ERR_009 | config.json missing | Create with `"algorithm-language": "Python"` |
| BACKTEST_ERR_010 | Data not available | Verify symbols exist in QC Cloud data catalog |

### Circuit Breaker Pattern

LEAN CLI failures can cascade across periods. Apply circuit breaker:

| Consecutive Failures | Action |
|---------------------|--------|
| 1 | Retry with 30s delay |
| 2 | Retry with 60s delay, warn user |
| 3 | HALT workflow, save checkpoint, alert |

**Health Check** (before retry):
```bash
lean --version  # Must succeed before retry
```

**Reset Condition**: Any successful period execution resets counter to 0.

---

## Output Format

```
Backtest: {algorithm} Tier {N}
==================================================
Hypothesis: {id} (Trial {n}/5)

[1/6] Testing: post_gfc_bull... OK Sharpe: 0.45
[2/6] Testing: gfc_bear... OK Sharpe: 0.22
...
==================================================
Gate: PASS/FAIL
Action: {next step}
Report: backtest-history/runs/{run_id}/verdict.md
```

**Generated Files**: `run-manifest.json`, `verdict.md`, `.checkpoint.json`

**Schemas**:
- Run output: `.claude/docs/command-docs/backtest/schemas/run-manifest.schema.json`
- Checkpoint: `.claude/docs/command-docs/backtest/schemas/checkpoint.schema.json`
- Dashboard: `.claude/docs/command-docs/backtest/schemas/dashboard.schema.json`

---

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `TRENDY_TRADER_PATH` | `$env:TRENDY_TRADER_PATH` | **REQUIRED** - Set in environment |
| `BACKTEST_TIMEOUT` | `600` | Per-period timeout (seconds) |

---

## Knowledge Base

### Command Documentation
- `.claude/docs/command-docs/backtest/docs/workflow-phases.md` - Detailed phases
- `.claude/docs/command-docs/backtest/docs/gate-thresholds.md` - Gate configuration
- `.claude/docs/command-docs/backtest/docs/checkpoint-management.md` - Resume/checkpoint

### External References
- `C:/Users/kemos/Repos/trendy-trader/quantconnect/QUICKSTART.md` - LEAN CLI setup, cloud commands
- `C:/Users/kemos/Repos/trendy-trader/quantconnect/README.md` - Algorithm infrastructure, signal format

### Related
- `/algo-strategy` - Create hypothesis (upstream)
- `.claude/skills/hypothesis-tracking/SKILL.md` - State management
- `.claude/skills/failure-analyzer/SKILL.md` - Failure classification
- `.claude/skills/regime-classifier/SKILL.md` - Multi-factor regime classification
- `.claude/skills/qc-memory-profiling/SKILL.md` - Memory estimation

---

## Orchestrator Integration

**Trigger Keywords**: backtest, tier test, run backtest, validate strategy

**Workflow**: `/algo-strategy -> /backtest tier 1 -> tier 2 -> tier 3 -> [lock params] -> tier 4 -> [DEPLOYABLE]`

**HDD Compliance**: Hypothesis required, params locked at Tier 4, trial limit (5), DSR at Tier 4
