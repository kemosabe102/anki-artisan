---
title: Algo-Strategy 17-Phase Workflow Architecture
date: 2025-01-09
status: active
tags: [algo-strategy, workflow, hdd, trading-strategy, investing]
---

# Algo-Strategy 17-Phase Workflow Architecture

> Hypothesis-Driven Development orchestration for systematic trading strategy generation.

---

## Overview

The `/algo-strategy` command implements a multi-phase workflow for generating trading strategies using Hypothesis-Driven Development (HDD) methodology. The architecture supports two modes:

| Mode | Phases | Use Case |
|------|--------|----------|
| `--classic` (DEFAULT) | 6 phases (P1-P6) | Rapid prototyping, hypothesis validation |
| `--full` | 17 phases (P1-P17) | Production-ready strategies with full validation |

---

## Architecture Layers

The 17-phase workflow is organized into four logical layers:

```text
+-----------------------------------------------------------------------+
|                         DEFINITION LAYER (P1-P3)                       |
|  P1: Investment Universe  |  P2: Backtest Constraints  |  P3: Universe Selection  |
+-----------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                          CLASSIC WORKFLOW (P4-P5)                      |
|           P4: Parse Input           |           P5: Hypothesis          |
+-----------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                          STRATEGY LAYER (P6-P8)                        |
|    P6: Position Sizing    |  P7: Execution Model  |  P8: Risk Mgmt    |
+-----------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                         VALIDATION LAYER (P9-P11)                      |
|   P9: Backtest Metrics  |  P10: Sensitivity  |  P11: Stress Testing   |
+-----------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                         EXECUTION LAYER (P12-P17)                      |
|  P12: Data Check | P13: Delegate | P14: Validate | P15: Present       |
|  P16: Audit Trail | P17: Deployment Ready                              |
+-----------------------------------------------------------------------+
```


---

## Layer Descriptions

### 1. Definition Layer (P1-P3) - Full Mode Only

Establishes the investment universe, temporal constraints, and validates data quality.

| Phase | Purpose | Gate | Agent |
|-------|---------|------|-------|
| P1: INVESTMENT_UNIVERSE | Parse symbols, asset class, universe type | UNIVERSE_DEFINED | - |
| P2: BACKTEST_CONSTRAINTS | Validate date range, frequency, warmup | CONSTRAINTS_VALID | - |
| P3: UNIVERSE_SELECTION | Survivor bias, liquidity validation | SURVIVOR_BIAS_CHECK | universe-selector |

**Samir Varma Integration**: Phase 3 validates that the universe has sufficient liquidity for realistic execution. Illiquid symbols create unrealistic backtests.

### 2. Classic Workflow (P4-P5) - Both Modes

Core HDD hypothesis formulation with anti-overfitting constraints.

| Phase | Purpose | Gate | Agent |
|-------|---------|------|-------|
| P4: PARSE | Extract 7 required strategy elements | INPUT | - |
| P5: HYPOTHESIS | Formulate testable hypothesis, lock params | PARAM_COUNT, PARAM_RANGES, HYPOTHESIS | - |

**Anti-Overfit Gates**:
- PARAM_COUNT: Block if >= 10 parameters (degrees of freedom)
- PARAM_RANGES: Block if any parameter range > 3x span (optimization surface)

### 3. Strategy Layer (P6-P8) - Full Mode Only

Position sizing, execution modeling, and risk management configuration.

| Phase | Purpose | Gate | Agent |
|-------|---------|------|-------|
| P6: POSITION_SIZING | Sizing method, regime adjustments | SIZING_METHOD_VALID, REGIME_ADJUSTMENT_CONFIGURED | risk-management-specialist |
| P7: EXECUTION_MODEL | Slippage, market impact, viability | SLIPPAGE_SENSITIVITY_PASS | execution-modeler |
| P8: RISK_MANAGEMENT | 5-factor regime, circuit breakers | REGIME_CLASSIFICATION_COMPLETE, CIRCUIT_BREAKERS_CONFIGURED | risk-management-specialist |

**Samir Varma Integration**:
- **200DMA Risk Asymmetry**: Above 200DMA = 67% returns/33% risk; Below = 33% returns/67% risk
- **5-Factor Regime Model**: Volatility, Correlation, Trend, Credit, Sentiment
- **CDAP Framework**: Context-aware drawdown management (not fixed thresholds)

### 4. Validation Layer (P9-P11) - Full Mode Only

