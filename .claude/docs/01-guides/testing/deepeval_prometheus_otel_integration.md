---
name: deepeval-prometheus-otel-integration
description: Complete guide for exporting DeepEval metrics to Prometheus via OpenTelemetry
date: 2025-11-26
---

# DeepEval → OpenTelemetry → Prometheus Integration Guide

## Overview

**Goal**: Capture all DeepEval test metrics (pass rates, quality scores, execution time, code review data) and export them to Prometheus for real-time dashboarding in Grafana.

**Three Export Paths Available**:
1. **Direct Prometheus Export** (simplest, single exporter)
2. **OTEL Collector → Prometheus** (recommended for production)
3. **OTEL Collector → Multiple Backends** (Prometheus + Datadog + New Relic, etc.)

---

## Architecture: Data Flow

```
┌─────────────────────────────────────────────────────┐
│  Claude Code Test Evaluator Agent                   │
│  - Runs tests in Docker                             │
│  - Collects: pass/fail, quality scores, time        │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│  DeepEval Test Suite Execution                      │
│  @observe decorator captures metrics                │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│  OpenTelemetry SDK (CNCF Standard)                  │
│  - Meter: Records metrics                           │
│  - Counters, Histograms, Gauges                     │
└────────────────┬────────────────────────────────────┘
                 │
    ┌────────────┴────────────┬──────────────┐
    │                         │              │
    ▼                         ▼              ▼
┌─────────┐           ┌──────────────┐  ┌──────────┐
│Prometheus│           │OTEL Collector│  │Datadog   │
│ Exporter │           │(Collector)   │  │New Relic │
└────┬────┘           └──────┬───────┘  └──────────┘
     │                       │
     └───────────────────────┼──────────────────────┐
                             │                      │
                    ┌────────▼────────┐    ┌────────▼────┐
                    │Prometheus TSDB  │    │Other Sinks  │
                    │Time-Series Data │    │             │
                    └────────┬────────┘    └─────────────┘
                             │
                    ┌────────▼────────┐
                    │Grafana Dashboard│
                    │Real-time Viz    │
                    └─────────────────┘
```

---

## Implementation: Code Examples

### Step 1: Configure OpenTelemetry Exporter

```python
# evaluations/otel_exporter.py

from opentelemetry import metrics, trace
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

# Option A: Export to OTEL Collector (recommended)
def setup_otel_collector_exporter():
    otlp_exporter = OTLPMetricExporter(
        endpoint="localhost:4317",  # OTEL Collector gRPC endpoint
    )
    metric_reader = PeriodicExportingMetricReader(otlp_exporter, interval_millis=5000)
    provider = MeterProvider(metric_readers=[metric_reader])
    metrics.set_meter_provider(provider)
    return provider

# Option B: Export directly to Prometheus (simpler for single-backend)
def setup_prometheus_exporter():
    from opentelemetry.exporter.prometheus import PrometheusMetricReader
    from prometheus_client import start_http_server
    
    prometheus_reader = PrometheusMetricReader()
    provider = MeterProvider(metric_readers=[prometheus_reader])
    metrics.set_meter_provider(provider)
    
    # Expose /metrics endpoint on port 8000
    start_http_server(8000, registry=prometheus_reader.get_metrics_data())
    return provider

# Initialize based on environment
import os
if os.getenv("USE_OTEL_COLLECTOR"):
    provider = setup_otel_collector_exporter()
else:
    provider = setup_prometheus_exporter()
```

### Step 2: Define Metrics for Your Test Evaluator

