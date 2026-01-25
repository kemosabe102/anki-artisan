# OpenTelemetry Python SDK Instrumentation Guide

**Purpose**: Add observability (traces, metrics) to Python application code

**Target Agents**: development, debugger

**Critical Distinction**: OpenTelemetry SDK is for instrumenting APPLICATION CODE. For testing infrastructure, see `telemetrygen-usage.md`.

---

## Overview

OpenTelemetry Python SDK enables applications to emit:

- **Traces**: Request flows across services (spans, parent-child relationships)
- **Metrics**: Business and system metrics (counters, histograms, gauges)
- **Logs**: Structured logging (with trace correlation)

**Use Cases**:

- Track request latency and error rates
- Monitor business KPIs (orders processed, revenue)
- Debug production issues with distributed tracing
- Capacity planning and performance optimization

---

## Installation & Setup

### Required Packages

```bash
# Core packages
uv add opentelemetry-api
uv add opentelemetry-sdk
uv add opentelemetry-semantic-conventions

# Exporters (OTLP for gauntlet-agents)
uv add opentelemetry-exporter-otlp

# Auto-instrumentation (optional)
uv add opentelemetry-distro
opentelemetry-bootstrap -a install
```

### Basic Initialization

```python
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource

# Configure resource (service identification)
resource = Resource.create({
    "service.name": "gauntlet-agents",
    "service.version": "1.0.0",
    "deployment.environment": "development"
})

# Initialize tracer provider
trace_provider = TracerProvider(resource=resource)
otlp_endpoint = "http://localhost:4317"  # OTEL Collector
span_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
processor = BatchSpanProcessor(span_exporter)
trace_provider.add_span_processor(processor)
trace.set_tracer_provider(trace_provider)

# Initialize meter provider
metric_exporter = OTLPMetricExporter(endpoint=otlp_endpoint, insecure=True)
metric_reader = PeriodicExportingMetricReader(metric_exporter)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)
```

---

## Basic Tracing Patterns

### Creating Spans

**Context Manager** (recommended):

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def process_request(user_id: str):
    with tracer.start_as_current_span("process_request") as span:
        # Span automatically active in this context
        span.set_attribute("user.id", user_id)
        result = do_work()
        span.set_attribute("result.count", len(result))
        return result
```

**Decorator Pattern**:

```python
@tracer.start_as_current_span("calculate")
def calculate(x: int, y: int) -> int:
    return x + y
```

**Nested Spans** (automatic parent-child):

```python
def handle_order(order_id: str):
    with tracer.start_as_current_span("handle_order") as parent:
        parent.set_attribute("order.id", order_id)

        # Child span 1
        with tracer.start_as_current_span("validate_order"):
            validate_inventory()

        # Child span 2
        with tracer.start_as_current_span("process_payment"):
            charge_card()
```

### Span Attributes & Events

**Standard Semantic Attributes**:

```python
from opentelemetry.semconv.trace import SpanAttributes

def api_handler(request):
    with tracer.start_as_current_span("api_handler") as span:
        # HTTP semantic conventions
        span.set_attribute(SpanAttributes.HTTP_METHOD, "POST")
        span.set_attribute(SpanAttributes.HTTP_URL, request.url)
        span.set_attribute(SpanAttributes.HTTP_STATUS_CODE, 200)

        # Custom business attributes
        span.set_attribute("user.id", request.user_id)
        span.set_attribute("order.value", 150.00)
```

**Span Events** (structured logs):

```python
def process_transaction():
    with tracer.start_as_current_span("process_transaction") as span:
        span.add_event("validation_started")
        validate()

        span.add_event("payment_processed", {
            "amount": 150.00,
            "currency": "USD",
            "method": "credit_card"
        })
```

**Error Handling**:

```python
from opentelemetry.trace import Status, StatusCode

def risky_operation():
    with tracer.start_as_current_span("risky_operation") as span:
        try:
            result = might_fail()
            span.set_status(Status(StatusCode.OK))
            return result
        except Exception as ex:
            span.set_status(Status(StatusCode.ERROR))
            span.record_exception(ex)  # Captures full traceback
            raise
```

### Context Propagation

**Implicit (automatic)**:

```python
def parent_function():
    with tracer.start_as_current_span("parent"):
        # Current span is automatically propagated
        child_function()

def child_function():
    # Gets current span from context automatically
    current_span = trace.get_current_span()
    current_span.set_attribute("key", "value")
```

**Span Links** (for async/batch processing):

```python
def batch_processor():
    with tracer.start_as_current_span("batch") as batch_span:
        ctx = batch_span.get_span_context()
        link = trace.Link(ctx)

        # Link child operations back to batch
        for item in items:
            with tracer.start_as_current_span(f"item_{item.id}", links=[link]):
                process_item(item)
