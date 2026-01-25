---
name: strategy-specification
description: 'Domain knowledge for trading strategy specification. Strategy types, JSON schema structure, 7-element framework (Universe, Entry, Exit, Sizing, Risk, Timeframe, Regime Filters), and QC integration patterns. Trigger: strategy spec, trading algorithm, QC code.'
---

# Strategy Specification

Domain knowledge for converting trading ideas into formal specifications.

---

## Quick Reference

### Strategy Types

| Type | Signal | Period | Indicators |
|------|--------|--------|------------|
| Momentum | Trend continuation | Days-weeks | EMA, Donchian, ADX |
| Mean-Reversion | Mean deviation | Hours-days | RSI, Bollinger, z-score |
| Event-Driven | Catalyst | Hours-days | SUE, sentiment |
| Multi-Factor | Combined | Weeks-months | Value, quality factors |

### 7-Element Framework

1. **Universe** - What securities to trade
2. **Entry** - Conditions to open position
3. **Exit** - Conditions to close position
4. **Sizing** - How much per trade
5. **Risk** - Portfolio-level limits
6. **Timeframe** - Bar resolution
7. **Regime Filters** - Market regime conditions (e.g., Price > 200DMA, volatility LOW/NORMAL)

---

## Strategy Specification Schema

```json
{
  "strategy_name": "string (kebab-case)",
  "strategy_type": "momentum|mean_reversion|event_driven|multi_factor",
  "universe": {
    "type": "static|dynamic|filtered",
    "symbols": ["array"],
    "filters": ["optional"]
  },
  "entry": {
    "conditions": ["array of conditions"],
    "logic": "AND|OR"
  },
  "exit": {
    "stop": {"type": "fixed|chandelier|atr", "params": {}},
    "target": {"type": "fixed|atr_multiple", "params": {}},
    "time_exit": "bars or null"
  },
  "position_sizing": {
    "method": "fixed_pct|r_multiple|volatility_scaled",
    "risk_pct": 0.01,
    "max_position_pct": 0.05
  },
  "risk_management": {
    "max_portfolio_heat": 0.10,
    "circuit_breaker": {"daily_loss_limit": 0.03}
  },
  "timeframe": "minute|hour|daily|weekly"
}
```

---

## Entry Condition Patterns

| Pattern | Example | Strategy Type |
|---------|---------|---------------|
| Crossover | `ema_20 > ema_50` | Momentum |
| Threshold | `rsi < 30` | Mean-Reversion |
| Breakout | `close > donchian_upper` | Momentum |
| Composite | `rsi < 30 AND close > sma_200` | Multi-Factor |

---

## Exit Condition Patterns

| Type | Example | Use Case |
|------|---------|----------|
| Chandelier Stop | `close < high - 3*ATR` | Trend following |
| Fixed Stop | `close < entry - 0.02*entry` | Mean reversion |
| Target | `close >= entry + 2*ATR` | Profit taking |
| Time Exit | `bars_held >= 5` | Regime-based |
| Signal Exit | `rsi > 70` | Indicator reversal |

---

## Position Sizing Methods

| Method | Formula | Risk Level |
|--------|---------|------------|
| Fixed Percent | `portfolio * 0.05` | Medium |
| R-Multiple (Van Tharp) | `(portfolio * risk_pct) / stop_distance` | Conservative |
| Volatility-Scaled | `(portfolio * target_vol) / asset_vol` | Adaptive |
| Regime-Adaptive | `R-Multiple * regime_multiplier` | Dynamic |

---

## Regime-Adaptive Position Sizing

When `method: "regime_adaptive"` is specified, position sizing scales based on market conditions.

### Formula
```
base_size = (portfolio * risk_pct) / stop_distance  # Van Tharp R-Multiple
regime = classify_regime(atr, lookback=252)
trend = classify_trend(price, sma_200)
final_size = base_size * regime_multipliers[regime] * trend_multipliers[trend]
```

### Default Multipliers

**Volatility Regime Multipliers**:
| Regime | Multiplier | Rationale |
|--------|------------|-----------|
| LOW | 1.2x | Lower volatility = larger positions, tighter stops |
| NORMAL | 1.0x | Standard position sizing |
| HIGH | 0.7x | Higher volatility = smaller positions, wider stops |

**Trend Filter Multipliers**:
| Trend | Multiplier | Rationale |
|-------|------------|-----------|
| above_200dma | 1.0x | Full sizing in bullish regime |
| below_200dma | 0.5x | Half sizing in bearish regime |

