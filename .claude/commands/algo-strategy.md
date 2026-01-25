---
argument-hint: '<strategy description> | --from-doc <doc-path> [--spec-only] [--skeleton-only] [--hypothesis-only] [--full|--classic]'
description: 'Generate trading strategies using Hypothesis-Driven Development. Supports 6-phase (--classic, DEFAULT) or 17-phase (--full) workflow with Definition, Strategy, Validation, and Execution Layers.'
allowed-tools: Task, Read, Glob, Grep, TodoWrite
model: opus
---

# Algo-Strategy Command

*Hypothesis-Driven Development orchestrator for trading strategies*

---

## Your Role

You are an **HDD Orchestrator**. Your job is to:
1. Parse strategy ideas (freeform or from docs)
2. Formulate testable hypotheses with locked parameters
3. Enforce anti-overfitting constraints BEFORE delegation
4. Delegate to strategy-builder with validated hypothesis bundles
5. Validate consistency between hypothesis and generated spec

---

## Pre-Flight Validation

**Before Phase 1, validate all required agents and references are available.**

### Required Agents (8 total)

| Agent | Path | Required For | Error Code |
|-------|------|--------------|------------|
| strategy-builder | `.claude/agents/investing/strategy-builder/strategy-builder.md` | P4/P13 (Delegation) | ALGO_ERR_050 |
| market-data-specialist | `.claude/agents/investing/market-data-specialist/market-data-specialist.md` | P3/P12 (Data Check) | ALGO_ERR_051 |
| risk-management-specialist | `.claude/agents/investing/risk-management-specialist/risk-management-specialist.md` | P6/P8 (Position/Risk) | ALGO_ERR_052 |
| universe-selector | `.claude/agents/investing/universe-selector/universe-selector.md` | P3 (Universe Selection, --full only) | ALGO_ERR_053 |
| execution-modeler | `.claude/agents/investing/execution-modeler/execution-modeler.md` | P7 (Execution Model, --full only) | ALGO_ERR_054 |
| backtester | `.claude/agents/investing/backtester/backtester.md` | P9 (Backtest Metrics, --full only) | ALGO_ERR_055 |
| sensitivity-tester | `.claude/agents/investing/sensitivity-tester/sensitivity-tester.md` | P10 (Sensitivity, --full only) | ALGO_ERR_056 |
| crisis-stress-tester | `.claude/agents/investing/crisis-stress-tester/crisis-stress-tester.md` | P11 (Stress Testing, --full only) | ALGO_ERR_057 |

### Pre-Flight Check (PHASE 0)

```text
PHASE 0: PRE-FLIGHT VALIDATION [BLOCKING]
|
+-- Flag Parsing (already added above)
|
+-- Agent Availability Check:
|     FOR agent IN required_agents:
|       path = .claude/agents/investing/{agent}/{agent}.md
|       IF NOT Glob(path) returns result:
|         IF --full mode OR agent in [strategy-builder, market-data-specialist, risk-management-specialist]:
|           RETURN ERROR: ALGO_ERR_05X "{agent} not found"
|         ELSE:
|           WARN: "Agent {agent} not available, --full mode disabled"
|
+-- Output: {agents_available: true, full_mode_available: true, warnings: []}
```

### Agent Not Found Error Format

```
ERROR: ALGO_ERR_053
Phase: P0 - PRE-FLIGHT
Description: Required agent "universe-selector" not found

Details:
Expected path: .claude/agents/investing/universe-selector/universe-selector.md
Agent is required for: P3 (Universe Selection) in --full mode

Recovery:
1. Verify agent exists at the expected path
2. If missing, create using: Task(agent-architect, "Create universe-selector agent")
3. Restart Claude Code session after agent creation
4. Alternatively, use --classic mode to skip Definition Layer

Note: Classic mode requires only strategy-builder, market-data-specialist, 
and risk-management-specialist agents.
```

---

## Modes

### Workflow Depth Flags

| Flag | Workflow | Description |
|------|----------|-------------|
| `--classic` | 6-phase (P1-P6) | Original workflow. DEFAULT when no flag specified. |
| `--full` | 17-phase (P1-P17) | Complete workflow with Definition, Strategy, Validation, and Execution Layers. |

### Flag Compatibility Matrix

| --classic | --full | --spec-only | --skeleton-only | --hypothesis-only | Valid? | Notes |
|-----------|--------|-------------|-----------------|-------------------|--------|-------|
| YES | NO | NO | NO | NO | ✓ | 6-phase workflow (DEFAULT) |
| NO | YES | NO | NO | NO | ✓ | 17-phase workflow |
| YES | YES | ANY | ANY | ANY | ✗ | INVALID: mutually exclusive |
| NO | NO | YES | NO | NO | ✓ | Spec output only |
| NO | NO | NO | YES | NO | ✓ | Skeleton output only |
| NO | NO | NO | NO | YES | ✓ | Hypothesis only |
| NO | YES | YES | NO | NO | ✓ | Full workflow, spec output |
| YES | NO | YES | NO | NO | ✓ | Classic workflow, spec output |
| ANY | ANY | YES | YES | ANY | ✗ | INVALID: spec-only + skeleton-only |

### Flag Conflict Validation (PHASE 0)

```text
PHASE 0: FLAG PARSING [BLOCKING]
  |-- Parse $ARGUMENTS for flags
  |-- Conflict detection:
  |     IF --classic AND --full:
  |       RETURN ERROR: ALGO_ERR_060 "Mutually exclusive workflow flags"
  |     IF --spec-only AND --skeleton-only:
  |       RETURN ERROR: ALGO_ERR_061 "Cannot use both output modes"
  |-- Default: --classic if no workflow flag specified
  |-- Output: {mode: <detected_mode>, workflow: classic|full}
```

### Flag Conflict Error Messages

**ALGO_ERR_060: Mutually Exclusive Workflow Flags**
```
ERROR: ALGO_ERR_060
Phase: P0 - FLAG PARSING
Description: Mutually exclusive workflow flags detected

Flags provided:
  --classic (6-phase workflow)
  --full (17-phase workflow)

These flags cannot be used together. Choose ONE workflow depth:

  /algo-strategy "description" --classic
    Uses 6-phase workflow (P1-P6): Parse -> Hypothesis -> Data -> Delegate -> Validate -> Present
  
  /algo-strategy "description" --full
    Uses 17-phase workflow (P1-P17): Adds Definition, Strategy, Validation, and Execution layers

Default (no flag): --classic
```

**ALGO_ERR_061: Conflicting Output Modes**
```
ERROR: ALGO_ERR_061
Phase: P0 - FLAG PARSING
Description: Conflicting output mode flags detected

Flags provided:
  --spec-only (JSON specification only)
  --skeleton-only (QC Python skeleton only)

These flags cannot be used together. Choose ONE output mode:

  /algo-strategy "description" --spec-only      # Outputs JSON spec only
  /algo-strategy "description" --skeleton-only  # Outputs Python skeleton only
  /algo-strategy "description"                  # Outputs both (default)
```

### Mode Flags

| User Says | Mode | Action |
|-----------|------|--------|
| `/algo-strategy "description"` | freeform | NL idea -> hypothesis -> spec + skeleton |
| `/algo-strategy --from-doc <path>` | doc_first | Extract strategy from existing docs |
| `/algo-strategy "desc" --spec-only` | spec_only | Generate JSON spec only |
| `/algo-strategy "desc" --skeleton-only` | skeleton_only | Generate QC Python only |
| `/algo-strategy "desc" --hypothesis-only` | hypothesis_only | Generate hypothesis bundle only |
| `/algo-strategy "desc" --full` | full_workflow | Use 17-phase workflow with all layers |

---

## Workflow Overview

### Workflow Selection

```text
--classic (DEFAULT): P1 -> P2 -> P3 -> P4 -> P5 -> P6
--full:              P1 -> P2 -> P3 -> P4 -> P5 -> P6 -> P7 -> P8 -> P9 -> P10 -> P11 -> P12 -> P13 -> P14 -> P15 -> P16 -> P17
                     └─ Definition ─┘  └─ Strategy ─────────┘  └─ Validation ───────┘  └─ Execution ────────────────────────┘
                                           P6: Position Sizing   P9: Backtest Metrics
                                           P7: Execution Model   P10: Parameter Sensitivity
                                           P8: Risk Management   P11: Stress Testing
```

### Full Workflow (17 Phases with Gates)

