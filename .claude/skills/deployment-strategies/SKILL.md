---
name: deployment-strategies
description: >
  Use this skill when selecting or implementing Kubernetes deployment strategies
  including rolling updates, canary deployments, blue-green deployments, and
  rollback procedures. Helps decide which strategy fits the use case.
  Trigger keywords: canary, blue-green, rolling update, deployment strategy,
  rollback, maxSurge, maxUnavailable, traffic splitting.
---

# Kubernetes Deployment Strategies

*Strategy selection, configuration, and rollback procedures for zero-downtime deployments*

## Table of Contents

1. [Strategy Selection Matrix](#strategy-selection-matrix)
2. [Rolling Update Configuration](#rolling-update-configuration)
3. [Canary Deployment Pattern](#canary-deployment-pattern)
4. [Blue-Green Deployment Pattern](#blue-green-deployment-pattern)
5. [Rollback Procedures](#rollback-procedures)
6. [Anti-Patterns](#anti-patterns)

---

## Strategy Selection Matrix

| Strategy | Best For | Risk Level | Rollback Speed | Resource Overhead |
|----------|----------|------------|----------------|-------------------|
| Rolling Update | Standard releases, gradual rollout | Low | Medium (undo) | Low (surge only) |
| Canary | High-risk changes, new features | Low-Medium | Fast (scale down) | Medium (parallel pods) |
| Blue-Green | Critical services, instant switchover | Medium | Instant (selector) | High (2x resources) |

### Decision Flow

```
Is instant rollback critical?
├── YES → Blue-Green
└── NO → Need gradual validation?
    ├── YES → Canary (percentage-based)
    └── NO → Rolling Update (default)
```

---

## Rolling Update Configuration

Default Kubernetes strategy for zero-downtime deployments.

### Basic Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Max pods above desired count
      maxUnavailable: 0  # Always maintain capacity
```

### Parameter Guide

| Parameter | Conservative | Balanced | Aggressive |
|-----------|--------------|----------|------------|
| maxSurge | 1 | 25% | 50% |
| maxUnavailable | 0 | 25% | 50% |

**Conservative**: Zero downtime risk, slower rollout
**Balanced**: Good for most workloads
**Aggressive**: Fast rollout, tolerates brief capacity reduction

### Rollout Monitoring

```bash
# Watch rollout progress
kubectl rollout status deployment/my-app -n <namespace>

# Check rollout history
kubectl rollout history deployment/my-app -n <namespace>
```

---

## Canary Deployment Pattern

Progressive rollout with traffic splitting for risk mitigation.

### Implementation Approach

Deploy canary as separate deployment, split traffic via Service or Ingress.

### Canary Deployment Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-canary
  labels:
    app: my-app
    track: canary
spec:
  replicas: 1  # Start small
  selector:
    matchLabels:
      app: my-app
      track: canary
  template:
    metadata:
      labels:
        app: my-app
        track: canary
    spec:
      containers:
      - name: my-app
        image: my-app:v2.0.0  # New version
```

### Progressive Rollout Stages

| Stage | Canary % | Duration | Validation |
|-------|----------|----------|------------|
| 1 | 10% | 15 min | Error rate, latency p99 |
| 2 | 50% | 30 min | Error rate, latency p99, resource usage |
| 3 | 100% | - | Promote canary, delete stable |

### Key Metrics to Watch

- Error rate: Should not exceed baseline + 0.1%
- Latency p99: Should not exceed baseline + 10%
- Pod restarts: Should be zero
- Memory/CPU: Should match stable version

### Rollback (Canary)

```bash
# Scale down canary immediately
kubectl scale deployment/my-app-canary --replicas=0 -n <namespace>

# Delete canary deployment
kubectl delete deployment/my-app-canary -n <namespace>
```

---

## Blue-Green Deployment Pattern

Dual environment setup for instant switchover and rollback.

### Implementation Approach

Maintain two identical environments (blue/green). Switch traffic via Service selector.

### Blue Environment (Current Production)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: blue
  template:
    metadata:
      labels:
        app: my-app
        version: blue
    spec:
      containers:
      - name: my-app
        image: my-app:v1.0.0
```

### Service Selector (Traffic Control)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app
spec:
  selector:
    app: my-app
    version: blue  # Change to "green" to switch traffic
  ports:
  - port: 80
    targetPort: 8080
```

### Switchover Procedure

```bash
# 1. Deploy green environment with new version
kubectl apply -f my-app-green.yaml -n <namespace>

# 2. Wait for green to be ready
kubectl rollout status deployment/my-app-green -n <namespace>

# 3. Switch traffic (patch service selector)
kubectl patch service my-app -p '{"spec":{"selector":{"version":"green"}}}' -n <namespace>

# 4. Verify traffic routing
kubectl get endpoints my-app -n <namespace>
```

### Rollback (Blue-Green)

```bash
# Instant rollback: switch selector back
kubectl patch service my-app -p '{"spec":{"selector":{"version":"blue"}}}' -n <namespace>
```

---

## Rollback Procedures

### Rolling Update Rollback

```bash
# View rollout history
kubectl rollout history deployment/my-app -n <namespace>

# Rollback to previous revision
kubectl rollout undo deployment/my-app -n <namespace>

# Rollback to specific revision
kubectl rollout undo deployment/my-app --to-revision=2 -n <namespace>

# Check rollback status
kubectl rollout status deployment/my-app -n <namespace>
```

### Rollback Decision Matrix

| Symptom | Action | Command |
|---------|--------|---------|
| Error rate spike | Immediate rollback | `kubectl rollout undo` |
| Latency degradation | Investigate, then rollback | Check logs first |
| OOMKilled pods | Rollback + adjust limits | `kubectl rollout undo` |
| Partial failure | Scale down, investigate | `kubectl scale --replicas=0` |

---

## Anti-Patterns

### Configuration Anti-Patterns

| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| `maxUnavailable: 100%` | Full downtime during rollout | Use `maxUnavailable: 0` or `25%` |
| No readiness probe | Traffic to unready pods | Always define readinessProbe |
| No liveness probe | Stuck pods not restarted | Define livenessProbe with appropriate delay |
| `initialDelaySeconds: 0` | Premature health checks | Set based on app startup time |
| No resource limits | OOMKilled, CPU throttling | Set requests and limits |
| `imagePullPolicy: Always` | Slow rollouts, registry dependency | Use specific tags + `IfNotPresent` |

### Process Anti-Patterns

| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Skip canary validation | Issues reach 100% traffic | Wait full validation period |
| No rollback plan | Panic during incidents | Document rollback before deploy |
| Manual selector edits | Error-prone switchover | Script or automate switchover |
| No metrics monitoring | Blind deployment | Watch error rate, latency during rollout |

### Health Check Requirements

```yaml
spec:
  containers:
  - name: my-app
    readinessProbe:
      httpGet:
        path: /health/ready
        port: 8080
      initialDelaySeconds: 10
      periodSeconds: 5
    livenessProbe:
      httpGet:
        path: /health/live
        port: 8080
      initialDelaySeconds: 30
      periodSeconds: 10
```

**Critical**: Never deploy without readiness probes. Rolling updates depend on probe status.
