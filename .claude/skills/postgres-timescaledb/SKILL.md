---
name: postgres-timescaledb
description: >
  Use this skill when writing SQL queries for TimescaleDB hypertables, optimizing
  chunk exclusion, creating continuous aggregates, or configuring compression.
  Covers financial time-series query patterns and fixed-date optimization.
  Trigger keywords: TimescaleDB, hypertable, chunk exclusion, continuous aggregate,
  cagg, compression, time_bucket, fixed dates, NOW() optimization.
---

# PostgreSQL/TimescaleDB Query Optimization

*Performance-first SQL patterns for TimescaleDB hypertables with 16x speedup techniques.*

## Table of Contents

1. [Chunk Exclusion Optimization](#chunk-exclusion-optimization)
2. [Query Creation Modes](#query-creation-modes)
3. [Continuous Aggregates](#continuous-aggregates)
4. [Compression Configuration](#compression-configuration)
5. [Index Strategy Quick Reference](#index-strategy-quick-reference)
6. [Reference Documentation](#reference-documentation)

---

## Chunk Exclusion Optimization

**CRITICAL**: Volatile expressions (`NOW()`, `CURRENT_DATE`) disable chunk exclusion, causing 16x slower queries.


### Problem: Volatile Expressions

```sql
-- SLOW (48-64s): Scans ALL chunks, then filters
SELECT symbol, date, close FROM market_data
WHERE date >= NOW() - INTERVAL '200 days' AND symbol = 'AAPL';
-- EXPLAIN: Chunks Excluded: 0
```

### Solution: Fixed Dates (16x Faster)

```sql
-- FAST (3-4s): Query planner knows exact chunk boundaries
SELECT symbol, date, close FROM market_data
WHERE date >= '2025-05-09' AND date < '2025-11-25' AND symbol = 'AAPL';
-- EXPLAIN: Chunks Excluded: 3135 (94% reduction)
```

### Python Implementation

```python
from datetime import datetime, timedelta

def query_with_chunk_exclusion(symbol: str, days: int = 200):
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)
    # CRITICAL: Fixed dates as parameters, NOT NOW() in SQL
    return f"WHERE date >= '{start_date}' AND date < '{end_date}'"
```

---

## Query Creation Modes


### create_query Mode

**Process**: Requirements -> Schema check -> Draft -> EXPLAIN -> Optimize

1. Gather requirements (tables, filters, aggregations)
2. Check schema in `COMPONENT_ALMANAC.md`
3. Draft query with fixed dates (not `NOW()`)
4. Validate with `EXPLAIN` (no ANALYZE on production)
5. Apply optimization patterns

**Output**: SQL query + EXPLAIN estimate + usage notes

### optimize_query Mode

**Process**: Crash risk check -> Bottleneck analysis -> Fix

1. **Crash Risk**: Check for crash-prone patterns (GROUP BY on full hypertable)
2. **EXPLAIN Analysis**: Look for Seq Scan, missing indexes, Chunks Excluded: 0
3. **Apply Fix**: Fixed dates, proper indexes, batch processing

**Crash Risk Indicators**:
- `row_count > 1M` + `GROUP BY` = potential OOM
- `Chunks Excluded: 0` = 16x slowdown
- `Seq Scan` on hypertable = missing index

### design_indexes Mode

**Process**: Query pattern analysis -> Index recommendation

Analyze query patterns, recommend index types based on selectivity and access patterns.

---

## Continuous Aggregates

**When to Use**: Same aggregation queried >10 times/day


### Daily OHLCV Summary Example

```sql
CREATE MATERIALIZED VIEW market_data_daily
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 day', date) AS day,
    symbol,
    FIRST(open, date) AS open,
    MAX(high) AS high,
    MIN(low) AS low,
    LAST(close, date) AS close,
    SUM(volume) AS volume
FROM market_data
GROUP BY day, symbol
WITH NO DATA;
```

### Refresh Policy Configuration

```sql
-- Auto-refresh last 7 days, every hour
SELECT add_continuous_aggregate_policy(
    'market_data_daily',
    start_offset => INTERVAL '7 days',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour'
);

-- Enable real-time mode (includes recent non-aggregated data)
ALTER MATERIALIZED VIEW market_data_daily
SET (timescaledb.materialized_only = false);
```

**Performance**: 225x speedup for dashboard queries (45s -> 0.2s)

---

## Compression Configuration


### Configuration Settings

```sql
ALTER TABLE market_data SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol',  -- Dimensional columns (NOT timestamp)
    timescaledb.compress_orderby = 'date DESC'   -- Time column
);

-- Compress chunks older than 30 days
SELECT add_compression_policy('market_data', INTERVAL '30 days');
```

### Key Rules

| Setting | Correct | Wrong |
|---------|---------|-------|
| `compress_segmentby` | `symbol`, `category` | `date`, `timestamp` |
| `compress_orderby` | `date DESC` | Multiple columns |
| Policy interval | 7-30 days | <7 days (write overhead) |

### Check Compression Status

```sql
SELECT chunk_name,
    pg_size_pretty(before_compression_total_bytes) AS before,
    pg_size_pretty(after_compression_total_bytes) AS after,
    ROUND(100 - (100.0 * after_compression_total_bytes / before_compression_total_bytes), 1) AS savings_pct
FROM chunk_compression_stats('market_data');
```

**Expected**: 85-95% storage reduction, 10-20% query overhead on compressed chunks

---

## Index Strategy Quick Reference


### Index Type Selection

| Index Type | Use Case | Selectivity | Size |
|------------|----------|-------------|------|
| **Composite (symbol, date DESC)** | 80% of queries | High | 100% |
| **BRIN (date)** | Large time-range analytics | Low | 10% |
| **B-tree (symbol)** | Symbol-only lookups, JOINs | Medium | 70% |

### Recommended Index Set

```sql
-- Primary composite (covers 80% of queries, 16x speedup)
CREATE INDEX idx_market_data_symbol_date
ON market_data(symbol, date DESC);

-- BRIN for time-range scans without symbol (90% smaller than B-tree)
CREATE INDEX idx_market_data_time_brin
ON market_data USING BRIN(date) WITH (pages_per_range = 128);

-- Partial index for volume queries (excludes zero volume)
CREATE INDEX idx_market_data_volume_date
ON market_data(volume, date DESC) WHERE volume > 0;
```

### When to Use Each

- **Composite (symbol, date)**: `WHERE symbol = X AND date >= Y` (most common)
- **BRIN**: `WHERE date BETWEEN '2024-01-01' AND '2024-12-31'` (no symbol filter)
- **B-tree vs BRIN**: B-tree for point lookups, BRIN for range scans on ordered data

---

## Reference Documentation


Detailed patterns and troubleshooting guides:

| Topic | Reference File |
|-------|----------------|
| Domain expertise | [reference/domain-expertise.md](reference/domain-expertise.md) |
| Query optimization patterns | [reference/timescaledb-query-optimization.md](reference/timescaledb-query-optimization.md) |
| Crash prevention | [../database-optimization/SKILL.md](../database-optimization/SKILL.md) |

---

## Anti-Patterns

| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| `NOW() - INTERVAL` in WHERE | Disables chunk exclusion | Use fixed dates from application |
| `DISTINCT` on hypertable | Full table scan, OOM risk | Use `symbols_cache` table |
| `compress_segmentby = 'date'` | Inefficient compression | Use dimensional columns |
| Missing composite index | Seq Scan on every query | Create `(symbol, date DESC)` |
| `GROUP BY` without date filter | Memory exhaustion | Always add date range |

---

## Validation Checklist

Before finalizing queries:

- [ ] Fixed dates used (no `NOW()`, `CURRENT_DATE`)
- [ ] EXPLAIN shows `Chunks Excluded > 0`
- [ ] Index Scan (not Seq Scan) for filtered queries
- [ ] Crash risk assessed for aggregations
- [ ] Compression config uses dimensional `segmentby`
