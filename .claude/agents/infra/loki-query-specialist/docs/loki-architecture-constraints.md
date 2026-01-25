# Loki Architecture & Configuration Constraints

**Category**: domain-specific
**Domain**: Local Loki v3.5.7 deployment configuration and query constraints
**Confidence**: 0.95
**Last Updated**: 2025-11-10T00:00:00Z
**Agent**: loki-query-specialist

---

## Overview

Local Loki v3.5.7 deployment configuration including schema version 13 with TSDB, OTLP resource attributes as indexed labels, query performance constraints, and retention policies. Understanding these constraints is critical for writing efficient queries and avoiding query failures.

**Key Concepts**:

- **Schema v13 (TSDB)**: Time Series Database index with filesystem storage backend
- **OTLP Resource Attributes**: 14 OpenTelemetry attributes automatically indexed as queryable labels
- **Query Limits**: Hard constraints on series count (1000), memory (2GB), and timeouts (5 minutes)
- **Retention Policy**: 168 hours (7 days) log retention with automatic cleanup

---

## Core Frameworks

### Framework 1: OTLP Resource Attributes as Indexed Labels

**Purpose**: Understand which log attributes are indexed and available for efficient stream selector filtering.

**When to Use**:
- When constructing stream selectors (`{label="value"}`)
- To optimize query performance (indexed labels = fast)
- When deciding between stream selector vs line filter

**Components** (14 Indexed Labels):

1. **service_name**: Service identifier (e.g., "orchestrator", "debugger")
2. **service_namespace**: Logical grouping (e.g., "gauntlet-agents")
3. **service_instance_id**: Unique instance identifier
4. **deployment_environment**: Environment name (e.g., "prod", "dev")
5. **telemetry_sdk_name**: SDK name (e.g., "opentelemetry")
6. **telemetry_sdk_language**: Language (e.g., "python")
7. **telemetry_sdk_version**: SDK version (e.g., "1.20.0")
8. **host_name**: Hostname of log source
9. **host_arch**: CPU architecture (e.g., "amd64")
10. **os_type**: Operating system (e.g., "linux")
11. **os_description**: OS version details
12. **process_pid**: Process ID
13. **process_executable_name**: Executable name
14. **process_executable_path**: Full executable path

**How to Apply**:

1. **Prefer indexed labels in stream selectors** for performance:
   ```logql
   {service_name="orchestrator"} |= "error"  ✅ Fast
   {job="loki"} |= "service: orchestrator" |= "error"  ❌ Slower
   ```

2. **Combine multiple indexed labels** to narrow scope:
   ```logql
   {service_name="api", deployment_environment="prod"}
   ```

3. **Avoid filtering on non-indexed attributes** in stream selector:
   ```logql
   {custom_field="value"}  ❌ Won't work (not indexed)
   {service_name="api"} | json | custom_field="value"  ✅ Correct
   ```

4. **Check available label values** before querying:
   - API endpoint: `/loki/api/v1/label/service_name/values`
   - Returns all service names with logs

**Example from Codebase**:

```yaml
# k8s/local/loki.yaml - OTLP configuration
otlp_config:
  resource_attributes:
    attributes_config:
      - action: index_label  # Creates queryable label
        attributes:
          - service.name        # → service_name label
          - service.namespace   # → service_namespace label
          - deployment.environment  # → deployment_environment label
```

**Source**: `k8s/local/loki.yaml` lines 45-72

---

### Framework 2: Schema v13 (TSDB) Storage Architecture

**Purpose**: Understand storage backend capabilities and limitations for query planning.

**When to Use**:
- When diagnosing query performance issues
- To understand retention behavior
- When estimating query resource usage

**Components**:

1. **Index Type**: TSDB (Time Series Database)
   - **Benefit**: Efficient time-range queries
   - **Limitation**: 7-day retention (168h)

2. **Storage Backend**: Filesystem
   - **Location**: `/loki/data` (container path)
   - **Limitation**: Single-node, no replication

3. **Chunk Format**: Compressed blocks
   - **Benefit**: Reduced storage footprint
   - **Limitation**: Query must decompress chunks

