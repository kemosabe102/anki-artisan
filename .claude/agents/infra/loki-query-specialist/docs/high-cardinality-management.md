# High-Cardinality Management

---
title: "High-Cardinality Management"
category: "Performance"
domain: "Observability"
confidence: 0.93
last_updated: "2025-11-10"
agent: "loki-query-specialist"
sources:
  - url: "https://grafana.com/docs/loki/latest/get-started/labels/bp-labels/"
    quality: 0.95
    contribution: "Label cardinality thresholds, best practices"
  - url: "https://grafana.com/docs/loki/latest/configure/#structured-metadata"
    quality: 0.92
    contribution: "structured_metadata configuration and usage"
  - url: "https://activecampaign.engineering/how-we-improved-our-loki-performance-after-discovering-a-critical-anti-pattern/"
    quality: 0.92
    contribution: "73% cost reduction case study"
---

## Overview

High-cardinality labels are the #1 cause of Loki performance degradation and cost explosion. A single high-cardinality label (>1000 unique values) can create millions of streams, overwhelming the index and making queries unusable.

**Purpose**: Detect, quantify, and remediate high-cardinality labels before they impact production systems.

**When to Use**:
- Before adding new labels to Promtail configuration
- When query errors show "max series limit exceeded"
- During cost optimization reviews
- Post-mortem analysis after performance incidents

**Impact**: Documented case studies show 73% cost reduction and 10-100x query speedup from cardinality remediation.

---

## What is High Cardinality?

### Definition

**Cardinality**: Number of unique values for a label across all log streams.

**Classification**:
- **Low Cardinality**: <20 unique values (e.g., service_name, namespace, log_level)
- **Medium Cardinality**: 20-100 unique values (e.g., pod_name in small clusters, endpoint paths)
- **High Cardinality**: >100 unique values (e.g., request_id, user_id, trace_id)

**Why It Matters**:
- Loki creates one stream per unique label combination
- High cardinality = exponential stream growth
- Stream count directly impacts query performance and cost

**Example**:
```
Scenario: 3 labels with different cardinalities
- service_name: 10 unique values (low)
- pod_name: 50 unique values (medium)
- request_id: 10,000 unique values (HIGH)

Stream count = 10 × 50 × 10,000 = 5,000,000 streams
Query impact: 5M streams to scan vs 500 streams without request_id label
```

---

## Detection Methods

### Method 1: logcli Label Analysis

```bash
# Check cardinality for specific label
logcli labels user_id --since=24h | wc -l

# Output: 15,234 (HIGH CARDINALITY DETECTED)

# List all labels with cardinality
logcli labels --since=24h

# Check label values distribution
logcli labels --since=24h user_id --limit=100
```

**Interpretation**:
- Result <20: Low cardinality (safe to use as label)
- Result 20-100: Medium cardinality (use with caution, monitor)
- Result >100: High cardinality (DO NOT use as label, migrate to structured_metadata)

---

### Method 2: Stream Count Analysis

```bash
# Count total streams for namespace
logcli series '{namespace="prod"}' --since=1h | wc -l

# Output: 45,237 (EXCESSIVE - should be <1000)

# Identify labels contributing to high stream count
logcli series '{namespace="prod"}' --since=1h | head -20
```

**Example Output**:
```
{namespace="prod",service="api",request_id="abc123"}
{namespace="prod",service="api",request_id="def456"}
{namespace="prod",service="api",request_id="ghi789"}
...
```

**Diagnosis**: request_id label creating 40K+ streams for single service.

---

### Method 3: Prometheus Metrics

```promql
# Total streams per namespace
loki_ingester_streams{namespace="prod"}

# Label cardinality (requires label_values scraping)
count(count by (user_id) (loki_ingester_streams{namespace="prod"}))

# Index size growth rate (indicates cardinality issues)
rate(loki_index_entry_bytes_total{namespace="prod"}[1h]) > 1000000
```

**Interpretation**:
- `loki_ingester_streams` >10,000: High cardinality likely
- `rate(loki_index_entry_bytes_total)` >1MB/hour: Index bloat from cardinality