```

---

## Metric Emission Patterns

### Counters (monotonically increasing)

```python
from opentelemetry import metrics

meter = metrics.get_meter(__name__)

# Create counter at module level (once)
request_counter = meter.create_counter(
    "http.requests",
    unit="1",
    description="Total HTTP requests"
)

# Use in business logic (many times)
def handle_request(method: str, status_code: int):
    request_counter.add(1, {
        "http.method": method,
        "http.status_code": status_code
    })
```

### Histograms (value distributions)

```python
# Track latency distributions
latency_histogram = meter.create_histogram(
    "http.request.duration",
    unit="ms",
    description="HTTP request latency"
)

import time
def timed_operation():
    start = time.time()
    do_work()
    duration_ms = (time.time() - start) * 1000
    latency_histogram.record(duration_ms, {"operation": "do_work"})
```

### Observable Gauges (async polling)

```python
from typing import Iterable
from opentelemetry.metrics import CallbackOptions, Observation
import psutil

def get_memory_usage(options: CallbackOptions) -> Iterable[Observation]:
    """Poll memory usage at collection interval"""
    memory = psutil.virtual_memory()
    yield Observation(memory.percent, {"memory.type": "physical"})

# Registers callback, invoked automatically
meter.create_observable_gauge(
    "system.memory.usage",
    callbacks=[get_memory_usage],
    unit="%",
    description="System memory usage percentage"
)
```

### UpDownCounter (can increase/decrease)

```python
# Track active connections
active_connections = meter.create_up_down_counter(
    "http.active_connections",
    unit="1",
    description="Currently active HTTP connections"
)

def on_connection_open():
    active_connections.add(1)

def on_connection_close():
    active_connections.add(-1)
```

---

## Production Best Practices

### Sampling (reduce overhead)

```python
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased, ParentBased

# Sample 10% of traces
sampler = ParentBased(root=TraceIdRatioBased(0.1))
provider = TracerProvider(sampler=sampler, resource=resource)
```

### Batch Processing (performance)

```python
# BatchSpanProcessor for production (not SimpleSpanProcessor)
processor = BatchSpanProcessor(
    span_exporter,
    max_queue_size=2048,        # Buffer size
    max_export_batch_size=512,  # Batch size
    schedule_delay_millis=5000  # Export every 5s
)
provider.add_span_processor(processor)
```

### Async Code Patterns

```python
import asyncio

async def async_operation():
    # Context propagation works automatically with asyncio
    with tracer.start_as_current_span("async_op") as span:
        await asyncio.sleep(1)
        span.set_attribute("result", "success")

async def parallel_tasks():
    with tracer.start_as_current_span("parallel_parent"):
        # Each task gets parent context automatically
        await asyncio.gather(
            async_operation(),
            async_operation(),
            async_operation()
        )
```

### Environment-Based Configuration (12-factor)

```bash
# Exporter configuration
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer token"

# Context propagation (W3C TraceContext + Baggage by default)
export OTEL_PROPAGATORS="tracecontext,baggage"

# Sampling
export OTEL_TRACES_SAMPLER="traceidratio"
export OTEL_TRACES_SAMPLER_ARG="0.1"

# Service identification
export OTEL_SERVICE_NAME="gauntlet-agents"
export OTEL_RESOURCE_ATTRIBUTES="service.version=1.0.0,deployment.environment=prod"
```

### Graceful Shutdown

```python
import atexit
from opentelemetry.sdk.trace import TracerProvider

provider = TracerProvider()
# ... setup ...

def cleanup():
    """Flush remaining spans before shutdown"""
    provider.force_flush(timeout_millis=5000)
    provider.shutdown()

