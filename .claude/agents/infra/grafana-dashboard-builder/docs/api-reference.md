# Prometheus API Reference

**Purpose**: Quick reference for Prometheus API endpoints used in dashboard creation

## Primary Endpoints

### 1. Metric Discovery
**Endpoint**: `GET /api/v1/label/__name__/values`

**Returns**: List of all metric names

**Usage**: Filter by intent keywords, validate metric existence

**Example**:
```bash
curl http://prometheus-server:9090/api/v1/label/__name__/values
```

### 2. Label Discovery
**Endpoint**: `GET /api/v1/series?match[]=<metric>`

**Returns**: All label dimensions for metric

**Usage**: Identify grouping labels, cardinality assessment

**Example**:
```bash
curl 'http://prometheus-server:9090/api/v1/series?match[]=http_requests_total'
```

### 3. Query Validation
**Endpoint**: `GET /api/v1/query?query=<promql>`

**Returns**: Instant query result or error

**Usage**: Syntax validation, metric existence check, result preview

**Example**:
```bash
curl 'http://prometheus-server:9090/api/v1/query?query=rate(http_requests_total[5m])'
```

### 4. Query Range Testing
**Endpoint**: `GET /api/v1/query_range?query=<promql>&start=<>&end=<>`

**Returns**: Time series data over range

**Usage**: Verify query returns expected data shape

**Example**:
```bash
curl 'http://prometheus-server:9090/api/v1/query_range?query=rate(http_requests_total[5m])&start=2025-01-01T00:00:00Z&end=2025-01-01T01:00:00Z&step=15s'
```

## Error Handling

- **Connection refused** → Prometheus not accessible, escalate to user
- **400 Bad Request** → PromQL syntax error, fix query and retry
- **Empty result set** → Metric doesn't exist or no data, suggest alternatives
- **503 Service Unavailable** → Prometheus overloaded, reduce query complexity

## PromQL Query Patterns

### Rate Intervals
```promql
# Scrape interval: 15s
# Minimum rate interval: 60s (4x scrape)

rate(metric[1m])   # Tactical, high sensitivity, noisy
rate(metric[5m])   # Balanced, default for most dashboards
rate(metric[1h])   # Strategic, smooth trends
```

### High-Cardinality Reduction
```promql
# Before (high cardinality - 1000s of series)
rate(http_requests_total[5m])

# After (reduced cardinality - 10s of series)
sum(rate(http_requests_total[5m])) by (service, status)

# Or: Top 10 only
topk(10, sum(rate(http_requests_total[5m])) by (service))
```

### Histogram Percentiles
```promql
# Histogram percentiles (correct aggregation)
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
)

# Multiple percentiles (separate queries)
histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```

### Example Query Construction
```promql
# Latency (95th percentile, 5m rate interval)
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))

# Error rate (5m rate, percentage)
sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
/
sum(rate(http_requests_total[5m])) by (service) * 100

# Saturation (current utilization with max capacity)
(redis_memory_used_bytes / redis_memory_max_bytes) * 100
```

## Grafana 12.x Schema Reference

### Required Dashboard Fields
```json
{
  "dashboard": {
    "title": "Dashboard Title",
    "uid": "unique-id",
    "panels": [],
    "schemaVersion": 39,
    "version": 1,
    "timezone": "browser",
    "time": {
      "from": "now-1h",
      "to": "now"
    }
  }
}
```

### Panel Structure
```json
{
  "id": 1,
  "title": "Panel Title",
  "type": "timeseries",
  "targets": [
    {
      "expr": "promql_query",
      "legendFormat": "{{label}}",
      "refId": "A"
    }
  ],
  "gridPos": { "h": 8, "w": 12, "x": 0, "y": 0 },
  "fieldConfig": {
    "defaults": {
      "unit": "short",
      "thresholds": {
        "mode": "absolute",
        "steps": [
          { "value": null, "color": "green" },
          { "value": 80, "color": "red" }
        ]
      }
    }
  }
}
```