---

### Method 4: Query Error Detection

**Symptom**: Queries fail with "max series limit exceeded" error

```bash
# Check query logs for series limit errors
logcli query '{job="loki/query"} | json | error =~ ".*max series.*"' --since=1h

# Example error message:
# "max entries limit exceeded, 1000 > 1000 for {namespace=\"prod\"}"
```

**Root Cause**: Grouping by high-cardinality label or broad stream selector matching too many streams.

---

## Thresholds & Alerts

### Cardinality Thresholds

| Threshold | Label Cardinality | Recommendation | Action |
|-----------|-------------------|----------------|--------|
| **Safe** | <20 unique values | Use as label | No action needed |
| **Caution** | 20-50 unique values | Monitor growth | Set alert, review quarterly |
| **Warning** | 50-100 unique values | Consider alternatives | Plan migration to structured_metadata |
| **Critical** | >100 unique values | Immediate remediation | Migrate to structured_metadata or log message |

### Stream Count Thresholds

| Threshold | Total Streams | Impact | Recommendation |
|-----------|---------------|--------|----------------|
| **Healthy** | <1,000 streams | Optimal performance | Continue monitoring |
| **Warning** | 1,000-10,000 streams | Query slowdown begins | Review label usage |
| **Critical** | >10,000 streams | Severe performance impact | Immediate remediation required |

**Formula**:
```
Expected Stream Count = Product of all label cardinalities

Example:
- service_name: 10 values
- namespace: 5 values
- deployment_environment: 3 values
Expected streams = 10 × 5 × 3 = 150 streams (healthy)
```

---

### Prometheus Alert Rules

```yaml
groups:
  - name: loki_cardinality_alerts
    interval: 5m
    rules:
      # High-cardinality label detected
      - alert: HighCardinalityLabel
        expr: |
          count(count by (user_id) (loki_ingester_streams{namespace="prod"})) > 100
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "High cardinality label detected: user_id"
          description: "Label user_id has {{$value}} unique values (threshold: 100)"

      # Excessive stream count
      - alert: ExcessiveStreamCount
        expr: |
          loki_ingester_streams{namespace="prod"} > 10000
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Excessive stream count in namespace prod"
          description: "{{$value}} streams detected (threshold: 10,000)"

      # Index size growth rate alert
      - alert: IndexBloat
        expr: |
          rate(loki_index_entry_bytes_total[1h]) > 1000000
        for: 30m
        labels:
          severity: warning
        annotations:
          summary: "Index bloat detected"
          description: "Index growing at {{$value}} bytes/hour (threshold: 1MB/hour)"

      # Query series limit exceeded
      - alert: QuerySeriesLimitExceeded
        expr: |
          rate(loki_query_error_total{error="max series limit exceeded"}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Queries hitting series limit"
          description: "{{$value}} queries/sec failing due to series limit"
```

---

## Migration to structured_metadata

### What is structured_metadata?

**structured_metadata** (Loki 2.9+): Metadata attached to logs WITHOUT creating new streams.

**Key Differences**:

| Feature | Labels | structured_metadata |
|---------|--------|---------------------|
| Stream creation | YES (each unique value = new stream) | NO (no streams) |
| Indexed | YES (fast filtering) | NO (requires scanning) |
| Cardinality limit | <100 recommended | Unlimited |
| Query performance | Fast (indexed) | Slower (full scan) |
| Use case | Low-cardinality dimensions | High-cardinality dimensions |

**When to Use**:
- Labels: Low-cardinality dimensions used for stream filtering (service, namespace, environment)
- structured_metadata: High-cardinality dimensions used for filtering AFTER stream selection (request_id, user_id, trace_id)

---

### Migration Strategy

#### Step 1: Identify High-Cardinality Labels

```bash
# Check all labels
logcli labels --since=24h

# Check cardinality for each
for label in $(logcli labels --since=24h); do
  echo "$label: $(logcli label-values $label --since=24h | wc -l)"
done
```