Backtest metrics, parameter sensitivity, and historical stress testing.

| Phase | Purpose | Gate | Agent |
|-------|---------|------|-------|
| P9: BACKTEST_METRICS | Sharpe, trade count, win rate, drawdown | SHARPE_MINIMUM, TRADE_COUNT_MINIMUM | backtester |
| P10: PARAMETER_SENSITIVITY | Noise test, walk-forward validation | NOISE_ROBUST, WALK_FORWARD_VALID | sensitivity-tester |
| P11: STRESS_TESTING | GFC 2008, COVID 2020, Rate Hike 2022 | CRISIS_2008, CRISIS_2020, CRISIS_2022 | crisis-stress-tester |

**Samir Varma Integration**:
- **Noise Test**: Perturb parameters +/-10% to detect overfitting (Varma methodology)
- **Walk-Forward**: 5-fold validation across different regimes
- **Crisis Periods**: Test against actual market crises to validate survivability

### 5. Execution Layer (P12-P17) - Both Modes

Data validation, strategy generation, and deployment preparation.

| Phase | Purpose | Gate | Agent |
|-------|---------|------|-------|
| P12: DATA_CHECK | OHLCV availability, indicator dependencies | DATA (non-blocking) | market-data-specialist |
| P13: DELEGATE | Generate JSON spec + QC skeleton | - | strategy-builder |
| P14: VALIDATE | Schema, syntax, consistency check | CONSISTENCY | - |
| P15: PRESENT/REVISE | Success output or revision taxonomy | - | - |
| P16: AUDIT_TRAIL | Log all parameters for reproducibility | - | - |
| P17: DEPLOYMENT_READY | Final viability, deployment config | - | - |

---

## Gate Summary Table

### Hard Gates (Blocking)

| Gate | Phase | Threshold | Description |
|------|-------|-----------|-------------|
| UNIVERSE_DEFINED | P1 | All fields | Symbols, asset class, universe type |
| CONSTRAINTS_VALID | P2 | All fields | Date range, frequency, warmup |
| SURVIVOR_BIAS_CHECK | P3 | >= 0.7 | Universe quality score |
| PARAM_COUNT | P5 | < 10 | Maximum parameters allowed |
| PARAM_RANGES | P5 | < 3x span | Parameter range limits |
| HYPOTHESIS | P5 | >= 0.7 | Testability score |
| SIZING_METHOD_VALID | P6 | In allowed list | fixed, volatility_scaled, kelly, regime_adjusted |
| REGIME_ADJUSTMENT_CONFIGURED | P6 | If enabled | Regime factors specified |
| SLIPPAGE_SENSITIVITY_PASS | P7 | Sharpe > 0.5 | After execution costs |
| REGIME_CLASSIFICATION_COMPLETE | P8 | All 5 factors | Volatility, Correlation, Trend, Credit, Sentiment |
| CIRCUIT_BREAKERS_CONFIGURED | P8 | All 4 set | Daily loss, max DD, position, sector |
| SHARPE_MINIMUM | P9 | >= 0.5 | Risk-adjusted return threshold |
| TRADE_COUNT_MINIMUM | P9 | >= 100 | Statistical significance |
| NOISE_ROBUST | P10 | < 30% degradation | Under +/-10% parameter noise |
| WALK_FORWARD_VALID | P10 | > 50% OOS/IS | Out-of-sample vs in-sample Sharpe |
| CRISIS_2008 | P11 | < 2x benchmark DD | GFC survivability |
| CRISIS_2020 | P11 | < 50% DD | COVID shock survivability |
| CRISIS_2022 | P11 | Sharpe > 0 OR DD < 30% | Rate hike survivability |
| CONSISTENCY | P14 | Pass | Hypothesis-spec alignment |

### Soft Gates (Warning)

| Gate | Phase | Threshold | Description |
|------|-------|-----------|-------------|
| DATA | P12 | >= 0.8 | Data confidence score (requires acknowledgment if < 0.8) |
| MECHANISM_SOUNDNESS | P14 | Pass | Strategy type matches hypothesis |

---

## Agent Delegation Matrix

### Classic Mode Agents

| Agent | Phase | Purpose | Input |
|-------|-------|---------|-------|
| market-data-specialist | P3 (parallel) | Validate data availability | symbols, date_range |
| risk-management-specialist | P3 (parallel) | Classify volatility regime | symbols, lookback=252 |
| strategy-builder | P4 | Generate JSON spec + QC skeleton | hypothesis_bundle |

