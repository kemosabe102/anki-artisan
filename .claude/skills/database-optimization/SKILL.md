---
name: database-optimization
description: >
  Use this skill when optimizing PostgreSQL/TimescaleDB query performance,
  assessing crash risk for aggregate queries, analyzing EXPLAIN output, or
  designing indexes. Covers memory safety, crash prevention patterns, and
  performance validation methodology.
  Trigger keywords: query optimization, EXPLAIN ANALYZE, slow query, crash risk,
  work_mem, GROUP BY, DISTINCT, index design, performance, OOM.
---

# PostgreSQL/TimescaleDB Database Optimization

*Memory-safe query optimization with crash prevention as the primary constraint.*

## Table of Contents

1. [Crash Risk Assessment](#crash-risk-assessment)
2. [Queries That Crash PostgreSQL](#queries-that-crash-postgresql)
3. [Safe Alternative Patterns](#safe-alternative-patterns)
4. [EXPLAIN ANALYZE Validation Workflow](#explain-analyze-validation-workflow)
5. [Detection Checklist](#detection-checklist)
6. [Reference Documentation](#reference-documentation)

---


## Crash Risk Assessment

**CRITICAL**: Assess memory impact BEFORE running any aggregate query on hypertables.

### Memory Estimation Formula

```
estimated_memory = row_count × avg_row_width × cardinality_factor
```

| Operation | Cardinality Factor | Example |
|-----------|-------------------|---------|
| GROUP BY | 1.5 | 12K symbols × 56 bytes × 1.5 = 1MB per chunk |
| DISTINCT | 2.0 | 12K symbols × 56 bytes × 2.0 = 1.3MB per chunk |
| Window Functions | 3.0 | Requires full partition in memory |

### Threshold Gate

```
IF estimated_memory > work_mem (16MB default) → BLOCK QUERY
```

**Example Calculation**:
- 36M rows × 56 bytes/row × 1.5 (GROUP BY) = 3GB estimated
- 3GB >> 16MB work_mem → **QUERY WILL CRASH**

---


## Queries That Crash PostgreSQL

### NEVER Run These on Large Hypertables

```sql
-- CRASH: Aggregate across all symbols without chunk exclusion
SELECT symbol, COUNT(*) FROM market_data GROUP BY symbol;

-- CRASH: DISTINCT on high-cardinality column (12K+ unique values)
SELECT DISTINCT symbol FROM market_data;

-- CRASH: Multiple aggregates with GROUP BY on dimensional columns
SELECT COUNT(*), MIN(date), MAX(date) FROM market_data GROUP BY symbol;

-- CRASH: Any GROUP BY/DISTINCT on non-partitioned columns without WHERE filters
SELECT category, COUNT(*) FROM large_hypertable GROUP BY category;
```

**Crash Frequency**: 100% failure rate on tables with 3335+ chunks and 12K+ unique values in GROUP BY column

### Root Causes

| Cause | Limit | Result |
|-------|-------|--------|
| Memory exhaustion | work_mem (16MB) | OOM error, connection terminated |
| Lock exhaustion | max_locks_per_transaction (4096) | "out of shared memory" error |
| Chunk explosion | 3335+ chunks without exclusion | PostgreSQL restart required |

---


## Safe Alternative Patterns

### Pattern 1: Symbol Cache Table (0.006s vs CRASH)

**Use Case**: Getting list of all symbols, symbol metadata

```sql
-- Maintain a lightweight lookup table
CREATE TABLE symbols_cache (
    symbol VARCHAR(10) PRIMARY KEY,
    name TEXT,
    sector TEXT,
    last_updated TIMESTAMP DEFAULT NOW()
);

-- Query symbols (FAST: 0.006s)
SELECT symbol FROM symbols_cache ORDER BY symbol;
```

**Rationale**: 12K rows × 3 columns << 36M rows × 7 columns

### Pattern 2: Single Symbol with Chunk Exclusion (3-4s)

**Use Case**: Time-series data for specific symbol

```sql
-- Optimal pattern: symbol filter + date ordering
SELECT date, open, high, low, close, volume
FROM market_data
WHERE symbol = 'AAPL'
ORDER BY date ASC;
```

**Why Safe**: `symbol = 'AAPL'` filters to ~3K rows, TimescaleDB excludes 94% of chunks


### Pattern 3: Multiple Specific Symbols (5-10s)

**Use Case**: Comparing 5-20 specific symbols

```sql
-- Use ANY(array) for better performance than IN
SELECT symbol, date, close
FROM market_data
WHERE symbol = ANY(ARRAY['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA'])
ORDER BY symbol, date;
```

**Limit**: Max 20 symbols per query to stay under work_mem limits

### Pattern 4: Per-Query work_mem Override (Supervised Only)

**Use Case**: One-off large aggregation with user supervision

```sql
-- Temporarily increase work_mem for THIS transaction only
SET LOCAL work_mem = '256MB';

-- Now safe to run (but still monitor execution time)
SELECT symbol, COUNT(*), AVG(close)
FROM market_data
WHERE date >= '2025-01-01'  -- Fixed date for chunk exclusion
GROUP BY symbol;
```

**Warnings**:
- Only use in interactive sessions, not application code
- Run `EXPLAIN` first to estimate cost
- 256MB × 10 connections = 2.5GB potential memory usage

---


## EXPLAIN ANALYZE Validation Workflow

### Step 1: Run EXPLAIN First (Not ANALYZE)

```sql
-- SAFE: Estimate cost without executing
EXPLAIN SELECT symbol, COUNT(*) FROM market_data
WHERE date >= '2025-01-01' GROUP BY symbol;
```

### Step 2: Analyze the Output

| Indicator | Good | Bad |
|-----------|------|-----|
| Scan Type | Index Scan, Index Only Scan | Seq Scan |
| Chunks Excluded | >90% of total chunks | 0 or low number |
| Estimated Rows | <100K per operation | Millions |
| Sort Method | quicksort Memory | external merge Disk |

### Step 3: Validate with EXPLAIN ANALYZE (Only If Safe)

```sql
-- Only run ANALYZE after confirming EXPLAIN shows safe estimates
EXPLAIN (ANALYZE, BUFFERS)
SELECT date, close FROM market_data
WHERE symbol = 'AAPL' AND date >= '2025-01-01';
```

### Step 4: Interpret Results

```
Index Scan using idx_market_data_symbol_date on market_data
  Index Cond: ((symbol = 'AAPL'::text) AND (date >= '2025-01-01'))
  Buffers: shared hit=1234 read=56
  -> Chunks Excluded: 3135 (94% reduction)  ← SUCCESS INDICATOR
```

---


## Detection Checklist

**Before running a query, check for crash indicators:**

| Check | Condition | Risk Level |
|-------|-----------|------------|
| GROUP BY | On non-time dimensional columns (symbol, category)? | HIGH |
| DISTINCT | On high-cardinality columns (>1K unique values)? | HIGH |
| WHERE clause | Missing or not limiting rows to <100K? | HIGH |
| Volatile expressions | `NOW()`, `CURRENT_DATE` preventing chunk exclusion? | MEDIUM |
| Multiple aggregates | COUNT, SUM, AVG in single query without date filter? | MEDIUM |

**Decision Matrix**:

| Checks Failed | Action |
|---------------|--------|
| 0 | Safe to run |
| 1 | Run EXPLAIN first, proceed with caution |
| 2+ | **QUERY WILL LIKELY CRASH** - Use safe alternative patterns |

### Quick Memory Check

```python
def estimate_memory(row_count: int, avg_row_width: int = 56, 
                   cardinality_factor: float = 1.5) -> str:
    estimated_mb = (row_count * avg_row_width * cardinality_factor) / (1024 * 1024)
    work_mem_mb = 16  # Default PostgreSQL work_mem
    if estimated_mb > work_mem_mb:
        return f"BLOCK: {estimated_mb:.0f}MB >> {work_mem_mb}MB work_mem"
    return f"SAFE: {estimated_mb:.1f}MB < {work_mem_mb}MB work_mem"
```

---


## Reference Documentation

Detailed guides for specific scenarios:

| Topic | Reference File |
|-------|----------------|
| Thinking frameworks | [reference/frameworks.md](reference/frameworks.md) |
| Crash prevention patterns | [reference/postgres-crash-prevention-patterns.md](reference/postgres-crash-prevention-patterns.md) |
| TimescaleDB query optimization | [../postgres-timescaledb/SKILL.md](../postgres-timescaledb/SKILL.md) |

---

## Quick Reference Table

| Pattern | Use Case | Performance | Safety |
|---------|----------|-------------|--------|
| **symbols_cache** | List all symbols | 0.006s | Always safe |
| **Single symbol** | Time-series for 1 symbol | 3-4s | Always safe |
| **Multiple symbols** | Compare 5-20 symbols | 5-10s | Safe (limit 20) |
| **Per-query work_mem** | One-off large agg | 30s-2min | Supervised only |
| **GROUP BY dimensional** | Aggregate all symbols | CRASH | Never use |

---

## Anti-Patterns

| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| `SELECT DISTINCT symbol FROM market_data` | Full scan, OOM | Use `symbols_cache` table |
| `GROUP BY symbol` without WHERE | Memory exhaustion | Add date filter or use cache |
| `NOW() - INTERVAL` in WHERE | Disables chunk exclusion | Use fixed dates |
| Running ANALYZE on untested query | May crash DB | Run EXPLAIN first |
| `work_mem = '1GB'` globally | Multiplied by connections | Use SET LOCAL per-query |
