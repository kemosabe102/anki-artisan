# OpenTelemetry Instrumentation Guide

> Comprehensive patterns for instrumenting Python applications with OpenTelemetry.

---

## Table of Contents

1. [Auto-Instrumentation Setup](#auto-instrumentation-setup)
2. [Manual Span Creation](#manual-span-creation)
3. [Context Propagation](#context-propagation)
4. [Async Instrumentation](#async-instrumentation)
5. [Common Library Instrumentation](#common-library-instrumentation)
6. [Exporter Configuration](#exporter-configuration)

---

## Auto-Instrumentation Setup

### Installation

```bash
# Core SDK
pip install opentelemetry-api opentelemetry-sdk

# Auto-instrumentation
pip install opentelemetry-distro opentelemetry-exporter-otlp

# Detect and install library instrumentations
opentelemetry-bootstrap -a install
```

### Runtime Execution

```bash
# Basic execution
opentelemetry-instrument python app.py

# With configuration
opentelemetry-instrument \
  --service_name order-service \
  --exporter_otlp_endpoint http://tempo:4317 \
  --exporter_otlp_protocol grpc \
  python app.py
```

### Environment Variable Configuration

```bash
export OTEL_SERVICE_NAME=order-service
export OTEL_RESOURCE_ATTRIBUTES="deployment.environment=production,service.version=1.2.3"
export OTEL_EXPORTER_OTLP_ENDPOINT=http://tempo:4317
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_TRACES_SAMPLER=parentbased_traceidratio
export OTEL_TRACES_SAMPLER_ARG=0.1

opentelemetry-instrument python app.py
```

---

## Manual Span Creation

### Basic Span

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def process_order(order_id: str) -> dict:
    with tracer.start_as_current_span("process_order") as span:
        # Business logic
        result = validate_order(order_id)
        return result
```

### Span with Attributes

```python
def process_order(order_id: str, order_type: str) -> dict:
    with tracer.start_as_current_span("process_order") as span:
        # Set attributes (keep cardinality low)
        span.set_attribute("order.id", order_id)
        span.set_attribute("order.type", order_type)  # "standard", "premium", "express"
        span.set_attribute("order.item_count", len(items))
        
        result = do_processing()
        return result
```

### Span with Status and Events

```python
from opentelemetry.trace import Status, StatusCode

def process_payment(payment_id: str) -> bool:
    with tracer.start_as_current_span("process_payment") as span:
        span.set_attribute("payment.id", payment_id)
        
        try:
            # Add event for significant milestones
            span.add_event("validation_started")
            validate_payment(payment_id)
            span.add_event("validation_completed")
            
            result = charge_payment(payment_id)
            span.set_status(Status(StatusCode.OK))
            return result
            
        except PaymentDeclinedException as e:
            span.set_status(Status(StatusCode.ERROR, "Payment declined"))
            span.record_exception(e)
            raise
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.record_exception(e)
            raise
```

---

## Context Propagation

### Automatic (HTTP Headers)

Auto-instrumentation handles this for supported libraries. Manual propagation:

```python
from opentelemetry import trace
from opentelemetry.propagate import inject, extract

# Inject context into outgoing request
def call_external_service(url: str, data: dict) -> dict:
    headers = {}
    inject(headers)  # Adds traceparent header
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Extract context from incoming request
def handle_request(request):
    context = extract(request.headers)
    with tracer.start_as_current_span("handle_request", context=context):
        return process(request)
```

### Between Threads

```python
from opentelemetry.context import attach, detach, get_current
from concurrent.futures import ThreadPoolExecutor

def process_items(items: list):
    with tracer.start_as_current_span("process_items"):
        # Capture current context
        ctx = get_current()
        
        def process_item(item):
            # Attach context in worker thread
            token = attach(ctx)
            try:
                with tracer.start_as_current_span("process_item"):
                    return do_work(item)
            finally:
                detach(token)
        
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(process_item, items))
        return results
```

---

## Async Instrumentation

### asyncio Context Propagation

```python
import asyncio
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

async def fetch_data(url: str) -> dict:
    with tracer.start_as_current_span("fetch_data") as span:
        span.set_attribute("http.url", url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                span.set_attribute("http.status_code", response.status)
                return await response.json()

async def process_multiple():
    with tracer.start_as_current_span("process_multiple"):
        # Context automatically propagates in asyncio
        results = await asyncio.gather(
            fetch_data("http://api1.example.com"),
            fetch_data("http://api2.example.com"),
        )
        return results
```

### Common Async Pitfall

```python
# WRONG: Span created outside async context
span = tracer.start_span("my_span")  # Detached from parent!

async def bad_async():
    # This span has no parent
    await do_work()
    span.end()

# CORRECT: Use context manager
async def good_async():
    with tracer.start_as_current_span("my_span"):
        await do_work()
```

---

## Common Library Instrumentation

### Requests (HTTP Client)

```bash
pip install opentelemetry-instrumentation-requests
```

```python
from opentelemetry.instrumentation.requests import RequestsInstrumentor
RequestsInstrumentor().instrument()

# All requests.* calls now create spans automatically
response = requests.get("http://api.example.com")
```

### Flask

```bash
pip install opentelemetry-instrumentation-flask
```

```python
from flask import Flask
from opentelemetry.instrumentation.flask import FlaskInstrumentor

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.route("/api/orders")
def get_orders():
    # Span automatically created for this endpoint
    return {"orders": []}
```

### FastAPI

```bash
pip install opentelemetry-instrumentation-fastapi
```

```python
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

@app.get("/api/orders")
async def get_orders():
    return {"orders": []}
```

### SQLAlchemy

```bash
pip install opentelemetry-instrumentation-sqlalchemy
```

```python
from sqlalchemy import create_engine
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

engine = create_engine("postgresql://...")
SQLAlchemyInstrumentor().instrument(engine=engine)

# All queries now create spans with:
# - db.system
# - db.statement (SQL query)
# - db.operation (SELECT, INSERT, etc.)
```

### Redis

```bash
pip install opentelemetry-instrumentation-redis
```

```python
from opentelemetry.instrumentation.redis import RedisInstrumentor
RedisInstrumentor().instrument()

# Redis operations create spans with:
# - db.system = "redis"
# - db.operation (GET, SET, etc.)
```

---

## Exporter Configuration

### OTLP to Tempo

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

# Configure resource
resource = Resource.create({
    SERVICE_NAME: "order-service",
    "deployment.environment": "production",
})

# Configure exporter
exporter = OTLPSpanExporter(
    endpoint="http://tempo:4317",
    insecure=True,
)

# Configure provider
provider = TracerProvider(resource=resource)
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)
```

### OTLP to Jaeger

```python
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Jaeger accepts OTLP on port 4317
exporter = OTLPSpanExporter(
    endpoint="http://jaeger:4317",
    insecure=True,
)
```

### Console (Development)

```python
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

provider = TracerProvider(resource=resource)
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)
```

---

## Attribute Best Practices

### Semantic Conventions

Use OpenTelemetry semantic conventions for standard attributes:

| Domain | Attribute | Example |
|--------|-----------|---------|
| HTTP | `http.method` | `GET`, `POST` |
| HTTP | `http.status_code` | `200`, `500` |
| HTTP | `http.url` | `https://api.example.com/orders` |
| Database | `db.system` | `postgresql`, `mysql` |
| Database | `db.operation` | `SELECT`, `INSERT` |
| Database | `db.name` | `orders_db` |

### Cardinality Rules

```python
# GOOD: Bounded cardinality
span.set_attribute("http.method", "GET")  # ~7 values
span.set_attribute("order.type", "premium")  # ~3-5 values
span.set_attribute("http.status_code", 200)  # ~50 values

# BAD: Unbounded cardinality
span.set_attribute("user.email", user.email)  # Millions
span.set_attribute("request.body", body)  # Infinite
span.set_attribute("order.id", order_id)  # Use span name instead
```

---

## Troubleshooting

### No Traces Appearing

1. **Check exporter endpoint**: Verify Tempo/Jaeger is reachable
2. **Check sampling**: Ensure sampler isn't dropping all traces
3. **Check resource attributes**: `service.name` must be set
4. **Check BatchSpanProcessor**: May need to flush before exit

```python
# Force flush on shutdown
import atexit
atexit.register(provider.force_flush)
```

### Broken Trace Context

1. **Check header propagation**: Ensure `traceparent` header passes through proxies
2. **Check instrumentation order**: Instrument before creating clients
3. **Check async context**: Use `start_as_current_span` not `start_span`

### High Memory Usage

1. **Reduce batch size**: Lower `max_export_batch_size`
2. **Increase export frequency**: Lower `schedule_delay_millis`
3. **Sample more aggressively**: Reduce sampling ratio

```python
from opentelemetry.sdk.trace.export import BatchSpanProcessor

processor = BatchSpanProcessor(
    exporter,
    max_queue_size=2048,  # Default 2048
    max_export_batch_size=256,  # Default 512
    schedule_delay_millis=5000,  # Default 5000
)
```