```text
/algo-strategy <input> [--from-doc] [--spec-only] [--skeleton-only] [--hypothesis-only] [--full]
|
+=== DEFINITION LAYER (--full mode only) ===
|
+-- P1: INVESTMENT_UNIVERSE
|   +-- Parse symbols and asset classes
|   +-- Identify universe scope (single, basket, index)
|   +-- [GATE: UNIVERSE_DEFINED] Universe validated
|
+-- P2: BACKTEST_CONSTRAINTS
|   +-- Parse date range (start_date, end_date)
|   +-- Parse frequency (1min, 1hour, daily)
|   +-- Validate lookback requirements (warmup periods)
|   +-- [GATE: CONSTRAINTS_VALID] All temporal constraints set
|
+-- P3: UNIVERSE_SELECTION
|   +-- Delegate to universe-selector agent
|   +-- Check survivor bias (delisted symbols)
|   +-- Validate liquidity thresholds
|   +-- Sector/industry coverage check
|   +-- [GATE: SURVIVOR_BIAS_CHECK] Universe quality validated
|
+=== CLASSIC WORKFLOW (both modes) ===
|
+-- P4: PARSE (was P1 in classic)
|   +-- Detect mode (freeform | doc_first | spec_only | skeleton_only | hypothesis_only)
|   +-- Parse arguments or read document
|   +-- [GATE: INPUT] 7 elements OR clarifying questions
|
+-- P5: HYPOTHESIS (was P2 in classic, HDD Core + ANTI-OVERFIT)
|   +-- Formulate: Cause -> Effect -> When -> Why
|   +-- Lock parameters before testing
|   +-- [GATE 5a: PARAM_COUNT] Count params, BLOCK if >=10
|   +-- [GATE 5b: PARAM_RANGES] Check for excessive spans (>3x), BLOCK if found
|   +-- [GATE 5c: HYPOTHESIS] Schema valid, params locked, testability >=0.7
|   +-- [GATE 5d: HANDOFF_VALID] Hypothesis bundle complete for P6 delegation (--full mode only)
|
+=== STRATEGY LAYER (--full mode only) ===
|
+-- P6: POSITION_SIZING (--full mode only)
|   +-- Determine sizing method (fixed, volatility_scaled, kelly, regime_adjusted)
|   +-- Configure regime adjustments (volatility, trend, correlation)
|   +-- Delegate to risk-management-specialist
|   +-- Validate against portfolio constraints
|   +-- [GATE 6a: SIZING_METHOD_VALID] Method from allowed list
|   +-- [GATE 6b: REGIME_ADJUSTMENT_CONFIGURED] Regime factors specified if enabled
|
+-- P7: EXECUTION_MODEL (--full mode only)
|   +-- Model execution costs via execution-modeler
|   +-- Validate slippage < 50 bps
|   +-- Validate market impact < 20 bps for liquid universe
|   +-- Run +50% slippage stress scenario
|   +-- [GATE: SLIPPAGE_SENSITIVITY_PASS] Sharpe after costs > 0.5 AND stress viable
|
+-- P8: RISK_MANAGEMENT (--full mode only)
|   +-- Classify current regime (5-factor model)
|   +-- Configure circuit breakers (daily loss, max drawdown, concentration)
|   +-- Apply 200DMA risk asymmetry
|   +-- [GATE: REGIME_CLASSIFICATION_COMPLETE] All 5 factors classified
|   +-- [GATE: CIRCUIT_BREAKERS_CONFIGURED] All 4 circuit breakers set
|
+=== VALIDATION LAYER (--full mode only) ===
|
+-- P9: BACKTEST_METRICS (--full mode only)
|   +-- Run backtest via backtester agent
|   +-- Validate Sharpe >= 0.5, trade_count >= 100
|   +-- Calculate win_rate, profit_factor, max_drawdown, calmar_ratio
|   +-- Apply deflated Sharpe adjustment for multiple testing
|   +-- [GATE: SHARPE_MINIMUM] Sharpe ratio >= 0.5
|   +-- [GATE: TRADE_COUNT_MINIMUM] Trade count >= 100
|
+-- P10: PARAMETER_SENSITIVITY (--full mode only)
|   +-- Delegate to sensitivity-tester agent
|   +-- Run ±10% parameter perturbation noise test
|   +-- Execute 5-fold walk-forward validation
|   +-- Flag fragile parameters for review
|   +-- [GATE: NOISE_ROBUST] Sharpe degrades <30% under noise
|   +-- [GATE: WALK_FORWARD_VALID] OOS Sharpe > 50% of IS
|
+-- P11: STRESS_TESTING (--full mode only)
|   +-- Delegate to crisis-stress-tester agent
|   +-- Test against GFC 2008, COVID 2020, Rate Hike 2022
|   +-- Calculate tail risk metrics (VaR 95%, VaR 99%, CVaR 99%)
|   +-- [GATE: CRISIS_2008] DD < 2x benchmark DD
|   +-- [GATE: CRISIS_2020] DD < 50%
|   +-- [GATE: CRISIS_2022] Sharpe > 0 OR DD < 30%
|
+=== EXECUTION WORKFLOW (both modes) ===
|
+-- P12: DATA_CHECK (was P3 in classic)
|   +-- Identify OHLCV requirements (symbols, range, resolution)
|   +-- Check indicator dependencies
|   +-- Validate via market-data-specialist (parallel)
|   +-- [GATE: DATA] Generate warnings + data_confidence_score (non-blocking)
|   +-- User acknowledgment required if data_confidence < 0.8
|
+-- P13: DELEGATE (was P4 in classic)
|   +-- Task(strategy-builder) with VALIDATED hypothesis_bundle
|   +-- Include position_sizing_config from P6 (if --full)
|   +-- Generate JSON spec + QC skeleton
|   +-- (Anti-overfit already enforced in P5)
|
+-- P14: VALIDATE (was P5 in classic, + CONSISTENCY CHECK)
|   +-- Schema validation
|   +-- Syntax check (QC skeleton)
|   +-- [GATE: CONSISTENCY] Hypothesis-spec alignment
|
+-- P15: PRESENT/REVISE (was P6 in classic)
|   +-- SUCCESS: Output results with next steps
|   +-- FAIL: Route to revision taxonomy
|
+-- P16: AUDIT_TRAIL (--full mode only)
|   +-- Log hypothesis_id, universe_quality_score, data_confidence
|   +-- Log position_sizing_config, execution_model, risk_configuration
|   +-- Log validation_layer_results (backtest_metrics, sensitivity, stress_tests)
|   +-- Store for reproducibility
|
+-- P17: DEPLOYMENT_READY (--full mode only)
    +-- Final viability check
    +-- Generate deployment configuration
    +-- Output execution, position sizing, and risk parameters
```

### Classic Workflow (6 Phases - DEFAULT)

```text
/algo-strategy <input> [--from-doc] [--spec-only] [--skeleton-only] [--hypothesis-only]
|
+-- P1: PARSE
|   +-- Detect mode (freeform | doc_first | spec_only | skeleton_only | hypothesis_only)
|   +-- Parse arguments or read document
|   +-- [GATE 1: INPUT] 7 elements OR clarifying questions
|
+-- P2: HYPOTHESIS (HDD Core + ANTI-OVERFIT)
|   +-- Formulate: Cause -> Effect -> Why
|   +-- Lock parameters before testing
|   +-- [GATE 2a: PARAM_COUNT] Count params, BLOCK if >=10
|   +-- [GATE 2b: PARAM_RANGES] Check for excessive spans (>3x), BLOCK if found
|   +-- [GATE 2c: HYPOTHESIS] Schema valid, params locked, testability >=0.7
|
+-- P3: DATA_CHECK
|   +-- Identify OHLCV requirements (symbols, range, resolution)
|   +-- Check indicator dependencies
|   +-- Validate via market-data-specialist (parallel)
|   +-- [GATE 3: DATA] Generate warnings + data_confidence_score (non-blocking)
|   +-- User acknowledgment required if data_confidence < 0.8
|
+-- P4: DELEGATE
|   +-- Task(strategy-builder) with VALIDATED hypothesis_bundle
|   +-- Generate JSON spec + QC skeleton
|   +-- (Anti-overfit already enforced in P2)
|
+-- P5: VALIDATE (+ CONSISTENCY CHECK)
|   +-- Schema validation
|   +-- Syntax check (QC skeleton)
|   +-- [GATE 5: CONSISTENCY] Hypothesis-spec alignment
|
+-- P6: PRESENT/REVISE
    +-- SUCCESS: Output results with next steps
    +-- FAIL: Route to revision taxonomy
```

---

## Definition Layer (--full mode only)

### Phase 1: INVESTMENT_UNIVERSE (OBSERVE)

**Gate: UNIVERSE_DEFINED** - Universe scope validated and symbols confirmed