**Example Output**:
```
service_name: 12 (LOW - keep as label)
namespace: 5 (LOW - keep as label)
request_id: 8,452 (HIGH - migrate to structured_metadata)
user_id: 3,219 (HIGH - migrate to structured_metadata)
```

---

#### Step 2: Update Promtail Configuration

**Before** (high-cardinality labels):
```yaml
scrape_configs:
  - job_name: api_logs
    static_configs:
      - labels:
          service_name: api
          namespace: prod
          request_id: __value__  # HIGH CARDINALITY - WRONG
          user_id: __value__     # HIGH CARDINALITY - WRONG
    pipeline_stages:
      - json:
          expressions:
            request_id: request_id
            user_id: user_id
```

**After** (structured_metadata migration):
```yaml
scrape_configs:
  - job_name: api_logs
    static_configs:
      - labels:
          service_name: api
          namespace: prod
          # request_id and user_id removed from labels
    pipeline_stages:
      - json:
          expressions:
            request_id: request_id
            user_id: user_id
      - structured_metadata:
          request_id: ""
          user_id: ""
```

**Result**:
- Stream count: 50,000 → 60 streams (99.9% reduction)
- Query time: 120s → 8s (93% improvement)
- Index size: 25MB → 1MB (96% reduction)

---

#### Step 3: Update Queries

**Before** (label filtering):
```logql
{service="api", request_id="abc123"}  # Won't work after migration
```

**After** (structured_metadata filtering):
```logql
{service="api"} | request_id="abc123"  # Filter on structured_metadata
```

**Key Difference**: structured_metadata filtering happens AFTER stream selection (requires scanning all streams for service="api", then filtering).

---

#### Step 4: Validate Migration

```bash
# 1. Check stream count reduced
logcli series '{service="api"}' --since=1h | wc -l
# Expected: <100 streams (down from thousands)

# 2. Verify structured_metadata extraction works
logcli query '{service="api"} | request_id="abc123"' --since=1h --limit=10
# Should return logs with request_id=abc123

# 3. Check query performance
time logcli query '{service="api"} | request_id="abc123"' --since=1h
# Expected: <10s (down from 60s+)

# 4. Monitor index size
# Prometheus query
loki_index_entry_bytes_total{namespace="prod"}
# Expected: Significant reduction after migration
```

---

### Alternative: Move to Log Message Fields

**When to Use**: Loki version <2.9 (no structured_metadata support)

**Strategy**: Remove high-cardinality labels, keep as JSON fields in log message

**Before** (high-cardinality label):
```yaml
static_configs:
  - labels:
      service_name: api
      request_id: __value__  # HIGH CARDINALITY
```

**After** (log message field):
```yaml
static_configs:
  - labels:
      service_name: api
      # request_id removed from labels
pipeline_stages:
  - json:
      expressions:
        request_id: request_id
  # No label extraction, stays in message
```

**Query Change**:
```logql
# Before
{service="api", request_id="abc123"}

# After
{service="api"} | json | request_id="abc123"
```

**Performance**: Similar to structured_metadata (requires full stream scan + JSON parsing).

---

## Real-World Case Studies

### Case Study 1: ActiveCampaign

**Problem**: High-cardinality labels causing cost explosion

**Detection**:
```bash
logcli series '{namespace="activecampaign"}' --since=1h | wc -l
# Result: 127,452 streams (critical)

# Identified high-cardinality labels:
# - customer_id: 50,000+ unique values
# - request_id: 75,000+ unique values
```

**Fix**:
1. Migrated customer_id and request_id to structured_metadata (Loki 2.9)
2. Reduced label set to: service_name, namespace, deployment_environment only

**Results**:
- **Cost**: $10,000/month → $2,700/month (73% reduction)
- **Stream count**: 127,452 → 45 streams (99.96% reduction)
- **Query time**: 90s → 9s (90% improvement)
- **Index size**: 120MB → 3MB (97.5% reduction)

**Timeline**: 2-week migration (1 week planning + 1 week rollout)

