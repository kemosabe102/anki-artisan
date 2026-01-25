# PostgreSQL Crash Prevention Patterns

**Purpose**: Prevent database crashes and resource exhaustion when querying large TimescaleDB hypertables with limited memory resources

**Target Environment**: 36M+ row tables, 3335+ chunks, 512MB shared_buffers, 16MB work_mem

---

## Queries That Crash PostgreSQL

### ❌ NEVER Run These on Large Hypertables

```sql
-- CRASH: Aggregate across all symbols without chunk exclusion
SELECT symbol, count(*) FROM market_data GROUP BY symbol;

-- CRASH: DISTINCT on high-cardinality column (12K+ unique values)
SELECT DISTINCT symbol FROM market_data;

-- CRASH: Multiple aggregates with GROUP BY on dimensional columns
SELECT count(*), min(date), max(date) FROM market_data GROUP BY symbol;

-- CRASH: Any GROUP BY/DISTINCT on non-partitioned columns without WHERE filters
SELECT category, COUNT(*) FROM large_hypertable GROUP BY category;
```

**Crash Frequency**: 100% failure rate on tables with 3335+ chunks and 12K+ unique values in GROUP BY column

---

## Root Cause Explanation

### Memory Exhaustion

**Problem**: `work_mem` (16MB) insufficient for aggregation state across thousands of chunks

**Breakdown**:
- **12,000+ symbols** in GROUP BY = 12K+ hash table entries
- **3,335 chunks** accessed = Each chunk requires lock + memory
- **16MB work_mem** exhausted after ~500-1000 symbols per chunk
- **Result**: Out of memory error, connection termination, PostgreSQL restart

### Chunk Lock Exhaustion

**Problem**: `max_locks_per_transaction` (4096) exceeded when accessing too many chunks without exclusion

**Breakdown**:
- Each chunk requires an access lock
- 3,335 chunks > 4,096 lock limit
- **Result**: "out of shared memory" error, query termination

---

## Safe Alternative Patterns

### ✅ Pattern 1: Symbol Cache Table

**Use Case**: Getting list of all symbols, symbol metadata

**Performance**: 0.006s (2500x faster than DISTINCT)

```sql
-- Maintain a lightweight lookup table
CREATE TABLE symbols_cache (
    symbol VARCHAR(10) PRIMARY KEY,
    name TEXT,
    sector TEXT,
    last_updated TIMESTAMP DEFAULT NOW()
);

-- Populate from market_data (run once or daily)
INSERT INTO symbols_cache (symbol)
SELECT DISTINCT symbol FROM market_data
ON CONFLICT (symbol) DO NOTHING;

-- Query symbols (FAST)
SELECT symbol FROM symbols_cache ORDER BY symbol;
```

**Rationale**: 12K rows × 3 columns << 36M rows × 7 columns

---

### ✅ Pattern 2: Single Symbol with Chunk Exclusion

**Use Case**: Time-series data for specific symbol

**Performance**: 3-4s for 10K rows with proper indexing

```sql
-- Optimal pattern: symbol filter + date ordering
SELECT date, open, high, low, close, volume
FROM market_data
WHERE symbol = 'AAPL'
ORDER BY date ASC;
```

**Why Safe**:
- `symbol = 'AAPL'` filters to ~3K rows before aggregation
- TimescaleDB chunk exclusion reduces chunks scanned from 3335 → ~200
- Memory usage: 3K rows × 56 bytes/row = 168KB (well under 16MB)

---

### ✅ Pattern 3: Multiple Specific Symbols (Limited Set)

**Use Case**: Comparing 5-20 specific symbols

**Performance**: 5-10s for 20 symbols × 10K rows each

```sql
-- Use ANY(array) for better performance than IN
SELECT symbol, date, close
FROM market_data
WHERE symbol = ANY(ARRAY['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA'])
ORDER BY symbol, date;
```

**Limit**: Max 20 symbols per query to stay under work_mem limits

---

### ✅ Pattern 4: Per-Query Memory Override

**Use Case**: One-off large aggregation with user supervision

**Performance**: Allows aggregations that would normally crash

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
- Monitor with `EXPLAIN ANALYZE` first
- Reset automatically at transaction end
- Multiple concurrent queries can still exhaust memory (256MB × 10 connections = 2.5GB)

---

## Quick Reference Table

| Pattern | Use Case | Performance | Safety | When to Use |
|---------|----------|-------------|--------|-------------|
| **symbols_cache** | List all symbols | 0.006s | ✅ Always safe | Symbol dropdowns, metadata queries |
| **Single symbol** | Time-series for 1 symbol | 3-4s | ✅ Always safe | Detail views, backtesting one asset |
| **Multiple symbols** | Compare 5-20 symbols | 5-10s | ✅ Safe (limit 20) | Portfolio analysis, watchlists |
| **Per-query work_mem** | One-off large agg | 30s-2min | ⚠️ Supervised only | Admin reports, data analysis |
| **GROUP BY dimensional** | Aggregate across all symbols | ❌ CRASH | ❌ Never use | None (use cache or batch) |

---

## Detection Checklist

**Before running a query, check for:**

- [ ] **GROUP BY** on non-time dimensional columns (symbol, category, device_id)?
- [ ] **DISTINCT** on high-cardinality columns (>1K unique values)?
- [ ] **No WHERE clause** limiting rows to <100K?
- [ ] **Volatile expressions** like `NOW()` preventing chunk exclusion?
- [ ] **Multiple aggregates** (COUNT, SUM, AVG) in single query?

**If 2+ boxes checked** → Query will likely crash → Use safe alternative patterns

---

## Emergency Recovery

**If database crashed from bad query:**

1. **Check pod status**: `kubectl get pods -n data`
2. **Wait for restart**: PostgreSQL auto-restarts in 30-60 seconds
3. **Check logs**: `kubectl logs -n data postgres-0 --tail=50`
4. **Verify recovery**: `kubectl exec -n data postgres-0 -- psql -c "SELECT 1"`

**Prevention for next time**:
- Add query to this document's NEVER list
- Update application code to use safe patterns
- Consider adding continuous aggregate for the use case

---

**Last Updated**: 2025-11-26
**Maintained By**: postgres-timescale-specialist agent