```python
# evaluations/metrics.py

from opentelemetry import metrics

meter = metrics.get_meter("claude-code-test-evaluator")

# Counter: Total tests passed
tests_passed_counter = meter.create_counter(
    name="tests_passed_total",
    description="Total number of tests passed",
    unit="1"
)

# Counter: Total tests failed
tests_failed_counter = meter.create_counter(
    name="tests_failed_total",
    description="Total number of tests failed",
    unit="1"
)

# Histogram: Execution time per test
execution_time_histogram = meter.create_histogram(
    name="test_execution_time_seconds",
    description="Time to execute each test",
    unit="s"
)

# Gauge: Current pass rate
pass_rate_gauge = meter.create_gauge(
    name="test_pass_rate_percent",
    description="Current pass rate percentage",
    unit="%"
)

# Gauge: Code quality score
code_quality_gauge = meter.create_gauge(
    name="code_quality_score",
    description="Overall code quality 0-1",
    unit="1"
)

# Gauge: Error handling score
error_handling_gauge = meter.create_gauge(
    name="error_handling_score",
    description="Error handling quality 0-1",
    unit="1"
)

# Gauge: Efficiency score
efficiency_gauge = meter.create_gauge(
    name="efficiency_score",
    description="Code efficiency 0-1",
    unit="1"
)

# Counter: Tool calls
tool_calls_counter = meter.create_counter(
    name="tool_calls_total",
    description="Total tool/API calls made",
    unit="1"
)

# Gauge: Token usage estimate
token_usage_gauge = meter.create_gauge(
    name="token_usage_estimated",
    description="Estimated tokens used",
    unit="1"
)

# Counter: Memory usage
memory_usage_gauge = meter.create_gauge(
    name="memory_peak_mb",
    description="Peak memory usage",
    unit="MB"
)
```

### Step 3: Record Metrics During Evaluation

```python
# claude_code_test_evaluator.py (updated)

from evaluations.metrics import (
    tests_passed_counter,
    tests_failed_counter,
    execution_time_histogram,
    pass_rate_gauge,
    code_quality_gauge,
    error_handling_gauge,
    efficiency_gauge,
    tool_calls_counter,
    token_usage_gauge,
    memory_usage_gauge
)

def evaluate_solution(self, solution, test_suite, scenario=None):
    """Execute and record metrics"""
    
    # Run tests
    exec_result = self.run_in_docker(solution, test_suite)
    
    # Extract results
    passed = exec_result.get('passed_tests', 0)
    failed = exec_result.get('failed_tests', 0)
    total = passed + failed
    execution_time = exec_result.get('execution_time_seconds', 0)
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    # Common attributes for all metrics (helps filter in Prometheus)
    attributes = {
        "difficulty": exec_result.get('difficulty', 'unknown'),
        "benchmark_id": exec_result.get('benchmark_id', 'unknown'),
        "agent_name": "claude-code-agent",
        "test_framework": "pytest"
    }
    
    # Record execution metrics
    tests_passed_counter.add(passed, attributes=attributes)
    tests_failed_counter.add(failed, attributes=attributes)
    execution_time_histogram.record(execution_time, attributes=attributes)
    pass_rate_gauge.set(pass_rate, attributes=attributes)
    
    # Record code quality metrics from review
    code_review = exec_result.get('code_review', {})
    code_quality_gauge.set(
        code_review.get('overall_score', 0),
        attributes=attributes
    )
    error_handling_gauge.set(
        code_review.get('error_handling_score', 0),
        attributes=attributes
    )
    efficiency_gauge.set(
        code_review.get('efficiency_score', 0),
        attributes=attributes
    )
    
    # Record resource metrics
    metrics_data = exec_result.get('metrics', {})
    tool_calls_counter.add(
        metrics_data.get('tool_calls', 0),
        attributes=attributes
    )
    token_usage_gauge.set(
        metrics_data.get('token_usage', 0),
        attributes=attributes
    )
    memory_usage_gauge.set(
        metrics_data.get('peak_memory_mb', 0),
        attributes=attributes
    )
    
    # Return standard report + metrics
    return {
        **exec_result,
        "metrics_recorded": True,
        "metrics_attributes": attributes
    }
```

---

## Setup: Docker Compose + OTEL Collector + Prometheus + Grafana

### docker-compose.yml