**Source**: [ActiveCampaign Blog](https://activecampaign.engineering/how-we-improved-our-loki-performance-after-discovering-a-critical-anti-pattern/)

---

### Case Study 2: Gauntlet Agents (Hypothetical Scenario)

**Problem**: Pod name label creating excessive streams

**Detection**:
```bash
logcli labels pod_name --since=24h | wc -l
# Result: 237 unique pod names (medium cardinality, but growing)

logcli series '{namespace="gauntlet-agents"}' --since=1h | wc -l
# Result: 1,421 streams (warning threshold)
```

**Analysis**:
- service_name: 12 values (low)
- deployment_environment: 3 values (low)
- pod_name: 237 values (medium, but high churn)
- Stream count: 12 × 3 × 237 = 8,532 potential streams (critical)

**Fix Options**:

**Option 1**: Remove pod_name label (recommended)
```yaml
# Before
static_configs:
  - labels:
      service_name: __value__
      deployment_environment: __value__
      pod_name: __value__  # REMOVE

# After
static_configs:
  - labels:
      service_name: __value__
      deployment_environment: __value__
```

**Option 2**: Migrate pod_name to structured_metadata
```yaml
pipeline_stages:
  - json:
      expressions:
        pod_name: pod_name
  - structured_metadata:
      pod_name: ""
```

**Expected Results**:
- Stream count: 1,421 → 36 streams (97% reduction)
- Query time: 25s → 5s (80% improvement)
- Index size: 5MB → 200KB (96% reduction)

---

## Migration Checklist

- [ ] **Pre-Migration**
  - [ ] Identify high-cardinality labels (cardinality >100)
  - [ ] Estimate current stream count
  - [ ] Check Loki version (structured_metadata requires 2.9+)
  - [ ] Document current query patterns
  - [ ] Calculate expected stream reduction

- [ ] **Configuration Changes**
  - [ ] Update Promtail configuration (remove high-cardinality labels)
  - [ ] Add structured_metadata or log message extraction
  - [ ] Test configuration in staging environment
  - [ ] Validate log ingestion still works

- [ ] **Query Migration**
  - [ ] Update dashboard queries (label filters → structured_metadata filters)
  - [ ] Update alerting rules
  - [ ] Update ad-hoc query templates
  - [ ] Document query pattern changes

- [ ] **Rollout**
  - [ ] Deploy Promtail configuration to production
  - [ ] Monitor stream count reduction
  - [ ] Monitor query performance improvement
  - [ ] Watch for errors in application logs

- [ ] **Validation**
  - [ ] Verify stream count <1000
  - [ ] Verify queries return correct results
  - [ ] Measure query performance improvement
  - [ ] Check index size reduction
  - [ ] Update documentation

- [ ] **Monitoring**
  - [ ] Set up cardinality alerts
  - [ ] Monitor stream count trend
  - [ ] Track index size growth
  - [ ] Review quarterly for new high-cardinality labels

---

## Sources

1. **Grafana Label Best Practices**: https://grafana.com/docs/loki/latest/get-started/labels/bp-labels/
   - Quality: 0.95
   - Contribution: Cardinality thresholds, label selection criteria

2. **Grafana Structured Metadata Docs**: https://grafana.com/docs/loki/latest/configure/#structured-metadata
   - Quality: 0.92
   - Contribution: structured_metadata configuration and migration

3. **ActiveCampaign Case Study**: https://activecampaign.engineering/how-we-improved-our-loki-performance-after-discovering-a-critical-anti-pattern/
   - Quality: 0.92
   - Contribution: Real-world 73% cost reduction results

4. **Query Optimization Patterns** (Internal): `.claude/docs/guides/loki-query-specialist/query-optimization-patterns.md`
   - Quality: 0.95
   - Contribution: Cardinality control framework

---

## Related Documentation

- `anti-pattern-detection-guide.md`: Anti-pattern #2 (High-cardinality labels)
- `query-optimization-patterns.md`: Framework 3 (Cardinality control for grouping)
- `format-improvement-strategies.md`: Log format migration patterns

---

## Changelog

- **2025-11-10**: Initial creation from researcher-external findings (confidence: 0.93)
