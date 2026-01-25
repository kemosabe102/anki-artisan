# Telemetry Tool Disambiguation Guide

**Purpose**: Quick reference to select the right telemetry tool for your task

**Target Agents**: ALL (code-quality, deployment-release, development, debugger, architecture)

---

## Two Different Tools

| Tool                  | Purpose                          | Used For                                                                    | Used By                           |
| --------------------- | -------------------------------- | --------------------------------------------------------------------------- | --------------------------------- |
| **telemetrygen**      | Generate **synthetic test data** | Testing observability infrastructure (OTEL Collector, Jaeger, Prometheus)   | code-quality, deployment-release     |
| **OpenTelemetry SDK** | Instrument **application code**  | Adding observability to real services (traces, metrics from business logic) | development, debugger |

**Critical Distinction**: telemetrygen tests INFRASTRUCTURE, OpenTelemetry SDK instruments CODE.

---

## Decision Tree

```
┌─ Task: I need to...
│
├─ Test if OTEL Collector/Jaeger is working?
│  └─ ✅ Use telemetrygen CLI
│     └─ See: telemetrygen-usage.md
│
├─ Load test observability infrastructure?
│  └─ ✅ Use telemetrygen K8s Job
│     └─ See: telemetrygen-usage.md (K8s section)
│
├─ Add tracing to application code?
│  └─ ✅ Use OpenTelemetry Python SDK
│     └─ See: opentelemetry-instrumentation.md
│
├─ Emit metrics from business logic?
│  └─ ✅ Use OpenTelemetry Python SDK
│     └─ See: opentelemetry-instrumentation.md (Metrics section)
│
├─ Debug missing spans in production?
│  └─ ⚠️ First isolate: infrastructure or code?
│     ├─ Test with telemetrygen: Does it work?
│     │  ├─ YES → Code instrumentation issue (use OpenTelemetry SDK)
│     │  └─ NO → Infrastructure issue (deployment-release domain)
│     └─ See: opentelemetry-instrumentation.md (debugger section)
│
└─ Validate observability stack after deployment?
   └─ ✅ Use telemetrygen CLI
      └─ See: telemetrygen-usage.md (deployment-release section)
```

---

## Quick Comparison

### telemetrygen CLI

**Purpose**: Synthetic test data generator

**Installation**:

```bash
go install github.com/open-telemetry/opentelemetry-collector-contrib/cmd/telemetrygen@latest
```

**Usage**:

```bash
telemetrygen traces --otlp-insecure --duration 5s
```

**When to Use**:

- ✅ Testing OTEL Collector connectivity
- ✅ Validating Jaeger trace storage
- ✅ Load testing observability infrastructure
- ✅ Troubleshooting observability stack deployment
- ❌ NEVER for instrumenting application code

**Agent Domains**:

- **code-quality**: Load testing (T024)
- **deployment-release**: Stack validation, troubleshooting

**Reference**: `.claude/docs/01-guides/infrastructure/observability/telemetrygen-usage.md`

---

### OpenTelemetry Python SDK

**Purpose**: Application code instrumentation

**Installation**:

```bash
uv add opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp
```

**Usage**:

```python
from opentelemetry import trace
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("operation"):
    do_work()
```

**When to Use**:

- ✅ Adding traces to Python functions/services
- ✅ Emitting business metrics (counters, histograms)
- ✅ Instrumenting packages/core/\*\* code
- ✅ Debugging trace propagation in application
- ❌ NEVER for testing infrastructure

**Agent Domains**:

- **development**: Adding observability to features
- **debugger**: Troubleshooting instrumentation issues

**Reference**: `.claude/docs/01-guides/infrastructure/observability/opentelemetry-instrumentation.md`

---

## Common Confusion Scenarios

### Scenario 1: "Add telemetry to new feature"

**Question**: Should I use telemetrygen?
**Answer**: ❌ NO - Use OpenTelemetry Python SDK to instrument code

**Correct Approach**:

```python
# In packages/core/my_feature.py
from opentelemetry import trace
tracer = trace.get_tracer(__name__)

def my_feature_function():
    with tracer.start_as_current_span("my_feature"):
        return process()
```

**Agent**: development
**Reference**: opentelemetry-instrumentation.md

---

### Scenario 2: "Test observability stack"

**Question**: Should I instrument code to test infrastructure?
**Answer**: ❌ NO - Use telemetrygen CLI to generate synthetic test data

**Correct Approach**:

```bash
# Test connectivity
telemetrygen traces --otlp-insecure --duration 5s

# Verify traces in Jaeger UI
# If telemetrygen works, infrastructure is OK
```