```yaml
version: '3.8'

services:
  # OpenTelemetry Collector: Receives metrics, routes to Prometheus
  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.88.0
    command: ["--config=/etc/otel-collector-config.yaml"]
    ports:
      - "4317:4317"    # OTLP gRPC receiver (agent sends here)
      - "4318:4318"    # OTLP HTTP receiver
      - "8888:8888"    # Prometheus exporter endpoint
    volumes:
      - ./otel-collector-config.yaml:/etc/otel-collector-config.yaml
    environment:
      - GOGC=80
    depends_on:
      - prometheus

  # Prometheus: Time-series database for metrics
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./prometheus-alerts.yml:/etc/prometheus/alerts.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=30d'

  # Grafana: Visualization dashboard
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - ./grafana/provisioning/datasources:/etc/grafana/provisioning/datasources
      - ./grafana/provisioning/dashboards:/etc/grafana/provisioning/dashboards
      - grafana_data:/var/lib/grafana
    depends_on:
      - prometheus

volumes:
  prometheus_data:
  grafana_data:
```

### otel-collector-config.yaml

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    send_batch_size: 1024
    timeout: 10s
  
  attributes:
    actions:
      - key: service.name
        value: claude-code-evaluator
        action: insert

exporters:
  prometheus:
    endpoint: "0.0.0.0:8888"
    namespace: deepeval
    
  # Optional: Add additional exporters
  # otlp:
  #   client:
  #     endpoint: https://api.honeycomb.io:443
  #     headers:
  #       x-honeycomb-team: ${HONEYCOMB_API_KEY}

service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors: [batch, attributes]
      exporters: [prometheus]
```

### prometheus.yml

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: []

rule_files:
  - "prometheus-alerts.yml"

scrape_configs:
  # Scrape OTEL Collector's Prometheus exporter
  - job_name: 'otel-collector'
    static_configs:
      - targets: ['localhost:8888']
    metric_relabel_configs:
      - source_labels: [__name__]
        regex: 'deepeval_.*'
        action: keep

  # Direct Prometheus exporter from evaluator (if used)
  - job_name: 'deepeval-metrics'
    scrape_interval: 5s
    static_configs:
      - targets: ['localhost:8000']
```

### prometheus-alerts.yml

```yaml
groups:
  - name: deepeval_alerts
    interval: 30s
    rules:
      # Alert when pass rate drops below 90%
      - alert: TestPassRateLow
        expr: test_pass_rate_percent < 90
        for: 5m
        annotations:
          summary: "Test pass rate dropped below 90%: {{ $value }}%"
          dashboard: "http://localhost:3000/d/deepeval"

      # Alert when execution time is too high
      - alert: TestExecutionTimeSlow
        expr: histogram_quantile(0.95, test_execution_time_seconds) > 10
        for: 5m
        annotations:
          summary: "95th percentile execution time is {{ $value }}s"

      # Alert when code quality degrades
      - alert: CodeQualityDegraded
        expr: code_quality_score < 0.75
        for: 10m
        annotations:
          summary: "Code quality score is {{ $value }}"

      # Alert on high token usage
      - alert: HighTokenUsage
        expr: token_usage_estimated > 5000
        for: 5m
        annotations:
          summary: "Token usage estimated at {{ $value }}"
```

### Grafana Datasource Provisioning

```yaml
# grafana/provisioning/datasources/prometheus.yml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
```

---

## Grafana Dashboard Queries & Panels

### Panel 1: Pass Rate Trend Over Time

**Query**:
```promql
100 * (
  rate(tests_passed_total[5m])
  / 
  (rate(tests_passed_total[5m]) + rate(tests_failed_total[5m]))
)
```

**Visualization**: Line graph
**Legend**: `{{ difficulty }}` (easy/medium/hard)

### Panel 2: Execution Time by Difficulty

**Query** (95th percentile):
```promql
histogram_quantile(0.95, rate(test_execution_time_seconds_bucket[5m])) by (difficulty)
```

**Visualization**: Bar chart or line graph
**Legend**: `{{ difficulty }}`

### Panel 3: Code Quality Scores

**Query** (gauge panel showing current values):
```promql
code_quality_score
error_handling_score
efficiency_score
```

**Visualization**: Gauge or stat panels
**Thresholds**: Green >0.8, Yellow 0.6-0.8, Red <0.6

### Panel 4: Test Count by Status

**Query** (stacked bar chart):
```promql
# Passed tests
rate(tests_passed_total[5m])

# Failed tests
rate(tests_failed_total[5m])
```

**Visualization**: Stacked bar chart
**Stacking**: Stack series on

