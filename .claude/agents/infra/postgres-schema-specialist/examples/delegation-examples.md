# Delegation Examples for postgres-schema-specialist

**Purpose**: Show orchestrator and other agents how to delegate database schema design and administration tasks

---

## When to Delegate to This Agent

### Trigger Conditions

Delegate to `postgres-schema-specialist` when:
- New table or schema design is needed
- Database migrations are required (ADD/ALTER/DROP columns, tables)
- TimescaleDB hypertable setup or configuration
- Index strategy design (structure decisions, not performance tuning)
- Constraint design (CHECK, UNIQUE, FOREIGN KEY, EXCLUSION)
- Backup and recovery strategy planning (RTO/RPO requirements)

### NOT This Agent

Do NOT delegate when:
- Query creation needed (SELECT, INSERT, UPDATE) -> Use `postgres-timescale-specialist`
- Query optimization or performance tuning -> Use `postgres-timescale-specialist`
- EXPLAIN ANALYZE profiling or interpretation -> Use `postgres-timescale-specialist`
- Production deployment of schema changes -> Use `k8s-deployment`
- Application code that uses the database -> Use `python-code-implementer`

---

## Example 1: Design New Table Schema

**Orchestrator says**:
```
Task(postgres-schema-specialist, "Design a schema for storing market orders with the following entities: orders (order_id, symbol, side, quantity, price, status, created_at), order_fills (fill_id, order_id, quantity, price, filled_at)")
```

**Agent returns**:
```json
{
  "status": "SUCCESS",
  "agent": "postgres-schema-specialist",
  "confidence": 0.91,
  "agent_specific_output": {
    "mode": "design_schema",
    "ddl_script": "CREATE TABLE orders (\n  order_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n  symbol VARCHAR(20) NOT NULL,\n  side VARCHAR(4) NOT NULL CHECK (side IN ('BUY', 'SELL')),\n  quantity NUMERIC(18,8) NOT NULL CHECK (quantity > 0),\n  price NUMERIC(18,8) NOT NULL CHECK (price > 0),\n  status VARCHAR(10) NOT NULL DEFAULT 'PENDING',\n  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()\n);\n\nCREATE TABLE order_fills (\n  fill_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n  order_id BIGINT NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,\n  quantity NUMERIC(18,8) NOT NULL CHECK (quantity > 0),\n  price NUMERIC(18,8) NOT NULL CHECK (price > 0),\n  filled_at TIMESTAMPTZ NOT NULL DEFAULT NOW()\n);",
    "normalization_level": "3NF",
    "design_decisions": [
      "BIGINT GENERATED for PKs - better index performance than UUID",
      "NUMERIC(18,8) for quantity/price - preserves financial precision",
      "TIMESTAMPTZ for timestamps - timezone-aware storage",
      "ON DELETE CASCADE for order_fills - orphan prevention",
      "CHECK constraints inline - immediate validation"
    ]
  }
}
```

---

## Example 2: Create Migration for Schema Change

**Orchestrator says**:
```
Task(postgres-schema-specialist, "Create a migration to add a 'fees' column (DECIMAL(10,4)) to the order_fills table with a default of 0. Table has ~5M rows.")
```

**Agent returns**:
```json
{
  "status": "SUCCESS",
  "agent": "postgres-schema-specialist",
  "confidence": 0.89,
  "agent_specific_output": {
    "mode": "create_migration",
    "migration": {
      "version": "V20250121_001__add_fees_to_order_fills",
      "up_script": "ALTER TABLE order_fills ADD COLUMN fees DECIMAL(10,4) NOT NULL DEFAULT 0;",
      "down_script": "ALTER TABLE order_fills DROP COLUMN fees;",
      "lock_analysis": {
        "lock_type": "ACCESS EXCLUSIVE",
        "estimated_duration": "< 1 second",
        "recommendation": "Safe for 5M rows with DEFAULT value. PostgreSQL 11+ adds NOT NULL with DEFAULT without full table rewrite."
      }
    },
    "design_decisions": [
      "DECIMAL(10,4) - sufficient precision for fee amounts",
      "DEFAULT 0 - enables NOT NULL without backfill",
      "Single ALTER - atomic operation, no transaction wrapper needed"
    ]
  }
}
```

---

## Example 3: Setup TimescaleDB Hypertable

**Orchestrator says**:
```
Task(postgres-schema-specialist, "Convert the market_data table to a TimescaleDB hypertable. Expected ingestion: 100K rows/day, 6-month retention, queries mostly on last 30 days.")
```

