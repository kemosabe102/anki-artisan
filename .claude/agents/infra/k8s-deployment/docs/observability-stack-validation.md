# Observability Stack Validation Guide

**Purpose**: Testing deployed observability infrastructure (OTEL Collector, Jaeger, Prometheus, Grafana) using telemetrygen and kubectl commands.

**When to Use**: After deploying observability stack to verify infrastructure is working correctly.

---

## Reference Documentation

- `.claude/docs/guides/telemetry-disambiguation.md` - Quick reference: infrastructure testing vs code instrumentation
- `.claude/docs/guides/telemetrygen-usage.md` - Complete telemetrygen CLI and K8s Job usage for stack validation

---

## Two Distinct Responsibilities

1. **Deploy observability infrastructure** (Jaeger pods, OTEL Collector, Prometheus) - k8s-deployment domain
2. **Deploy telemetrygen Jobs** for load testing infrastructure - k8s-deployment domain
3. **Instrument application code** (OpenTelemetry SDK in Python/Go) - Delegate to python-code-implementer (NOT k8s-deployment)

---

## Testing Stack After Deployment

### Quick Connectivity Test

```bash
# Test OTEL Collector endpoint
AGENT_NAME=k8s-deployment telemetrygen traces --otlp-endpoint otel-collector-service.gauntlet-agents.svc.cluster.local:4317 --otlp-insecure --duration 5s

# Verify in Jaeger UI: http://localhost:16686
# Expected: Traces visible within 5-10 seconds
```

---

### Load Testing (K8s Job approach)

```bash
# Deploy pre-built load test Job
AGENT_NAME=k8s-deployment kubectl apply -f k8s/local/telemetrygen-job.yaml

# Monitor job completion
AGENT_NAME=k8s-deployment kubectl logs -n gauntlet-agents -l job-name=telemetrygen-load-test -f

# Verify traces via Jaeger UI (NodePort access)
# Open http://localhost:31686 in browser and check for telemetrygen service
# OR use curl from host:
curl -s "http://localhost:31686/api/traces?service=telemetrygen&limit=100" | jq '.data | length'
```

---

## Troubleshooting Workflow

### 1. Isolate Infrastructure vs Application

**Run telemetrygen to test stack**:
```bash
AGENT_NAME=k8s-deployment telemetrygen traces --otlp-insecure --duration 5s
```

- ✅ **If telemetrygen works** → Stack is OK, application instrumentation issue (delegate to debugger)
- ❌ **If telemetrygen fails** → Infrastructure issue (k8s-deployment domain)

---

### 2. Common Infrastructure Issues

**Connection refused**: OTEL Collector not running
- **Check**: `kubectl get pods -n gauntlet-agents -l app=otel-collector`
- **Fix**: Restart collector pod or check service endpoints

**Traces not in Jaeger**: Collector pipeline misconfigured
- **Check**: `kubectl logs -n gauntlet-agents -l app=otel-collector`
- **Fix**: Verify `exporters:` section in collector ConfigMap

**Low success rate (<95%)**: Collector overload
- **Check**: `kubectl top pods -n gauntlet-agents -l app=otel-collector`
- **Fix**: Increase CPU/memory limits or scale replicas

---

### 3. Validation Checklist

- [ ] OTEL Collector receiving traces (check logs for "ExportTraceServiceRequest")
- [ ] Jaeger storing traces (query API: http://localhost:16686/api/traces)
- [ ] Prometheus scraping collector metrics (check /metrics endpoint)
- [ ] Success rate ≥99% for baseline load scenario

---

## K8s Resources

- **Job manifest**: `k8s/local/telemetrygen-job.yaml` (3 load scenarios: baseline/high-throughput/spike)
- **Collector config**: `k8s/local/otel-collector.yaml` (pipeline configuration)
- **Jaeger deployment**: `k8s/local/jaeger.yaml` (trace storage backend)

---

## Related Scripts

- `scripts/verify_traces.py` - Verify traces via Jaeger API
- `scripts/deployment/deploy-local-k8s.sh` - Full stack deployment (if exists)

---

## Best Practices

- ✅ Test with telemetrygen after every observability stack deployment
- ✅ Start with 5-second connectivity test before load testing
- ✅ Use K8s Jobs for repeatable load tests (not ad-hoc CLI commands)
- ❌ Do NOT use telemetrygen for application code instrumentation (delegate to python-code-implementer)

---

## Service-Specific Troubleshooting Guides

**Observability Stack Troubleshooting Guides** (explicit file paths for link validation):

- `docs/04-guides/observability/jaeger-troubleshooting.md` - Jaeger v2 ConfigMap mounting, Badger storage, OTLP receivers (ports 4317/4318), trace persistence validation
- `docs/04-guides/observability/otel-collector-troubleshooting.md` - Memory limiter configuration, batch processor optimization, GOMEMLIMIT tuning, failure mode diagnosis
- `docs/04-guides/observability/prometheus-troubleshooting.md` - Storage retention policies, PersistentVolume configuration, scrape target validation, capacity planning
- `docs/04-guides/observability/grafana-troubleshooting.md` - Data source provisioning (Prometheus/Jaeger), Kubernetes service URL patterns, connection troubleshooting

---

**See Also**:
- `.claude/docs/guides/telemetry-disambiguation.md` - Domain boundaries
- `.claude/docs/guides/telemetrygen-usage.md` - Complete CLI reference
- `../../docs/04-guides/observability/` - Service-specific troubleshooting
