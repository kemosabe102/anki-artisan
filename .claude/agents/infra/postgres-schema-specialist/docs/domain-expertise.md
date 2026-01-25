# Domain Expertise: PostgreSQL Schema Specialist

> **Internal reference for schema design patterns, workflow operations, and integration protocols.**

---

## Workflow Operations by Mode

### 1. design_schema Mode

**Purpose**: Create new table/schema designs from requirements.

| Phase | Actions | Validation |
|-------|---------|------------|
| **Analysis** | Parse entity requirements, identify relationships, extract data types | Requirements checklist complete |
| **Research** | Check existing schema patterns, lookup similar tables, verify naming conventions | No naming conflicts |
| **Design** | Apply normalization (3NF minimum), select primary key strategy, define NOT NULL constraints | Normalization validated |
| **DDL Generation** | Generate CREATE TABLE statement with constraints | Syntax validation |
| **Validation** | Verify 3NF compliance, check constraint coverage, validate naming | All checks pass |
| **Documentation** | Record design decisions, document rationale for type choices | Design doc complete |

**Critical Checkpoints**:
- Functional dependencies identified before table creation
- Primary key strategy justified (BIGINT GENERATED vs UUID vs natural)
- All required fields marked NOT NULL


### 2. create_migration Mode

**Purpose**: Modify existing schema with versioned, reversible migrations.

| Phase | Actions | Validation |
|-------|---------|------------|
| **Analysis** | Inspect current table structure, count rows, identify dependencies | Table metadata retrieved |
| **Research** | Check migration history, identify version conflicts, review lock patterns | No version conflicts |
| **Design** | Plan ALTER sequence, determine lock requirements, design rollback | Lock impact assessed |
| **UP/DOWN Generation** | Generate forward migration, generate reversible DOWN script | Both scripts valid |
| **Risk Assessment** | Calculate lock duration, identify blocking operations, plan mitigation | Risk level acceptable |
| **Validation** | Verify UP/DOWN symmetry, test rollback completeness | Rollback tested |

**Critical Checkpoints**:
- Row count retrieved for tables >1M rows
- Lock type identified (ACCESS EXCLUSIVE vs SHARE UPDATE EXCLUSIVE)
- DOWN script fully reverses UP script

---

### 3. design_indexes Mode

**Purpose**: Design index structures for query patterns (not optimization).

| Phase | Actions | Validation |
|-------|---------|------------|
| **Analysis** | Gather expected query patterns, identify filter/sort columns | Query patterns documented |
| **Research** | Check existing indexes, identify redundancy, review index types | No redundant indexes |
| **Design** | Select index type (B-tree, GIN, GiST, BRIN), order composite columns | Type justified |
| **DDL Generation** | Generate CREATE INDEX statements, consider CONCURRENTLY | Syntax valid |
| **Impact Assessment** | Estimate index size, assess write overhead, plan maintenance | Impact acceptable |

**Critical Checkpoints**:
- Index type matches data/query characteristics
- Composite index column order matches query patterns
- CONCURRENTLY used for production indexes


---

### 4. setup_hypertable Mode

**Purpose**: Configure TimescaleDB hypertables for time-series data.

| Phase | Actions | Validation |
|-------|---------|------------|
| **Analysis** | Assess data volume, ingestion rate, query patterns | Volume metrics gathered |
| **Research** | Check TimescaleDB version, review compression options, lookup retention patterns | Version compatible |
| **Configuration** | Calculate chunk interval, define compression policy, set retention | Calculations documented |
| **DDL Generation** | Generate create_hypertable(), add_compression_policy(), add_retention_policy() | Syntax valid |
| **Validation** | Verify table is empty, confirm PK includes time column, test policies | All preconditions met |

**Critical Checkpoints**:
- Table empty before hypertable conversion
- Primary key includes time column
- Chunk interval justified with calculation

---

### 5. design_constraints Mode

**Purpose**: Design data integrity constraints (CHECK, UNIQUE, FK).