### Combined Example
```
Portfolio: $100,000
Risk per trade: 1%
Stop distance: $2.00
Base size: ($100,000 * 0.01) / $2.00 = 500 shares

Scenario A (LOW volatility, above 200DMA):
  500 * 1.2 * 1.0 = 600 shares

Scenario B (HIGH volatility, above 200DMA):
  500 * 0.7 * 1.0 = 350 shares

Scenario C (NORMAL volatility, below 200DMA):
  500 * 1.0 * 0.5 = 250 shares

Scenario D (HIGH volatility, below 200DMA):
  500 * 0.7 * 0.5 = 175 shares
```

### Integration
Regime-adaptive sizing requires delegation to `risk-management-specialist` for regime classification before position sizing calculation.

---

## Risk Parameters (Conservative Defaults)

| Parameter | Default | Max Allowed |
|-----------|---------|-------------|
| Risk per trade | 1% | 2% |
| Max position | 5% | 10% |
| Portfolio heat | 10% | 15% |
| Daily loss limit | 3% | 5% |
| Correlated positions | 3 | 5 |

---

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| Undefined exit | Always specify stop + target or time |
| Fixed dollar sizing | Use percentage-based sizing |
| No portfolio heat limit | Cap at 10-15% total risk |
| Single exit condition | Multiple conditions (stop AND target) |
---

## HDD Parameter Locking (MANDATORY)

> **Philosophy**: Every parameter is a degree of freedom. More degrees = more overfitting risk.

### Constraints

| Constraint | Limit | Violation Response |
|------------|-------|-------------------|
| Max trials per hypothesis | 5 | HALT, require new hypothesis |
| Max parameters total | 10 | WARN at 8, REJECT at 10 |
| Single change per trial | 1 | REJECT multi-param changes |
| Parameter sweep requests | 0 | REJECT "optimize", "sweep", "find best" |

### Parameter Categories

| Category | Lock Level | Rationale |
|----------|------------|-----------|
| Indicator periods (EMA, RSI, ATR) | HIGH | Core signal, high overfit risk |
| Entry/Exit thresholds | HIGH | Directly affects edge |
| Risk parameters (% per trade) | MEDIUM | Safety, not edge |
| Universe selection | LOW | Market exposure, not edge |
| Timeframe | LOW | Data granularity |

### Hypothesis-Parameter Binding

Each hypothesis MUST specify:
```json
{
  "hypothesis_id": "H001",
  "locked_parameters": [
    "ema_fast_period",
    "ema_slow_period", 
    "rsi_threshold",
    "atr_multiplier"
  ],
  "testable_parameter": "ema_fast_period",
  "test_value": 20,
  "rationale": "Testing whether 20-day EMA (monthly cycle) captures momentum better than 14-day"
}
```

### Statistical Constraints (Anti-Overfitting)

| Metric | Minimum | Maximum | Rationale |
|--------|---------|---------|-----------|
| Trade count | 100 | - | Statistical significance |
| Backtest trials on dataset | - | 30 | Dataset burn prevention |
| Parameters per indicator | - | 3 | Complexity limit |
| Total strategy parameters | - | 10 | DOF constraint |

### Deflated Sharpe Warning

When reporting Sharpe ratio, ALWAYS show deflated version:

```
DSR = SR × √(1 - skew_adj × trials)

Example:
- Raw Sharpe: 1.8
- Trials on this dataset: 12
- Deflated Sharpe: 0.6
- Verdict: NOT statistically significant after 12 trials
```

---

## Backtest Validation Gates (MUST PASS)

These gates MUST pass before a strategy can proceed beyond backtest phase.

| Gate | Threshold | Action on Fail |
|------|-----------|----------------|
| Trade Count | ≥ 100 | REJECT: "Insufficient sample size" |
| Sharpe (raw) | ≥ 0.5 | WARN: "Below statistical significance" |
| Sharpe (deflated) | ≥ 0.3 | REJECT: "Fails multiple comparison correction" |
| Max Drawdown | ≤ 25% | WARN: "High tail risk" |
| OOS/IS Sharpe Ratio | ≥ 0.5 | REJECT: "Curve-fit detected" |

### Gate Enforcement

1. **REJECT gates** are hard stops - strategy cannot proceed
2. **WARN gates** allow proceed with documented risk
3. All gates checked in order, first failure determines action

---

## Smell Tests (Auto-Flag)

| Metric | Threshold | Action |
|--------|-----------|--------|
| Sharpe > 3.0 | SUSPICIOUS | FLAG: "Likely overfitting or look-ahead bias" |
| Max DD < 5% | SUSPICIOUS | FLAG: "Unrealistic risk profile" |
| Win Rate > 70% | SUSPICIOUS | FLAG: "Check for selection bias" |
| Avg Trade < 0.1% | WARN | FLAG: "May not survive transaction costs" |
| Trades < 100 | REJECT | "Insufficient sample size" |

---

## Hypothesis-Driven Development

### Hypothesis Template
"I believe [CAUSE] leads to [EFFECT] WHEN [REGIME_CONDITION] because [WHY]"