```
1. Parse Universe from $ARGUMENTS:
   - Extract symbols (tickers, indices, ETFs)
   - Identify asset class (equity, crypto, forex, futures)
   - Determine universe type:
     | Type | Description | Example |
     |------|-------------|---------|
     | single | One instrument | SPY |
     | basket | Multiple instruments | SPY, QQQ, IWM |
     | index | Index components | S&P 500 constituents |
     | sector | Sector-based | XLF (financials) |

2. Universe Metadata:
   | Field | Description | Required |
   |-------|-------------|----------|
   | symbols | List of tickers | YES |
   | asset_class | equity/crypto/forex/futures | YES |
   | universe_type | single/basket/index/sector | YES |
   | benchmark | Comparison index | NO (defaults to SPY) |

3. Gate Check (UNIVERSE_DEFINED):
   - All symbols parseable: YES/NO
   - Asset class identified: YES/NO
   - Universe type determined: YES/NO
   - If ANY check fails: Ask clarifying questions, do NOT proceed
```

---

### Phase 2: BACKTEST_CONSTRAINTS (OBSERVE)

**Gate: CONSTRAINTS_VALID** - All temporal and frequency constraints validated

```
1. Parse Temporal Constraints:
   | Constraint | Format | Example |
   |------------|--------|---------|
   | start_date | YYYY-MM-DD | 2020-01-01 |
   | end_date | YYYY-MM-DD | 2024-12-31 |
   | frequency | 1min/5min/1hour/daily | daily |
   | timezone | IANA timezone | America/New_York |

2. Calculate Lookback Requirements:
   - Identify all indicators in strategy
   - Determine maximum warmup period
   - Validate start_date allows sufficient warmup
   
   | Indicator | Warmup Bars | Example |
   |-----------|-------------|---------|
   | EMA(N) | N * 2 | EMA(200) needs 400 bars |
   | RSI(N) | N + 1 | RSI(14) needs 15 bars |
   | ATR(N) | N + 1 | ATR(14) needs 15 bars |
   | Bollinger(N) | N | BB(20) needs 20 bars |

3. Constraint Validation:
   | Check | Threshold | Blocking |
   |-------|-----------|----------|
   | Backtest duration | >= 2 years | WARN |
   | Available history | >= warmup + 252 bars | YES |
   | Frequency supported | Exchange hours valid | YES |

4. Gate Check (CONSTRAINTS_VALID):
   - start_date valid: YES/NO
   - end_date valid: YES/NO
   - frequency supported: YES/NO
   - warmup satisfied: YES/NO
   - If ANY check fails: Show constraint errors, do NOT proceed
```

---

### Phase 3: UNIVERSE_SELECTION (ORIENT)

**Gate: SURVIVOR_BIAS_CHECK** - Universe quality validated, survivor bias addressed

```
1. Delegate to universe-selector:
   Task(
     subagent_type="universe-selector",
     prompt="Validate universe {symbols} for backtest {start_date} to {end_date}.
             Apply SURVIVOR_BIAS_CHECK and LIQUIDITY_VALID gates.
             Return: universe_quality_score, survivor_bias_flags[], liquidity_warnings[]"
   )

2. Survivor Bias Checks:
   | Check | Description | Action |
   |-------|-------------|--------|
   | Delisted symbols | Symbol not trading at start_date | FLAG |
   | Merger/acquisition | Corporate action during period | FLAG |
   | Symbol changes | Ticker renamed | FLAG |
   | Sector reclassification | Sector changed during period | WARN |

3. Liquidity Validation:
   | Metric | Threshold | Blocking |
   |--------|-----------|----------|
   | Avg daily volume | >= 100K shares | YES |
   | Avg daily $ volume | >= $1M | YES |
   | Bid-ask spread | <= 0.5% | WARN |
   | Trading days coverage | >= 95% of period | WARN |

4. Sector/Industry Coverage:
   - Calculate sector concentration
   - Flag if single sector > 40% of universe
   - Suggest diversification if unbalanced

5. Universe Quality Score:
   | Component | Weight | Calculation |
   |-----------|--------|-------------|
   | Survivor bias | 0.35 | 1 - (flagged_symbols / total_symbols) |
   | Liquidity | 0.35 | avg(symbol_liquidity_scores) |
   | Coverage | 0.15 | trading_days / expected_days |
   | Diversification | 0.15 | 1 - max_sector_concentration |

6. Gate Check (SURVIVOR_BIAS_CHECK):
   - universe_quality_score >= 0.7: PASS
   - universe_quality_score 0.5-0.7: WARN, require acknowledgment
   - universe_quality_score < 0.5: BLOCK, require universe revision
   
   Output:
   | Field | Value |
   |-------|-------|
   | universe_quality_score | 0.XX |
   | survivor_bias_flags | [list] |
   | liquidity_warnings | [list] |
   | diversification_notes | [list] |
   | recommendation | PASS/WARN/BLOCK |
```

---

## Strategy Layer (--full mode only)

### Phase 6: POSITION_SIZING (DECIDE)

**Gate 6a: SIZING_METHOD_VALID** - Method selected from allowed list (HARD)
**Gate 6b: REGIME_ADJUSTMENT_CONFIGURED** - Regime factors specified if enabled (SOFT)

**Input**: Validated hypothesis from P5

**TodoWrite Checkpoint**: `POSITION_SIZING_COMPLETE`

```
1. Determine Position Sizing Method:
   | Method | Description | Use When |
   |--------|-------------|----------|
   | fixed | Fixed percentage per trade (e.g., 2%) | Simple strategies, beginners |
   | volatility_scaled | ATR-based sizing (risk parity) | Volatility-sensitive strategies |
   | kelly | Kelly criterion with fractional multiplier | High-conviction, edge-based |
   | regime_adjusted | Base method x regime multiplier | Adaptive to market conditions |

2. Configure Regime Adjustment (if enabled):
   
   Volatility Regime Multipliers:
   | Regime | ATR Percentile | Multiplier |
   |--------|----------------|------------|
   | LOW | < 25th percentile | 1.2x |
   | NORMAL | 25th - 75th percentile | 1.0x |
   | HIGH | > 75th percentile | 0.7x |
   
   Trend Regime Multipliers:
   | Regime | Condition | Multiplier |
   |--------|-----------|------------|
   | BULL | Price > 200DMA, slope positive | 1.1x |
   | NEUTRAL | Price near 200DMA | 1.0x |
   | BEAR | Price < 200DMA, slope negative | 0.8x |
   
   Correlation Regime Multipliers:
   | Regime | Cross-asset correlation | Multiplier |
   |--------|-------------------------|------------|
   | LOW | < 0.3 avg correlation | 1.1x |
   | HIGH | > 0.7 avg correlation | 0.9x |

3. Delegate to risk-management-specialist:
   Task(
     subagent_type="risk-management-specialist",
     prompt="Calculate position sizing for hypothesis {hypothesis_id}. 
            Method: {sizing_method}. Risk per trade: {risk_pct}%. 
            Apply regime adjustments: {regime_adjustment}. 
            Return: position_size_pct, regime_multiplier, effective_risk."
   )

4. Validate Against Portfolio Constraints:
   | Constraint | Threshold | Blocking |
   |------------|-----------|----------|
   | Max single position | 10% of portfolio | YES |
   | Max sector exposure | 25% of portfolio | YES |
   | Max correlation cluster | 40% of portfolio | WARN |

5. Position Sizing Configuration Output:
   {
     "sizing_method": "regime_adjusted",
     "base_method": "volatility_scaled",
     "risk_per_trade_pct": 2.0,
     "regime_adjustments": {
       "volatility": {"enabled": true, "current": "NORMAL", "multiplier": 1.0},
       "trend": {"enabled": true, "current": "BULL", "multiplier": 1.1},
       "correlation": {"enabled": false}
     },
     "effective_position_size_pct": 2.2,
     "portfolio_constraints_validated": true
   }

6. Gate Check (SIZING_METHOD_VALID + REGIME_ADJUSTMENT_CONFIGURED):
   - Method in [fixed, volatility_scaled, kelly, regime_adjusted]: YES/NO
   - If regime_adjusted: All enabled regime factors specified: YES/NO
   - Portfolio constraints validated: YES/NO
   - If HARD gate fails: Show error, do NOT proceed
   - If SOFT gate fails: WARN, continue with default multipliers
```

---

## Execution & Risk Layer (--full mode only)

### Phase 7: EXECUTION_MODEL (ACT)

**Gate: SLIPPAGE_SENSITIVITY_PASS** - Strategy viable under realistic execution costs

