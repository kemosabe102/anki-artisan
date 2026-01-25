# Van Tharp R-Multiple Position Sizing

## Core Formula

```
Position_Size = Risk_Dollars / Stop_Distance
Risk_Dollars = Account_Equity × Risk_Pct (default 1%)
Stop_Distance = |Entry_Price - Stop_Price|
```

## Example Calculation

```
Account: $100,000 | Risk: 1% = $1,000
Entry: $50.00 | Stop: $48.00 | Distance: $2.00
Position: $1,000 / $2.00 = 500 shares
Capital Required: 500 × $50 = $25,000
```

## Risk Percentage Selection

| Account Size | Risk % | Rationale |
|--------------|--------|-----------|
| <$25K | 0.5% | Capital preservation |
| $25K-$100K | 1.0% | Standard retail |
| >$100K | 1.0-2.0% | Configurable |

## Portfolio Heat (Aggregate Risk)

```
Per_Position_Risk = Position_Size × |Entry - Stop|
Total_Risk = Sum(Per_Position_Risk)
Portfolio_Heat = (Total_Risk / Account_Equity) × 100%
```

**Limit**: 5-10% (default 10%)

## Validation Rules

1. **Buying Power**: `position_size × entry_price <= available_capital`
2. **Risk Match**: `position_size × stop_distance ≈ risk_dollars` (within $1)
3. **Stop Side**: Long: `stop < entry` | Short: `stop > entry`
4. **Heat Check**: `current_heat + new_risk <= max_heat`

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Stale account equity | Fetch current equity before each calculation |
| Fixed dollar risk (not %) | Always use `account_equity × risk_pct` |
| Rounding errors | Round position DOWN (conservative) |
| Ignoring slippage | Add 5-10% buffer to stop distance |

## Integration

**Upstream**: ATR from technical-indicator-specialist for stop calculation
**Downstream**: Orchestrator submits entry + stop order pair

## Confidence-Scaled Position Sizing (Skepticism-First)

**Philosophy**: More noise than signal in markets. Pattern confidence should directly scale position risk - less confident patterns get smaller allocations.

### Formula

```
effective_risk_pct = base_risk_pct × pattern_confidence
position_size = (account_equity × effective_risk_pct × regime_multiplier) / stop_distance
```

Where:
- `base_risk_pct` = 1% (default Van Tharp R-multiple, preserved)
- `pattern_confidence` = 0.4-0.95 (from pattern-detector)
- `regime_multiplier` = volatility adjustment (0.7-1.2)

### Watchlist Routing (Confidence Floor)

**IF pattern_confidence < 0.5**:
- Route to WATCHLIST (observation only)
- NO position sizing calculation performed
- Log: "Pattern confidence {conf} below 0.5 floor. Routed to watchlist."
- Watchlist entries have 72-hour TTL by default

**IF pattern_confidence >= 0.5**:
- Apply scaling: `effective_risk = base_risk × confidence`
- Continue normal position sizing flow

### Examples

| Pattern Confidence | Base Risk | Effective Risk | Position Action |
|-------------------|-----------|----------------|-----------------|
| 0.45 | 1% | N/A | Watchlist (below floor) |
| 0.50 | 1% | 0.50% | Execute (minimum) |
| 0.65 | 1% | 0.65% | Execute |
| 0.75 | 1% | 0.75% | Execute |
| 0.85 | 1% | 0.85% | Execute |
| 0.95 | 1% | 0.95% | Execute (maximum) |

**Full Calculation Example**:
- Account equity: $100,000
- Pattern confidence: 0.75
- Regime multiplier: 1.0 (normal volatility)
- Entry price: $50
- Stop price: $48 (stop distance: $2)

```
effective_risk_pct = 1% × 0.75 = 0.75%
risk_dollars = $100,000 × 0.0075 = $750
position_size = $750 / $2 = 375 shares
```

Compare to without confidence scaling: 500 shares at 1% risk.

### Integration with Existing Multipliers

The confidence scaling stacks multiplicatively with regime_multiplier:

```
final_position = base_position × pattern_confidence × regime_multiplier

Example (all factors active):
- Base: 500 shares (1% risk)
- Pattern confidence: 0.75 → 375 shares
- Regime (HIGH vol): 0.7 → 262 shares
```

This ensures conservative sizing when BOTH pattern confidence is moderate AND market volatility is elevated.
