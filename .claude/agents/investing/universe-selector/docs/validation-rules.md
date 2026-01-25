# Validation Rules

## Gate Definitions

### UNIVERSE_DEFINED (HARD)
**Purpose**: Ensure all input symbols are valid and parseable.

**Criteria**:
- Symbol matches pattern: `^[A-Z]{1,5}$`
- Asset class identifiable
- No duplicate symbols

**Failure**: Immediate FAIL, list invalid symbols

### SURVIVOR_BIAS_CHECK (HARD)
**Purpose**: Prevent lookback bias from delisted/acquired securities.

**Criteria**:
- No symbols delisted within date range
- No M&A events affecting symbol
- Point-in-time composition valid

**Failure**: FAIL, list excluded symbols with reasons

### LIQUIDITY_VALID (HARD)
**Purpose**: Ensure universe is tradeable with acceptable slippage.

**Criteria**:
- ADV >= `min_adv` (default: $1M)
- Market cap >= `min_market_cap` (default: $100M)

**Failure**: FAIL, list illiquid symbols

### DATA_AVAILABLE (HARD)
**Purpose**: Verify sufficient OHLCV data for backtesting.

**Criteria**:
- Coverage >= `min_data_coverage` (default: 95%)
- No critical gaps (>5 consecutive days)

**Failure**: FAIL, list symbols with insufficient data

### SECTOR_BALANCED (SOFT)
**Purpose**: Warn on concentration risk.

**Criteria**:
- No single sector > `max_sector_concentration` (default: 40%)

**Failure**: WARN only (does not block PASS status)

## Quality Score Formula

```
universe_quality_score = 
    (universe_defined_score * 0.15) +
    (survivor_bias_score * 0.25) +
    (liquidity_score * 0.25) +
    (data_available_score * 0.25) +
    (sector_balanced_score * 0.10)
```

### Per-Gate Scoring

| Gate | Pass Score | Partial Score | Fail Score |
|------|------------|---------------|------------|
| UNIVERSE_DEFINED | 100 | N/A | 0 |
| SURVIVOR_BIAS_CHECK | 100 | 100 - (excluded_pct * 100) | 0 if all fail |
| LIQUIDITY_VALID | 100 | 100 - (illiquid_pct * 100) | 0 if all fail |
| DATA_AVAILABLE | coverage_pct * 100 | coverage_pct * 100 | 0 |
| SECTOR_BALANCED | 100 if < 40% | 80 if 40-50% | 60 if > 50% |

## Default Thresholds

| Parameter | Default | Range | Notes |
|-----------|---------|-------|-------|
| `min_adv` | $1,000,000 | $100K - $100M | Average daily volume |
| `min_market_cap` | $100,000,000 | $10M - $10B | Market capitalization |
| `min_data_coverage` | 0.95 | 0.80 - 1.00 | OHLCV completeness |
| `max_sector_concentration` | 0.40 | 0.25 - 0.60 | Single sector limit |
| `lookback_buffer_days` | 252 | 60 - 504 | Survivor bias window |