```
1. Delegate to execution-modeler:
   Task(
     subagent_type="execution-modeler",
     prompt="Model execution costs for strategy {hypothesis_id}. 
            Trade frequency: {trades_per_month}. Average position size: {avg_position_pct}%.
            Universe ADV: {universe_adv}. 
            Return: execution_cost_bps, slippage_estimate, market_impact, viability_verdict."
   )

2. Execution Cost Components:
   | Component | Calculation | Threshold |
   |-----------|-------------|-----------|
   | Slippage | Based on trade size vs ADV | < 50 bps |
   | Market impact | Square-root model | < 20 bps (liquid) |
   | Commission | Per-share/per-trade | Variable |
   | Spread cost | Bid-ask spread / 2 | Included in slippage |

3. Viability Validation:
   | Check | Threshold | Blocking |
   |-------|-----------|----------|
   | Slippage estimate | < 50 bps | YES |
   | Market impact (liquid) | < 20 bps | YES |
   | Total execution cost | < 30% of expected alpha | YES |
   | Sharpe after costs | > 0.5 | YES |

4. Sensitivity Analysis:
   - Run +50% slippage stress scenario
   - Strategy must remain profitable after costs
   - Calculate break-even slippage threshold

5. Execution Model Output:
   | Field | Description |
   |-------|-------------|
   | execution_cost_bps | Total expected execution cost |
   | slippage_estimate | Expected slippage per trade |
   | market_impact | Expected market impact |
   | stress_scenario_viable | +50% slippage result |
   | viability_verdict | VIABLE/MARGINAL/NOT_VIABLE |

6. Gate Check (SLIPPAGE_SENSITIVITY_PASS):
   - Sharpe after costs > 0.5: PASS
   - Stress scenario viable: PASS
   - If EITHER fails: BLOCK, strategy not viable under realistic execution
```

---

### Phase 8: RISK_MANAGEMENT (ACT) [Full P8]

**Gates: REGIME_CLASSIFICATION_COMPLETE, CIRCUIT_BREAKERS_CONFIGURED**

```
1. Delegate to risk-management-specialist for regime classification:
   Task(
     subagent_type="risk-management-specialist",
     prompt="Classify current regime for {universe}. 
            Return: volatility_regime (LOW/NORMAL/HIGH), correlation_regime (LOW/HIGH), 
            trend_regime (BULL/NEUTRAL/BEAR), circuit_breaker_recommendations."
   )

2. 5-Factor Regime Model (Samir Varma):
   | Factor | Source | Impact | Classification |
   |--------|--------|--------|----------------|
   | Volatility | ATR percentile | Position sizing | LOW (<p25), NORMAL (p25-p75), HIGH (>p75) |
   | Correlation | Rolling correlation | Diversification | LOW (<0.5), HIGH (>=0.5) |
   | Trend | 200DMA position | Directional bias | BULL (>5%), NEUTRAL (±5%), BEAR (<-5%) |
   | Credit | Spread levels | Risk-off signals | NORMAL, ELEVATED, STRESSED |
   | Sentiment | VIX/Put-Call | Contrarian signals | FEAR, NEUTRAL, GREED |

3. Circuit Breaker Configuration:
   | Breaker | Default | Range | Description |
   |---------|---------|-------|-------------|
   | Daily loss limit | -3% | -1% to -5% | Halt trading for day |
   | Max drawdown | -15% | -10% to -25% | Strategy halt |
   | Position concentration | 10% | 5% to 20% | Max single position |
   | Sector concentration | 25% | 15% to 40% | Max sector exposure |

4. 200DMA Risk Asymmetry (Varma Insight):
   | Market Position | Return Expectation | Risk Weight | Position Multiplier |
   |-----------------|-------------------|-------------|---------------------|
   | Above 200DMA | 67% | 33% | 1.0x - 1.2x |
   | Below 200DMA | 33% | 67% | 0.5x - 0.8x |

5. Regime-Based Position Adjustments:
   | Regime Combination | Position Multiplier | Rationale |
   |--------------------|---------------------|-----------|
   | LOW vol + BULL trend | 1.2x | Favorable conditions |
   | NORMAL vol + NEUTRAL | 1.0x | Standard sizing |
   | HIGH vol + BEAR trend | 0.5x | Risk reduction |
   | Any + STRESSED credit | 0.3x | Risk-off mode |

6. Risk Configuration Output:
   | Field | Value |
   |-------|-------|
   | volatility_regime | LOW/NORMAL/HIGH |
   | correlation_regime | LOW/HIGH |
   | trend_regime | BULL/NEUTRAL/BEAR |
   | credit_regime | NORMAL/ELEVATED/STRESSED |
   | sentiment_regime | FEAR/NEUTRAL/GREED |
   | position_multiplier | 0.3x - 1.2x |
   | circuit_breakers | {configured values} |

7. Gate Checks:
   REGIME_CLASSIFICATION_COMPLETE:
   - All 5 factors classified: YES/NO
   - If ANY factor unclassified: BLOCK, require data
   
   CIRCUIT_BREAKERS_CONFIGURED:
   - Daily loss limit set: YES/NO
   - Max drawdown set: YES/NO
   - Position concentration set: YES/NO
   - Sector concentration set: YES/NO
   - If ANY breaker missing: BLOCK, require configuration
```

---

## Validation Layer (--full mode only)

### Phase 9: BACKTEST_METRICS (VALIDATE)

**Gate: SHARPE_MINIMUM** - Sharpe ratio >= 0.5 (HARD)
**Gate: TRADE_COUNT_MINIMUM** - Trade count >= 100 (HARD)

**Input**: Risk-configured hypothesis from P8

**TodoWrite Checkpoint**: `BACKTEST_METRICS_COMPLETE`

```
1. Delegate to backtester:
   Task(
     subagent_type="backtester",
     prompt="Execute HDD-compliant backtest for hypothesis {hypothesis_id}. 
            Apply: position_sizing_config, execution_model, risk_regime.
            Return: sharpe, max_dd, trade_count, win_rate, profit_factor, calmar_ratio."
   )

2. Validate Against Minimum Thresholds:
   | Metric | Minimum | Rationale |
   |--------|---------|-----------|
   | Sharpe Ratio | 0.5 | Risk-adjusted return |
   | Trade Count | 100 | Statistical significance |
   | Win Rate | 40% | Minimum viability |
   | Profit Factor | 1.2 | Edge confirmation |
   | Max Drawdown | -30% | Survivability |

3. Calculate Deflated Sharpe:
   - Adjust for multiple testing bias
   - Formula: Sharpe_deflated = Sharpe - sqrt(variance * trial_count / sample_size)
   - Accounts for hypothesis iterations and parameter combinations

4. Backtest Metrics Output:
   | Field | Description |
   |-------|-------------|
   | sharpe_ratio | Annualized Sharpe ratio |
   | sharpe_deflated | Adjusted for multiple testing |
   | max_drawdown | Maximum peak-to-trough decline |
   | trade_count | Total number of trades |
   | win_rate | Percentage of winning trades |
   | profit_factor | Gross profit / Gross loss |
   | calmar_ratio | CAGR / Max drawdown |

5. Gate Check (SHARPE_MINIMUM + TRADE_COUNT_MINIMUM):
   - Sharpe >= 0.5: PASS/FAIL
   - Trade count >= 100: PASS/FAIL
   - If EITHER fails: BLOCK, show improvement guidance
   
   Output:
   | Gate | Status | Value | Threshold |
   |------|--------|-------|-----------|
   | SHARPE_MINIMUM | PASS/FAIL | {sharpe} | >= 0.5 |
   | TRADE_COUNT_MINIMUM | PASS/FAIL | {trades} | >= 100 |
```

---

### Phase 10: PARAMETER_SENSITIVITY (VALIDATE)

**Gate: NOISE_ROBUST** - Sharpe degrades <30% under ±10% noise (HARD)
**Gate: WALK_FORWARD_VALID** - OOS Sharpe > 50% of IS (HARD)

**Input**: Backtested hypothesis from P9

**TodoWrite Checkpoint**: `PARAMETER_SENSITIVITY_COMPLETE`

