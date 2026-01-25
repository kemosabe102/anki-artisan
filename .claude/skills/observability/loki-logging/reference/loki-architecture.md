# Loki Architecture & Configuration Constraints

## Table of Contents

1. [Schema v13 (TSDB) Storage](#schema-v13-tsdb-storage)
2. [OTLP Resource Attributes](#otlp-resource-attributes)
3. [Query Performance Constraints](#query-performance-constraints)
4. [Structured Metadata Support](#structured-metadata-support)
5. [Integration Points](#integration-points)
6. [Validation Checks](#validation-checks)

---

## Schema v13 (TSDB) Storage

### Components

| Component | Value | Limitation |
|-----------|-------|------------|
| Index Type | TSDB | 7-day retention (168h) |
| Storage Backend | Filesystem | Single-node, no replication |
| Chunk Format | Compressed | Query must decompress |
| Index Granularity | Per-stream | High cardinality = overhead |

### Time-Range Optimization

```logql
{service="api"} [5m]   # ✅ Fast (TSDB optimized)
{service="api"} [7d]   # ⚠️ Slower (queries entire retention)
{service="api"} [8d]   # ❌ Partial results (only 7 days available)
```

### Schema Configuration

```yaml
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

---

## OTLP Resource Attributes

### 14 Indexed Labels

| Attribute | Example Value |
|-----------|---------------|
| service_name | orchestrator, api |
| service_namespace | gauntlet-agents |
| service_instance_id | unique-id-123 |
| deployment_environment | prod, dev, staging |
| telemetry_sdk_name | opentelemetry |
| telemetry_sdk_language | python |
| telemetry_sdk_version | 1.20.0 |
| host_name | server-001 |
| host_arch | amd64 |
| os_type | linux |
| os_description | Ubuntu 22.04 |
| process_pid | 12345 |
| process_executable_name | python |
| process_executable_path | /usr/bin/python |

### Query Patterns

```logql
# ✅ Fast: Use indexed labels in stream selector
{service_name="orchestrator"} |= "error"

# ❌ Slower: Line filter without indexed label
{job="loki"} |= "service: orchestrator" |= "error"

# ✅ Combine indexed labels to narrow scope
{service_name="api", deployment_environment="prod"}

# ❌ Non-indexed attributes require parser
{custom_field="value"}  # Won't work
{service_name="api"} | json | custom_field="value"  # ✅ Correct
```

### OTLP Configuration

```yaml
otlp_config:
  resource_attributes:
    attributes_config:
      - action: index_label
        attributes:
          - service.name        # → service_name label
          - service.namespace   # → service_namespace label
          - deployment.environment
```

---

## Query Performance Constraints

### Hard Limits

| Limit | Value | Exceeded Behavior |
|-------|-------|-------------------|
| max_query_series | 1,000 | 400 error |
| query_timeout | 5 minutes | 503 error |
| max_query_lookback | 168h (7d) | Partial results |
| max_concurrent_queries | 32 | Queries queue |
| max_entries_limit_per_query | 5,000 | Results truncated |

### Mitigation Strategies

**Series Limit Exceeded:**
```logql
# ❌ Too many series
count by (pod) (rate({namespace="prod"}[7d]))

# ✅ Reduced time range
count by (pod) (rate({namespace="prod"}[1h]))

# ✅ Use aggregations
sum(rate({namespace="prod"}[5m]))
```

**Query Timeout:**
```logql
# ❌ Large time range
{namespace="prod"} [7d]

# ✅ Use $__auto for automatic adjustment
rate({service="api"}[$__auto])
```

### Limits Configuration

```yaml
limits_config:
  max_query_series: 1000
  query_timeout: 5m
  max_query_lookback: 168h
  max_concurrent_queries: 32
  max_entries_limit_per_query: 5000
  split_queries_by_interval: 1h
```

---

## Structured Metadata Support

### Labels vs Structured Metadata

| Feature | Labels | Structured Metadata |
|---------|--------|---------------------|
| Stream creation | YES | NO |
| Indexed | YES (fast) | NO (scanning) |
| Cardinality limit | <100 recommended | Unlimited |
| Use case | Low-cardinality | High-cardinality |

### When to Use Each

**Labels** (low-cardinality):
- service_name, namespace, environment
- log_level, http_method, status_code

**Structured Metadata** (high-cardinality):
- request_id, user_id, trace_id
- session_id, correlation_id

### Query Pattern

```logql
# Cannot use in stream selector
{request_id="abc123"}  # ❌ Won't work

# Access via parser
{service="api"} | request_id="abc123"  # ✅ Correct
```

### Configuration

```yaml
limits_config:
  allow_structured_metadata: true
  max_structured_metadata_size: 64KB
  max_structured_metadata_entries_count: 128
```

---

## Integration Points

### OTLP Collector Pipeline

```
Application (OTLP SDK)
    ↓
OTLP Collector
    ↓ (enriches, maps attributes)
Loki (indexes labels, stores logs)
```

### Grafana Dashboard Integration

```logql
# Dashboard variable query
GET /loki/api/v1/label/service_name/values

# Panel query with auto-interval
sum by (service_name) (count_over_time({namespace="gauntlet-agents"}[$__auto]))
```

---

## Validation Checks

### Series Count Validation

```logql
# Count series before execution
count(count by (pod) (rate({namespace="prod"}[5m])))
```

**Pass**: Series count < 1000
**Fail**: Series count >= 1000

### Time Range Validation

**Pass**: Time range <= 168h AND from >= (now - 168h)
**Fail**: Time range > 168h

### Label Cardinality Validation

```logql
# Check label cardinality
count(count by (label_name) ({namespace="prod"}[5m]))
```

**Pass**: Cardinality < 100 unique values
**Fail**: Cardinality > 100 (likely series limit issues)

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Exceeding 1000 series | Add more selective stream selectors |
| Query timeout >5min | Reduce time range or use aggregations |
| Querying outside 7-day retention | Limit queries to last 168h |
| High-cardinality label in selector | Move to structured metadata |
| Using [1d] range on short query | Use [$__auto] for auto adjustment |
| Grouping by high-cardinality label | Use topk() or aggregate without grouping |

---

## Sources

- Grafana Loki Configuration: https://grafana.com/docs/loki/latest/configuration/
- OpenTelemetry Semantic Conventions: https://opentelemetry.io/docs/specs/semconv/resource/
