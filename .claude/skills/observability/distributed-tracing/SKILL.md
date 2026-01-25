---
name: distributed-tracing
description: >
  Use this skill when instrumenting applications with OpenTelemetry, correlating
  traces with logs/metrics, configuring sampling strategies, or querying Tempo/Jaeger.
  Covers trace context propagation, exemplars, and root cause analysis workflows.
  Keywords: tracing, opentelemetry, otel, tempo, jaeger, span, trace_id, exemplar.
---

# Distributed Tracing

Implement distributed tracing with OpenTelemetry instrumentation, cross-signal correlation, and optimized sampling strategies.

## Reference Documentation

**Detailed Guides** (read when relevant):
- **OpenTelemetry Instrumentation** → [reference/otel-instrumentation.md](reference/otel-instrumentation.md)
- **Trace Correlation Patterns** → [reference/trace-correlation.md](reference/trace-correlation.md)

---

## Trace Structure Fundamentals

### Core Concepts

| Concept | Definition | Example |
|---------|------------|---------|
| **Trace** | End-to-end request journey | Single API call through all services |
| **Span** | Unit of work within a trace | Database query, HTTP request |
| **Trace Context** | Propagated identifiers | `trace_id`, `span_id`, `trace_flags` |

### W3C Trace Context (Standard)

```
traceparent: 00-{trace_id}-{parent_span_id}-{trace_flags}
tracestate: vendor=value,vendor2=value2
```

**Example Header**:
```
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
```

- `00`: Version
- `4bf92f3577b34da6a3ce929d0e0e4736`: 32-char trace_id
- `00f067aa0ba902b7`: 16-char parent_span_id
- `01`: Sampled flag

### Span Hierarchy

```
[Root Span: HTTP GET /api/orders]
  └─ [Child: Database Query]
  └─ [Child: External API Call]
       └─ [Grandchild: Serialization]
```

### Span Attributes vs Events

| Feature | Span Attributes | Span Events |
|---------|----------------|-------------|
| Purpose | Describe the span | Record point-in-time occurrences |
| Cardinality | Should be bounded | Can be high (within limits) |
| Example | `http.method=GET` | `exception` event with stack trace |
| Query Use | Filter/group spans | Debug specific issues |

---

## OpenTelemetry Instrumentation

### Python Auto-Instrumentation Setup

```bash
# Install core packages
pip install opentelemetry-distro opentelemetry-exporter-otlp

# Auto-install instrumentation for detected libraries
opentelemetry-bootstrap -a install
```

**Runtime Command**:
```bash
opentelemetry-instrument \
  --service_name my-service \
  --exporter_otlp_endpoint http://tempo:4317 \
  python app.py
```

### Manual Span Creation

```python
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer(__name__)

def process_order(order_id: str) -> dict:
    with tracer.start_as_current_span("process_order") as span:
        # Set attributes (low-cardinality only)
        span.set_attribute("order.id", order_id)
        span.set_attribute("order.type", "standard")
        
        try:
            result = do_processing(order_id)
            span.set_status(Status(StatusCode.OK))
            return result
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.record_exception(e)
            raise
```

### Resource Attributes (Required)

```python
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

resource = Resource.create({
    SERVICE_NAME: "order-service",
    "service.namespace": "gauntlet-agents",
    "deployment.environment": "production",
    "service.version": "1.2.3",
})
```

---

## Trace-Log Correlation

### Injecting trace_id into Logs

```python
import logging
from opentelemetry import trace

class TraceIdFilter(logging.Filter):
    def filter(self, record):
        span = trace.get_current_span()
        ctx = span.get_span_context()
        record.trace_id = format(ctx.trace_id, '032x') if ctx.is_valid else "0" * 32
        record.span_id = format(ctx.span_id, '016x') if ctx.is_valid else "0" * 16
        return True

# Configure logging
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '{"timestamp":"%(asctime)s","level":"%(levelname)s",'
    '"trace_id":"%(trace_id)s","span_id":"%(span_id)s",'
    '"message":"%(message)s"}'
))
handler.addFilter(TraceIdFilter())
logging.getLogger().addHandler(handler)
```

### Querying Loki with trace_id

```logql
# Find logs for specific trace
{service_name="order-service"} | json | trace_id="4bf92f3577b34da6a3ce929d0e0e4736"

# Find error logs with trace context
{service_name="order-service"} | json | level="error" | trace_id != ""
```

---

## Trace-Metric Correlation (Exemplars)

### What Are Exemplars?

Exemplars link metric data points to specific traces, enabling drill-down from aggregated metrics to individual requests.

**Use Case**: "The p99 latency spiked. Show me an example slow request."

### Adding Exemplars to Histograms

```python
from opentelemetry import trace
from prometheus_client import Histogram

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'Request latency',
    ['method', 'endpoint']
)

def handle_request(method: str, endpoint: str, duration: float):
    span = trace.get_current_span()
    ctx = span.get_span_context()
    
    # Record with exemplar containing trace_id
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(
        duration,
        exemplar={'trace_id': format(ctx.trace_id, '032x')}
    )
```