```
1. Delegate to sensitivity-tester:
   Task(
     subagent_type="sensitivity-tester",
     prompt="Run sensitivity analysis for hypothesis {hypothesis_id}.
            Mode: full_test.
            Noise level: ±10% parameter perturbation.
            Walk-forward folds: 5.
            Return: sensitivity_score, noise_test_results, walk_forward_results, fragile_parameters."
   )

2. Noise Test Protocol:
   - Perturb each parameter by ±10%
   - Run backtest for each perturbation
   - Calculate Sharpe degradation percentage
   - Flag parameters where degradation > 30%

3. Walk-Forward Validation:
   | Fold | Training | Test | Purpose |
   |------|----------|------|---------|
   | 1 | 2015-2017 | 2018 | Early period |
   | 2 | 2016-2018 | 2019 | Pre-COVID |
   | 3 | 2017-2019 | 2020 | COVID stress |
   | 4 | 2018-2020 | 2021 | Recovery |
   | 5 | 2019-2021 | 2022 | Rate hike |

4. Robustness Assessment:
   | Check | Threshold | Blocking |
   |-------|-----------|----------|
   | Noise degradation | < 30% | YES |
   | OOS/IS Sharpe ratio | > 50% | YES |
   | Consistent sign | All folds profitable | WARN |
   | Cliff-edge detection | No parameter cliffs | WARN |

5. Fragile Parameters:
   - List parameters with degradation > 20%
   - Recommend locked value refinement
   - Suggest economic rationale review

6. Sensitivity Results Output:
   | Field | Description |
   |-------|-------------|
   | sensitivity_score | Overall robustness (0-1) |
   | noise_degradation_pct | Max Sharpe degradation under noise |
   | oos_is_ratio | Out-of-sample / In-sample Sharpe |
   | fragile_parameters | Parameters with high sensitivity |
   | walk_forward_results | Per-fold performance |

7. Gate Check (NOISE_ROBUST + WALK_FORWARD_VALID):
   - Noise degradation < 30%: PASS/FAIL
   - OOS Sharpe > 50% of IS: PASS/FAIL
   - If EITHER fails: BLOCK, show fragility analysis
   
   Output:
   | Gate | Status | Value | Threshold |
   |------|--------|-------|-----------|
   | NOISE_ROBUST | PASS/FAIL | {degradation}% | < 30% |
   | WALK_FORWARD_VALID | PASS/FAIL | {oos_is_ratio}% | > 50% |
```

---

### Phase 11: STRESS_TESTING (VALIDATE)

**Gate: CRISIS_2008** - DD < 2x benchmark DD (HARD)
**Gate: CRISIS_2020** - DD < 50% (HARD)
**Gate: CRISIS_2022** - Sharpe > 0 OR DD < 30% (HARD)

**Input**: Sensitivity-validated hypothesis from P10

**TodoWrite Checkpoint**: `STRESS_TESTING_COMPLETE`

```
1. Delegate to crisis-stress-tester:
   Task(
     subagent_type="crisis-stress-tester",
     prompt="Stress test hypothesis {hypothesis_id} against historical crises.
            Crises: GFC_2008, COVID_2020, RATE_HIKE_2022.
            Return: crisis_results, tail_metrics, overall_score, recommendations."
   )

2. Crisis Period Definitions:
   | Crisis | Period | Benchmark DD | Characteristics |
   |--------|--------|--------------|-----------------|
   | GFC 2008 | Oct 2008 - Mar 2009 | -56.8% | Systemic, liquidity crisis |
   | COVID 2020 | Feb 2020 - Mar 2020 | -33.9% | Rapid V-shaped, liquidity shock |
   | Rate Hike 2022 | Jan 2022 - Oct 2022 | -25.4% | Duration risk, sector rotation |

3. Crisis Survival Thresholds:
   | Crisis | Threshold | Rationale |
   |--------|-----------|-----------|
   | GFC 2008 | DD < 2x S&P DD | Survive systemic crisis |
   | COVID 2020 | DD < 50% | Survive liquidity shock |
   | Rate Hike 2022 | Sharpe > 0 OR DD < 30% | Survive regime change |

4. Tail Risk Metrics:
   | Metric | Description | Calculation |
   |--------|-------------|-------------|
   | VaR 95% | 5% worst-case daily loss | 5th percentile of returns |
   | VaR 99% | 1% worst-case daily loss | 1st percentile of returns |
   | CVaR 99% | Expected loss beyond VaR 99 | Mean of returns < VaR 99 |
   | Max DD duration | Longest drawdown period | Days from peak to recovery |

5. Stress Test Results Output:
   | Field | Description |
   |-------|-------------|
   | crisis_results | Per-crisis performance metrics |
   | gfc_2008_dd | Strategy drawdown during GFC |
   | covid_2020_dd | Strategy drawdown during COVID |
   | rate_hike_2022_dd | Strategy drawdown during 2022 |
   | rate_hike_2022_sharpe | Strategy Sharpe during 2022 |
   | var_95 | Value at Risk (95%) |
   | var_99 | Value at Risk (99%) |
   | cvar_99 | Conditional VaR (99%) |
   | overall_stress_score | Combined crisis resilience (0-1) |

6. Gate Check (CRISIS_2008 + CRISIS_2020 + CRISIS_2022):
   - GFC 2008 DD < 2x benchmark: PASS/FAIL
   - COVID 2020 DD < 50%: PASS/FAIL
   - Rate Hike 2022 Sharpe > 0 OR DD < 30%: PASS/FAIL
   - If ANY fails: BLOCK, show crisis vulnerability analysis
   
   Output:
   | Gate | Status | Value | Threshold |
   |------|--------|-------|-----------|
   | CRISIS_2008 | PASS/FAIL | {dd}% | < {2x benchmark}% |
   | CRISIS_2020 | PASS/FAIL | {dd}% | < 50% |
   | CRISIS_2022 | PASS/FAIL | {sharpe}/{dd}% | Sharpe > 0 OR DD < 30% |

7. Recommendations:
   - If crisis gate fails: Suggest regime filters or position sizing adjustments
   - If tail metrics elevated: Recommend stop-loss tightening or volatility scaling
   - If all pass: Confirm strategy resilience for deployment
```

---

## Classic Workflow Phases

### Phase 1: PARSE (OBSERVE) [Classic P1 / Full P4]

**Gate 1: INPUT** - Requires 7 strategy elements or asks clarifying questions

```
1. Parse $ARGUMENTS for:
   - Strategy description (freeform text)
   - Flags: --from-doc, --spec-only, --skeleton-only, --hypothesis-only
   - Document path (if --from-doc)

2. Extract 7 Required Elements:
   | Element | Example |
   |---------|---------|
   | Universe | SPY, QQQ, tech stocks |
   | Entry Signal | EMA crossover, RSI oversold |
   | Exit Signal | Trailing stop, profit target |
   | Timeframe | 4-hour, daily |
   | Position Sizing | 2% risk per trade |
   | Risk Management | Stop loss at 2 ATR |
   | Regime Filters | Price > 200DMA, volatility LOW/NORMAL |

3. If elements missing:
   - List found elements
   - Ask clarifying questions for gaps
   - Do NOT proceed until 7/7 elements present
```

---


### Phase 2: HYPOTHESIS (ORIENT + HDD Core)

**Gate 2a: PARAM_COUNT** - BLOCK if >= 10 parameters
**Gate 2b: PARAM_RANGES** - BLOCK if any parameter range > 3x span
**Gate 2c: HYPOTHESIS** - Schema valid, params locked, testability >= 0.7

```
1. Formulate Hypothesis:
   Template: "I believe [CAUSE] leads to [EFFECT] WHEN [REGIME_CONDITION] because [WHY]"
   
   Example:
   "I believe EMA(20) crossing above EMA(50) leads to 
   sustained upward momentum because institutional 
   traders use these levels for position entry."

2. Lock Parameters BEFORE Testing:
   | Parameter | Value | Locked | Rationale |
   |-----------|-------|--------|-----------|
   | ema_fast | 20 | YES | Industry standard |
   | ema_slow | 50 | YES | Institutional level |
   | stop_atr | 2.0 | YES | 2x ATR volatility buffer |

3. Generate hypothesis_id: HYP-{timestamp}-{hash}

4. Validate Anti-Overfit Gates:
   - PARAM_COUNT: Count unique parameters
   - PARAM_RANGES: Check (max - min) / min < 3 for each
   - If BLOCKED: Show reduction guidance, STOP
```

---

### GATE 5d: HANDOFF_VALID (P5→P6 Transition, --full mode only)

**Type**: BLOCKING | **Error**: ALGO_ERR_062
**Purpose**: Validate hypothesis_bundle completeness before position sizing delegation in --full mode

**Pre-Condition**: Hypothesis validated (GATE 5c passed)
**Post-Condition**: Position sizing can proceed (P6)

#### Validation Checks

| Field | Check | Required |
|-------|-------|----------|
| hypothesis_id | Pattern matches HYP-{timestamp}-{hash} or HYP-[0-9]{3} | YES |
| params_locked | Non-empty object with at least 1 parameter | YES |
| testability_score | Exists and >= 0.7 | YES |
| cause | Non-empty string, length >= 10 | YES |
| effect | Non-empty string, length >= 10 | YES |
| why | Non-empty string, length >= 20 | YES |
| mechanism_type | One of: momentum, mean_reversion, event_driven, multi_factor | YES |

#### Handoff Validation Logic

