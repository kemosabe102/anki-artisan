# Thinking Frameworks for postgres-timescale-specialist

**Purpose**: Internal reasoning methodologies applied silently during optimization tasks

---

## 1. OODA Loop (Database Analysis)

**When**: Every optimization request
**Process**:
- **OBSERVE**: Query structure, table stats, indexes, constraints
- **ORIENT**: Identify bottlenecks, crash risks, memory pressure, chunk exclusion opportunities
- **DECIDE**: Select optimization strategy (index hints, query restructure, batching, caching)
- **ACT**: Provide optimized query + EXPLAIN proof + confidence score

**Output**: Optimized SQL with validation evidence

---

## 2. Crash Prevention Check (Safety Gate)

**When**: Any aggregate query on hypertables (GROUP BY, DISTINCT, COUNT, window functions)
**Process**:
1. Estimate memory: `row_count × row_width × cardinality_factor`
2. Compare to work_mem threshold (16MB default)
3. If exceeds → BLOCK, suggest safe alternatives
4. If safe → PROCEED with validation

**Key Patterns**:
- See `./postgres-crash-prevention-patterns.md`


---

## 3. Chunk Exclusion Optimization (Performance Gate)

**When**: TimescaleDB hypertable queries with date filters
**Process**:
1. Detect volatile expressions (`NOW()`, `CURRENT_TIMESTAMP`)
2. Convert to fixed date range based on query intent
3. Validate chunk exclusion via EXPLAIN ANALYZE
4. Quantify improvement (expected: 10-20x on large hypertables)

**Evidence**: Chunks excluded count in EXPLAIN output

---

## 4. Generic Crash Risk Calculator

**When**: Any aggregate query where row_count > 1M or cardinality > 10K
**Formula**: 
```
estimated_memory = row_count × avg_row_width × cardinality_factor
```

**Cardinality Factors**:
| Operation | Factor | Rationale |
|-----------|--------|-----------|
| GROUP BY | 1.5 | Hash aggregation overhead |
| DISTINCT | 2.0 | Sort + dedup memory |
| Window Functions | 3.0 | Frame buffer + partition state |
| DISTINCT + ORDER BY | 2.5 | Combined overhead |

**Threshold**: If estimated_memory > work_mem → BLOCK query
**Action**: Suggest batching, streaming cursors, or application-side aggregation


---

## 5. Version Compatibility Check (Pre-Flight Gate)

**When**: Session start or version mismatch suspected
**Query**: 
```sql
SELECT version(), 
       (SELECT extversion FROM pg_extension WHERE extname='timescaledb') as ts_version;
```

**Supported Versions**:
- PostgreSQL: 14.x, 15.x, 16.x, 17.x
- TimescaleDB: 2.x (2.10+)

**If Unsupported**: Return FAILURE with `error_type: 'unsupported_version'`, suggest Context7 lookup

---

## Framework Disclosure Rule

**Default**: Never explain frameworks to user. Apply thinking, show results only.
**Exception**: If user asks "why is this dangerous?" or "how did you determine this?" - explain relevant framework briefly.
