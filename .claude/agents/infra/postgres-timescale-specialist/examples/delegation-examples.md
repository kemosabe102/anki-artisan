# Delegation Examples for postgres-timescale-specialist

**Purpose**: Show orchestrator and other agents how to delegate database optimization tasks

---

## When to Delegate to This Agent

### Trigger Conditions

Delegate to `postgres-timescale-specialist` when:
- SQL query performance issues or slow queries
- EXPLAIN ANALYZE interpretation needed
- TimescaleDB hypertable optimization
- Index design or review
- PostgreSQL configuration tuning
- Preventing database crashes from expensive operations

### NOT This Agent

Do NOT delegate when:
- Database DDL/schema administration → Use `postgres-schema-specialist`
- Schema design or migrations → Use `postgres-schema-specialist`
- Hypertable setup/configuration → Use `postgres-schema-specialist`
- Production deployment changes → Use `k8s-deployment`
- Technical indicator computation → Use `technical-indicator-specialist`
- Application code changes → Use `python-code-implementer`

---

## Basic Delegation Pattern

### Query Optimization

**Orchestrator says**:
```
Task(postgres-timescale-specialist, "Optimize this slow query for the market_data table")
```

**Agent returns**:
```json
{
  "status": "SUCCESS",
  "agent": "postgres-timescale-specialist",
  "confidence": 0.92,
  "agent_specific_output": {
    "original_query": "SELECT ... WHERE date >= NOW() - INTERVAL '200 days'",
    "optimized_query": "SELECT ... WHERE date >= '2025-05-09' AND date < '2025-11-25'",
    "improvement_factors": ["chunk_exclusion", "fixed_dates"],
    "estimated_speedup": "16x",
    "explain_summary": "Index Scan instead of Seq Scan, 47 chunks excluded"
  }
}
```

---

## Complex Delegation Pattern

### Task with Full Context

**Orchestrator says**:
```
Task(postgres-timescale-specialist, "Optimize this query for the market_data hypertable (36M rows, 3335 chunks):

SELECT symbol, AVG(close)
FROM market_data
WHERE date >= NOW() - INTERVAL '30 days'
GROUP BY symbol;

Constraints: Must not crash database, work_mem=16MB")
```

**Required context**:
- `table_info`: Row count, chunk count, hypertable status
- `memory_constraints`: work_mem, shared_buffers limits
- `query`: The SQL to optimize

**Agent returns** (success):
```json
{
  "status": "SUCCESS",
  "agent": "postgres-timescale-specialist",
  "confidence": 0.88,
  "agent_specific_output": {
    "crash_risk_detected": true,
    "original_query": "SELECT symbol, AVG(close) FROM market_data WHERE...",
    "safe_alternative": "Use symbols_cache + per-symbol queries with chunk exclusion",
    "optimized_approach": [
      "1. Get symbols from symbols_cache",
      "2. For each symbol batch (10-20): SELECT AVG(close) WHERE symbol=X AND date >= fixed_date",
      "3. Aggregate results in application"
    ],
    "rationale": "GROUP BY symbol across 3335 chunks exceeds 16MB work_mem"
  }
}
```

**Agent returns** (failure):
```json
{
  "status": "FAILURE",
  "agent": "postgres-timescale-specialist",
  "confidence": 0.4,
  "failure_details": {
    "failure_type": "insufficient_context",
    "reasons": ["Table stats not provided", "Cannot determine if hypertable"],
    "recovery_suggestions": ["Provide \\d+ table_name output", "Confirm TimescaleDB hypertable status"]
  }
}
```

---

## Multi-Agent Coordination

### Upstream Agents (provide input)

| Agent | Provides | Example |
|-------|----------|---------|
| `python-code-implementer` | Data access queries needing optimization | "This query in data_loader.py is slow" |
| `market-data-specialist` | Database schema questions | "How should I query 200-day rolling windows?" |

### Downstream Agents (consume output)

| Agent | Uses | For |
|-------|------|-----|
| `python-code-implementer` | Optimized query | Updating application code |
| `k8s-deployment` | Config recommendations | PostgreSQL StatefulSet tuning |

---

## Examples by Mode

### Mode: optimize_query

**Delegation**:
```
Task(postgres-timescale-specialist, "This query takes 48 seconds, need it under 5s:
SELECT date, close FROM market_data WHERE date >= NOW() - INTERVAL '200 days' AND symbol = 'AAPL'")
```

**Expected output**: Optimized query with fixed dates, EXPLAIN proof, 16x speedup

### Mode: design_indexes

**Delegation**:
```
Task(postgres-timescale-specialist, "Design indexes for these query patterns on market_data:
1. Filter by symbol + date range
2. Filter by date range only
3. Aggregate by symbol for specific date")
```

**Expected output**: Index recommendations (B-tree vs BRIN), CREATE INDEX statements, storage estimates

### Mode: audit_performance

**Delegation**:
```
Task(postgres-timescale-specialist, "Audit database performance for the data namespace. 
Check: index usage, table bloat, cache hit ratio, slow queries")
```

**Expected output**: Prioritized findings, monitoring queries, improvement roadmap

---

## Handoff Examples

### Handoff to postgres-schema-specialist

**Scenario**: User asks to add a new column or create a hypertable

**This agent responds**:
```json
{
  "status": "HANDOFF",
  "agent": "postgres-timescale-specialist",
  "handoff_to": "postgres-schema-specialist",
  "reason": "DDL/schema administration is outside this agent's scope",
  "context_to_pass": {
    "table": "market_data",
    "request": "Add new column for adjusted_close",
    "performance_notes": "Table has 36M rows across 3335 chunks"
  }
}
```

**Orchestrator should**:
```
Task(postgres-schema-specialist, "Add adjusted_close column to market_data hypertable. 
Context: 36M rows, 3335 chunks - coordinate with postgres-timescale-specialist for index recommendations after schema change.")
```
