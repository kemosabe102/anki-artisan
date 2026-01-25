---
name: prometheus-monitoring
description: >
  Use this skill when configuring Prometheus scrape targets, creating ServiceMonitors,
  managing metric pipelines, or optimizing collection. Covers scrape configs,
  relabeling, metric discovery, and pipeline architecture.
  Keywords: prometheus, servicemonitor, scrape, relabel, metrics, collection.
---

# Prometheus Monitoring Skill

*Configure scrape targets, ServiceMonitors, and metric pipelines for Prometheus*

## Reference Documentation

**Detailed Guides** (read when relevant):
- **ServiceMonitor Patterns** → [reference/servicemonitor-patterns.md](reference/servicemonitor-patterns.md)
- **Relabeling Cookbook** → [reference/relabeling-cookbook.md](reference/relabeling-cookbook.md)

## Quick Reference

| Task | Section |
|------|---------|
| Create ServiceMonitor for a service | [ServiceMonitor Configuration](#servicemonitor-configuration) |
| Add static scrape target | [Scrape Configuration](#scrape-configuration-patterns) |
| Transform or filter labels | [Relabeling Rules](#relabeling-rules) |
| Discover endpoints automatically | [Metric Discovery](#metric-discovery) |
| Optimize scrape performance | [Performance Tuning](#performance-tuning) |

---

## ServiceMonitor Configuration

ServiceMonitor is a Prometheus Operator CRD that auto-configures scrape targets from Kubernetes services.

### Basic ServiceMonitor

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: my-service-monitor
  namespace: observability
  labels:
    release: prometheus  # Must match Prometheus operator selector
spec:
  selector:
    matchLabels:
      app: my-service     # Selects services with this label
  namespaceSelector:
    matchNames:
      - my-namespace      # Watch services in these namespaces
  endpoints:
    - port: metrics       # Named port from Service spec
      interval: 30s       # Scrape interval (default: 30s)
      path: /metrics      # Metrics endpoint path
      scheme: http        # http or https
```

### Key CRD Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `selector.matchLabels` | Select target Services | `app: api-server` |
| `namespaceSelector.matchNames` | Limit to specific namespaces | `[prod, staging]` |
| `namespaceSelector.any: true` | Watch all namespaces | - |
| `endpoints[].port` | Service port name (not number) | `metrics`, `http` |
| `endpoints[].interval` | Scrape frequency | `15s`, `30s`, `60s` |
| `endpoints[].scrapeTimeout` | Max scrape duration | `10s` (must be < interval) |
| `endpoints[].honorLabels` | Prefer target labels over job labels | `true` |

### ServiceMonitor with TLS

```yaml
endpoints:
  - port: https-metrics
    scheme: https
    tlsConfig:
      insecureSkipVerify: false
      caFile: /etc/prometheus/certs/ca.crt
      certFile: /etc/prometheus/certs/tls.crt
      keyFile: /etc/prometheus/certs/tls.key
```

---

## Scrape Configuration Patterns

For non-operator deployments or static targets, configure scrapes in `prometheus.yml`.

### Static Targets

```yaml
scrape_configs:
  - job_name: 'otel-collector'
    static_configs:
      - targets: ['otel-collector-service:8889']
    scrape_interval: 30s
    metrics_path: /metrics

  - job_name: 'windows-exporter'
    static_configs:
      - targets: ['host.docker.internal:9182']
    scrape_interval: 30s
```

### Kubernetes Service Discovery

```yaml
scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      # Only scrape pods with prometheus.io/scrape annotation
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      # Use custom port from annotation
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        target_label: __address__
        regex: (.+)
        replacement: $1
```

### Common Job Patterns

| Job Type | Typical Interval | Path |
|----------|------------------|------|
| Application metrics | 15-30s | `/metrics` |
| Infrastructure (node_exporter) | 30-60s | `/metrics` |
| Database exporters | 30-60s | `/metrics` |
| Health monitoring | 10-15s | `/health` or `/ready` |

---

## Relabeling Rules

Transform labels before ingestion to reduce cardinality or enrich data.

### Common Relabeling Actions

| Action | Purpose | Example Use |
|--------|---------|-------------|
| `keep` | Only scrape matching targets | Filter by annotation |
| `drop` | Exclude matching targets | Skip test namespaces |
| `replace` | Transform label values | Extract service from pod name |
| `labelmap` | Copy matched labels | Preserve Kubernetes labels |
| `labeldrop` | Remove labels | Drop high-cardinality labels |
| `hashmod` | Shard targets | Distribute across Prometheus replicas |

### Practical Examples

```yaml
relabel_configs:
  # Keep only pods with scrape annotation
  - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
    action: keep
    regex: "true"

  # Add namespace label
  - source_labels: [__meta_kubernetes_namespace]
    target_label: namespace

  # Extract service name from pod
  - source_labels: [__meta_kubernetes_pod_name]
    target_label: pod
    regex: '(.+)-[a-z0-9]+-[a-z0-9]+'
    replacement: '$1'

metric_relabel_configs:
  # Drop high-cardinality metrics
  - source_labels: [__name__]
    regex: 'go_gc_.*'
    action: drop

  # Remove user_id label (unbounded cardinality)
  - regex: 'user_id'
    action: labeldrop

  # Keep only our namespaces
  - source_labels: [namespace]
    action: keep
    regex: '(gauntlet-agents|observability|data)'
```

### Label Normalization

```yaml
relabel_configs:
  # Normalize environment values
  - source_labels: [environment]
    regex: 'production|prod'
    target_label: environment
    replacement: 'prod'
```

---

## Metric Discovery

### API Endpoints for Discovery

| Endpoint | Purpose |
|----------|---------|
| `/api/v1/targets` | List all scrape targets and health |
| `/api/v1/targets/metadata` | Metric metadata from targets |
| `/api/v1/metadata` | All metric metadata |
| `/api/v1/status/config` | Current Prometheus configuration |
| `/api/v1/status/tsdb` | TSDB stats (cardinality, series count) |

### Discovery Commands

```bash
# List all targets
curl http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, health: .health}'

# Check target metadata
curl http://localhost:9090/api/v1/targets/metadata?match_target={job="my-service"}

# Get metric names for a job
curl http://localhost:9090/api/v1/label/__name__/values?match[]={job="my-service"}
```

---

## Pipeline Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌─────────────┐     ┌─────────────┐
│ Application │────▶│ OTel Collector  │────▶│ Prometheus  │────▶│  Grafana    │
│  /metrics   │     │  (optional)     │     │  TSDB       │     │  Dashboard  │
└─────────────┘     └─────────────────┘     └─────────────┘     └─────────────┘
      │                    │                       │
      │              ┌─────▼─────┐          ┌──────▼──────┐
      │              │ Transform │          │ Alert Rules │
      │              │ Relabel   │          │ Recording   │
      │              └───────────┘          └─────────────┘
      │
      └──────────────────────────────────────────────┘
               Direct scrape (alternative path)
```

### Collection Patterns

| Pattern | When to Use |
|---------|-------------|
| Direct Scrape | Single Prometheus, simple deployments |
| OTel Collector | Multi-backend, protocol translation |
| Remote Write | Long-term storage (Thanos, Cortex) |
| Federation | Cross-cluster aggregation |

---

## Performance Tuning

### Scrape Interval Guidelines

| Metric Type | Recommended Interval |
|-------------|---------------------|
| Business metrics | 15s |
| Infrastructure | 30s |
| Slow-changing (disk) | 60s |
| Health checks | 10s |

### Sample Limits

```yaml
scrape_configs:
  - job_name: 'high-volume-app'
    sample_limit: 10000        # Max samples per scrape
    body_size_limit: 50MB      # Max response size
    scrape_timeout: 10s        # Must be < interval
```

### Cardinality Control

```yaml
# Alert on high cardinality
- alert: HighMetricCardinality
  expr: count by(__name__) ({__name__=~".+"}) > 10000
  labels:
    severity: warning
```

**Cardinality Best Practices**:
- Drop unbounded labels (user_id, request_id, pod names)
- Use recording rules to pre-aggregate
- Monitor `prometheus_tsdb_head_series` for growth

---

## Integration Points

### Alertmanager Integration

```yaml
# In prometheus.yml
alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']
```

### Dashboard Integration

```yaml
# Grafana datasource
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus-service:9090
    access: proxy
```

### Recording Rules for Dashboards

```yaml
groups:
  - name: service_metrics
    interval: 30s
    rules:
      - record: service:http_requests:rate5m
        expr: sum(rate(http_requests_total[5m])) by (service)
      - record: service:http_error_ratio:rate5m
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
          /
          sum(rate(http_requests_total[5m])) by (service)
```

---

## Validation Checklist

Before deploying scrape configuration:

- [ ] Target endpoints respond with valid Prometheus format
- [ ] ServiceMonitor selector matches target Service labels
- [ ] Scrape interval appropriate for metric type
- [ ] High-cardinality labels dropped via relabeling
- [ ] Sample limits configured for high-volume targets
- [ ] TSDB disk space sufficient for retention period

**Test scrape from Prometheus pod**:
```bash
kubectl exec -it prometheus-pod -- wget -O- http://target:port/metrics
```

---

## Project References

- Prometheus deployment: `k8s/local/observability/prometheus/prometheus.yaml`
- OTel Collector config: `k8s/local/observability/otel-collector/otel-collector.yaml`
- Troubleshooting guide: `docs/04-guides/observability/prometheus-troubleshooting.md`