### Panel 5: Tool Calls per Benchmark

**Query**:
```promql
rate(tool_calls_total[1h]) by (benchmark_id)
```

**Visualization**: Pie chart or bar chart
**Legend**: `{{ benchmark_id }}`

### Panel 6: Resource Usage Heatmap

**Query** (execution time distribution):
```promql
rate(test_execution_time_seconds_bucket[5m])
```

**Visualization**: Heatmap
**Bucket options**: Auto-scale

### Panel 7: Token Usage Trend

**Query**:
```promql
token_usage_estimated
```

**Visualization**: Line graph with threshold line
**Threshold**: Draw line at token budget (e.g., 2000)

### Panel 8: Pass Rate Gauge

**Query**:
```promql
test_pass_rate_percent
```

**Visualization**: Gauge
**Thresholds**: 0, 75 (red), 90 (yellow), 100 (green)

---

## Environment Configuration

### .env file for Docker Compose

```env
# OTEL Configuration
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
OTEL_EXPORTER_OTLP_PROTOCOL=grpc
USE_OTEL_COLLECTOR=true

# Prometheus Configuration
PROMETHEUS_RETENTION=30d
PROMETHEUS_SCRAPE_INTERVAL=15s

# Grafana Configuration
GF_SECURITY_ADMIN_PASSWORD=your_secure_password
GF_USERS_ALLOW_SIGN_UP=false
```

### Python Environment Setup

```bash
# Install required packages
pip install \
  opentelemetry-api==1.20.0 \
  opentelemetry-sdk==1.20.0 \
  opentelemetry-exporter-prometheus==0.41b0 \
  opentelemetry-exporter-otlp==1.20.0 \
  prometheus-client==0.19.0 \
  deepeval>=1.0.0

# Set environment variables
export OTEL_EXPORTER_OTLP_ENDPOINT=localhost:4317
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export USE_OTEL_COLLECTOR=true
```

---

## Deployment: Quick Start

### 1. Start All Services

```bash
docker-compose up -d
```

### 2. Verify Services Running

```bash
# Check OTEL Collector
curl http://localhost:8888/metrics | head -20

# Check Prometheus
curl http://localhost:9090/api/v1/targets

# Access Grafana
open http://localhost:3000  # admin:admin
```

### 3. Configure Grafana

- Login to Grafana (http://localhost:3000)
- Data Source → Prometheus → http://prometheus:9090
- Create dashboard using queries above
- Set up alerts based on thresholds

### 4. Run Your Evaluations

```python
from claude_code_test_evaluator import ClaudeCodeTestEvaluator

evaluator = ClaudeCodeTestEvaluator()
result = evaluator.evaluate_solution(solution_code, test_suite)
# Metrics automatically exported to Prometheus
```

### 5. Monitor Dashboard

- Open Grafana dashboard
- Watch real-time metrics update every 5 seconds
- Alerts trigger when thresholds exceeded

---

## Multi-Backend Export (Advanced)

If you want metrics going to multiple destinations:

```yaml
# otel-collector-config.yaml (multi-backend)

exporters:
  prometheus:
    endpoint: "0.0.0.0:8888"
  
  datadog:
    api:
      key: ${DATADOG_API_KEY}
      site: datadoghq.com
  
  newrelic:
    apikey: ${NEW_RELIC_API_KEY}
  
  jaeger:
    endpoint: http://jaeger:14250

service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors: [batch, attributes]
      exporters: [prometheus, datadog, newrelic]  # All get metrics
```

---

## Summary

✅ **What's Captured**:
- Test pass/fail counts
- Execution time per test
- Code quality metrics
- Tool call counts
- Token usage
- Memory peak
- Error handling scores
- Efficiency scores

✅ **What's Visualized**:
- Real-time pass rate trends
- Code quality degradation alerts
- Performance regressions (execution time)
- Resource usage patterns
- Per-difficulty metrics comparison

✅ **What's Alerts**:
- Pass rate drops below threshold
- Execution time exceeds budget
- Code quality degrades
- Token usage spikes
- Custom thresholds based on SLOs

This setup gives you **production-grade observability** for your Claude Code agent evaluation pipeline!
