---
name: market-data-validation
description: >
  Validates OHLCV market data using 8-field schema and 7 consistency rules.
  Use when checking data quality, handling API fallbacks, or processing missing data.
  Trigger keywords: OHLCV, data quality, validation, market data, API connector.
---

# Market Data Validation

Validate financial time-series data quality through systematic OHLCV schema checks and consistency rules.

---

## Quick Reference

### 8-Field Schema

| Field | Type | Format |
|-------|------|--------|
| open | float64 | >= 0 |
| high | float64 | >= 0 |
| low | float64 | >= 0 |
| close | float64 | >= 0 |
| volume | int64 | >= 0 |
| timestamp | datetime64 | ISO 8601 UTC (YYYY-MM-DDTHH:MM:SSZ) |
| adj_close | float64 | >= 0 |
| ticker | string | 1-5 uppercase alphanumeric |

### 7 Consistency Rules

1. `High >= max(Open, Close)`
2. `Low <= min(Open, Close)`
3. `High >= Low`
4. `Volume >= 0`
5. No negative prices (Open, High, Low, Close, AdjClose >= 0)
6. Chronological ordering (timestamps strictly increasing)
7. Valid ticker format (regex: `^[A-Z0-9]{1,5}$`)

---

## Quality Thresholds

| Pass Rate | Action | Rationale |
|-----------|--------|-----------|
| >= 99% | **ACCEPT** | High-quality dataset, minor violations acceptable |
| 95-99% | **WARNING** | Accept with normalization, flag for review |
| < 95% | **QUARANTINE** | Reject, generate violation report, escalate |

---

## Workflow: 6-Phase Ingestion Pipeline

```
1. Acquisition → 2. Schema Validation → 3. Consistency Validation
        ↓                  ↓                      ↓
4. Missing Data Handling → 5. Corporate Actions → 6. Final Validation & Storage
```

**Phase Details**:
1. **Acquisition**: Fetch from API/file, normalize to DataFrame
2. **Schema Validation**: Verify 8 fields present, correct types
3. **Consistency Validation**: Apply 7 rules, flag violations with row indices
4. **Missing Data**: Forward-fill (<=5 bars), omit with flag (>5 bars)
5. **Corporate Actions**: Apply splits/dividends, preserve unadjusted prices
6. **Storage**: Persist with quality metadata, audit trail

---

## Reference Documentation

Detailed guides for specific validation scenarios:

| Reference | Purpose |
|-----------|---------|
| [references/ohlcv-schema.md](references/ohlcv-schema.md) | 8-field schema, 7 consistency rules with examples |
| [references/api-fallback.md](references/api-fallback.md) | Alpaca->Polygon->Yahoo chain, circuit breaker |
| [references/missing-data.md](references/missing-data.md) | Forward-fill, omit, interpolation strategies |
| [references/corporate-actions.md](references/corporate-actions.md) | Splits, dividends, CRSP methodology |

---

## Anti-Patterns

| Anti-Pattern | Why Wrong | Correct Approach |
|--------------|-----------|------------------|
| Skip validation for "trusted" sources | All data can corrupt in transit | `validate_all=True` always |
| Backward fill in backtesting | Creates look-ahead bias | Forward-fill or omit only |
| Interpolate volume data | Volume interpolation meaningless | Use NaN or forward-fill |
| Raise exceptions for API errors | Breaks orchestrator flow | Return status codes |

---

## Compliance Standards

- **FINRA Rule 6893**: Timeliness, accuracy, integrity, completeness
- **ISO 8601**: UTC timestamp format (unambiguous)
- **CRSP**: Adjusted close methodology for corporate actions

