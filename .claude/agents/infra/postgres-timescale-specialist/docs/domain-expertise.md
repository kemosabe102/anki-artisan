# Database Performance Expertise for postgres-timescale-specialist

**Purpose**: Workflow operations, retry specifications, and token management for database optimization tasks

---

## Workflow Operations

### 1. Query Optimization (`optimize_query`)

**Input**: SQL query, table context, performance requirements

**Phases**:
1. **Analysis** - Parse query structure, identify tables, estimate complexity
2. **Research** - Check table stats, indexes, chunk counts
3. **Diagnosis** - Run EXPLAIN ANALYZE, identify bottlenecks
4. **Optimization** - Apply chunk exclusion, index hints, restructuring
5. **Validation** - Verify improvement with EXPLAIN ANALYZE
6. **Documentation** - Before/after comparison with rationale

### 2. Index Design (`design_indexes`)

**Input**: Query patterns, table schema, performance goals

**Phases**:
1. **Analysis** - Collect query patterns, identify filter/sort columns
2. **Research** - Review existing indexes, check redundancy
3. **Design** - Propose B-tree/BRIN/composite indexes
4. **Impact Assessment** - Estimate storage and maintenance cost
5. **Validation** - CREATE INDEX statements with rationale

### 3. Performance Audit (`audit_performance`)

**Input**: Table name or query set, performance concerns

**Phases**:
1. **Analysis** - Gather table stats, index info, query patterns
2. **Diagnosis** - Identify bloat, missing indexes, config issues
3. **Recommendations** - Prioritized improvement list
4. **Validation** - Monitoring queries provided

### 4. Configuration Tuning (`tune_configuration`)

**Input**: Resource constraints, workload type (OLTP/OLAP)

**Phases**:
1. **Analysis** - Current settings vs available resources
2. **Research** - Apply tuning formulas for memory, connections
3. **Recommendations** - postgresql.conf changes with rationale
4. **Risk Assessment** - Identify potential issues

---

## Retry Logic Specifications

| Error Type | Max Retries | Backoff | Action |
|------------|-------------|---------|--------|
| Connection failure | 3 | 5s → 15s → 45s | Return FAILURE with diagnostic |
| Query timeout (>120s) | 1 | Immediate | Simplify query (remove ORDER BY, LIMIT 1000) |
| Out of memory | 0 | None | Return FAILURE with memory recommendations |
| Crash risk detected | 0 | None | Block query, return safe alternatives |

---

## Token Budget Guidelines

**Response Targets**:
- SUCCESS response: 200-500 tokens (query + key metrics)
- FAILURE diagnostic: 300-800 tokens (error + recovery steps)
- Full EXPLAIN: Summarize top 3 bottlenecks, store full output in temp file

**Compression Strategies**:
- Return optimized query + improvement summary (not full analysis)
- For EXPLAIN >100 lines: Extract key nodes (Seq Scan, Index Scan, Sort, Hash)
- Large results: Provide sample + statistics, not full data
- Config recommendations: Top 3 highest-impact changes only

**Temp File Usage**:
- Full EXPLAIN: `.claude/temp/postgres-timescale-specialist/explain_{timestamp}.txt`
- Detailed analysis: `.claude/temp/postgres-timescale-specialist/index_analysis_{timestamp}.md`

---

## Integration Points

### Upstream (provide input)
| Agent | Provides |
|-------|----------|
| `python-code-implementer` | Query optimization requests for data access |
| `market-data-specialist` | Database layer questions |

### Downstream (consume output)
| Agent | Uses |
|-------|------|
| Implementation agents | Optimized queries |
| `k8s-deployment` | PostgreSQL config recommendations |

---

## Pre-Flight Checklist (Version-Aware)

**For All Operations** (MANDATORY):
- [ ] **Version Detection**: Query `SELECT version(), (SELECT extversion FROM pg_extension WHERE extname='timescaledb')` - validate against supported versions (PostgreSQL 14-17, TimescaleDB 2.x)
- [ ] **Version Mismatch Handling**: If version > documented, return FAILURE with `error_type: 'unsupported_version'` and suggest Context7 lookup for current version docs

**For Query Optimization**:
- [ ] Target table(s) and estimated row counts identified
- [ ] Existing indexes on filter columns checked
- [ ] Memory constraints assessed (work_mem, shared_buffers)
- [ ] Chunk count evaluated for TimescaleDB hypertables
- [ ] Crash risk assessed for aggregate queries

**For Index Recommendations**:
- [ ] Query patterns and WHERE clauses analyzed
- [ ] Existing index coverage checked
- [ ] B-tree vs BRIN tradeoffs evaluated
- [ ] Maintenance overhead considered
