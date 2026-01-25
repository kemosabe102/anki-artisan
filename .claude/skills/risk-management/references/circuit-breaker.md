# Trading Circuit Breaker Pattern

## Four-State Machine

| State | Loss Threshold | Position Sizing | Actions |
|-------|----------------|-----------------|---------|
| NORMAL | <1.5% | 100% | Full trading |
| WARNING | 1.5% - 2.1% | 50% | Alerts enabled |
| CRITICAL | 2.1% - 3.0% | 0% (exit-only) | No new positions |
| BREAKER | >=3.0% | 0% (halted) | All trading suspended |

## State Transition Formula

```python
loss_pct = (current_pnl / starting_equity) x 100

if loss_pct <= -3.0%:    state = BREAKER
elif loss_pct <= -2.1%:  state = CRITICAL
elif loss_pct <= -1.5%:  state = WARNING
else:                     state = NORMAL
```

## Threshold Rationale

| Threshold | % of Daily Limit | Purpose |
|-----------|------------------|---------|
| 1.5% | 50% | Early warning, reduce exposure |
| 2.1% | 70% | Near limit, exit-only mode |
| 3.0% | 100% | Full halt, protect capital |

## Order Approval Logic

| State | Entry Orders | Exit Orders |
|-------|--------------|-------------|
| NORMAL | Approve (100%) | Approve |
| WARNING | Approve (50% size) | Approve |
| CRITICAL | REJECT | Approve |
| BREAKER | REJECT | REJECT |

## Session-Based Reset

- **Reset Time**: Market close (4:00 PM ET for US equities)
- **New Starting Equity**: `previous_starting + final_pnl`
- **Reset Frequency**: Once per trading day only
- **NO intraday resets** (prevents gaming the system)

## Key Rules

1. **Graduated transitions**: States escalate, never skip
2. **No hysteresis**: Transition immediately when threshold breached
3. **Session integrity**: Track starting equity per session
4. **Audit trail**: Log all state transitions with timestamps
5. **Include unrealized**: Count unrealized P&L, not just realized

## Implementation Pattern

```python
class TradingCircuitBreaker:
    def can_enter_position(self) -> bool:
        return self.state in [NORMAL, WARNING]
    
    def get_position_multiplier(self) -> float:
        return {
            NORMAL: 1.0,
            WARNING: 0.5,
            CRITICAL: 0.0,
            BREAKER: 0.0
        }[self.state]
```

## Anti-Patterns

| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Time-based resets | Allows gaming | Session-based only |
| Binary halt | No early warning | Use graduated states |
| Manual override | Defeats purpose | No override during session |
| Realized P&L only | Hides paper losses | Include unrealized |