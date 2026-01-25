---
name: pattern-detection
description: >
  Detects trading patterns (breakout, pullback, PEAD, divergence) with Dempster-Shafer multi-indicator coordination.
  Use when identifying patterns, coordinating indicator signals, or classifying market regimes.
  Trigger keywords: pattern detection, breakout, pullback, PEAD, divergence, Dempster-Shafer.
---

# Pattern Detection

Detect high-probability trading patterns using pre-computed indicators with multi-indicator confirmation, confidence scoring (0.4-0.95), and evidence bundles.

---

## Quick Reference

### 4 Pattern Types

| Pattern | Method | Confidence Range | Regime |
|---------|--------|------------------|--------|
| **Breakout** | Donchian channel + volume | 0.6-0.9 | Trending (ADX >25) |
| **Pullback** | EMA reclaim + RSI | 0.5-0.9 | Trending (ADX >25) |
| **PEAD** | SUE + gap + sentiment | 0.5-0.95 | Volatile (ATR >80th pct) |
| **Divergence** | Price vs indicator peaks | 0.4-0.9 | Ranging (ADX <20) |

### Confidence Factors (Additive)

| Factor | Bonus | Applies To |
|--------|-------|------------|
| Volume > 1.5x avg | +0.1 | Breakout, Pullback |
| ADX > 25 | +0.1 | Breakout, Pullback |
| Gap > 2% ATR | +0.1 | Breakout |
| RSI confirmation | +0.1 | Pullback |
| Sentiment alignment | +0.2 | PEAD |
| Multi-indicator agreement | +0.2 | Divergence |

---

## Workflow: Regime -> Pattern -> Coordination

```
1. CLASSIFY REGIME (ADX-based)
   |
   v
2. SELECT PATTERNS by regime
   |
   v
3. DETECT PATTERNS using pre-computed indicators
   |
   v
4. COORDINATE SIGNALS (tiered fallback)
   |
   v
5. OUTPUT with confidence scores + evidence
```

### Regime Classification

| Regime | Condition | Patterns |
|--------|-----------|----------|
| Trending | ADX > 25 | breakout, pullback, hidden_divergence |
| Ranging | ADX < 20 | regular_divergence, support_resistance |
| Volatile | ATR > 80th percentile | PEAD (news-driven) |

### Multi-Indicator Coordination

**Tiered Fallback Strategy** (based on conflict K):

| K-Conflict | Method | Rationale |
|------------|--------|-----------|
| K < 0.3 | Dempster-Shafer | Low conflict, combine evidence mathematically |
| 0.3-0.5 | Weighted Voting | Moderate conflict, use weight-based aggregation |
| K > 0.5 | Consensus | High conflict, require majority agreement |

---

## Reference Documentation

| Reference | Purpose |
|-----------|---------|
| [references/patterns.md](references/patterns.md) | 4 pattern frameworks with confidence formulas |
| [references/dempster-shafer.md](references/dempster-shafer.md) | BPA assignment, combination rule, K-conflict |
| [references/coordination.md](references/coordination.md) | Tiered fallback: DS -> Weighted -> Consensus |
| [references/regime-adaptive.md](references/regime-adaptive.md) | ADX thresholds, pattern selection per regime |

---

## Required Input Data

Pre-computed indicators (NOT computed by this skill):

| Category | Columns |
|----------|---------|
| OHLCV | open, high, low, close, volume, timestamp |
| Indicators | atr_14, ema_20, ema_50, rsi_14, adx_14, donchian_upper_20, donchian_lower_20 |
| Sentiment | zS (standardized score), burst_detected (optional) |

---

## Anti-Patterns

| Anti-Pattern | Why Wrong | Correct Approach |
|--------------|-----------|------------------|
| Over-optimizing parameters | Curve-fitting reduces forward performance | Use defaults (20-day Donchian, 14-day RSI) |
| Ignoring volume | High false positive rate | Require volume > 1.5x for breakouts |
| Single-indicator dependence | Noise sensitivity | Multi-indicator confirmation |
| Wrong regime patterns | Whipsaws in ranging markets | ADX < 20 disables breakout signals |
| Delayed PEAD analysis | Misses optimal entry | Real-time sentiment integration |
| Ignoring conflict (K > 0.5) | False confidence | Fallback to Consensus voting |

---

## Error Recovery

| Condition | Action | Confidence Impact |
|-----------|--------|-------------------|
| Missing indicator column | Skip indicator, renormalize | Flag in output |
| Insufficient history (<50 bars) | FAIL with recommendation | N/A |
| Multiple missing (>50%) | FAIL, insufficient coverage | N/A |
| Regime change mid-analysis | Continue with flag | 0.8x penalty |
| DS conflict K > 0.5 | Fallback to Consensus | Flag coordination_fallback |