4. **Index Granularity**: Per-stream TSDB index
   - **Benefit**: Fast stream selector filtering
   - **Limitation**: High cardinality = more index overhead

**How to Apply**:

1. **Optimize for time-range queries**:
   ```logql
   {service="api"} [5m]  ✅ Fast (TSDB optimized)
   {service="api"} [7d]  ⚠️ Slower (queries entire retention)
   ```

2. **Understand retention limits** (168 hours):
   ```logql
   {service="api"} [8d]  ❌ Will return partial results (only 7 days available)
   ```

3. **Avoid high-cardinality labels**:
   ```logql
   {request_id=~".*"}  ❌ High cardinality (unique per request)
   {service_name=~".*"}  ✅ Low cardinality (few unique services)
   ```

**Example from Codebase**:

```yaml
# k8s/local/loki.yaml - Schema configuration
schema_config:
  configs:
    - from: 2024-01-01
      store: tsdb
      object_store: filesystem
      schema: v13
      index:
        prefix: index_
        period: 24h
```

**Source**: `k8s/local/loki.yaml` lines 28-37

---

### Framework 3: Query Performance Constraints

**Purpose**: Stay within query limits to avoid failures and timeouts.

**When to Use**:
- When writing queries for large time ranges
- To diagnose query timeout errors
- When optimizing dashboard queries

**Components**:

1. **max_query_series**: 1000 series
   - **Meaning**: Maximum unique label combinations returned
   - **Exceeding**: Returns 400 error "max series limit exceeded"

2. **query_timeout**: 5 minutes (300s)
   - **Meaning**: Maximum query execution time
   - **Exceeding**: Returns 503 error with timeout message

3. **max_query_lookback**: 168h (7 days)
   - **Meaning**: Maximum time range for queries
   - **Exceeding**: Returns partial results or error

4. **max_concurrent_queries**: 32
   - **Meaning**: Maximum simultaneous queries
   - **Exceeding**: Queries queue until slot available

5. **max_entries_limit_per_query**: 5000
   - **Meaning**: Maximum log lines returned
   - **Exceeding**: Results truncated to 5000 lines

**How to Apply**:

1. **Reduce time range if hitting series limit**:
   ```logql
   # ❌ Too many series
   count by (pod) (rate({namespace="prod"}[7d]))

   # ✅ Reduced time range
   count by (pod) (rate({namespace="prod"}[1h]))
   ```

2. **Use aggregations to reduce series count**:
   ```logql
   # ❌ Returns 1 series per pod (could exceed 1000)
   rate({namespace="prod"}[5m])

   # ✅ Returns 1 series total
   sum(rate({namespace="prod"}[5m]))
   ```

3. **Add more selective stream selectors**:
   ```logql
   # ❌ Broad query (many series)
   {namespace="prod"}

   # ✅ Narrow query (fewer series)
   {namespace="prod", service_name="api"}
   ```

4. **Break large queries into smaller chunks**:
   ```logql
   # Instead of 7-day query, run 7 separate 1-day queries
   ```

**Example from Codebase**:

```yaml
# k8s/local/loki.yaml - Query limits
limits_config:
  max_query_series: 1000
  query_timeout: 5m
  max_query_lookback: 168h
  max_concurrent_queries: 32
  max_entries_limit_per_query: 5000
  split_queries_by_interval: 1h
```

**Source**: `k8s/local/loki.yaml` lines 75-95

---

### Framework 4: Structured Metadata Support

**Purpose**: Leverage structured metadata for high-cardinality data without impacting index size.

**When to Use**:
- For high-cardinality values (request IDs, user IDs, trace IDs)
- When label cardinality would exceed limits
- To store context without creating indexed labels

**Components**:

1. **Structured Metadata**: Key-value pairs attached to log lines
   - **Not indexed**: Cannot be used in stream selectors
   - **Queryable**: Can be filtered after parsing
   - **Use case**: High-cardinality attributes

2. **Access Pattern**:
   ```logql
   # Cannot use in stream selector
   {request_id="abc123"}  ❌ Won't work

   # Access via line filter or parser
   {service="api"} | json | request_id="abc123"  ✅ Correct
   ```