| Phase | Actions | Validation |
|-------|---------|------------|
| **Analysis** | Identify integrity requirements, gather business rules | Requirements complete |
| **Design** | Name constraints meaningfully, define CHECK conditions, configure FK actions | Naming convention followed |
| **DDL Generation** | Generate ALTER TABLE ADD CONSTRAINT statements | Syntax valid |
| **Performance Assessment** | Assess validation overhead, plan NOT VALID + VALIDATE | Impact acceptable |
| **Validation** | Test constraint with sample data, verify FK cascade behavior | Constraints tested |

**Critical Checkpoints**:
- Constraint names follow convention: `{table}_{columns}_{type}`
- FK ON DELETE/UPDATE actions explicitly specified
- Large tables use NOT VALID + VALIDATE CONSTRAINT pattern


---

### 6. design_backup_strategy Mode

**Purpose**: Plan backup and disaster recovery procedures.

| Phase | Actions | Validation |
|-------|---------|------------|
| **Analysis** | Gather RTO/RPO requirements, assess data criticality, identify compliance needs | Requirements documented |
| **Design** | Select backup method, define schedule, plan retention, design recovery procedure | Strategy justified |
| **Documentation** | Create backup runbook, document recovery steps, define testing schedule | Runbook complete |
| **Validation** | Verify backup can meet RTO/RPO, review recovery procedure completeness | Targets achievable |

**Critical Checkpoints**:
- RTO/RPO explicitly defined
- Backup method matches recovery requirements
- Recovery procedure tested

---

## Retry Logic Specifications

| Error Type | Max Retries | Backoff Strategy | Action on Exhaustion |
|------------|-------------|------------------|----------------------|
| **Connection failure** | 3 | Exponential: 5s -> 15s -> 45s | Return FAILURE with diagnostic, include connection parameters (sanitized) |
| **Schema validation error** | 0 | None | Return FAILURE immediately with constraint violation details |
| **Migration conflict** | 0 | None | Return FAILURE immediately with version conflict and resolution steps |
| **Permission denied** | 0 | None | Return FAILURE immediately with required permissions list |
| **Timeout (query)** | 2 | Linear: 10s -> 20s | Return FAILURE with timeout context and optimization suggestions |
| **Lock contention** | 2 | Exponential: 5s -> 25s | Return FAILURE with lock holder info and retry window suggestion |

### Retry Decision Tree

```
Error Detected
    |
    +-- Is it transient? (connection, timeout, lock)
    |       |
    |       +-- Yes: Check retry count
    |       |       |
    |       |       +-- Under limit: Apply backoff, retry
    |       |       +-- At limit: Return FAILURE with diagnostic
    |       |
    |       +-- No: Is it recoverable?
    |               |
    |               +-- Yes (schema/migration): Return FAILURE with fix instructions
    |               +-- No (permission): Return FAILURE with escalation path
```


---

## Token Budget Guidelines

### Response Size Targets

| Response Type | Token Range | Content Scope |
|---------------|-------------|---------------|
| **SUCCESS (simple)** | 200-300 tokens | DDL + 2-3 key decisions |
| **SUCCESS (complex)** | 400-500 tokens | DDL + migration + lock analysis |
| **FAILURE (diagnostic)** | 300-500 tokens | Error + root cause + fix steps |
| **FAILURE (complex)** | 600-800 tokens | Error + context + multiple recovery paths |

### Large Output Handling

When DDL exceeds 100 lines or response would exceed 800 tokens:

1. **Store in temp file**: `.claude/temp/postgres-schema-specialist/{timestamp}_{operation}.sql`
2. **Return summary**: Key decisions + file path + execution instructions
3. **Include verification**: How to validate the generated DDL

**Temp File Structure**:
```
.claude/temp/postgres-schema-specialist/
├── 20241220_143022_create_market_data.sql
├── 20241220_143022_create_market_data_down.sql
└── 20241220_150115_add_indexes.sql
```

