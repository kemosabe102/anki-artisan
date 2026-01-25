---
title: Algo-Strategy Quick Reference Card
date: 2025-01-09
status: active
tags: [algo-strategy, quick-reference, cheatsheet, investing]
---

# Algo-Strategy Quick Reference Card

> One-page reference for /algo-strategy command usage.

---

## Command Syntax

```bash
/algo-strategy <description> [flags]
/algo-strategy --from-doc <path> [flags]
```

---

## Mode Flags

| Flag | Effect |
|------|--------|
| `--classic` | 6-phase workflow (DEFAULT) |
| `--full` | 17-phase workflow with all validation |
| `--from-doc <path>` | Extract strategy from document |
| `--spec-only` | Output JSON spec only |
| `--skeleton-only` | Output QC Python only |
| `--hypothesis-only` | Output hypothesis bundle only |

---

## Quick Examples

```bash
# Basic strategy (classic mode)
/algo-strategy "EMA 20/50 crossover on SPY, daily, 2% risk"

# Full validation workflow
/algo-strategy "Momentum on QQQ with regime filter" --full

# From document
/algo-strategy --from-doc docs/strategies/mean-reversion.md

# Hypothesis review only
/algo-strategy "RSI bounce on tech" --hypothesis-only
```

---

## 7 Required Elements

Every strategy must define:

1. **Universe**: SPY, QQQ, tech stocks
2. **Entry Signal**: EMA crossover, RSI oversold
3. **Exit Signal**: Trailing stop, profit target
4. **Timeframe**: 4-hour, daily
5. **Position Sizing**: 2% risk per trade
6. **Risk Management**: Stop loss at 2 ATR
7. **Regime Filters**: Price > 200DMA, volatility LOW/NORMAL

---

## Gate Pass/Fail Criteria

### Hard Gates (Block on Fail)

| Gate | Threshold | Fix If Fails |
|------|-----------|--------------|
| PARAM_COUNT | < 10 params | Reduce parameters |
| PARAM_RANGES | < 3x span | Narrow ranges |
| HYPOTHESIS | testability >= 0.7 | Improve formulation |
| SURVIVOR_BIAS_CHECK | quality >= 0.7 | Revise universe |
| SLIPPAGE_SENSITIVITY | Sharpe > 0.5 after costs | Reduce position size |
| SHARPE_MINIMUM | >= 0.5 | Refine entry/exit |
| TRADE_COUNT | >= 100 trades | Extend backtest |
| NOISE_ROBUST | < 30% degradation | Reduce sensitivity |
| WALK_FORWARD | OOS > 50% IS | Simplify strategy |
| CRISIS_2008 | DD < 2x benchmark | Add regime filter |
| CRISIS_2020 | DD < 50% | Add circuit breaker |
| CRISIS_2022 | Sharpe > 0 OR DD < 30% | Add rate filter |

### Soft Gates (Warning Only)

| Gate | Threshold | Note |
|------|-----------|------|
| DATA | confidence >= 0.8 | Requires acknowledgment if < 0.8 |
| MECHANISM_SOUNDNESS | Pass | Strategy type matches hypothesis |

---

## Error Code Quick Lookup

### Input Errors (P1-P5)

| Code | Issue | Fix |
|------|-------|-----|
| ALGO_ERR_001 | < 7 elements | Provide missing elements |
| ALGO_ERR_002 | Untestable hypothesis | Reformulate cause/effect/why |
| ALGO_ERR_004 | Too many params | Reduce to < 10 |

### Definition Errors (P1-P3, Full)

| Code | Issue | Fix |
|------|-------|-----|
| ALGO_ERR_010 | Universe undefined | List explicit tickers |
| ALGO_ERR_015 | Survivor bias > 30% | Remove delisted symbols |
| ALGO_ERR_017 | Quality < 0.5 | Major universe revision |

### Strategy Layer Errors (P6-P8, Full)

| Code | Issue | Fix |
|------|-------|-----|
| ALGO_ERR_020 | Invalid sizing method | Use: fixed, volatility_scaled, kelly, regime_adjusted |
| ALGO_ERR_021 | Slippage > 50 bps | Reduce size or increase liquidity |
| ALGO_ERR_025 | Regime incomplete | Provide data for all 5 factors |
| ALGO_ERR_026 | Missing breakers | Set all 4 circuit breakers |

### Validation Errors (P9-P11, Full)

| Code | Issue | Fix |
|------|-------|-----|
| ALGO_ERR_030 | Sharpe < 0.5 | Improve entry/exit or add regime filter |
| ALGO_ERR_031 | Trades < 100 | Extend period or relax conditions |
| ALGO_ERR_035 | Noise fail > 30% | Reduce parameter sensitivity |
| ALGO_ERR_036 | Walk-forward fail | Simplify or archive hypothesis |
| ALGO_ERR_038 | GFC fail | Add bear market filter |
| ALGO_ERR_039 | COVID fail | Add volatility protection |
| ALGO_ERR_040 | 2022 fail | Add rate sensitivity filter |

---

## Regime Quick Reference

### 200DMA Position (Varma)

| Position | Returns | Risk | Sizing |
|----------|---------|------|--------|
| Above 200DMA | 67% | 33% | 1.0x-1.2x |
| Below 200DMA | 33% | 67% | 0.5x-0.8x |

### Volatility Regime

| Regime | ATR Percentile | Multiplier |
|--------|----------------|------------|
| LOW | < 25th | 1.2x |
| NORMAL | 25th-75th | 1.0x |
| HIGH | > 75th | 0.7x |

### Circuit Breakers (Defaults)

| Breaker | Default | Range |
|---------|---------|-------|
| Daily loss | -3% | -1% to -5% |
| Max drawdown | -15% | -10% to -25% |
| Position | 10% | 5% to 20% |
| Sector | 25% | 15% to 40% |

---

## Hypothesis Template

```text
"I believe [CAUSE] leads to [EFFECT] WHEN [REGIME] because [WHY]"
```

**Example**:
```text
"I believe EMA(20) crossing above EMA(50) leads to 
sustained upward momentum WHEN price is above 200DMA 
in LOW/NORMAL volatility because institutional 
traders use these levels for position entry."
```

---

## Anti-Overfit Checklist

- [ ] Parameters < 10
- [ ] Parameter ranges < 3x span
- [ ] Parameters locked BEFORE testing
- [ ] Trade count >= 100
- [ ] Noise test: < 30% degradation
- [ ] Walk-forward: OOS > 50% IS

---

## Related Documentation

| Doc | Location |
|-----|----------|
| Workflow Details | `.claude/docs/investing/algo-strategy-workflow.md` |
| Agent Index | `.claude/docs/investing/agent-index.md` |
| Samir Varma | `.claude/docs/investing/samir/samir-varma-insights.md` |
| Command | `.claude/commands/algo-strategy.md` |
