---
name: deepeval-evaluation-runbook
description: Operational runbook for the DeepEval agent evaluation system
date: 2025-12-03
---

# DeepEval Evaluation System Runbook

## Overview

The DeepEval evaluation system provides automated quality metrics collection for Claude Code agent tests. It captures pass rates, execution times, and quality scores, exporting them to Prometheus for real-time monitoring in Grafana.

### Key Features

- **Automatic instrumentation**: Tests are instrumented via pytest plugin (no code changes needed)
- **Opt-in activation**: Metrics only collected when `DEEPEVAL_METRICS_ENABLED=true`
- **Quality gates**: Blocks agent creation if pass rate <90% or quality score <0.75
- **Real-time dashboards**: Grafana visualization with 15-second refresh

### Components

| Component | Port | Purpose |
|-----------|------|---------|
| OTEL Collector | 4317 (gRPC), 8888 (metrics) | Receives and routes metrics |
| Prometheus | 9090 | Time-series metrics storage |
| Grafana | 3000 | Dashboards and alerting |


---

## Architecture

```
Test Execution (pytest)
         |
         v
  Pytest Plugin (packages/evaluations/pytest_plugin.py)
         |
         v
  MetricsRecorder (packages/evaluations/recorder.py)
         |
         v
  OTEL SDK (packages/evaluations/otel_exporter.py)
         |
         v (gRPC :4317)
  OTEL Collector
         |
         v (scrape :8888)
  Prometheus
         |
         v (query :9090)
  Grafana Dashboard
```

### Data Flow

1. **Test runs**: pytest executes tests normally
2. **Hook captures**: `pytest_runtest_makereport` hook records pass/fail and timing
3. **Metrics recorded**: MetricsRecorder updates OTEL counters and gauges
4. **Export**: OTEL SDK exports to collector every 5 seconds
5. **Scrape**: Prometheus scrapes collector every 15 seconds
6. **Visualize**: Grafana queries Prometheus and displays dashboards

---

## Setup

### Prerequisites

- Docker installed and running
- Kubernetes cluster (minikube or similar) for K8s deployment
- uv package manager installed


### Enable Metrics Collection

```bash
# Run tests with metrics enabled
DEEPEVAL_METRICS_ENABLED=true uv run pytest tests/

# Or set in environment
export DEEPEVAL_METRICS_ENABLED=true
uv run pytest tests/
```

### Start Observability Stack (K8s)

```bash
# Verify pods are running
kubectl get pods -n observability

# Services are accessible via NodePorts (no port-forward needed):
# - Grafana: http://localhost:30030
# - Prometheus: http://localhost:30090
# - OTEL Collector gRPC: localhost:30317
```

### Verify Stack Health

```bash
# Check Prometheus is healthy
curl -s http://localhost:9090/-/healthy

# Check OTEL Collector metrics endpoint
curl -s http://localhost:8888/metrics | head -20

# Check Grafana is accessible
curl -s http://localhost:3000/api/health
```

---

## Usage

### Viewing Dashboards

1. Open Grafana: http://localhost:30030 (NodePort)
2. Login with admin credentials (default: admin/admin)
3. Navigate to Dashboards > DeepEval Metrics


### Dashboard Panels

| Panel | PromQL Query | Purpose |
|-------|--------------|---------|
| Pass Rate Trend | `deepeval_test_pass_rate_percent` | Track pass rate over time |
| Execution Time | `histogram_quantile(0.95, deepeval_test_execution_time_seconds_bucket)` | P95 test duration |
| Quality Score | `deepeval_code_quality_score` | Overall quality gauge |
| Test Counts | `rate(deepeval_tests_passed_total[5m])` | Tests passed per minute |

### Interpreting Alerts

| Alert | Condition | Action |
|-------|-----------|--------|
| DeepEvalPassRateLow | pass_rate < 90% for 5min | Review failing tests, fix before merging |
| DeepEvalQualityDegraded | quality_score < 0.75 for 5min | Check code review feedback |

### Quality Gate Check

Run before creating new agents:

```bash
# Check quality gates
uv run python scripts/quality_gate_check.py

# Skip gates (prototyping only)
uv run python scripts/quality_gate_check.py --skip-quality-gate

# Custom thresholds
uv run python scripts/quality_gate_check.py \
  --pass-rate-threshold=85 \
  --quality-threshold=0.70
```

