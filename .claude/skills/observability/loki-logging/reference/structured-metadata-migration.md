# Structured Metadata Migration Guide

> Migrating high-cardinality data from labels to structured metadata in Loki 3.0+.

---

## Table of Contents

1. [Overview](#overview)
2. [When to Use Structured Metadata](#when-to-use-structured-metadata)
3. [Cardinality Thresholds](#cardinality-thresholds)
4. [Migration Patterns](#migration-patterns)
5. [Promtail Configuration](#promtail-configuration)
6. [Query Pattern Updates](#query-pattern-updates)
7. [Migration Checklist](#migration-checklist)

---

## Overview

Loki 3.0 introduced **structured metadata** as a solution for high-cardinality data that shouldn't be indexed as labels but needs to be searchable. Key benefits:

- **No cardinality impact**: Metadata isn't indexed in stream selectors
- **Still filterable**: Use `| key=value` after stream selector
- **Cost reduction**: Fewer unique streams = lower storage/memory

---

## When to Use Structured Metadata

### Use Structured Metadata For

| Data Type | Example | Rationale |
|-----------|---------|-----------|
| Request IDs | `request_id`, `correlation_id` | Unique per request |
| Trace IDs | `trace_id`, `span_id` | High cardinality by design |
| User IDs | `user_id`, `customer_id` | Many unique values |
| Session IDs | `session_id` | Per-user-session uniqueness |
| Transaction IDs | `txn_id`, `order_id` | Business-unique identifiers |

### Keep as Labels

| Data Type | Example | Rationale |
|-----------|---------|-----------|
| Service name | `service`, `app` | Low cardinality, primary query filter |
| Environment | `env`, `environment` | 3-5 values |
| Log level | `level` | 5-7 values |
| Namespace | `namespace` | Tens of values |
| Pod name | `pod` | Moderate cardinality, useful for filtering |

---

## Cardinality Thresholds

### Decision Matrix

| Estimated Unique Values | Recommendation |
|-------------------------|----------------|
| < 100 | Label (indexed) |
| 100 - 1,000 | Consider context (query patterns) |
| 1,000 - 10,000 | Structured metadata preferred |
| > 10,000 | Structured metadata required |

### Formula for Stream Cardinality

```
Total Streams = Π(unique_values_per_label)
```

Example:
- `namespace`: 10 values
- `service`: 50 values  
- `pod`: 200 values
- `level`: 5 values

Total = 10 × 50 × 200 × 5 = **500,000 streams**

Adding `request_id` (10M unique) would create 5 trillion theoretical streams.

---

## Migration Patterns

### Pattern 1: Pack Stage (Promtail)

Embed high-cardinality data into log line JSON:

```yaml
# Before: Labels
pipeline_stages:
  - json:
      expressions:
        request_id: request_id
        trace_id: trace_id
  - labels:
      request_id:  # BAD: Creates cardinality explosion
      trace_id:

# After: Pack into log line
pipeline_stages:
  - json:
      expressions:
        request_id: request_id
        trace_id: trace_id
        level: level
  - labels:
      level:       # Keep low-cardinality
  - pack:
      labels:
        - request_id
        - trace_id
      ingest_timestamp: true
```

### Pattern 2: Structured Metadata (Loki 3.0+)

Use OTLP-native structured metadata:

```yaml
# Promtail config for structured metadata
pipeline_stages:
  - json:
      expressions:
        request_id: request_id
        trace_id: trace_id
  - structured_metadata:
      request_id:
      trace_id:
```

### Pattern 3: Hybrid Approach

Keep frequently-filtered data as labels, rest as metadata:

```yaml
pipeline_stages:
  - json:
      expressions:
        level: level
        service: service
        request_id: request_id
        user_id: user_id
  - labels:
      level:     # Frequently filtered
      service:   # Frequently filtered
  - structured_metadata:
      request_id:  # High cardinality, sometimes filtered
      user_id:     # High cardinality, sometimes filtered
```

---

## Promtail Configuration

### Before Migration

```yaml
scrape_configs:
  - job_name: app
    pipeline_stages:
      - json:
          expressions:
            level: level
            request_id: request_id
            trace_id: trace_id
            user_id: user_id
      - labels:
          level:
          request_id:    # Problem: High cardinality
          trace_id:      # Problem: High cardinality
          user_id:       # Problem: High cardinality
```

### After Migration (Pack Approach)

```yaml
scrape_configs:
  - job_name: app
    pipeline_stages:
      - json:
          expressions:
            level: level
            request_id: request_id
            trace_id: trace_id
            user_id: user_id
      - labels:
          level:         # Keep: Low cardinality
      - pack:
          labels:
            - request_id
            - trace_id
            - user_id
          ingest_timestamp: true
```

### After Migration (Structured Metadata)

```yaml
scrape_configs:
  - job_name: app
    pipeline_stages:
      - json:
          expressions:
            level: level
            request_id: request_id
            trace_id: trace_id
            user_id: user_id
      - labels:
          level:
      - structured_metadata:
          request_id:
          trace_id:
          user_id:
```

---

## Query Pattern Updates

### Before: Label-Based Queries

```logql
# Won't work after migration - these are no longer labels
{service="api", request_id="abc123"}
{service="api"} | request_id="abc123"  # Wrong syntax
```

### After: Filter Expression Queries

```logql
# Pack approach: Filter JSON in log line
{service="api"} | json | request_id="abc123"

# Structured metadata: Direct filter
{service="api"} | request_id="abc123"

# Combined filtering
{service="api", level="error"} 
  | request_id="abc123" 
  | trace_id="xyz789"
```

### Performance Comparison

| Query Type | Before Migration | After Migration |
|------------|------------------|-----------------|
| By label only | Fast (indexed) | Fast (indexed) |
| By removed label | Fast (indexed) | Slower (post-filter) |
| By metadata | N/A | Medium (bloom filter) |
| Combined | Fast | Fast + Medium |

---

## Migration Checklist

### Pre-Migration

- [ ] Audit current label cardinality (`count by (__name__)(log_lines_total)`)
- [ ] Identify labels with >1000 unique values
- [ ] Document affected dashboards and alerts
- [ ] Plan query migration

### Migration Steps

1. [ ] Update Promtail pipeline stages
2. [ ] Deploy Promtail changes to staging
3. [ ] Verify new log format in Loki
4. [ ] Update Grafana dashboards with new query syntax
5. [ ] Update alerting rules
6. [ ] Monitor cardinality reduction
7. [ ] Deploy to production
8. [ ] Deprecate old queries

### Post-Migration Validation

- [ ] Cardinality reduced by expected amount
- [ ] No query errors in dashboards
- [ ] Alert rules firing correctly
- [ ] Query performance acceptable

---

## Troubleshooting

### High Cardinality Persists

**Symptom**: Stream count still high after migration

**Check**: Verify Promtail is using updated config:
```bash
kubectl rollout status daemonset/promtail -n monitoring
curl -s localhost:9080/config | grep -A20 pipeline_stages
```

### Queries Return No Results

**Symptom**: Queries using old label syntax return empty

**Fix**: Update query syntax:
```logql
# Old (won't work)
{app="api", request_id="123"}

# New
{app="api"} | request_id="123"
```

### Structured Metadata Not Appearing

**Symptom**: Metadata fields not filterable

**Check**: Verify Loki version supports structured metadata (3.0+):
```bash
curl -s localhost:3100/loki/api/v1/status/buildinfo | jq .version
```

---

**Source**: Loki Documentation + Deprecated loki-query-specialist agent