**Agent returns**:
```json
{
  "status": "SUCCESS",
  "agent": "postgres-schema-specialist",
  "confidence": 0.92,
  "agent_specific_output": {
    "mode": "setup_hypertable",
    "ddl_script": "-- Convert to hypertable (table must be empty or use migrate_data => true)\nSELECT create_hypertable('market_data', 'timestamp', chunk_time_interval => INTERVAL '1 week');\n\n-- Enable compression (after 7 days)\nALTER TABLE market_data SET (timescaledb.compress, timescaledb.compress_segmentby = 'symbol');\nSELECT add_compression_policy('market_data', INTERVAL '7 days');\n\n-- Set retention policy (6 months)\nSELECT add_retention_policy('market_data', INTERVAL '6 months');",
    "hypertable": {
      "table_name": "market_data",
      "time_column": "timestamp",
      "chunk_interval": "1 week",
      "compression_policy": "After 7 days, segment by symbol",
      "retention_policy": "Drop chunks older than 6 months"
    },
    "design_decisions": [
      "1-week chunks - optimal for 100K rows/day (~700K/chunk)",
      "Compress after 7 days - balances query speed vs storage",
      "Segment by symbol - enables efficient per-symbol queries on compressed data",
      "6-month retention - matches business requirement"
    ]
  }
}
```

---

## Example 4: Design Index Strategy

**Orchestrator says**:
```
Task(postgres-schema-specialist, "Design indexes for the orders table. Expected query patterns: 1) Filter by symbol + date range, 2) Filter by status + created_at, 3) Lookup by order_id")
```

**Agent returns**:
```json
{
  "status": "SUCCESS",
  "agent": "postgres-schema-specialist",
  "confidence": 0.87,
  "agent_specific_output": {
    "mode": "design_indexes",
    "indexes": [
      {
        "index_name": "idx_orders_symbol_created_at",
        "index_type": "btree",
        "create_statement": "CREATE INDEX idx_orders_symbol_created_at ON orders (symbol, created_at DESC);",
        "design_rationale": "Composite index for symbol + date range queries. Symbol first for equality, created_at second for range scan."
      },
      {
        "index_name": "idx_orders_status_created_at",
        "index_type": "btree",
        "create_statement": "CREATE INDEX idx_orders_status_created_at ON orders (status, created_at DESC) WHERE status IN ('PENDING', 'PARTIAL');",
        "design_rationale": "Partial index for active orders only. Reduces index size, speeds up common queries."
      },
      {
        "index_name": "orders_pkey",
        "index_type": "btree",
        "create_statement": "-- Already exists: PRIMARY KEY on order_id",
        "design_rationale": "PK lookup already optimal via implicit B-tree index."
      }
    ],
    "design_decisions": [
      "Composite indexes ordered by selectivity (equality columns first)",
      "Partial index for status - most queries filter active orders",
      "DESC on created_at - optimizes ORDER BY ... DESC LIMIT N patterns"
    ]
  }
}
```

---

## Example 5: Design Constraints

**Orchestrator says**:
```
Task(postgres-schema-specialist, "Add constraints to orders table: side must be 'BUY' or 'SELL', quantity must be positive, price must be positive, status must be one of PENDING/FILLED/CANCELLED/REJECTED")
```

**Agent returns**:
```json
{
  "status": "SUCCESS",
  "agent": "postgres-schema-specialist",
  "confidence": 0.93,
  "agent_specific_output": {
    "mode": "design_constraints",
    "constraints": [
      {
        "constraint_name": "chk_orders_side",
        "constraint_type": "CHECK",
        "definition": "ALTER TABLE orders ADD CONSTRAINT chk_orders_side CHECK (side IN ('BUY', 'SELL'));",
        "validation_impact": "Validates against existing rows. Fast for small tables."
      },
      {
        "constraint_name": "chk_orders_quantity_positive",
        "constraint_type": "CHECK",
        "definition": "ALTER TABLE orders ADD CONSTRAINT chk_orders_quantity_positive CHECK (quantity > 0);",
        "validation_impact": "Validates against existing rows. Ensure no zero/negative quantities exist."
      },
      {
        "constraint_name": "chk_orders_price_positive",
        "constraint_type": "CHECK",
        "definition": "ALTER TABLE orders ADD CONSTRAINT chk_orders_price_positive CHECK (price > 0);",
        "validation_impact": "Validates against existing rows. Ensure no zero/negative prices exist."
      },
      {
        "constraint_name": "chk_orders_status",
        "constraint_type": "CHECK",
        "definition": "ALTER TABLE orders ADD CONSTRAINT chk_orders_status CHECK (status IN ('PENDING', 'FILLED', 'CANCELLED', 'REJECTED'));",
        "validation_impact": "Validates against existing rows. Migration may fail if invalid statuses exist."
      }
    ],
    "design_decisions": [
      "Named constraints - easier to reference in error messages and migrations",
      "Separate constraints per column - granular control for future modifications",
      "IN clause for enums - clearer than multiple OR conditions"
    ]
  }
}
```

---

## Example 6: Failure - Insufficient Context

**Orchestrator says**:
```
Task(postgres-schema-specialist, "Create a migration to add a column")
```

