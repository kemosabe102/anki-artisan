# telemetrygen Usage Guide

**Purpose**: Generate synthetic telemetry data (traces, logs, metrics) to test observability infrastructure

**Target Agents**: code-quality, deployment-release

**Critical Distinction**: telemetrygen is for testing INFRASTRUCTURE, NOT for instrumenting application code. See `opentelemetry-instrumentation.md` for code instrumentation.

---

## Overview

telemetrygen is an official OpenTelemetry CLI tool for generating test telemetry to validate:

- OTEL Collectors are receiving data
- Jaeger is storing traces
- Prometheus is ingesting metrics
- End-to-end observability stack connectivity

**Use Cases**:

- Connectivity testing (5-second bursts)
- Load testing observability infrastructure
- Validating collector pipelines
- Performance benchmarking

---

## Installation

### Primary Method (Go)

```bash
go install github.com/open-telemetry/opentelemetry-collector-contrib/cmd/telemetrygen@latest
```

### Docker Alternative

```bash
make docker-telemetrygen
# Or use pre-built images
docker run ghcr.io/open-telemetry/opentelemetry-collector-contrib/telemetrygen:latest
```

---

## CLI Usage

### Basic Syntax

```bash
telemetrygen [signal-type] [flags]
```

**Signal Types**: `traces`, `logs`, `metrics`

### Common Examples

**1. Test Connectivity** (recommended first test):

```bash
telemetrygen traces --otlp-insecure --duration 5s
```

Expected: 5 seconds of traces sent to localhost:4317

**2. Generate Specific Quantity**:

```bash
telemetrygen traces --otlp-insecure --traces 1
```

Expected: Exactly 1 trace span generated

**3. Continuous Generation at Controlled Rate**:

```bash
telemetrygen traces --otlp-insecure --continuous --rate 0.1
```

Expected: 1 span every 10 seconds (0.1 = 10% frequency)

**4. Load Testing** (high throughput):

```bash
telemetrygen traces --otlp-insecure --duration 30s --rate 100
```

Expected: 3,000 spans (100 spans/sec × 30s)

**5. Generate Logs**:

```bash
telemetrygen logs --duration 5s --otlp-insecure
```

**6. Generate Metrics**:

```bash
telemetrygen metrics --duration 5s --otlp-insecure
```

---

## Configuration Parameters

| Parameter         | Purpose                                 | Example                            |
| ----------------- | --------------------------------------- | ---------------------------------- |
| `--otlp-insecure` | Disable TLS (local dev ONLY)            | Required for localhost testing     |
| `--otlp-endpoint` | OTLP endpoint (default: localhost:4317) | `--otlp-endpoint collector:4317`   |
| `--duration 5s`   | Run for time period                     | `5s`, `1m`, `10m`                  |
| `--traces N`      | Generate N specific spans               | `--traces 100`                     |
| `--continuous`    | Run indefinitely                        | Combine with `--rate`              |
| `--rate 0.1`      | Signals per second                      | `0.1` = every 10s, `100` = 100/sec |
| `--help`          | View all options                        | `telemetrygen traces --help`       |

**Default Endpoint**: `localhost:4317` (gRPC OTLP protocol)

---

## Kubernetes Deployment

### Gauntlet-Agents K8s Job

**File**: `k8s/local/telemetrygen-job.yaml`

**3 Load Scenarios** (set via `SCENARIO` env var):

| Scenario        | Rate (spans/sec) | Duration | Workers | Total Spans |
| --------------- | ---------------- | -------- | ------- | ----------- |
| baseline        | 100              | 30s      | 2       | 3,000       |
| high-throughput | 1,000            | 60s      | 10      | 60,000      |
| spike           | 5,000            | 30s      | 20      | 150,000     |

**Deploy**:

```bash
kubectl apply -f k8s/local/telemetrygen-job.yaml
```

**Configuration**:

- **Namespace**: gauntlet-agents
- **Endpoint**: otel-collector-service.gauntlet-agents.svc.cluster.local:4317
- **Auto-cleanup**: TTL 3600s (1 hour after completion)
- **Resource Limits**: CPU 100m-500m, Memory 128Mi-256Mi

---

## Testing Setup

### Minimal Collector Config

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317

exporters:
  debug:
    verbosity: detailed

service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [debug]
    logs:
      receivers: [otlp]
      exporters: [debug]
    metrics:
      receivers: [otlp]
      exporters: [debug]
