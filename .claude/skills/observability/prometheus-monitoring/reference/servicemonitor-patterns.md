# ServiceMonitor Patterns Reference

> Prometheus Operator ServiceMonitor configuration patterns and best practices.

---

## Table of Contents

1. [Overview](#overview)
2. [CRD Structure](#crd-structure)
3. [Label Selector Patterns](#label-selector-patterns)
4. [Endpoint Configuration](#endpoint-configuration)
5. [Namespace Selector Patterns](#namespace-selector-patterns)
6. [TLS and Authentication](#tls-and-authentication)
7. [Relabeling Configuration](#relabeling-configuration)
8. [Common Patterns](#common-patterns)
9. [Best Practices](#best-practices)
10. [Common Pitfalls](#common-pitfalls)

---

## Overview

ServiceMonitor is a CRD from Prometheus Operator that declaratively specifies how Kubernetes services should be monitored. Key principle: **ServiceMonitors select Services (not Pods directly)**. The Service's Endpoints are then scraped.

---

## CRD Structure

### Minimal ServiceMonitor

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: example-app
  namespace: monitoring
  labels:
    release: prometheus  # Must match Prometheus serviceMonitorSelector
spec:
  selector:
    matchLabels:
      app: example-app
  endpoints:
    - port: metrics
```

### Complete Structure

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: example-app
  namespace: monitoring
  labels:
    release: prometheus
spec:
  selector:
    matchLabels:
      app: example-app
    matchExpressions:
      - key: environment
        operator: In
        values: [production, staging]
  namespaceSelector:
    matchNames:
      - default
      - production
  endpoints:
    - port: metrics
      path: /metrics
      interval: 30s
      scrapeTimeout: 10s
      scheme: https
      tlsConfig:
        insecureSkipVerify: false
      relabelings: []
      metricRelabelings: []
  targetLabels:
    - environment
  podTargetLabels:
    - pod-template-hash
  sampleLimit: 10000
  labelLimit: 100
```

---

## Label Selector Patterns

### matchLabels (Equality)

```yaml
spec:
  selector:
    matchLabels:
      app: my-application
      component: api
```

### matchExpressions (Set-Based)

```yaml
spec:
  selector:
    matchExpressions:
      - key: app
        operator: In
        values: [frontend, backend, api]
      - key: monitoring
        operator: Exists
      - key: deprecated
        operator: DoesNotExist
```

| Operator | Description |
|----------|-------------|
| `In` | Value in specified set |
| `NotIn` | Value not in set |
| `Exists` | Key exists |
| `DoesNotExist` | Key does not exist |

---

## Endpoint Configuration

```yaml
endpoints:
  - port: metrics        # Named port from Service spec
    path: /metrics       # Default: /metrics
    interval: 30s        # Scrape interval
    scrapeTimeout: 10s   # Must be <= interval
    scheme: https        # http or https
    honorTimestamps: true
```

### Port Specification

```yaml
endpoints:
  # By port name (recommended)
  - port: metrics
  
  # By port number
  - targetPort: 9090
```

**Important**: `port` refers to the Service port name, not container port.

---

## Namespace Selector Patterns

### Same Namespace (Default)

```yaml
# Omit namespaceSelector - same namespace as ServiceMonitor
```

### Specific Namespaces

```yaml
spec:
  namespaceSelector:
    matchNames:
      - production
      - staging
```

### All Namespaces

```yaml
spec:
  namespaceSelector:
    any: true
```

**Warning**: `any: true` can cause high cardinality. Use with label selectors.

---

## TLS and Authentication

### TLS Configuration

```yaml
endpoints:
  - port: metrics
    scheme: https
    tlsConfig:
      insecureSkipVerify: false
      ca:
        secret:
          name: prometheus-tls
          key: ca.crt
      cert:
        secret:
          name: prometheus-tls
          key: tls.crt
      keySecret:
        name: prometheus-tls
        key: tls.key
```

### Bearer Token

```yaml
endpoints:
  - port: metrics
    bearerTokenFile: /var/run/secrets/kubernetes.io/serviceaccount/token
```

### Basic Auth

```yaml
endpoints:
  - port: metrics
    basicAuth:
      username:
        name: basic-auth-secret
        key: username
      password:
        name: basic-auth-secret
        key: password
```

---

## Relabeling Configuration

### relabelings (Before Scrape)

```yaml
endpoints:
  - port: metrics
    relabelings:
      - sourceLabels: [__meta_kubernetes_namespace]
        targetLabel: namespace
      - sourceLabels: [__meta_kubernetes_pod_name]
        targetLabel: pod
      - sourceLabels: [__meta_kubernetes_pod_label_app]
        targetLabel: app
      - sourceLabels: [__meta_kubernetes_pod_label_skip_monitoring]
        regex: "true"
        action: drop
```

### metricRelabelings (After Scrape)

```yaml
endpoints:
  - port: metrics
    metricRelabelings:
      - sourceLabels: [__name__]
        regex: 'go_.*|process_.*'
        action: drop
      - regex: 'request_id'
        action: labeldrop
```

---

## Common Patterns

### Standard Web Application

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: web-app
  labels:
    release: prometheus
spec:
  selector:
    matchLabels:
      app: web-app
  endpoints:
    - port: http
      path: /metrics
      interval: 30s
```

### Spring Boot Actuator

```yaml
spec:
  endpoints:
    - port: http
      path: /actuator/prometheus
      interval: 30s
```

### Database Exporter

```yaml
spec:
  endpoints:
    - port: metrics
      interval: 60s        # Longer interval for DB
      scrapeTimeout: 30s
```

---

## Best Practices

### 1. Label Consistency

```yaml
metadata:
  labels:
    release: prometheus    # Match Prometheus serviceMonitorSelector
    team: platform
```

### 2. Resource Limits

```yaml
spec:
  sampleLimit: 10000
  targetLimit: 100
  labelLimit: 50
```

### 3. Scrape Interval Guidelines

| Workload Type | Interval |
|---------------|----------|
| High-frequency | 15s |
| Standard apps | 30s |
| Database exporters | 60s |
| Batch jobs | 5m |

### 4. Use Named Ports

```yaml
# Service
spec:
  ports:
    - name: metrics
      port: 9090

# ServiceMonitor
endpoints:
  - port: metrics
```

---

## Common Pitfalls

### ServiceMonitor Not Picked Up

**Cause**: Labels don't match Prometheus `serviceMonitorSelector`.

```yaml
# Check Prometheus CR
spec:
  serviceMonitorSelector:
    matchLabels:
      release: prometheus  # ServiceMonitor must have this
```

### No Targets Found

**Causes**:
- Service labels don't match selector
- Service in different namespace
- Port name mismatch

### Scrape Timeout Errors

**Rule**: `scrapeTimeout < interval`

### High Cardinality

**Solution**:
```yaml
spec:
  sampleLimit: 10000
  endpoints:
    - metricRelabelings:
        - sourceLabels: [__name__]
          regex: 'expensive_.*'
          action: drop
```

---

**Source**: Prometheus Operator Documentation via Context7