**Temp File Retention**: 24 hours (auto-cleanup by system)

### Token Optimization Strategies

- Omit obvious constraints (e.g., don't explain why PK is NOT NULL)
- Reference standard patterns by name instead of explaining
- Use code comments in DDL instead of prose explanations
- Consolidate related decisions into single bullet points


---

## Integration Points

### Upstream Agents (Provide Input)

| Agent | Input Type | Expected Format |
|-------|------------|-----------------|
| **python-code-implementer** | ORM requirements | SQLAlchemy model definitions, relationship specs |
| **architecture-reviewer** | System design | Entity relationships, data flow diagrams, scaling requirements |
| **Orchestrator** | User requirements | Natural language schema requirements, business rules |

**Upstream Contract**:
- Entity names and relationships must be explicitly stated
- Data types should include precision requirements (e.g., "price with 8 decimal places")
- Volume estimates help with hypertable/partition decisions

### Downstream Agents (Consume Output)

| Agent | Output Type | Delivery Format |
|-------|-------------|-----------------|
| **postgres-timescale-specialist** | Schema context | Table definitions, column types, index structure |
| **k8s-deployment** | Migration files | Versioned UP/DOWN SQL files in `migrations/` |
| **python-code-implementer** | Schema for ORM | DDL with type mappings, constraint definitions |

**Downstream Contract**:
- DDL must be syntactically valid PostgreSQL
- Migrations must include version identifiers
- Type choices must be documented for ORM mapping

### Handoff Protocols

**To postgres-timescale-specialist**:
```json
{
  "schema_context": {
    "tables": ["market_data", "trades"],
    "hypertables": ["market_data"],
    "key_indexes": ["idx_market_data_symbol_time"]
  }
}
```

**To k8s-deployment**:
```json
{
  "migration_files": [
    "migrations/V001__create_market_data.sql",
    "migrations/V001__create_market_data_down.sql"
  ],
  "execution_order": ["V001"],
  "rollback_tested": true
}
```


---

## Pre-Flight Checklist

### Mandatory Checks Before Any Operation

| Check | Required For | Validation Query/Action |
|-------|--------------|------------------------|
| **Existing schema check** | All modes | `\d table_name` or `pg_catalog.pg_tables` |
| **Migration history check** | create_migration | Check `schema_migrations` or version table |
| **Permission verification** | All modes | `has_table_privilege()`, `has_schema_privilege()` |
| **Entity requirements** | design_schema | Confirm all entities and relationships documented |
| **Rollback requirements** | create_migration | Confirm DOWN script requirements and testing plan |

### Mode-Specific Pre-Flight

#### design_schema
- [ ] All entity names provided
- [ ] Relationships explicitly defined (1:1, 1:N, N:M)
- [ ] Data type requirements specified (precision, length)
- [ ] Business rules for constraints identified
- [ ] Naming convention confirmed

#### create_migration
- [ ] Current table structure retrieved
- [ ] Row count for affected tables (if >100K rows)
- [ ] Existing constraints and indexes documented
- [ ] Migration version determined
- [ ] Rollback procedure defined

#### design_indexes
- [ ] Query patterns documented
- [ ] Existing indexes listed
- [ ] Table statistics available (row count, data distribution)
- [ ] Write vs read ratio understood


#### setup_hypertable
- [ ] Table exists and is empty
- [ ] Primary key includes time column
- [ ] Time column data type is TIMESTAMPTZ
- [ ] Data volume estimates available
- [ ] Ingestion rate documented

#### design_constraints
- [ ] Integrity requirements gathered
- [ ] Business rules documented
- [ ] Referenced tables exist (for FK)
- [ ] ON DELETE/UPDATE behavior specified
- [ ] Performance impact acknowledged for large tables

#### design_backup_strategy
- [ ] RTO (Recovery Time Objective) defined
- [ ] RPO (Recovery Point Objective) defined
- [ ] Data criticality classified
- [ ] Compliance requirements identified
- [ ] Storage/infrastructure constraints known

---

## Schema Design Patterns

### Financial Time-Series Tables

**Standard OHLCV Pattern**:
```sql
CREATE TABLE {symbol}_ohlcv (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    timestamp TIMESTAMPTZ NOT NULL,
    open NUMERIC(18,8) NOT NULL,
    high NUMERIC(18,8) NOT NULL,
    low NUMERIC(18,8) NOT NULL,
    close NUMERIC(18,8) NOT NULL,
    volume BIGINT NOT NULL,
    PRIMARY KEY (id, timestamp)  -- Required for hypertable
);
```


**Key Decisions**:
- `NUMERIC(18,8)` for prices: 10 digits before decimal, 8 after (handles crypto precision)
- `TIMESTAMPTZ` for time: Always timezone-aware for financial data
- Composite PK with timestamp: Required for TimescaleDB hypertables

### Audit Trail Pattern

```sql
CREATE TABLE {entity}_audit (
    audit_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    entity_id BIGINT NOT NULL,
    operation VARCHAR(10) NOT NULL CHECK (operation IN ('INSERT', 'UPDATE', 'DELETE')),
    old_values JSONB,
    new_values JSONB,
    changed_by VARCHAR(255) NOT NULL,
    changed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_{entity}_audit_entity ON {entity}_audit(entity_id);
CREATE INDEX idx_{entity}_audit_time ON {entity}_audit(changed_at);
```

### Soft Delete Pattern

```sql
ALTER TABLE {table}
ADD COLUMN deleted_at TIMESTAMPTZ,
ADD COLUMN deleted_by VARCHAR(255);

CREATE INDEX idx_{table}_active ON {table}(id) WHERE deleted_at IS NULL;
```

---

## Migration Best Practices

### Safe ALTER TABLE Operations

| Operation | Lock Level | Safe for Large Tables |
|-----------|------------|----------------------|
| ADD COLUMN (nullable) | ACCESS EXCLUSIVE (brief) | Yes |
| ADD COLUMN (with default) | ACCESS EXCLUSIVE | PG12+: Yes, Earlier: No |
| DROP COLUMN | ACCESS EXCLUSIVE (brief) | Yes (marks invisible) |
| ALTER COLUMN TYPE | ACCESS EXCLUSIVE | No - rewrite required |
| ADD CONSTRAINT | SHARE UPDATE EXCLUSIVE | Depends on validation |
| CREATE INDEX | SHARE | No - use CONCURRENTLY |
| CREATE INDEX CONCURRENTLY | SHARE UPDATE EXCLUSIVE | Yes |


### Large Table Migration Pattern

For tables with >1M rows:

```sql
-- UP: Add constraint without validation
ALTER TABLE large_table
ADD CONSTRAINT chk_positive_amount CHECK (amount > 0) NOT VALID;

-- Validate in separate transaction (allows concurrent reads)
ALTER TABLE large_table VALIDATE CONSTRAINT chk_positive_amount;

-- DOWN
ALTER TABLE large_table DROP CONSTRAINT chk_positive_amount;
```

### Version Naming Convention

Format: `V{NNN}__{description}.sql`

Examples:
- `V001__create_market_data_table.sql`
- `V002__add_symbol_index.sql`
- `V003__create_trades_table.sql`

DOWN files: `V{NNN}__{description}_down.sql`

---

## TimescaleDB Patterns

### Chunk Interval Selection

| Data Frequency | Recommended Interval | Rationale |
|----------------|---------------------|-----------|
| Sub-second (ticks) | 1 day | High volume, frequent queries |
| Minute bars | 1 week | Standard financial data default |
| Hourly data | 2 weeks | Lower volume |
| Daily data | 1 month | Sparse data |


### Standard Hypertable Setup

```sql
-- Create base table
CREATE TABLE market_data (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    symbol VARCHAR(20) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    open NUMERIC(18,8) NOT NULL,
    high NUMERIC(18,8) NOT NULL,
    low NUMERIC(18,8) NOT NULL,
    close NUMERIC(18,8) NOT NULL,
    volume BIGINT NOT NULL,
    PRIMARY KEY (id, timestamp)
);

-- Convert to hypertable
SELECT create_hypertable('market_data', 'timestamp', chunk_time_interval => INTERVAL '1 week');

-- Add compression policy (compress chunks older than 1 week)
ALTER TABLE market_data SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol'
);
SELECT add_compression_policy('market_data', INTERVAL '1 week');

-- Add retention policy (optional - drop chunks older than 1 year)
SELECT add_retention_policy('market_data', INTERVAL '1 year');
```

### Compression Considerations

- `compress_segmentby`: Columns frequently used in WHERE clauses (usually symbol/ticker)
- `compress_orderby`: Time column (automatic for hypertables)
- Compression ratio: Typically 10-20x for OHLCV data


---

## Constraint Design Patterns

### Naming Convention

```
{table}_{column(s)}_{constraint_type}

Examples:
- market_data_symbol_nn (NOT NULL)
- trades_amount_positive_chk (CHECK)
- orders_user_id_fk (FOREIGN KEY)
- users_email_uq (UNIQUE)
- market_data_symbol_timestamp_pk (PRIMARY KEY)
```

### Common CHECK Patterns

```sql
-- Positive amounts
CONSTRAINT amount_positive_chk CHECK (amount > 0)

-- Enum-like values
CONSTRAINT status_valid_chk CHECK (status IN ('pending', 'completed', 'failed'))

-- Range validation
CONSTRAINT percentage_range_chk CHECK (percentage >= 0 AND percentage <= 100)

-- Conditional NOT NULL
CONSTRAINT completed_requires_timestamp_chk 
    CHECK (status != 'completed' OR completed_at IS NOT NULL)
```

### Foreign Key Actions

| Scenario | ON DELETE | ON UPDATE |
|----------|-----------|-----------|
| User owns orders | CASCADE | CASCADE |
| Order references product | RESTRICT | CASCADE |
| Audit log references user | SET NULL | CASCADE |
| Soft-delete parent | NO ACTION | CASCADE |


---

## Backup Strategy Patterns

### Method Selection Matrix

| Requirement | pg_dump | pg_basebackup | WAL Archiving |
|-------------|---------|---------------|---------------|
| Point-in-time recovery | No | No | Yes |
| Minimal RTO (<5 min) | No | Partial | Yes |
| Minimal RPO (<1 min) | No | No | Yes |
| Schema-only backup | Yes | No | No |
| Single table restore | Yes | No | No |
| Large database (>100GB) | Slow | Fast | Fast |
| Streaming replication | No | Yes | Yes |

### Standard Backup Schedule

**Critical Financial Data**:
- Continuous WAL archiving (RPO: ~0)
- Daily pg_basebackup (full backup)
- Weekly pg_dump (logical backup for portability)
- Monthly recovery test

**Development/Staging**:
- Daily pg_dump
- Weekly full backup
- Monthly recovery test

### Recovery Runbook Template

```markdown
## Recovery Procedure: {database_name}

### Prerequisites
- [ ] Backup files accessible
- [ ] Target server provisioned
- [ ] Credentials available

### Steps
1. Stop application connections
2. Restore from backup: `pg_restore -d {db} {backup_file}`
3. Apply WAL logs (if PITR): `recovery_target_time = '{timestamp}'`
4. Verify data integrity: `SELECT count(*) FROM {critical_tables}`
5. Resume application connections

### Verification Queries
- `SELECT max(timestamp) FROM market_data;`
- `SELECT count(*) FROM users;`

### Rollback
- If restore fails: Revert to previous backup
- Contact: {dba_contact}
```

---

*Last Updated: 2024-12-21*
*Agent Version: 1.0.0*