**Agent returns**:
```json
{
  "status": "FAILURE",
  "agent": "postgres-schema-specialist",
  "confidence": 0.25,
  "error_type": "insufficient_context",
  "agent_specific_output": {
    "mode": "create_migration",
    "failure_details": {
      "failure_type": "insufficient_context",
      "reasons": [
        "Table name not specified",
        "Column name not specified",
        "Column data type not specified",
        "Nullability requirement unknown",
        "Default value requirement unknown"
      ],
      "recovery_suggestions": [
        "Specify target table name",
        "Provide column name and data type",
        "Indicate if column should be NOT NULL",
        "Specify default value if needed",
        "Provide approximate row count for lock analysis"
      ]
    }
  }
}
```

---

## Example 7: Handoff to postgres-timescale-specialist

After completing schema design, the user requests query optimization.

**Scenario**: Schema design complete, user asks "Now optimize queries for this table"

**Agent returns**:
```json
{
  "status": "SUCCESS",
  "agent": "postgres-schema-specialist",
  "confidence": 0.90,
  "agent_specific_output": {
    "mode": "design_schema",
    "ddl_script": "-- Schema design complete (see above)",
    "handoff_recommended": true,
    "handoff_target": "postgres-timescale-specialist",
    "handoff_reason": "Query optimization is outside schema design scope. Delegate query tuning to postgres-timescale-specialist.",
    "handoff_context": {
      "tables_created": ["orders", "order_fills"],
      "indexes_designed": ["idx_orders_symbol_created_at", "idx_orders_status_created_at"],
      "suggested_delegation": "Task(postgres-timescale-specialist, 'Optimize queries for the orders and order_fills tables. Indexes available: idx_orders_symbol_created_at, idx_orders_status_created_at')"
    }
  }
}
```

**Orchestrator action**: Delegate to `postgres-timescale-specialist` with provided context.

---

## Example 8: Handoff to k8s-deployment

After completing migration script, the user requests production deployment.

**Scenario**: Migration ready, user asks "Deploy this to production"

**Agent returns**:
```json
{
  "status": "SUCCESS",
  "agent": "postgres-schema-specialist",
  "confidence": 0.88,
  "agent_specific_output": {
    "mode": "create_migration",
    "migration": {
      "version": "V20250121_002__add_audit_columns",
      "up_script": "ALTER TABLE orders ADD COLUMN updated_at TIMESTAMPTZ;",
      "down_script": "ALTER TABLE orders DROP COLUMN updated_at;",
      "lock_analysis": {
        "lock_type": "ACCESS EXCLUSIVE",
        "estimated_duration": "< 100ms",
        "recommendation": "Safe for production"
      }
    },
    "handoff_recommended": true,
    "handoff_target": "k8s-deployment",
    "handoff_reason": "Production deployment is outside schema design scope. Delegate deployment to k8s-deployment.",
    "handoff_context": {
      "migration_file": "V20250121_002__add_audit_columns.sql",
      "target_database": "production",
      "lock_safe": true,
      "suggested_delegation": "Task(k8s-deployment, 'Deploy migration V20250121_002__add_audit_columns.sql to production PostgreSQL. Lock analysis: ACCESS EXCLUSIVE < 100ms, safe for production.')"
    }
  }
}
```

**Orchestrator action**: Delegate to `k8s-deployment` with migration file and safety analysis.

---

## Confidence Thresholds

| Confidence | Action |
|------------|--------|
| >= 0.75 | Proceed with generation - sufficient context for reliable DDL |
| 0.50 - 0.74 | Generate with explicit assumptions - document what was assumed |
| < 0.50 | Return FAILURE requesting context - too risky to generate DDL |

### Confidence Factors

| Factor | Weight | Description |
|--------|--------|-------------|
| Table structure clarity | 0.30 | Are columns, types, constraints specified? |
| Row count known | 0.20 | Needed for lock analysis on large tables |
| Relationship clarity | 0.20 | Are foreign keys and references defined? |
| Business rules specified | 0.15 | Are constraints and validations clear? |
| Environment context | 0.15 | PostgreSQL version, TimescaleDB presence |

---

## Multi-Agent Coordination

### Upstream Agents (provide input)

| Agent | Provides | Example |
|-------|----------|---------|
| `python-code-implementer` | Entity requirements from code | "We need a table for storing X based on this dataclass" |
| `architecture-reviewer` | Schema design requirements | "Design tables following this domain model" |
| `technical-pm` | Feature requirements | "New feature needs persistent storage for Y" |

### Downstream Agents (consume output)

| Agent | Uses | For |
|-------|------|-----|
| `postgres-timescale-specialist` | Schema + indexes | Query optimization on new tables |
| `k8s-deployment` | Migration scripts | Production deployment |
| `python-code-implementer` | DDL structure | ORM model generation |
| `test-creator` | Schema definition | Database integration tests |
