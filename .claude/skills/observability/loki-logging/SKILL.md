---
name: loki-logging
description: >
  Use this skill when configuring log forwarding, managing retention policies,
  designing label strategies, or optimizing logging infrastructure. Covers
  Promtail config, structured_metadata, cardinality management.
  Keywords: loki, logging, promtail, retention, labels, structured_metadata.
---

# Loki Logging Infrastructure

Configure log forwarding, retention policies, and label strategies for optimal Loki performance.

## Reference Documentation

**Detailed Guides** (read when relevant):
- **Loki Architecture** → [reference/loki-architecture.md](reference/loki-architecture.md)
- **Structured Metadata Migration** → [reference/structured-metadata-migration.md](reference/structured-metadata-migration.md)
- **Promtail Configuration** → [reference/promtail-configuration.md](reference/promtail-configuration.md)

## Label Strategy

### Bounded Cardinality Principle

Labels create streams. High-cardinality labels cause stream explosion.

**Cardinality Thresholds:**
| Range | Classification | Action |
|-------|----------------|--------|
| <20 values | Low (Safe) | Use as label |
| 20-100 values | Medium (Caution) | Monitor, consider migration |
| >100 values | High (Critical) | Migrate to structured_metadata |

**Good Labels (Low Cardinality):**
- `service_name`, `namespace`, `deployment_environment`, `log_level`

**Bad Labels (High Cardinality):**
- `request_id`, `user_id`, `trace_id`, `session_id`, `pod_name` (dynamic)

### structured_metadata Migration

Loki 2.9+ supports structured_metadata for high-cardinality data WITHOUT creating streams.

**Before (High-Cardinality Label):**
```yaml
static_configs:
  - labels:
      service_name: api
      request_id: __value__  # WRONG: Creates millions of streams
```

**After (structured_metadata):**
```yaml
static_configs:
  - labels:
      service_name: api
      # request_id removed from labels
pipeline_stages:
  - json:
      expressions:
        request_id: request_id
  - structured_metadata:
      request_id: ""
```

**Impact**: 73% cost reduction documented (ActiveCampaign case study), 99%+ stream count reduction.

**Query Change:**
```logql
# Before (label filter)
{service="api", request_id="abc123"}

# After (structured_metadata filter)
{service="api"} | request_id="abc123"
```

---

## Promtail Configuration Patterns

### Standard JSON Log Forwarding

```yaml
scrape_configs:
  - job_name: app_logs
    static_configs:
      - targets: [localhost]
        labels:
          job: app_logs
          service_name: api
          deployment_environment: prod
          __path__: /var/log/app/*.log

    pipeline_stages:
      # 1. Parse JSON
      - json:
          expressions:
            timestamp: timestamp
            level: level
            message: message
            user_id: user_id

      # 2. Extract timestamp
      - timestamp:
          source: timestamp
          format: RFC3339

      # 3. Low-cardinality labels only
      - labels:
          level: ""

      # 4. High-cardinality to structured_metadata
      - structured_metadata:
          user_id: ""
```

### Label Extraction Rules

1. **Only extract low-cardinality values as labels**
2. **Use structured_metadata for high-cardinality values**
3. **Timestamp extraction required for correct ordering**
4. **JSON parser preferred over regexp (100x faster)**

---

## Retention Policy Configuration

### Gauntlet Agents Default: 168h (7 days)

```yaml
# k8s/local/loki.yaml
limits_config:
  retention_period: 168h
  max_query_lookback: 168h
```

### Retention Considerations

| Environment | Recommended Retention | Rationale |
|-------------|----------------------|-----------|
| Development | 24-72h | Cost savings, fast iteration |
| Staging | 72-168h | Enough for testing cycles |
| Production | 168h-720h | Compliance, debugging needs |

**Query Constraint**: Queries beyond retention return empty/partial results.

---

## OTLP Integration (Gauntlet Agents)

**Critical**: Gauntlet Agents uses OTLP format, NOT JSON lines.

### OTLP Resource Attributes as Labels

14 attributes auto-indexed from OTLP:
- `service_name`, `service_namespace`, `service_instance_id`
- `deployment_environment`
- `telemetry_sdk_name`, `telemetry_sdk_language`, `telemetry_sdk_version`
- `host_name`, `host_arch`, `os_type`, `os_description`
- `process_pid`, `process_executable_name`, `process_executable_path`

### Query Pattern for OTLP Logs

```logql
# Use indexed OTLP attributes in stream selector
{service_name="orchestrator", service_namespace="gauntlet-agents"}
| json
| level="error"
```

**Anti-Pattern**: Do NOT use `| json` parser on OTLP logs expecting JSON structure - causes JSONParserErr.

---

## High-Cardinality Management

### Detection Methods

```bash
# Check label cardinality
logcli labels user_id --since=24h | wc -l
# >100 = HIGH CARDINALITY

# Check stream count
logcli series '{namespace="prod"}' --since=1h | wc -l
# >10,000 = CRITICAL
```

### Cost Reduction Patterns

**ActiveCampaign Case Study Results:**
- Stream count: 127,452 to 45 (99.96% reduction)
- Cost: $10,000/month to $2,700/month (73% reduction)
- Query time: 90s to 9s (90% improvement)

**Migration Checklist:**
- [ ] Identify labels with >100 unique values
- [ ] Update Promtail config (remove high-cardinality labels)
- [ ] Add structured_metadata extraction
- [ ] Update queries (label filter to metadata filter)
- [ ] Validate stream count reduction

---

## Log Format Recommendations

### Format Preference Hierarchy

1. **JSON** (preferred): 100x faster parsing than regexp
2. **Logfmt**: Fast parsing, compact format
3. **Pattern**: 10x faster than regexp for consistent structures
4. **Regexp**: Last resort for irregular formats

### JSON Format Standard

```json
{
  "timestamp": "2025-01-15T14:23:45Z",
  "level": "error",
  "service": "api",
  "message": "Database timeout",
  "duration_ms": 5000,
  "user_id": "abc123"
}
```

**Anti-Patterns to Avoid:**
1. **JSON-in-String**: `{"message": "{\"nested\":\"json\"}"}`
2. **Mixed formats**: Inconsistent structure across log lines
3. **Nested JSON**: Deep nesting requires multi-stage parsing
4. **Unstructured**: Plain text requiring regexp extraction

---

## Architecture Constraints

### Query Limits (Local Deployment)

| Limit | Value | Error When Exceeded |
|-------|-------|---------------------|
| max_query_series | 1000 | 400 "max series limit exceeded" |
| query_timeout | 5m | 503 timeout |
| max_query_lookback | 168h | Empty/partial results |
| max_entries_limit | 5000 | Results truncated |

### Structured Metadata Limits

```yaml
limits_config:
  allow_structured_metadata: true
  max_structured_metadata_size: 64KB
  max_structured_metadata_entries_count: 128
```

---

## Quick Reference

### Stream Count Formula

```
Expected Streams = Product of all label cardinalities
Example: 10 services x 5 namespaces x 3 environments = 150 streams (healthy)
```

### Health Thresholds

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Total Streams | <1,000 | 1,000-10,000 | >10,000 |
| Label Cardinality | <20 | 20-100 | >100 |
| Query Time | <10s | 10-60s | >60s |

---

## Validation Checklist

Before deploying logging configuration:

- [ ] All labels have bounded cardinality (<100 values)
- [ ] High-cardinality data uses structured_metadata
- [ ] Retention period matches compliance requirements
- [ ] Stream count projected to remain <10,000
- [ ] JSON format used where possible
- [ ] Timestamp extraction configured