```

### Launch Collector

```bash
docker run -p 4317:4317 \
  -v $(pwd)/config.yaml:/etc/otelcol-contrib/config.yaml \
  ghcr.io/open-telemetry/opentelemetry-collector-releases/opentelemetry-collector-contrib:0.86.0
```

### Verify Traces in Jaeger

After running telemetrygen:

1. Open Jaeger UI: http://localhost:16686
2. Select service: "telemetrygen" (default service name)
3. Click "Find Traces"
4. Expected: Traces within last 1 hour

---

## Agent-Specific Guidance

### For code-quality (T024 Load Testing)

**Use Case**: Validate observability infrastructure can handle production load

**Recommended Approach**:

1. Deploy K8s Job with scenario: `kubectl apply -f k8s/local/telemetrygen-job.yaml`
2. Monitor OTEL Collector metrics (CPU, memory, throughput)
3. Query Jaeger API to verify trace storage: `scripts/verify_traces.py`
4. Validate success rate ≥99% (e.g., 2,970/3,000 spans for baseline)

**Example Task** (T024):

```python
# In test suite
def test_load_testing_with_telemetrygen():
    # Deploy K8s Job
    subprocess.run(["kubectl", "apply", "-f", "k8s/local/telemetrygen-job.yaml"])

    # Wait for completion (baseline: ~35s)
    wait_for_job_completion("telemetrygen-load-test", timeout=60)

    # Verify traces in Jaeger
    result = verify_traces(service_name="telemetrygen", expected_count=3000)
    assert result.success_rate >= 0.99
```

**Alternative**: Python SDK approach (see `scripts/generate_test_traces.py` for example using OpenTelemetry Python SDK instead of telemetrygen CLI)

---

### For deployment-release

**Use Case**: Test observability stack after deployment, troubleshoot connectivity issues

**Troubleshooting Workflow**:

1. **Test Collector connectivity**:

   ```bash
   telemetrygen traces --otlp-endpoint otel-collector-service.gauntlet-agents.svc.cluster.local:4317 --otlp-insecure --duration 5s
   ```

   - If fails: Check OTEL Collector logs: `kubectl logs -n gauntlet-agents -l app=otel-collector`

2. **Isolate stack vs app issues**:
   - If telemetrygen works but app doesn't → instrumentation bug (delegate to debugger)
   - If telemetrygen fails → infrastructure issue (deployment-release domain)

3. **Validate end-to-end pipeline**:

   ```bash
   # Generate traces
   telemetrygen traces --otlp-insecure --traces 10

   # Check Jaeger UI immediately
   # Expected: 10 traces visible within 5-10 seconds
   ```

---

## Best Practices

✅ **DO**:

- Use `--otlp-insecure` for local development ONLY
- Test with `--duration 5s` before continuous generation
- Use specific counts (`--traces N`) for repeatable tests
- Combine `--continuous --rate 0.1` for controlled load testing
- Start with short durations to validate collector configuration

❌ **DON'T**:

- Use `--otlp-insecure` in production (reference examples/secure-tracing for TLS)
- Use telemetrygen for application code instrumentation (use OpenTelemetry SDK)
- Run high-rate continuous generation without monitoring collector resource usage
- Assume telemetrygen validates APPLICATION instrumentation (it only tests infrastructure)

---

## Common Issues

**Issue**: `connection refused` on localhost:4317

- **Cause**: OTEL Collector not running
- **Fix**: Start collector: `docker run -p 4317:4317 ...`

**Issue**: Traces generated but not visible in Jaeger

- **Cause**: Collector not configured to export to Jaeger
- **Fix**: Check collector config `exporters:` section

**Issue**: Low success rate (<95%)

- **Cause**: Collector overload or sampling
- **Fix**: Increase collector resources or reduce telemetrygen rate

---

## Related Documentation

- **Code Instrumentation**: See `opentelemetry-instrumentation.md` for adding tracing to application code
- **Tool Disambiguation**: See `telemetry-disambiguation.md` for when to use telemetrygen vs OpenTelemetry SDK
- **Observability Implementation**: See `docs/03-implementation/observability/Local Kubernetes OpenTelemetry Monitoring - Complete Implementation Guide.md`

---

**Version**: 1.0
**Last Updated**: 2025-10-27
**Confidence**: 0.92 (based on official OpenTelemetry docs + gauntlet-agents codebase analysis)