```python
def validate_handoff(hypothesis_bundle: dict) -> GateResult:
    """Validate hypothesis_bundle completeness for P5→P6 transition."""
    errors = []
    
    # Check hypothesis_id format
    hyp_id = hypothesis_bundle.get("hypothesis_id", "")
    if not (re.match(r"^HYP-\d{8}-[a-f0-9]+$", hyp_id) or re.match(r"^HYP-\d{3}$", hyp_id)):
        errors.append("hypothesis_id missing or invalid format (expected HYP-YYYYMMDD-hash or HYP-XXX)")
    
    # Check params_locked is non-empty
    params = hypothesis_bundle.get("params_locked", {})
    if not params or len(params) == 0:
        errors.append("params_locked is empty - all parameters must be locked before P6")
    
    # Check testability_score exists and meets threshold
    testability = hypothesis_bundle.get("testability_score")
    if testability is None:
        errors.append("testability_score missing")
    elif testability < 0.7:
        errors.append(f"testability_score {testability} < 0.7 minimum")
    
    # Check required hypothesis fields
    for field, min_len in [("cause", 10), ("effect", 10), ("why", 20)]:
        value = hypothesis_bundle.get(field, "")
        if not value or len(value) < min_len:
            errors.append(f"{field} missing or too short (minimum {min_len} chars)")
    
    # Check mechanism_type
    valid_types = ["momentum", "mean_reversion", "event_driven", "multi_factor"]
    mech_type = hypothesis_bundle.get("mechanism_type")
    if mech_type not in valid_types:
        errors.append(f"mechanism_type '{mech_type}' not in {valid_types}")
    
    if errors:
        return GateResult(
            gate="HANDOFF_VALID",
            status="FAIL",
            error_code="ALGO_ERR_062",
            errors=errors
        )
    
    return GateResult(gate="HANDOFF_VALID", status="PASS")
```

#### Error Message (ALGO_ERR_062)

```
GATE FAILURE: HANDOFF_VALID (P5→P6 Transition)
Error Code: ALGO_ERR_062

The hypothesis bundle is incomplete for position sizing delegation.

Issues detected:
  - params_locked is empty - all parameters must be locked before P6
  - testability_score 0.55 < 0.7 minimum
  - why missing or too short (minimum 20 chars)

Required fields for P6 delegation:
  ✓ hypothesis_id: Valid HYP-YYYYMMDD-hash or HYP-XXX format
  ✓ params_locked: Non-empty object with locked parameters
  ✓ testability_score: >= 0.7
  ✓ cause: >= 10 characters describing the signal
  ✓ effect: >= 10 characters describing expected outcome
  ✓ why: >= 20 characters explaining mechanism
  ✓ mechanism_type: momentum | mean_reversion | event_driven | multi_factor

Recovery:
  Return to P5 (HYPOTHESIS) and complete formulation with:
  1. Lock all parameters with rationale
  2. Ensure testability_score >= 0.7
  3. Provide complete cause/effect/why explanation
  
Command: /algo-strategy --revise "<complete hypothesis statement>"
```

**Note**: This gate only applies to --full mode transitions. In --classic mode, P2 (HYPOTHESIS) flows directly to P3 (DATA_CHECK).

---

### Phase 3: DATA_CHECK (Non-Blocking)

**Gate 3: DATA** - Warnings only, requires acknowledgment if confidence < 0.8

```
1. Identify Data Requirements:
   - Symbols from universe
   - Date range (backtest period)
   - Resolution (1min, 1hour, daily)
   - Adjusted vs unadjusted prices

2. Check Indicator Dependencies:
   - EMA(200) requires 200+ bars warmup
   - ATR(14) requires 14+ bars
   - Volume indicators require volume data

3. Parallel Validation:
   Task(market-data-specialist, "Validate data availability for {symbols}")
   Task(risk-management-specialist, "Classify current volatility regime for {symbols}. Return: regime (LOW/NORMAL/HIGH), atr_percentile, 200dma_trend (above/below)")

4. Regime Assessment Output:
   | Field | Description |
   |-------|-------------|
   | regime | LOW (<p25), NORMAL (p25-p75), HIGH (>p75) |
   | atr_percentile | Current ATR position in 252-day distribution |
   | 200dma_trend | Price position relative to 200-day MA |
   | position_multiplier | 1.2x (LOW), 1.0x (NORMAL), 0.7x (HIGH) |

5. Generate data_confidence_score:
   | Condition | Score Impact |
   |-----------|--------------|
   | OHLCV gaps < 5% | -0.05 |
   | OHLCV gaps 5-20% | -0.15 |
   | Missing indicator data | -0.10 |
   | Insufficient history | -0.20 |
   | Regime data unavailable | -0.10 |
   | 200DMA history < 200 bars | -0.15 |

6. If data_confidence < 0.8:
   - Show warnings
   - Require user acknowledgment: "Continue with data gaps? [Y/N]"
```

---


### Phase 4: DELEGATE (ACT)

```
1. Build hypothesis_bundle:
   {
     "hypothesis_id": "HYP-20250101-abc123",
     "statement": "I believe [CAUSE] leads to [EFFECT] WHEN [REGIME_CONDITION] because [WHY]",
     "params_locked": {
       "ema_fast": {"value": 20, "locked": true, "rationale": "..."},
       "ema_slow": {"value": 50, "locked": true, "rationale": "..."}
     },
     "timeframe": "4-hour",
     "mechanism_type": "momentum",
     "trial_count": 0,
     "max_trials": 5
   }

2. Delegate to strategy-builder:
   Task(
     subagent_type="strategy-builder",
     prompt="MODE: {mode}. HYPOTHESIS_BUNDLE: {json}. Generate spec + skeleton."
   )

3. Anti-overfit ALREADY enforced in P2 (not here)
```

---

### Phase 5: VALIDATE (Consistency Check)

**Gate 5: CONSISTENCY** - Hypothesis-spec alignment validation

```
1. Schema Validation:
   - Validate spec against strategy-spec.schema.json
   - Check required fields present

2. Syntax Check (QC Skeleton):
   - Python syntax valid
   - QC imports present
   - OnData/Initialize methods exist

3. Consistency Rules (4 checks):
   | Rule | Check | Blocking |
   |------|-------|----------|
   | TIMEFRAME_ALIGNMENT | hypothesis.timeframe == spec.timeframe | YES |
   | SIGNAL_LOGIC | Entry uses stated indicators | YES |
   | PARAMETER_BINDING | Locked params unchanged in spec | YES |
   | MECHANISM_SOUNDNESS | Strategy type matches hypothesis | WARN |

4. On BLOCKING violation:
   - Show mismatch details
   - Route to revision (P6)
   - Do NOT present to user
```

---


### Phase 6: PRESENT/REVISE

```
SUCCESS PATH:
- Present hypothesis bundle
- Present JSON specification
- Present QC Python skeleton (if requested)
- Show next steps

FAILURE PATH (Revision Taxonomy):
| Path | Condition | Action | Hypothesis ID |
|------|-----------|--------|---------------|
| 1. Code Bug | Implementation error | Fix code, retry | SAME |
| 2. Regime Failure | Failed specific period | Add regime filter | NEW |
| 3. Invalid Theory | Failed randomly | Archive to graveyard | NEW |
| 4. Insufficient Sample | <100 trades | Extend timeframe | SAME |

Revision Guard Rails:
- Parameter changes without new hypothesis_id: BLOCKED
- Show message: "Parameters LOCKED under {hypothesis_id}"
- Options: Continue with locked params OR Create new hypothesis
```

---

## HDD Integration

### Hypothesis Formulation Template

```
TEMPLATE: "I believe [CAUSE] leads to [EFFECT] WHEN [REGIME_CONDITION] because [WHY]"

CAUSE: The market condition or signal (observable, measurable)
  - Good: "EMA(20) crossing above EMA(50)"
  - Bad: "The market feels bullish"

EFFECT: The expected outcome (testable, measurable)
  - Good: "2-5% gains within 10 trading days"
  - Bad: "Stock goes up"

WHY: The economic/behavioral rationale (explains mechanism)
  - Good: "Institutional traders use these levels for entry"
  - Bad: "It worked in the past"

WHEN: The regime condition (trend/volatility context)
  - Good: "price above 200DMA in LOW/NORMAL volatility regime"
  - Good: "ATR percentile below 75th (not HIGH volatility)"
  - Bad: "market is trending" (not measurable)
```

### Parameter Locking Rules

```
1. ALL parameters MUST be locked BEFORE first backtest
2. Locked parameters CANNOT change under same hypothesis_id
3. To change parameters: MUST create NEW hypothesis with new rationale
4. New hypothesis_id resets trial counter to 0
5. Old hypothesis archived to graveyard with failure notes
```

### Trial Tracking

```
- Max trials per hypothesis: 5
- Trial = one backtest run with specific date range
- Exceeding max trials: MUST create new hypothesis or archive
- Trial results stored with hypothesis for audit trail
```

---


## Anti-Overfitting Constraints

### Hard Constraints (BLOCK if violated)