**How to Apply**:

1. **Store high-cardinality data as structured metadata**:
   - Request IDs, user IDs, trace IDs, session IDs
   - These would create too many index entries as labels

2. **Use indexed labels for low-cardinality filtering**:
   - Service names, namespaces, environments, log levels
   - Small set of unique values

3. **Query pattern**: Stream selector → Parser → Metadata filter
   ```logql
   {service="api"} | json | trace_id="xyz789"
   ```

**Example from Codebase**:

```yaml
# k8s/local/loki.yaml - Structured metadata enabled
limits_config:
  allow_structured_metadata: true
  max_structured_metadata_size: 64KB
  max_structured_metadata_entries_count: 128
```

**Source**: `k8s/local/loki.yaml` lines 88-91

---

## Integration Points

### Integration 1: OTLP Collector Pipeline

**Relationship**: Logs flow from OpenTelemetry SDK → OTLP Collector → Loki, with resource attributes mapped to labels.

**Coordination Pattern**:

1. **Application emits logs** with OTLP SDK:
   - Resource attributes: service.name, service.namespace, etc.
   - Log attributes: level, message, timestamp, custom fields

2. **OTLP Collector processes logs**:
   - Enriches with host/process attributes
   - Maps resource attributes to Loki labels (14 attributes)
   - Preserves log attributes as structured metadata

3. **Loki indexes and stores logs**:
   - Creates TSDB index on mapped labels
   - Stores log body + structured metadata in chunks

**Example Usage**:

```python
# Application code with OpenTelemetry SDK
from opentelemetry import trace, logs

resource = Resource.create({
    "service.name": "orchestrator",  # → service_name label
    "service.namespace": "gauntlet-agents",  # → service_namespace label
    "deployment.environment": "prod"  # → deployment_environment label
})

logger = logs.get_logger(__name__, resource=resource)
logger.info("Processing request", extra={"request_id": "abc123"})  # request_id = structured metadata
```

Query in Loki:
```logql
{service_name="orchestrator", service_namespace="gauntlet-agents"}
| json
| request_id="abc123"
```

**Dependencies**:
- OTLP Collector must be configured to forward to Loki
- Resource attributes must match Loki's `otlp_config.resource_attributes.attributes`
- Application SDK must set appropriate resource attributes

---

### Integration 2: Grafana Dashboards

**Relationship**: Grafana queries Loki via HTTP API, respecting query limits and timeout constraints.

**Coordination Pattern**:

1. **Dashboard variable queries** (label value selection):
   ```
   GET /loki/api/v1/label/service_name/values
   ```

2. **Panel queries** (log/metric visualization):
   ```
   GET /loki/api/v1/query_range?query={service="api"}[5m]
   ```

3. **Auto-interval adjustment** with `$__auto`:
   ```logql
   rate({service="api"}[$__auto])
   ```
   - Grafana calculates interval based on dashboard time range
   - Prevents query timeout on large time ranges

**Example Usage**:

```json
// Grafana dashboard panel
{
  "targets": [
    {
      "expr": "sum by (service_name) (count_over_time({namespace=\"gauntlet-agents\"}[$__auto]))",
      "refId": "A"
    }
  ]
}
```

**Dependencies**:
- Grafana datasource configured with Loki URL (`http://loki:3100`)
- Queries must stay under max_query_series (1000) and query_timeout (5m)
- Use `$__auto` for automatic interval adjustment

---

## Validation & Quality Checks

### Check 1: Query Series Count Validation

**What to Validate**: Ensure query won't exceed max_query_series (1000) before execution.

**Validation Method**:

1. Run query with `count()` wrapper to estimate series count:
   ```logql
   count(count by (pod) (rate({namespace="prod"}[5m])))
   ```

2. Compare result to max_query_series limit (1000)

3. If exceeding limit, apply mitigation strategies

**Pass Criteria**: Series count < 1000
**Fail Criteria**: Series count >= 1000 (will return 400 error)

