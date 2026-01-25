---
name: risk-management
description: >
  Manages position sizing using Van Tharp R-multiples and 4-state circuit breaker.
  Use when calculating position size, placing stops, tracking portfolio heat, or managing circuit breaker state.
  Trigger keywords: position sizing, R-multiple, circuit breaker, portfolio heat, stop loss.
---

# Risk Management Skill

*Van Tharp R-multiple position sizing with 4-state circuit breaker protection*

## Quick Reference

### Position Sizing Formula (Van Tharp)

```
Position_Size = Risk_Dollars / Stop_Distance
Risk_Dollars = Account_Equity x Risk_Pct (default 1%)
Stop_Distance = |Entry_Price - Stop_Price|
```

**Example**: $100K account, 1% risk = $1,000. Entry $50, Stop $48 = $2 distance.
Position = $1,000 / $2 = 500 shares ($25K capital required).

### Portfolio Heat Limit

```
Heat_Pct = (Sum(Position_Risk) / Account_Equity) x 100
Limit: 10% maximum (default)
```

---

## Cross-Skill Dependencies

**ATR Calculation**: This skill does NOT compute ATR internally.

| Dependency | Source Skill | Request Format | Fallback |
|------------|--------------|----------------|----------|
| ATR(22) | `technical-indicators` | "Calculate ATR(22) for {symbol}" | 2% fixed stop |

**Delegation Protocol**:
1. Request ATR(22) from `technical-indicators` skill
2. If response within timeout (5s): Use ATR value for Chandelier stop
3. If unavailable after 2 retries: Apply 2% fixed stop fallback
4. Log which method was used in position sizing rationale

**Why Delegation**: ATR requires OHLCV data and TA-Lib/pandas-ta. Risk management focuses on position sizing math, not indicator computation.

---

## Circuit Breaker States

| State | Loss Threshold | Position Sizing | Actions |
|-------|----------------|-----------------|---------|
| NORMAL | <1.5% | 100% | Full trading |
| WARNING | 1.5% - 2.1% | 50% | Alerts enabled |
| CRITICAL | 2.1% - 3.0% | 0% (exit-only) | No new positions |
| BREAKER | >=3.0% | 0% (halted) | All trading suspended |

**Transitions**: Immediate when threshold breached. No hysteresis.
**Reset**: Session-based only (4:00 PM ET market close).

---

## Chandelier Stops (ATR-Based)

**Long**: `Stop = Highest_High(22) - (ATR(22) x 3.0)`
**Short**: `Stop = Lowest_Low(22) + (ATR(22) x 3.0)`

**Key Rules**:
- Same period (22) for ATR and high/low lookback
- Stops only move favorably (lock profits)
- Update at bar close only

**Fallback**: If ATR unavailable after 2 retries, use 2% fixed stop.

---

## Workflow

```
1. Check circuit breaker state
2. Get ATR from technical-indicator-specialist (or use fallback)
3. Calculate Chandelier stop
4. Apply Van Tharp formula: shares = risk_dollars / stop_distance
5. Validate constraints (buying power, heat, stop side)
6. Return position sizing with rationale
```

---

## Reference Documentation

| Reference | Purpose |
|-----------|---------|
| [references/van-tharp.md](references/van-tharp.md) | Position sizing formula, risk percentages by account |
| [references/chandelier-stops.md](references/chandelier-stops.md) | ATR-based stop formulas, trailing logic |
| [references/circuit-breaker.md](references/circuit-breaker.md) | 4-state machine, transitions, reset rules |
| [references/validation-rules.md](references/validation-rules.md) | Buying power, stop side, heat constraints |

---

## Anti-Patterns

| Anti-Pattern | Why Wrong | Correct Approach |
|--------------|-----------|------------------|
| Fixed dollar stops | Ignores volatility | ATR-based Chandelier stops |
| Position without stop | Unlimited risk exposure | Always define stop first |
| Exceed 10% heat | Portfolio concentration risk | Reject new positions |
| Override circuit breaker | Defeats safety mechanism | Respect state restrictions |
| Percentage stops | One-size-fits-all ignores price action | Use ATR x 3.0 multiplier |
| Move stop against position | Gives back locked profits | Stops only move favorably |

---

## Validation Checklist

Before position sizing output:

- [ ] Circuit breaker state checked (NORMAL or WARNING for entry)
- [ ] Stop calculated (ATR-based or 2% fallback)
- [ ] Formula: `shares = risk_dollars / stop_distance`
- [ ] Stop on correct side (long: stop < entry, short: stop > entry)
- [ ] Risk match: `shares x stop_distance = risk_dollars` (within $1)
- [ ] Buying power: `shares x entry <= available_capital`
- [ ] Heat check: `current_heat + new_risk <= 10%`