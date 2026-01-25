# Delegation Examples

## Full Universe Validation

```markdown
Task(universe-selector, "Validate universe ['SPY', 'QQQ', 'IWM', 'DIA', 'VTI'] for backtest period 2020-01-01 to 2024-12-31. Apply all 5 validation gates. Return universe_quality_score and list of validated_symbols.")
```

**Expected Output**: JSON with status, quality score, gate results, validated symbols

## Survivor Bias Check Only

```markdown
Task(universe-selector, "Check ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'META'] for survivor bias from 2015-01-01 to present. Flag any symbols that were delisted, acquired, or underwent major restructuring. Include exclusion reasons.")
```

**Use Case**: Pre-screening before full validation

## Sector Concentration Analysis

```markdown
Task(universe-selector, "Analyze sector concentration for ['XLF', 'XLK', 'XLE', 'XLV', 'XLI', 'XLY', 'XLP', 'XLB', 'XLRE', 'XLU']. Report sector breakdown and flag if any sector exceeds 40% concentration.")
```

**Use Case**: Portfolio diversification check

## Custom Thresholds

```markdown
Task(universe-selector, "Validate ['AAPL', 'MSFT', 'GOOGL'] with custom thresholds: min_adv=$5M, min_market_cap=$500M, min_data_coverage=0.98, max_sector_concentration=0.30. Date range: 2022-01-01 to 2024-12-31.")
```

**Use Case**: Stricter institutional-grade validation

## ETF Universe Screening

```markdown
Task(universe-selector, "Validate ETF universe ['SPY', 'QQQ', 'IWM', 'EFA', 'EEM', 'AGG', 'TLT', 'GLD', 'VNQ'] for multi-asset strategy backtest 2018-01-01 to 2024-12-31. Check for survivorship, liquidity, and cross-asset sector exposure.")
```

**Use Case**: Multi-asset allocation strategy

## Integration with algo-strategy

```markdown
# In algo-strategy P1-P3 Definition Layer:
Task(universe-selector, "Validate hypothesis universe: {hypothesis.universe}. Date range: {hypothesis.backtest_start} to {hypothesis.backtest_end}. Return validation result for UNIVERSE_DEFINED gate.")
```

**Use Case**: Automated gate check in algo-strategy workflow
