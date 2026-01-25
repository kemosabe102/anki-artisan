# Trace Correlation Patterns

> Connecting traces with logs and metrics for unified observability.

---

## Table of Contents

1. [Trace-Log Correlation](#trace-log-correlation)
2. [Trace-Metric Correlation (Exemplars)](#trace-metric-correlation-exemplars)
3. [Grafana Configuration](#grafana-configuration)
4. [Cross-Signal Debugging Workflow](#cross-signal-debugging-workflow)

---

## Trace-Log Correlation

### Why Correlate?

- **Context**: See logs for a specific request without searching
- **Debugging**: Jump from error log to full trace
- **Root Cause**: Understand what happened before/after an event

### Log Format with trace_id

Structure logs to include trace context:

```json
{
  "timestamp": "2025-01-15T14:23:45.123Z",
  "level": "error",
  "message": "Database timeout",
  "service": "order-service",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7"
}
```

### Python Implementation

```python
import logging
import json
from datetime import datetime
from opentelemetry import trace

class TraceContextFilter(logging.Filter):
    """Inject trace context into log records."""
    
    def filter(self, record):
        span = trace.get_current_span()
        ctx = span.get_span_context()
        
        if ctx.is_valid:
            record.trace_id = format(ctx.trace_id, '032x')
            record.span_id = format(ctx.span_id, '016x')
        else:
            record.trace_id = "0" * 32
            record.span_id = "0" * 16
        
        return True


class JSONFormatter(logging.Formatter):
    """Format logs as JSON with trace context."""
    
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname.lower(),
            "message": record.getMessage(),
            "logger": record.name,
            "trace_id": getattr(record, 'trace_id', '0' * 32),
            "span_id": getattr(record, 'span_id', '0' * 16),
        }
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


# Setup
def configure_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    handler.addFilter(TraceContextFilter())
    
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
```

### Querying Logs by trace_id

#### Loki (LogQL)

```logql
# Find all logs for a trace
{service_name="order-service"} | json | trace_id="4bf92f3577b34da6a3ce929d0e0e4736"

# Find error logs with trace context
{service_name="order-service"} | json | level="error" | trace_id!=""

# Aggregate log counts by trace
{service_name="order-service"} | json | count_over_time([5m]) by (trace_id)
```

#### Using structured_metadata (Loki 3.0+)

Configure Promtail to extract trace_id as structured metadata:

```yaml
pipeline_stages:
  - json:
      expressions:
        trace_id: trace_id
        span_id: span_id
  - structured_metadata:
      trace_id:
      span_id:
```

Query with metadata filter:

```logql
{service_name="order-service"} | trace_id="4bf92f3577b34da6a3ce929d0e0e4736"
```

---

## Trace-Metric Correlation (Exemplars)

### What Are Exemplars?

Exemplars are sample trace references attached to metric data points. They answer: "Show me an example request that contributed to this metric."

**Use Cases**:
- P99 latency spike → Show a slow request trace
- Error rate increase → Show an error trace
- Traffic pattern anomaly → Show representative request

### Prometheus Exemplar Format

```
http_request_duration_seconds_bucket{le="0.5"} 1000 # {trace_id="abc123"} 0.48 1609459200.000
```

Components:
- Metric value: `1000`
- Exemplar label: `trace_id="abc123"`
- Exemplar value: `0.48` (observed value)
- Timestamp: `1609459200.000`

### Python Implementation

```python
from prometheus_client import Histogram, REGISTRY
from opentelemetry import trace

# Enable exemplar support
REGISTRY.set_default_labels({})

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'Request latency in seconds',
    ['method', 'endpoint', 'status'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)


def record_request_latency(method: str, endpoint: str, status: int, duration: float):
    """Record request latency with exemplar linking to current trace."""
    span = trace.get_current_span()
    ctx = span.get_span_context()
    
    exemplar = None
    if ctx.is_valid:
        exemplar = {'trace_id': format(ctx.trace_id, '032x')}
    
    REQUEST_LATENCY.labels(
        method=method,
        endpoint=endpoint,
        status=str(status)
    ).observe(duration, exemplar=exemplar)
```

### Exposing Exemplars (Prometheus)

Prometheus must scrape with OpenMetrics format:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'app'
    scrape_interval: 15s
    honor_labels: true
    metrics_path: /metrics
    params:
      # Request OpenMetrics format for exemplar support
      format: ['prometheus']
    static_configs:
      - targets: ['app:8000']
```

---

## Grafana Configuration

### Data Source Links

Configure data sources to link between signals:

#### Prometheus → Tempo Link

```yaml
# Grafana provisioning: datasources/prometheus.yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090
    jsonData:
      exemplarTraceIdDestinations:
        - name: trace_id
          datasourceUid: tempo
          urlDisplayLabel: View Trace
```

#### Loki → Tempo Link

```yaml
# Grafana provisioning: datasources/loki.yaml
apiVersion: 1
datasources:
  - name: Loki
    type: loki
    url: http://loki:3100
    jsonData:
      derivedFields:
        - name: trace_id
          matcherRegex: '"trace_id":"([a-f0-9]+)"'
          url: '${__value.raw}'
          datasourceUid: tempo
          urlDisplayLabel: View Trace
```

#### Tempo → Loki Link

```yaml
# Grafana provisioning: datasources/tempo.yaml
apiVersion: 1
datasources:
  - name: Tempo
    type: tempo
    url: http://tempo:3200
    jsonData:
      tracesToLogs:
        datasourceUid: loki
        tags: ['service.name']
        mappedTags: [{ key: 'service.name', value: 'service_name' }]
        filterByTraceID: true
        filterBySpanID: false
      tracesToMetrics:
        datasourceUid: prometheus
        tags: [{ key: 'service.name', value: 'service' }]
```

### Enabling Exemplars in Panels

1. **Edit panel** → Query options
2. **Enable "Exemplars"** toggle
3. **Configure**: Exemplar color, visibility threshold

### "Logs for this span" Button

With proper Tempo→Loki configuration, clicking a span shows "Logs" button that queries:

```logql
{service_name="<service>"} | trace_id="<trace_id>"
```

---

## Cross-Signal Debugging Workflow

### Scenario: High Latency Alert

**Step 1: Start with Metric**

Grafana panel shows p99 latency spike at 14:23.

**Step 2: Click Exemplar**

Exemplar dot on the spike shows `trace_id=abc123`. Click to open Tempo.

**Step 3: Analyze Trace**

Trace view shows:
- Total duration: 5.2s
- Slow span: `db.query` took 4.8s
- Span attributes: `db.statement="SELECT * FROM orders WHERE..."`

**Step 4: View Logs**

Click "Logs for this span" to see:
```
14:23:45.123 WARN  Query exceeded 1s threshold
14:23:49.987 ERROR Connection pool exhausted, retrying...
```

**Step 5: Root Cause**

Logs reveal connection pool exhaustion caused the slow query.

### Scenario: Error Rate Spike

**Step 1: Alert Fires**

`ErrorRate > 5%` for `order-service`.

**Step 2: Query Error Traces**

```traceql
{resource.service.name="order-service" && status=error}
```

**Step 3: Examine Error Span**

Span shows:
- `exception.type`: `TimeoutError`
- `exception.message`: `Connection to payment-service timed out`

**Step 4: Correlate with Logs**

```logql
{service_name="order-service"} | json | level="error" | line_format "{{.message}}"
```

**Step 5: Check Upstream**

Payment service traces show it was also experiencing errors due to database issues.

---

## Correlation Checklist

### Prerequisites

- [ ] Trace exporter configured (OTLP to Tempo/Jaeger)
- [ ] Log format includes `trace_id` and `span_id`
- [ ] Prometheus scraping with exemplar support
- [ ] Grafana data sources linked

### Verification Steps

1. **Trace → Logs**
   ```bash
   # Get a trace_id from Tempo
   curl "http://tempo:3200/api/search?limit=1" | jq '.traces[0].traceID'
   
   # Query Loki for that trace
   curl -G "http://loki:3100/loki/api/v1/query" \
     --data-urlencode 'query={service_name="order-service"} | json | trace_id="<trace_id>"'
   ```

2. **Metrics → Traces (Exemplars)**
   ```bash
   # Check exemplars in Prometheus
   curl "http://prometheus:9090/api/v1/query_exemplars?query=http_request_duration_seconds_bucket"
   ```

3. **Logs → Traces**
   - Search logs in Grafana
   - Click trace_id link
   - Verify trace opens in Tempo

### Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| No trace link in logs | Missing derived field config | Configure Loki data source |
| Empty exemplars | Wrong scrape format | Add OpenMetrics format param |
| "Logs" button missing | Tempo→Loki not linked | Configure tracesToLogs |
| trace_id = 0000... | No active span | Check instrumentation order |

---

## Best Practices

### trace_id Formatting

Always use lowercase hex, 32 characters:

```python
# Correct
trace_id = format(ctx.trace_id, '032x')  # "4bf92f3577b34da6a3ce929d0e0e4736"

# Wrong
trace_id = str(ctx.trace_id)  # "123456789012345678901234567890"
trace_id = hex(ctx.trace_id)  # "0x4bf92f..."
```

### Exemplar Sampling

Don't attach exemplars to every observation (memory overhead):

```python
import random

def record_with_sampled_exemplar(value: float, labels: dict):
    exemplar = None
    # Only attach exemplar 10% of the time
    if random.random() < 0.1:
        span = trace.get_current_span()
        ctx = span.get_span_context()
        if ctx.is_valid:
            exemplar = {'trace_id': format(ctx.trace_id, '032x')}
    
    histogram.labels(**labels).observe(value, exemplar=exemplar)
```

### Log Volume Management

High-traffic services generate many logs. Filter strategically:

```logql
# Don't: Query all logs then filter
{service_name="api"} | json | trace_id="abc123"

# Do: Use structured_metadata if available
{service_name="api"} | trace_id="abc123"

# Do: Pre-filter by time if you know when the trace occurred
{service_name="api"} | json | trace_id="abc123" [2025-01-15T14:20:00Z to 2025-01-15T14:25:00Z]
```