atexit.register(cleanup)
```

---

## Agent-Specific Guidance

### For development

**Use Case**: Add observability to new features in `packages/core/**`

**Recommended Approach**:

1. **Import at module level**:

   ```python
   from opentelemetry import trace
   tracer = trace.get_tracer(__name__)
   ```

2. **Instrument public functions**:

   ```python
   def public_api(param: str) -> Result:
       with tracer.start_as_current_span("public_api") as span:
           span.set_attribute("param", param)
           return internal_logic(param)
   ```

3. **Add business metrics**:

   ```python
   from opentelemetry import metrics
   meter = metrics.get_meter(__name__)

   operation_counter = meter.create_counter("operations.completed")

   def complete_operation():
       do_work()
       operation_counter.add(1, {"status": "success"})
   ```

4. **Error handling pattern**:
   ```python
   with tracer.start_as_current_span("operation") as span:
       try:
           result = risky_work()
           span.set_status(Status(StatusCode.OK))
           return result
       except SpecificError as ex:
           span.set_status(Status(StatusCode.ERROR))
           span.record_exception(ex)
           span.set_attribute("error.type", "SpecificError")
           raise
   ```

**What to Instrument**:

- ✅ Public API functions (entry points)
- ✅ External calls (HTTP, database, API)
- ✅ Business logic boundaries (orders, payments, analysis)
- ✅ Long-running operations (>100ms)
- ❌ Utility functions (<10ms, called frequently)
- ❌ Private internal helpers (creates noise)

**Gauntlet-Agents Example** (see `scripts/generate_test_traces.py`):

```python
# Real example from codebase
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Setup
provider = TracerProvider(resource=Resource.create({"service.name": "test-service"}))
exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)

# Usage
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("test_operation"):
    do_work()
```

---

### For debugger

**Use Case**: Troubleshoot missing spans, incorrect attributes, trace propagation issues

**Common Issues & Solutions**:

**1. Missing Spans**:

```python
# Problem: No spans appearing in Jaeger
# Cause: Tracer not initialized

# Fix: Check initialization at module load
from opentelemetry import trace
tracer = trace.get_tracer(__name__)  # Must happen after set_tracer_provider()

# Verify:
current_span = trace.get_current_span()
print(f"Span valid: {current_span.is_recording()}")  # Should be True
```

**2. Broken Context Propagation**:

```python
# Problem: Child spans not linking to parent
# Cause: Context not propagated across threads/processes

# Fix: Use context.attach() for thread pools
from opentelemetry import context

def worker_thread():
    # Get context from parent thread
    ctx = context.get_current()
    token = context.attach(ctx)
    try:
        with tracer.start_as_current_span("worker"):
            do_work()
    finally:
        context.detach(token)
```

**3. Incorrect Attributes**:

```python
# Problem: Attributes not showing in Jaeger
# Cause: Set after span closed

# Fix: Set attributes BEFORE span exits
with tracer.start_as_current_span("operation") as span:
    result = do_work()
    span.set_attribute("result.count", len(result))  # Inside with block
    # NOT here - span already closed
```

**4. Performance Impact**:

```python
# Problem: High latency after adding tracing
# Cause: Synchronous export (SimpleSpanProcessor)

# Fix: Use BatchSpanProcessor (async export)
processor = BatchSpanProcessor(exporter)  # Not SimpleSpanProcessor
provider.add_span_processor(processor)
```

**Debugging Workflow**:

1. **Isolate infrastructure vs code**:
   - Use `telemetrygen traces --otlp-insecure --duration 5s` to test collector
   - If telemetrygen works but app doesn't → instrumentation bug

2. **Enable debug logging**:

   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   logging.getLogger("opentelemetry").setLevel(logging.DEBUG)
   ```

3. **Check span validity**:

   ```python
   span = trace.get_current_span()
   print(f"Recording: {span.is_recording()}")  # Must be True
   print(f"Context: {span.get_span_context()}")  # Must have valid trace_id
   ```

4. **Verify exporter connectivity**:
   ```python
   from opentelemetry.sdk.trace.export import ConsoleSpanExporter
   # Temporarily replace OTLP exporter with console
   processor = BatchSpanProcessor(ConsoleSpanExporter())
   # Check if spans appear in console
   ```

---

## Related Documentation

- **Infrastructure Testing**: See `telemetrygen-usage.md` for testing OTEL Collector/Jaeger
- **Tool Disambiguation**: See `telemetry-disambiguation.md` for when to use SDK vs telemetrygen
- **Observability Implementation**: See `docs/03-implementation/observability/Local Kubernetes OpenTelemetry Monitoring - Complete Implementation Guide.md`
- **Gauntlet-Agents Example**: See `scripts/generate_test_traces.py` for real SDK usage

---

## Key Takeaways

1. **Auto-instrumentation First**: Use `opentelemetry-instrument` for framework tracing, add manual spans for business logic
2. **Resource Attribution**: Always configure service.name and deployment.environment
3. **BatchSpanProcessor**: Default for production (5s batching, 512 span batches)
4. **Semantic Conventions**: Use `opentelemetry.semconv.trace.SpanAttributes` for standard attributes
5. **Context Propagation**: Automatic in sync/async code, use span links for batch/queue processing
6. **Error Handling**: Always call `span.record_exception()` + `set_status(ERROR)` in except blocks
7. **Metrics at Module Level**: Create instruments once, use repeatedly (not per-request)
8. **Environment Configuration**: Prefer `OTEL_*` env vars over code for deployment flexibility

---

**Version**: 1.0
**Last Updated**: 2025-10-27
**Confidence**: 0.92 (based on official OpenTelemetry Python docs + gauntlet-agents codebase)
