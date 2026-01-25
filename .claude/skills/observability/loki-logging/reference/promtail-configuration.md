# Promtail Configuration Reference

> Configuration reference for Grafana Promtail - the log collection agent for Loki.

---

## Table of Contents

1. [Overview](#overview)
2. [Pipeline Stages](#pipeline-stages)
3. [Scrape Configurations](#scrape-configurations)
4. [Label Extraction Patterns](#label-extraction-patterns)
5. [Multi-line Log Handling](#multi-line-log-handling)
6. [Pipeline Stage Ordering](#pipeline-stage-ordering)
7. [Rate Limiting](#rate-limiting)
8. [Best Practices](#best-practices)

---

## Overview

Promtail discovers targets, attaches labels, and pushes log entries to Loki. Configuration consists of:
- **server**: HTTP/gRPC settings
- **clients**: Loki endpoints
- **positions**: Track file read positions
- **scrape_configs**: Log sources and processing pipelines

---

## Pipeline Stages

### Parsing Stages

#### docker

```yaml
pipeline_stages:
  - docker: {}
```

Parses Docker JSON logging driver format.

#### cri

```yaml
pipeline_stages:
  - cri: {}
```

Parses Container Runtime Interface format (containerd/CRI-O).

#### json

```yaml
pipeline_stages:
  - json:
      expressions:
        level: level
        msg: message
        user_id: context.user.id  # Nested extraction
```

#### logfmt

```yaml
pipeline_stages:
  - logfmt:
      mapping:
        level:
        msg:
        ts:
```

#### regex

```yaml
pipeline_stages:
  - regex:
      expression: '^(?P<ip>\S+) \S+ (?P<user>\S+) \[(?P<timestamp>[^\]]+)\]'
```

### Transform Stages

#### multiline

```yaml
pipeline_stages:
  - multiline:
      firstline: '^\d{4}-\d{2}-\d{2}'
      max_wait_time: 3s
      max_lines: 128
```

#### pack

```yaml
pipeline_stages:
  - pack:
      labels:
        - request_id
        - trace_id
      ingest_timestamp: true
```

Embeds extracted labels into log line as JSON (reduces label cardinality).

#### template

```yaml
pipeline_stages:
  - template:
      source: level
      template: '{{ ToLower .Value }}'
```

### Action Stages

#### labels

```yaml
pipeline_stages:
  - labels:
      level:
      service:
```

Promotes extracted values to Loki labels.

#### labelallow / labeldrop

```yaml
pipeline_stages:
  - labelallow:
      - job
      - namespace
      - pod
  - labeldrop:
      - filename
```

#### timestamp

```yaml
pipeline_stages:
  - timestamp:
      source: ts
      format: RFC3339Nano
      fallback_formats:
        - RFC3339
        - UnixMs
```

Formats: `RFC3339`, `RFC3339Nano`, `Unix`, `UnixMs`, `UnixUs`, `UnixNs`

#### output

```yaml
pipeline_stages:
  - output:
      source: message
```

Sets final log line content.

### Filtering Stages

#### match

```yaml
pipeline_stages:
  - match:
      selector: '{job="nginx"}'
      stages:
        - regex:
            expression: '...'
  - match:
      selector: '{level="debug"}'
      action: drop
```

#### drop

```yaml
pipeline_stages:
  - drop:
      expression: '.*healthcheck.*'
      drop_counter_reason: healthcheck
```

---

## Scrape Configurations

### Kubernetes Pods

```yaml
scrape_configs:
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_promtail_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: pod
      - source_labels: [__meta_kubernetes_pod_uid, __meta_kubernetes_pod_container_name]
        target_label: __path__
        separator: /
        replacement: /var/log/pods/*$1/*.log
    pipeline_stages:
      - cri: {}
```

### Docker Logs

```yaml
scrape_configs:
  - job_name: docker
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
    relabel_configs:
      - source_labels: [__meta_docker_container_name]
        regex: '/(.*)'
        target_label: container
    pipeline_stages:
      - docker: {}
```

### File-Based

```yaml
scrape_configs:
  - job_name: system
    static_configs:
      - targets:
          - localhost
        labels:
          job: varlogs
          __path__: /var/log/*.log
```

### Journal

```yaml
scrape_configs:
  - job_name: journal
    journal:
      max_age: 12h
      labels:
        job: systemd-journal
    relabel_configs:
      - source_labels: [__journal__systemd_unit]
        target_label: unit
```

---

## Label Extraction Patterns

### From JSON Logs

```yaml
pipeline_stages:
  - json:
      expressions:
        level: level
        trace_id: trace_id
  - labels:
      level:        # Low cardinality - promote
  - pack:
      labels:
        - trace_id  # High cardinality - pack
```

### From Access Logs

```yaml
pipeline_stages:
  - regex:
      expression: '^(?P<ip>\S+).*"(?P<method>\w+).*" (?P<status>\d+)'
  - labels:
      method:
      status:
```

---

## Multi-line Log Handling

### Java Stack Traces

```yaml
pipeline_stages:
  - multiline:
      firstline: '^\d{4}-\d{2}-\d{2}[T ]?\d{2}:\d{2}:\d{2}'
      max_wait_time: 3s
      max_lines: 128
```

### Python Tracebacks

```yaml
pipeline_stages:
  - multiline:
      firstline: '^(Traceback|  File|\w+Error:)'
      max_wait_time: 3s
```

### Go Panic

```yaml
pipeline_stages:
  - multiline:
      firstline: '^(panic:|goroutine \d+)'
      max_wait_time: 3s
```

---

## Pipeline Stage Ordering

**Recommended order:**

```yaml
pipeline_stages:
  # 1. Container runtime parsing
  - cri: {}
  
  # 2. Multi-line aggregation
  - multiline:
      firstline: '...'
  
  # 3. Content parsing
  - json:
      expressions: {}
  
  # 4. Timestamp extraction
  - timestamp:
      source: ts
      format: RFC3339Nano
  
  # 5. Label manipulation
  - labels:
      level:
  - labeldrop:
      - filename
  
  # 6. Filtering
  - drop:
      expression: '.*healthcheck.*'
  
  # 7. Pack high-cardinality
  - pack:
      labels:
        - trace_id
  
  # 8. Output transformation
  - output:
      source: msg
```

---

## Rate Limiting

### Client Configuration

```yaml
clients:
  - url: http://loki:3100/loki/api/v1/push
    batchwait: 1s
    batchsize: 1048576  # 1MB
    rate_limit_config:
      enabled: true
      rate_bytes: 5242880  # 5MB/s
      burst_size_bytes: 10485760
    backoff_config:
      min_period: 500ms
      max_period: 5m
      max_retries: 10
```

### Limits

```yaml
limits_config:
  readline_rate: 100
  readline_burst: 1000
  readline_rate_enabled: true
  max_streams: 10000
```

---

## Best Practices

### 1. Label Cardinality Management

```yaml
# BAD: High cardinality labels
- labels:
    request_id:  # Unique per request

# GOOD: Pack high cardinality
- pack:
    labels:
      - request_id
```

### 2. Efficient Regex

```yaml
# BAD
- regex:
    expression: '.*(?P<error>error.*).*'

# GOOD
- regex:
    expression: '^(?P<timestamp>\d{4}-\d{2}-\d{2}T\S+) (?P<level>\w+) (?P<message>.+)$'
```

### 3. Drop Noise Early

```yaml
pipeline_stages:
  - drop:
      expression: '.*(healthz|readyz).*'
  # Then process remaining
  - regex: {}
```

### 4. Consistent Timestamp Handling

```yaml
pipeline_stages:
  - timestamp:
      source: ts
      format: RFC3339Nano
      fallback_formats:
        - RFC3339
      action_on_failure: fudge  # Use arrival time if fails
```

---

**Source**: Grafana Loki Documentation via Context7