---

## Troubleshooting

### Metrics Not Appearing in Prometheus


**Symptoms**: Dashboard shows "No data" or stale values

**Diagnosis**:
```bash
# Check if OTEL collector is receiving metrics
curl -s http://localhost:8888/metrics | grep deepeval

# Check Prometheus targets
curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | select(.labels.job == "otel-collector")'

# Check if env var is set
echo $DEEPEVAL_METRICS_ENABLED
```

**Solutions**:
1. Ensure `DEEPEVAL_METRICS_ENABLED=true` when running tests
2. Verify OTEL collector is running and accessible on port 4317
3. Check Prometheus is scraping the collector endpoint
4. Wait 15-30 seconds for metrics to propagate

### Connection Refused to OTEL Collector

**Symptoms**: Warning in test output about failed metrics initialization

**Diagnosis**:
```bash
# Check if collector is listening
nc -zv localhost 4317

# Check pod status
kubectl get pods -n observability -l app=otel-collector
```

**Solutions**:
1. Start the OTEL collector service
2. Verify port-forward is active: `kubectl port-forward -n observability svc/otel-collector 4317:4317`
3. Check firewall rules are not blocking port 4317


### Quality Gate Check Fails Unexpectedly

**Symptoms**: `quality_gate_check.py` returns exit code 1

**Diagnosis**:
```bash
# Check current metrics values using PrometheusClient
uv run python -c "from packages.evaluations.prometheus_client import PrometheusClient; c = PrometheusClient(); print(f'Pass rate: {c.get_pass_rate()}'); print(f'Quality score: {c.get_quality_score()}')"

# Manual Prometheus query
curl -s 'http://localhost:9090/api/v1/query?query=deepeval_test_pass_rate_percent' | jq '.data.result[0].value[1]'
```

**Solutions**:
1. Review failing tests and fix them
2. If metrics are stale, run a fresh test suite with metrics enabled
3. Use `--skip-quality-gate` flag for prototyping (not production)

### High Overhead (>5%)

**Symptoms**: Benchmark shows overhead exceeding 5% threshold

**Diagnosis**:
```bash
# Run verbose benchmark
uv run python scripts/benchmark_overhead.py --verbose --iterations=5
```

**Solutions**:
1. Check for network latency to OTEL collector
2. Verify collector is not overloaded
3. Consider increasing export interval in `otel_exporter.py`

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEEPEVAL_METRICS_ENABLED` | `false` | Enable/disable metrics collection |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `localhost:4317` | OTEL collector gRPC endpoint |


### Quality Gate Thresholds

| Threshold | Default | Description |
|-----------|---------|-------------|
| Pass Rate | 90% | Minimum test pass rate |
| Quality Score | 0.75 | Minimum code quality score (0-1) |

### Alert Thresholds

| Alert | Threshold | Duration |
|-------|-----------|----------|
| DeepEvalPassRateLow | <90% | 5 minutes |
| DeepEvalQualityDegraded | <0.75 | 5 minutes |

---

## Key Files

| File | Purpose |
|------|---------|
| `packages/evaluations/pytest_plugin.py` | Pytest hooks for metrics capture |
| `packages/evaluations/recorder.py` | MetricsRecorder wrapper for OTEL instruments |
| `packages/evaluations/otel_exporter.py` | OTEL SDK configuration |
| `packages/evaluations/metrics.py` | Metric instrument definitions |
| `packages/evaluations/prometheus_client.py` | Prometheus query client |
| `scripts/quality_gate_check.py` | Quality gate CLI tool |
| `scripts/benchmark_overhead.py` | Overhead benchmark script |
| `k8s/local/observability/grafana/dashboards/deepeval-metrics.json` | Grafana dashboard |
| `k8s/local/observability/prometheus/rules/deepeval-alerts.yaml` | Prometheus alert rules |

---

## Related Documentation

- [DeepEval Prometheus OTEL Integration Guide](./deepeval_prometheus_otel_integration.md)
- [SPEC: DeepEval Agent Evaluation System](../../../../docs/01-planning/specifications/015-deepeval-agent-evaluation/SPEC.md)
- [BENCHMARK Results](../../../../docs/01-planning/specifications/015-deepeval-agent-evaluation/BENCHMARK.md)