### Grafana Exemplar Visualization

1. Enable exemplars in Prometheus data source
2. In panel options, toggle "Exemplars" on
3. Click exemplar dots to jump to trace view

---

## Sampling Strategies

### Head-Based Sampling

Decision made at trace start. Simple but may miss interesting traces.

| Ratio | Environment | Rationale |
|-------|-------------|-----------|
| 100% | Development | Full visibility |
| 10-50% | Staging | Balance cost/visibility |
| 1-10% | Production | Cost control |
| 100% (errors) | All | Always capture failures |

```python
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

sampler = TraceIdRatioBased(0.1)  # 10% sampling
```

### Tail-Based Sampling (Tempo/Collector)

Decision after trace complete. Keeps interesting traces, drops boring ones.

```yaml
# OpenTelemetry Collector config
processors:
  tail_sampling:
    decision_wait: 10s
    policies:
      - name: errors-policy
        type: status_code
        status_code: {status_codes: [ERROR]}

      - name: slow-traces
        type: latency
        latency: {threshold_ms: 1000}
      - name: probabilistic
        type: probabilistic
        probabilistic: {sampling_percentage: 10}
```

### Sampling Decision Matrix

| Signal | Head-Based | Tail-Based |
|--------|------------|------------|
| All traces | Low cost, gaps | Higher cost, complete |
| Errors | May miss | Always captured |
| Slow requests | May miss | Always captured |
| Implementation | Simple | Requires collector |

---

## Tempo/Jaeger Query Patterns

### Search by trace_id

```bash
# Tempo API
curl "http://tempo:3200/api/traces/4bf92f3577b34da6a3ce929d0e0e4736"

# Jaeger API  
curl "http://jaeger:16686/api/traces/4bf92f3577b34da6a3ce929d0e0e4736"
```

### Search by Service + Operation

```bash
# Tempo TraceQL
curl -G "http://tempo:3200/api/search" \
  --data-urlencode 'q={resource.service.name="order-service" && name="process_order"}'

# Jaeger
curl "http://jaeger:16686/api/traces?service=order-service&operation=process_order"
```

### Duration-Based Queries (TraceQL)

```traceql
# Spans longer than 1 second
{duration > 1s}

# Slow database queries
{span.db.system="postgresql" && duration > 500ms}

# Error spans in specific service
{resource.service.name="api" && status=error}
```

### Tag Filtering

```traceql
# By HTTP status
{span.http.status_code >= 500}

# By custom attribute
{span.order.type="premium" && duration > 2s}
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Not propagating context | Broken traces | Use W3C traceparent header |
| 100% sampling in prod | Excessive cost/storage | Use 1-10% + tail sampling |
| High-cardinality attributes | Query performance | Bound attribute values |
| Missing service.name | Unidentifiable spans | Always set resource attributes |
| No error status on exceptions | Silent failures | Call `span.set_status(ERROR)` |
| Spans without parent | Orphaned spans | Ensure context propagation |

### Common Mistakes

```python
# WRONG: High-cardinality attribute
span.set_attribute("user.email", user.email)  # Millions of values

# CORRECT: Use ID reference
span.set_attribute("user.id", user.id)

# WRONG: No context propagation in async
async def process():
    span = tracer.start_span("process")  # Detached!
    
# CORRECT: Propagate context
async def process():
    with tracer.start_as_current_span("process"):
        await do_work()
```

---

## Validation Checklist

Before deploying tracing configuration:

- [ ] `service.name` resource attribute set
- [ ] `deployment.environment` resource attribute set
- [ ] W3C Trace Context propagation enabled
- [ ] Sampling strategy appropriate for environment
- [ ] trace_id injected into logs (for correlation)
- [ ] Exemplars configured for key histograms
- [ ] Error spans have ERROR status set
- [ ] Span attributes bounded (no user emails, raw IDs)
- [ ] Exporter configured (OTLP to Tempo/Jaeger)

---

## Quick Reference

### Environment Variables

```bash
# Service identification
OTEL_SERVICE_NAME=order-service
OTEL_RESOURCE_ATTRIBUTES=deployment.environment=production

# Exporter configuration
OTEL_EXPORTER_OTLP_ENDPOINT=http://tempo:4317
OTEL_EXPORTER_OTLP_PROTOCOL=grpc

# Sampling
OTEL_TRACES_SAMPLER=parentbased_traceidratio
OTEL_TRACES_SAMPLER_ARG=0.1
```

### Trace Health Thresholds

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Trace completeness | >95% | 80-95% | <80% |
| Avg span count/trace | 5-50 | 50-200 | >200 |
| Error trace rate | <5% | 5-15% | >15% |
| Sampling rate (prod) | 1-10% | 10-50% | >50% |
