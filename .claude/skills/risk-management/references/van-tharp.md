# Van Tharp R-Multiple Position Sizing

## Core Formula

```
Position_Size = Risk_Dollars / Stop_Distance
Risk_Dollars = Account_Equity x Risk_Pct (default 1%)
Stop_Distance = |Entry_Price - Stop_Price|
```

## Example Calculation

```
Account: $100,000 | Risk: 1% = $1,000
Entry: $50.00 | Stop: $48.00 | Distance: $2.00
Position: $1,000 / $2.00 = 500 shares
Capital Required: 500 x $50 = $25,000
```

## Risk Percentage by Account Size

| Account Size | Risk % | Rationale |
|--------------|--------|-----------|
| <$25K | 0.5% | Capital preservation, PDT restrictions |
| $25K-$100K | 1.0% | Standard retail default |
| >$100K | 1.0-2.0% | Configurable based on strategy |

## R-Multiple Concepts

| Term | Definition |
|------|------------|
| R | Initial risk per trade (1R = risk_dollars) |
| +2R | Profit = 2x initial risk |
| -1R | Loss = initial risk (stopped out) |
| Expectancy | Average R-multiple across all trades |

**Position Expectancy Example**:
- 40% win rate, average win +2.5R, average loss -1R
- Expectancy = (0.4 x 2.5) + (0.6 x -1) = +0.4R per trade

## Portfolio Heat (Aggregate Risk)

```
Per_Position_Risk = Position_Size x |Entry - Stop|
Total_Risk = Sum(Per_Position_Risk)
Portfolio_Heat = (Total_Risk / Account_Equity) x 100%
```

**Limit**: 10% maximum (default)

## Confidence Scoring

| Confidence | Position Multiplier |
|------------|---------------------|
| High (>0.8) | 1.0x (full size) |
| Medium (0.5-0.8) | 0.5-0.75x |
| Low (<0.5) | Skip or 0.25x |

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Stale account equity | Fetch current equity before calculation |
| Fixed dollar risk | Always use `account_equity x risk_pct` |
| Rounding errors | Round position DOWN (conservative) |
| Ignoring slippage | Add 5-10% buffer to stop distance |