### Full Mode Additional Agents

| Agent | Phase | Purpose | Input |
|-------|-------|---------|-------|
| universe-selector | P3 | Survivor bias, liquidity validation | symbols, start_date, end_date |
| risk-management-specialist | P6 | Position sizing, regime adjustments | hypothesis_id, sizing_method, risk_pct |
| execution-modeler | P7 | Slippage, market impact modeling | trade_frequency, position_size, universe_adv |
| risk-management-specialist | P8 | 5-factor regime, circuit breakers | universe, regime_factors |
| backtester | P9 | HDD-compliant backtest execution | hypothesis_bundle + configs |
| sensitivity-tester | P10 | Noise test, walk-forward validation | hypothesis_id, noise_level, folds |
| crisis-stress-tester | P11 | Historical crisis stress testing | hypothesis_id, crisis_periods |
| strategy-builder | P13 | Generate JSON spec + QC skeleton | hypothesis_bundle + position_sizing |
| market-data-specialist | P12 (parallel) | Validate data availability | symbols, date_range |

---

## Mode Flags

### Workflow Depth

| Flag | Workflow | Description |
|------|----------|-------------|
| `--classic` | 6-phase (P1-P6) | Original workflow. DEFAULT when no flag specified. |
| `--full` | 17-phase (P1-P17) | Complete workflow with all layers. |

### Output Mode Flags

| Flag | Mode | Output |
|------|------|--------|
| (none) | freeform | NL idea -> hypothesis -> spec + skeleton |
| `--from-doc <path>` | doc_first | Extract strategy from existing docs |
| `--spec-only` | spec_only | Generate JSON spec only |
| `--skeleton-only` | skeleton_only | Generate QC Python only |
| `--hypothesis-only` | hypothesis_only | Generate hypothesis bundle only |

---

## Example Invocations

### Classic Mode (DEFAULT)

```bash
# Freeform strategy description
/algo-strategy "EMA crossover on SPY, 20/50 period, daily timeframe, 2% risk per trade"

# From existing document
/algo-strategy --from-doc docs/strategies/mean-reversion.md

# Hypothesis only (for review)
/algo-strategy "RSI oversold bounce on tech stocks" --hypothesis-only
```

### Full Mode

```bash
# Complete 17-phase workflow
/algo-strategy "Momentum strategy on QQQ with regime filtering" --full

# Full workflow with spec output only
/algo-strategy --from-doc docs/strategies/trend-following.md --full --spec-only
```

---

## Samir Varma Concept Integration

The 17-phase workflow incorporates key insights from Samir Varma PhD:

### 200DMA Risk Asymmetry (P6, P8)

| Market Position | Return Expectation | Risk Weight | Position Multiplier |
|-----------------|-------------------|-------------|---------------------|
| Above 200DMA | 67% | 33% | 1.0x - 1.2x |
| Below 200DMA | 33% | 67% | 0.5x - 0.8x |

### CDAP Framework (P8)

Coherent Drawdown-Adjusted Performance replaces fixed drawdown thresholds:
- Regime integration (bull/bear, volatility state)
- Cross-asset confirmation (bonds, commodities, VIX)
- Context-aware risk adjustment

### 5-Factor Regime Model (P8)

| Factor | Source | Classification |
|--------|--------|----------------|
| Volatility | ATR percentile | LOW (<p25), NORMAL (p25-p75), HIGH (>p75) |
| Correlation | Rolling correlation | LOW (<0.5), HIGH (>=0.5) |
| Trend | 200DMA position | BULL (>5%), NEUTRAL (+/-5%), BEAR (<-5%) |
| Credit | Spread levels | NORMAL, ELEVATED, STRESSED |
| Sentiment | VIX/Put-Call | FEAR, NEUTRAL, GREED |

### Anti-Overfitting Methodology (P5, P10)

- Lock parameters BEFORE testing (no post-hoc adjustment)
- Noise test: +/-10% parameter perturbation
- Walk-forward: 5-fold out-of-sample validation
- Pattern stress-testing (Varma methodology)

---

## References

- Command: `.claude/commands/algo-strategy.md`
- Samir Varma: `.claude/docs/investing/samir/samir-varma-insights.md`
- Agent Index: `.claude/docs/investing/agent-index.md`
- Quick Reference: `.claude/docs/investing/algo-strategy-quick-ref.md`
