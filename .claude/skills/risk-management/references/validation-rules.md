# Position Sizing Validation Rules

## Pre-Calculation Checks

| Check | Rule | Failure Action |
|-------|------|----------------|
| Circuit Breaker | State = NORMAL or WARNING | REJECT position |
| Account Equity | equity > 0 | REJECT position |
| Entry Price | price > 0 | REJECT position |
| Risk Percentage | 0 < risk_pct <= 0.05 | Cap at 5% |

## Position Sizing Validation

### 1. Buying Power Check

```
position_value = position_size x entry_price
PASS: position_value <= available_capital
FAIL: Reduce position to fit or REJECT
```

### 2. Risk Match Check

```
actual_risk = position_size x stop_distance
expected_risk = account_equity x risk_pct
PASS: |actual_risk - expected_risk| <= $1
FAIL: Recalculate position size
```

### 3. Stop Side Check

**Long Position**:
```
PASS: stop_price < entry_price
FAIL: Invalid stop (would trigger immediately)
```

**Short Position**:
```
PASS: stop_price > entry_price
FAIL: Invalid stop (would trigger immediately)
```

### 4. Portfolio Heat Check

```
current_heat = sum(existing_position_risks) / account_equity
new_heat = current_heat + (new_risk / account_equity)
PASS: new_heat <= max_heat (default 10%)
FAIL: REJECT or reduce position to fit
```

## Post-Calculation Validation

| Validation | Formula | Tolerance |
|------------|---------|-----------|
| Position non-negative | shares > 0 | Exact |
| Risk within tolerance | |actual - expected| / expected | <= 1% |
| Round direction | floor(shares) | Always down |
| Capital utilization | value / equity | <= 25% per position |

## Constraint Priority

When multiple constraints conflict, apply in order:

1. **Circuit Breaker** (hard stop)
2. **Portfolio Heat** (aggregate limit)
3. **Buying Power** (capital limit)
4. **Risk Match** (formula accuracy)

## Error Responses

| Constraint | Error Code | Message |
|------------|------------|---------|
| Circuit Breaker | CB_HALT | "Trading halted: circuit breaker active" |
| Heat Exceeded | HEAT_MAX | "Portfolio heat would exceed 10%" |
| Buying Power | CAPITAL_INSUF | "Insufficient buying power" |
| Stop Invalid | STOP_SIDE | "Stop on wrong side of entry" |

## Validation Output Format

```json
{
  "status": "APPROVED|REJECTED|ADJUSTED",
  "position_size": 500,
  "stop_price": 48.00,
  "risk_dollars": 1000,
  "validations": {
    "circuit_breaker": "PASS",
    "buying_power": "PASS",
    "risk_match": "PASS",
    "stop_side": "PASS",
    "heat_check": "PASS"
  },
  "warnings": [],
  "adjustments": []
}
```