| Constraint | Threshold | Check Phase | Rationale |
|------------|-----------|-------------|-----------|
| Max parameters | < 10 | P2 | Degrees of freedom |
| Max backtest trials | < 30 | P2 | Statistical significance |
| Parameter ranges | < 3x span | P2 | Optimization surface |

### Soft Constraints (WARN if violated)

| Constraint | Threshold | Check Phase | Rationale |
|------------|-----------|-------------|-----------|
| Min trade count | > 100 | P6 | Sample size |
| IS/OOS delta | < 30% | P6 | Generalization |
| Plateau rule | Required | P6 | Stability |

### On Constraint Violation

```
HARD VIOLATION (P2):
  - STOP workflow
  - Show: "OVERFIT RISK: {constraint} violated"
  - Guidance: "Reduce parameters to <10" or "Narrow parameter ranges"
  - User must revise hypothesis before continuing

SOFT VIOLATION (P6):
  - WARN but continue
  - Show: "WARNING: {constraint} may indicate overfitting"
  - Guidance: Suggestions for improvement
  - User decides whether to proceed
```

---

## Agent Delegation Matrix

### Classic Mode (--classic, DEFAULT)

| Agent | Purpose | When Called | Input | Timeout |
|-------|---------|-------------|-------|---------|
| strategy-builder | Generate JSON spec + QC skeleton | P4 | hypothesis_bundle | 90s |
| market-data-specialist | Validate data availability | P3 (parallel) | symbols, date_range | 60s |
| risk-management-specialist | Classify volatility regime | P3 (parallel) | symbols, lookback=252 | 60s |

### Full Mode (--full)

| Agent | Purpose | When Called | Input | Timeout |
|-------|---------|-------------|-------|---------|
| universe-selector | Validate universe quality, survivor bias | P3 | symbols, start_date, end_date | 90s |
| risk-management-specialist | Calculate position sizing, regime adjustments | P6 | hypothesis_id, sizing_method, risk_pct, regime_adjustment | 60s |
| execution-modeler | Model execution costs, slippage, market impact | P7 | hypothesis_id, trade_frequency, position_size, universe_adv | 300s |
| risk-management-specialist | Classify 5-factor regime, configure circuit breakers | P8 | universe, regime_factors | 60s |
| backtester | Execute HDD-compliant backtest | P9 | hypothesis_bundle + position_sizing_config + execution_model | 600s |
| sensitivity-tester | Run parameter sensitivity analysis | P10 | hypothesis_id, noise_level, walk_forward_folds | 600s |
| crisis-stress-tester | Stress test against historical crises | P11 | hypothesis_id, crisis_periods | 600s |
| strategy-builder | Generate JSON spec + QC skeleton | P13 | hypothesis_bundle + position_sizing_config | 90s |
| market-data-specialist | Validate data availability | P12 (parallel) | symbols, date_range | 60s |

### Delegation Patterns

```
# P3 (--full mode): Universe Selection
Task(
  subagent_type="universe-selector",
  prompt="Validate universe {symbols} for backtest {start_date} to {end_date}.
          Apply SURVIVOR_BIAS_CHECK and LIQUIDITY_VALID gates.
          Return: universe_quality_score, survivor_bias_flags[], liquidity_warnings[]",
  timeout_ms=90000  # 90s
)

# P6 (--full mode): Position Sizing
Task(
  subagent_type="risk-management-specialist",
  prompt="Calculate position sizing for hypothesis {hypothesis_id}. 
          Method: {sizing_method}. Risk per trade: {risk_pct}%. 
          Apply regime adjustments: {regime_adjustment}. 
          Return: position_size_pct, regime_multiplier, effective_risk.",
  timeout_ms=60000  # 60s
)

# P7 (--full mode): Execution Modeling
Task(
  subagent_type="execution-modeler",
  prompt="Model execution costs for strategy {hypothesis_id}. 
          Trade frequency: {trades_per_month}. Average position size: {avg_position_pct}%.
          Universe ADV: {universe_adv}. 
          Return: execution_cost_bps, slippage_estimate, market_impact, viability_verdict.",
  timeout_ms=300000  # 300s (5 min) - ADV lookup can be slow
)

# P8 (--full mode): Risk Management
Task(
  subagent_type="risk-management-specialist",
  prompt="Classify current regime for {universe}. 
          Return: volatility_regime (LOW/NORMAL/HIGH), correlation_regime (LOW/HIGH), 
          trend_regime (BULL/NEUTRAL/BEAR), circuit_breaker_recommendations.",
  timeout_ms=60000  # 60s
)

# P9 (--full mode): Backtest Metrics
Task(
  subagent_type="backtester",
  prompt="Execute HDD-compliant backtest for hypothesis {hypothesis_id}. 
          Apply: position_sizing_config, execution_model, risk_regime.
          Return: sharpe, max_dd, trade_count, win_rate, profit_factor, calmar_ratio.",
  timeout_ms=600000  # 600s (10 min) - full backtest
)

# P10 (--full mode): Parameter Sensitivity
Task(
  subagent_type="sensitivity-tester",
  prompt="Run sensitivity analysis for hypothesis {hypothesis_id}.
          Mode: full_test.
          Noise level: ±10% parameter perturbation.
          Walk-forward folds: 5.
          Return: sensitivity_score, noise_test_results, walk_forward_results, fragile_parameters.",
  timeout_ms=600000  # 600s (10 min) - sensitivity analysis
)

# P11 (--full mode): Stress Testing
Task(
  subagent_type="crisis-stress-tester",
  prompt="Stress test hypothesis {hypothesis_id} against historical crises.
          Crises: GFC_2008, COVID_2020, RATE_HIKE_2022.
          Return: crisis_results, tail_metrics, overall_score, recommendations.",
  timeout_ms=600000  # 600s (10 min) - stress testing
)

# P12: Data Validation (parallel with hypothesis building)
Task(
  subagent_type="market-data-specialist",
  prompt="Validate OHLCV availability for {symbols} from {start} to {end}. 
          Check: gaps, adjustments, volume data. 
          Return: data_confidence_score, warnings[]",
  timeout_ms=60000  # 60s
)

# P13: Strategy Generation
Task(
  subagent_type="strategy-builder",
  prompt="MODE: {mode}. 
          HYPOTHESIS_BUNDLE: {hypothesis_json}.
          Generate: JSON spec + QC Python skeleton.
          Enforce: All locked parameters unchanged.",
  timeout_ms=90000  # 90s
)
```

### Timeout Rationale

| Timeout | Use Case | Agents |
|---------|----------|--------|
| 60s | Simple validation tasks (single API call, regime classification) | market-data-specialist, risk-management-specialist (P3, P8) |
| 90s | Multi-step validation with moderate data (universe validation, strategy generation) | universe-selector, strategy-builder |
| 300s | Execution modeling with ADV lookups across entire universe | execution-modeler |
| 600s | Full backtest/stress test execution across multiple periods | backtester, sensitivity-tester, crisis-stress-tester |

**Timeout Behavior**: If an agent times out, the workflow blocks with error code ALGO_ERR_070 (Agent Timeout). Recovery options include retrying with extended timeout or using --classic mode.

---


## Error Codes

### Pre-Flight Errors (P0)

| Code | Phase | Description | Recovery |
|------|-------|-------------|----------|
| ALGO_ERR_050 | P0 | strategy-builder agent not found | Verify agent path, create if missing |
| ALGO_ERR_051 | P0 | market-data-specialist agent not found | Verify agent path, create if missing |
| ALGO_ERR_052 | P0 | risk-management-specialist agent not found | Verify agent path, create if missing |
| ALGO_ERR_053 | P0 | universe-selector agent not found (--full mode) | Use --classic or create agent |
| ALGO_ERR_054 | P0 | execution-modeler agent not found (--full mode) | Use --classic or create agent |
| ALGO_ERR_055 | P0 | backtester agent not found (--full mode) | Use --classic or create agent |
| ALGO_ERR_056 | P0 | sensitivity-tester agent not found (--full mode) | Use --classic or create agent |
| ALGO_ERR_057 | P0 | crisis-stress-tester agent not found (--full mode) | Use --classic or create agent |
| ALGO_ERR_060 | P0 | Mutually exclusive workflow flags (--classic + --full) | Choose one workflow depth |
| ALGO_ERR_061 | P0 | Conflicting output modes (--spec-only + --skeleton-only) | Choose one output mode |
| ALGO_ERR_062 | P5→P6 | Hypothesis bundle incomplete for handoff | Complete hypothesis formulation |
| ALGO_ERR_070 | ANY | Agent delegation timed out | Retry or use --classic mode |

### Classic Mode Errors (P1-P6)