### Required Fields
- hypothesis_id: Unique identifier (HYP-XXX)
- cause: Market condition or signal
- effect: Expected price behavior
- why: Economic/behavioral rationale
- testability_score: 0.0-1.0 (minimum 0.7)
- params_locked: Dict of locked parameter values
- trial_number: 0-5 (resets on new hypothesis)

---

## Anti-Overfit Constraints

### Hard Constraints (BLOCKING)
| Constraint | Threshold | Rationale |
|------------|-----------|-----------|
| Max parameters | <10 | Degrees of freedom |
| Max trials | <30 | Statistical significance |
| Parameter ranges | <3x span | Optimization surface |

### Soft Constraints (WARNING)
| Constraint | Threshold | Rationale |
|------------|-----------|-----------|
| Min trades | >100 | Sample size |
| IS/OOS delta | <30% | Generalization |

---

## Documentation Extraction Patterns

### Supported Locations
- `docs/investing/*.md` - Architecture/design docs
- `.claude/agents/investing/*/templates/*.py` - QC templates

### Element Extraction Rules
- Universe: Look for "symbols", "universe", "securities"
- Entry: Look for "entry", "buy", "long condition"
- Exit: Look for "exit", "sell", "close position"
- Sizing: Look for "position size", "allocation"
- Risk: Look for "stop loss", "risk", "max drawdown"
- Timeframe: Look for "daily", "hourly", "resolution"
---

## Regime-Aware Strategy Validation

Every strategy MUST be tested across volatility regimes to ensure robustness.

### Volatility Regime Definitions

| Regime | ATR Percentile | Description |
|--------|----------------|-------------|
| LOW | < p25 | Calm markets, low volatility |
| NORMAL | p25 - p75 | Typical market conditions |
| HIGH | > p75 | Elevated volatility, stress periods |

### Regime Testing Requirements

1. **Minimum Coverage**: Strategy must have trades in all 3 regimes
2. **Performance Threshold**: Sharpe ≥ 0.3 in each regime (not just aggregate)
3. **Regime Attribution**: If strategy fails in ONE regime only, add regime filter

### Regime Failure Attribution

| Failure Pattern | Diagnosis | Action |
|-----------------|-----------|--------|
| Fails HIGH only | Volatility-sensitive | Add HIGH regime filter → NEW hypothesis |
| Fails LOW only | Needs volatility | Add LOW regime filter → NEW hypothesis |
| Fails NORMAL only | Unusual, investigate | Check for implementation bug |
| Fails ALL regimes | No edge found | ARCHIVE to graveyard |

### Regime Filter Syntax

When adding regime filter, hypothesis must specify:
```json
{
  "regime_filter": {
    "allowed_regimes": ["LOW", "NORMAL"],
    "excluded_regimes": ["HIGH"],
    "atr_lookback": 22,
    "percentile_window": 252
  }
}
```

### Cross-Regime Correlation

| Metric | Threshold | Interpretation |
|--------|-----------|----------------|
| Regime correlation < 0.3 | GOOD | Strategy adapts to conditions |
| Regime correlation 0.3-0.7 | OK | Some regime dependency |
| Regime correlation > 0.7 | WARN | Strategy may be regime-locked |
---

## Regime-Adaptive Circuit Breaker

Circuit breaker thresholds adjust based on current volatility regime. Tighter thresholds in LOW volatility (anomaly detection), looser in HIGH volatility (expected variance).

### Threshold by Regime

| Regime | WARNING | CRITICAL | BREAKER |
|--------|---------|----------|---------|
| LOW | -1.0% | -1.5% | -2.0% |
| NORMAL | -1.5% | -2.1% | -3.0% |
| HIGH | -2.0% | -3.0% | -4.0% |

### State Transitions

| Current State | Trigger | New State | Action |
|---------------|---------|-----------|--------|
| NORMAL | Daily loss ≥ WARNING | WARNING | Reduce position size 50% |
| WARNING | Daily loss ≥ CRITICAL | CRITICAL | Exit-only mode, no new positions |
| CRITICAL | Daily loss ≥ BREAKER | BREAKER | All trading halted |
| Any | Session close (4:00 PM ET) | NORMAL | Reset for new session |

### Regime Detection for Circuit Breaker

```python
# Pseudocode for regime detection
atr_current = ATR(22)
atr_percentile = percentile_rank(atr_current, lookback=252)

if atr_percentile < 25:
    regime = "LOW"
elif atr_percentile > 75:
    regime = "HIGH"
else:
    regime = "NORMAL"
```

### Integration with Risk Management

The circuit breaker integrates with the risk-management skill:
- Uses ATR from `technical-indicators` skill
- Reports state to `hypothesis-tracking` for trial metadata
- Failure during BREAKER state → check for regime_mismatch failure mode