**Agent**: deployment-release or code-quality
**Reference**: telemetrygen-usage.md

---

### Scenario 3: "Traces not appearing in Jaeger"

**Question**: Is this a telemetrygen issue?
**Answer**: ⚠️ DEPENDS - Need to isolate infrastructure vs code

**Debugging Workflow**:

1. **Test infrastructure with telemetrygen**:
   ```bash
   telemetrygen traces --otlp-insecure --traces 10
   ```
2. **Check Jaeger UI**:
   - ✅ If telemetrygen traces appear → Code instrumentation issue (OpenTelemetry SDK)
   - ❌ If telemetrygen traces DON'T appear → Infrastructure issue (deployment-release)

**Agents**: debugger (code issues) or deployment-release (infra issues)
**References**: Both guides

---

### Scenario 4: "Load test observability infrastructure"

**Question**: Should I write code with OpenTelemetry SDK?
**Answer**: ❌ NO - Use telemetrygen K8s Job for infrastructure load testing

**Correct Approach**:

```bash
# Deploy pre-built load test Job
kubectl apply -f k8s/local/telemetrygen-job.yaml

# Monitor OTEL Collector resources
kubectl top pods -n gauntlet-agents -l app=otel-collector
```

**Agent**: code-quality (T024)
**Reference**: telemetrygen-usage.md (K8s section)

---

## Agent-Specific Quick Reference

| Agent                       | Primary Tool         | When to Use                                                | Reference                        |
| --------------------------- | -------------------- | ---------------------------------------------------------- | -------------------------------- |
| **code-quality**           | telemetrygen CLI/Job | T024 load testing, infrastructure validation               | telemetrygen-usage.md            |
| **deployment-release**          | telemetrygen CLI     | Stack testing, troubleshooting, connectivity validation    | telemetrygen-usage.md            |
| **development** | OpenTelemetry SDK    | Adding tracing/metrics to packages/core/\*\*               | opentelemetry-instrumentation.md |
| **debugger**                | Both (isolate first) | Troubleshoot infrastructure vs code instrumentation issues | Both guides                      |
| **architecture**     | Context only         | Review observability architecture, not implementation      | This guide                       |

---

## Gauntlet-Agents Codebase Examples

### telemetrygen Usage (Infrastructure Testing)

**File**: `k8s/local/telemetrygen-job.yaml`
**Purpose**: Load testing OTEL Collector with 3 scenarios (baseline, high-throughput, spike)
**Usage**: `kubectl apply -f k8s/local/telemetrygen-job.yaml`

**Alternative**: No Python scripts currently use telemetrygen CLI (intentional - scripts use SDK instead)

---

### OpenTelemetry SDK Usage (Application Code)

**File**: `scripts/generate_test_traces.py`
**Purpose**: Generate test traces using Python SDK for Jaeger persistence testing
**Pattern**:

```python
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

provider = TracerProvider(resource=Resource.create({"service.name": "test"}))
exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)
provider.add_span_processor(BatchSpanProcessor(exporter))

tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("test_operation"):
    do_work()
```

---

## Key Takeaways

1. **telemetrygen = Infrastructure Testing Tool**
   - Generates synthetic data to test OTEL Collector/Jaeger
   - NOT for instrumenting application code
   - CLI tool or K8s Job

2. **OpenTelemetry SDK = Code Instrumentation Library**
   - Adds observability to real application code
   - Emits traces/metrics from business logic
   - Python library imported in packages/core/\*\*

3. **Decision Rule**:
   - Testing infrastructure? → telemetrygen
   - Instrumenting code? → OpenTelemetry SDK
   - Debugging? → Isolate first (test with telemetrygen, fix with SDK if needed)

4. **Agent Delegation**:
   - Infrastructure tasks → code-quality, deployment-release
   - Code instrumentation → development
   - Troubleshooting → debugger (uses both tools for isolation)

---

**Version**: 1.0
**Last Updated**: 2025-10-27
**Confidence**: 0.95 (comprehensive disambiguation with decision trees and examples)

---

## Related Documentation

- **telemetrygen Details**: `.claude/docs/01-guides/infrastructure/observability/telemetrygen-usage.md`
- **OpenTelemetry SDK Details**: `.claude/docs/01-guides/infrastructure/observability/opentelemetry-instrumentation.md`
- **Observability Implementation**: `docs/03-implementation/observability/Local Kubernetes OpenTelemetry Monitoring - Complete Implementation Guide.md`