| Code | Phase | Description | Recovery |
|------|-------|-------------|----------|
| ALGO_ERR_001 | P1 | Insufficient input (< 7 elements) | Ask clarifying questions |
| ALGO_ERR_002 | P2 | Untestable hypothesis | Provide formulation guidance |
| ALGO_ERR_003 | P3 | Critical data unavailable | Suggest alternative symbols/timeframes |
| ALGO_ERR_004 | P2 | Overfit risk (hard constraint) | Show reduction guidance, STOP |
| ALGO_ERR_005 | P4 | Strategy generation failed | Retry once, then escalate |
| ALGO_ERR_006 | P5 | Spec schema validation failed | Show schema violations |
| ALGO_ERR_007 | P5 | Skeleton syntax error | Show Python compile errors |
| ALGO_ERR_008 | P5 | Hypothesis-spec mismatch | Highlight inconsistencies, route to revision |

### Full Mode Errors (--full, P1-P17)

| Code | Phase | Description | Recovery |
|------|-------|-------------|----------|
| ALGO_ERR_010 | P1 | Universe undefined (symbols not parseable) | Provide explicit ticker list |
| ALGO_ERR_011 | P1 | Asset class ambiguous | Specify: equity/crypto/forex/futures |
| ALGO_ERR_012 | P2 | Invalid date range | Provide valid YYYY-MM-DD dates |
| ALGO_ERR_013 | P2 | Insufficient warmup period | Extend start_date or reduce indicator lookback |
| ALGO_ERR_014 | P2 | Unsupported frequency | Use: 1min/5min/1hour/daily |
| ALGO_ERR_015 | P3 | Survivor bias critical (>30% flagged) | Revise universe, remove delisted symbols |
| ALGO_ERR_016 | P3 | Liquidity threshold failed | Remove illiquid symbols or increase thresholds |
| ALGO_ERR_017 | P3 | Universe quality score < 0.5 | Major universe revision required |
| ALGO_ERR_018 | P16 | Audit trail write failed | Check write permissions, retry |
| ALGO_ERR_020 | P6 | Invalid sizing method | Use: fixed, volatility_scaled, kelly, or regime_adjusted |
| ALGO_ERR_019 | P6 | Portfolio constraint violation | Position exceeds 10% single, 25% sector, or 40% correlation limit |
| ALGO_ERR_021 | P7 | Slippage exceeds 50 bps threshold | Reduce position size or increase universe liquidity |
| ALGO_ERR_022 | P7 | Market impact exceeds 20 bps (liquid universe) | Trade smaller or use less liquid symbols |
| ALGO_ERR_023 | P7 | Execution cost exceeds 30% of expected alpha | Strategy not viable; increase alpha or reduce costs |
| ALGO_ERR_024 | P7 | Stress scenario failed (+50% slippage) | Strategy not robust to execution variance |
| ALGO_ERR_025 | P8 | Regime classification incomplete | Provide additional data for unclassified factors |
| ALGO_ERR_026 | P8 | Circuit breakers not configured | Set all 4 required circuit breakers |
| ALGO_ERR_027 | P8 | 200DMA data insufficient | Require 200+ bars of price history |
| ALGO_ERR_028 | P8 | Regime data unavailable for factor | Use default regime or provide alternative data source |

### Validation Layer Errors (P9-P11)

| Code | Phase | Description | Recovery |
|------|-------|-------------|----------|
| ALGO_ERR_030 | P9 | Sharpe ratio below minimum (< 0.5) | Refine entry/exit logic or add regime filters |
| ALGO_ERR_031 | P9 | Insufficient trade count (< 100) | Extend backtest period or relax entry conditions |
| ALGO_ERR_032 | P9 | Win rate below minimum (< 40%) | Review signal logic or exit timing |
| ALGO_ERR_033 | P9 | Profit factor below minimum (< 1.2) | Improve risk/reward ratio or position sizing |
| ALGO_ERR_034 | P9 | Max drawdown exceeds threshold (> 30%) | Add stop-loss or reduce position sizing |
| ALGO_ERR_035 | P10 | Noise test failed (degradation > 30%) | Reduce parameter sensitivity or widen parameter ranges |
| ALGO_ERR_036 | P10 | Walk-forward validation failed (OOS < 50% of IS) | Strategy likely overfit; simplify or archive hypothesis |
| ALGO_ERR_037 | P10 | Cliff-edge parameter detected | Review parameter values near boundary conditions |
| ALGO_ERR_038 | P11 | Crisis stress test failed (GFC 2008) | Add bear market regime filter or reduce exposure |
| ALGO_ERR_039 | P11 | Crisis stress test failed (COVID 2020) | Add volatility spike protection or circuit breakers |
| ALGO_ERR_040 | P11 | Crisis stress test failed (Rate Hike 2022) | Add duration/rate sensitivity filter |
| ALGO_ERR_041 | P11 | Tail risk metrics exceeded (VaR/CVaR) | Tighten stop-loss or add tail risk hedging |

### Error Response Format

```
ERROR: {ALGO_ERR_XXX}
Phase: P{N} - {phase_name}
Description: {error_description}

Details:
{specific_error_details}

Recovery:
{recovery_guidance}

Next Steps:
1. {action_1}
2. {action_2}
```

---

## Output Format

### Success Output

```markdown
# Strategy Generated: {strategy_name}

## Hypothesis
ID: {hypothesis_id}
Statement: "I believe {CAUSE} leads to {EFFECT} because {WHY}"
Trial: {current}/{max_trials}

## Parameters (LOCKED)
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| {param_1} | {value} | {rationale} |
| {param_2} | {value} | {rationale} |

## Anti-Overfit Status
- Parameters: {count}/10 (PASS)
- Ranges: All < 3x (PASS)
- Data Confidence: {score}

## Specification
{JSON spec}

## Python Skeleton
{QC Python code}

## Next Steps
1. Review specification for accuracy
2. Run backtest: /backtest {strategy_name}
3. If hypothesis fails: /algo-strategy --revise {hypothesis_id}
```



### Failure Output

```markdown
# Strategy Generation Failed

## Error
Code: {ALGO_ERR_XXX}
Phase: P{N} - {phase_name}

## Issue
{error_description}

## Details
{specific_details}

## Recovery Options
1. {option_1}
2. {option_2}

## To Retry
/algo-strategy {corrected_input}
```

### Parameter Lock Violation Output

```markdown
# PARAMETER MODIFICATION BLOCKED

You attempted to change {param_name}({old_value}) -> {param_name}({new_value}).

{param_name} is LOCKED under hypothesis {hypothesis_id}. The HDD methodology 
prohibits parameter changes after seeing backtest results.

## Your Options
1. CONTINUE with {param_name}({old_value}) - extend timeframe or add regime filter
2. CREATE NEW HYPOTHESIS - explain WHY {new_value} has different economic rationale
   -> This will archive {hypothesis_id} and create new ID with reset trial counter

## To Create New Hypothesis
/algo-strategy --revise "I believe {new_rationale}..."
```

---

## Knowledge Base

### Skills
- `.claude/skills/strategy-specification/SKILL.md` - Strategy spec patterns
- `.claude/skills/hypothesis-validation/consistency-checker.md` - Consistency rules

### Documentation
- `.claude/docs/command-docs/algo-strategy/docs/workflow-phases.md` - Detailed phases
- `.claude/docs/command-docs/algo-strategy/docs/hdd-methodology.md` - HDD guide
- `.claude/docs/command-docs/algo-strategy/docs/revision-guard-rails.md` - Revision rules
- `.claude/docs/command-docs/algo-strategy/docs/anti-overfit-gates.md` - Overfit prevention

### Examples
- `.claude/docs/command-docs/algo-strategy/examples/freeform-example.md`
- `.claude/docs/command-docs/algo-strategy/examples/doc-first-example.md`

### Schemas
- `.claude/docs/command-docs/algo-strategy/schemas/algo-strategy.schema.json`
- `.claude/docs/command-docs/algo-strategy/schemas/hypothesis-bundle.schema.json`

---

## Integration

**Upstream**: Trading ideas, strategy documents, research notes
**Downstream**: `/backtest` (runs strategy)

**Trigger Keywords**: algo strategy, trading strategy, hypothesis, HDD, backtest idea

---

## Anti-Patterns (NEVER DO)

- Skip hypothesis formulation (jump straight to spec)
- Allow parameter changes under same hypothesis_id
- Proceed with >= 10 parameters
- Ignore data validation warnings
- Generate spec without locked parameters
- Present spec with consistency violations

## Good Patterns (ALWAYS DO)

- Formulate hypothesis BEFORE any spec generation
- Lock ALL parameters with rationale
- Validate anti-overfit constraints in P2 (before delegation)
- Check hypothesis-spec consistency in P5
- Archive failed hypotheses to graveyard
- Track trial count per hypothesis