**Remediation**:
- Add more selective stream selectors: `{namespace="prod", service="api"}`
- Reduce time range: `[5m]` instead of `[1h]`
- Aggregate at higher level: `sum()` instead of `sum by (pod)`
- Split into multiple queries by label value

---

### Check 2: Time Range Validation

**What to Validate**: Ensure query time range is within retention period (168h).

**Validation Method**:

1. Calculate query time range from dashboard/API parameters
2. Compare to max_query_lookback (168h = 7 days)
3. Check if `from` timestamp is within retention window

**Pass Criteria**: Time range <= 168h AND from >= (now - 168h)
**Fail Criteria**: Time range > 168h OR from < (now - 168h)

**Remediation**:
- Reduce time range to 7 days maximum
- Adjust dashboard default time range
- Use relative time ranges: "Last 6 hours" instead of absolute dates
- Inform user if historical data requested is outside retention

---

### Check 3: Label Cardinality Validation

**What to Validate**: Ensure grouped labels have reasonable cardinality to avoid series explosion.

**Validation Method**:

1. Query label value count:
   ```logql
   count(count by (label_name) ({namespace="prod"}[5m]))
   ```

2. Identify high-cardinality labels (>100 unique values)

3. Assess if grouping by this label will exceed series limit

**Pass Criteria**: Label cardinality < 100 unique values
**Fail Criteria**: Label cardinality > 100 (likely to cause series limit issues)

**Remediation**:
- Avoid grouping by high-cardinality labels (request_id, trace_id)
- Use structured metadata for high-cardinality data
- Group by low-cardinality labels (service_name, namespace)
- Apply additional filters to reduce cardinality before grouping

---

## Common Pitfalls & Solutions

| Pitfall                              | Detection                                  | Solution                                    |
| ------------------------------------ | ------------------------------------------ | ------------------------------------------- |
| Exceeding series limit (1000)        | 400 error "max series limit exceeded"      | Add more selective stream selectors         |
| Query timeout (>5min)                | 503 error with timeout message             | Reduce time range or use aggregations       |
| Querying outside retention (>7 days) | Empty results or partial data              | Limit queries to last 7 days (168h)         |
| High-cardinality label as stream selector | "label not found" or performance issues    | Move to structured metadata or line filter  |
| Using `[1d]` range on short query    | Insufficient data points for visualization | Use `[$__auto]` for automatic adjustment    |
| Grouping by high-cardinality label   | Series count explosion                     | Aggregate without grouping or use topk()    |

---

## Glossary

- **TSDB**: Time Series Database index format (Loki schema v13)
- **OTLP**: OpenTelemetry Protocol for log/metric/trace ingestion
- **Resource Attributes**: OpenTelemetry metadata describing log source (service, host, process)
- **Indexed Labels**: Labels stored in TSDB index for fast stream selector filtering
- **Structured Metadata**: Key-value pairs attached to logs but not indexed
- **Cardinality**: Number of unique values for a label (high cardinality = performance impact)
- **Series**: Unique combination of label values (each series counted toward 1000 limit)
- **Retention Period**: Time logs are stored before automatic deletion (168h = 7 days)

---

## Sources & References

1. Codebase Reference: `k8s/local/loki.yaml`
   - Pattern: Loki v3.5.7 configuration with schema v13, OTLP mapping, query limits
   - Usage: Local Kubernetes deployment configuration
   - Lines: 1-150 (full configuration)

2. Grafana Loki Documentation - Configuration: https://grafana.com/docs/loki/latest/configuration/
   - Accessed: 2025-11-10
   - Confidence: 0.90

3. OpenTelemetry Semantic Conventions: https://opentelemetry.io/docs/specs/semconv/resource/
   - Accessed: 2025-11-10
   - Confidence: 0.90

---

## Changelog

- **2025-11-10**: Initial documentation created from researcher-codebase findings (confidence: 0.95)

---

## Related Documentation

- `logql-syntax-reference.md`: LogQL syntax and query structure
- `query-optimization-patterns.md`: Query performance best practices
- `api-validation-workflow.md`: Loki HTTP API for query testing
