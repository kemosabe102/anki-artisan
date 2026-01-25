---
name: kubernetes-deployment
description: >
  Use this skill when deploying to Kubernetes, managing kubectl operations,
  troubleshooting K8s failures, or working with Kustomize overlays. Covers
  7-phase deployment pipeline, script orchestration, and event-driven diagnosis.
  Trigger keywords: k8s, kubernetes, kubectl, kustomize, deploy, pods, services,
  namespace, manifest, rollout, CrashLoopBackOff, ImagePullBackOff.
---

# Kubernetes Deployment Skill

*Script-driven Kubernetes orchestration with event-driven troubleshooting*

## Table of Contents

1. [Quick Reference](#quick-reference)
2. [7-Phase Deployment Pipeline](#7-phase-deployment-pipeline)
3. [Script Orchestration](#script-orchestration)
4. [Event-Driven Diagnosis](#event-driven-diagnosis)
5. [Service Discovery](#service-discovery)
6. [Anti-Patterns](#anti-patterns)
7. [Reference Documentation](#reference-documentation)

---

## Quick Reference

| Operation | Command/Script |
|-----------|----------------|
| Deploy stack | `AGENT_NAME=deployment-release bash scripts/deployment/deploy-local-k8s.sh` |
| Setup secrets | `AGENT_NAME=deployment-release bash scripts/deployment/setup-k8s-secrets.sh` |
| Validate manifests | `AGENT_NAME=deployment-release bash scripts/deployment/validate-k8s-manifests.sh` |
| Cleanup | `AGENT_NAME=deployment-release bash scripts/deployment/deploy-local-k8s.sh --cleanup` |
| Restart deployment | `AGENT_NAME=deployment-release kubectl rollout restart deployment/<name>` |
| Check pod status | `AGENT_NAME=deployment-release kubectl get pods -n <namespace>` |
| View events | `AGENT_NAME=deployment-release kubectl get events --sort-by=.lastTimestamp` |

---

## 7-Phase Deployment Pipeline

Execute phases sequentially for full deployments:

### Phase 1: Pre-Flight
Verify cluster connectivity and prerequisites.

```bash
AGENT_NAME=deployment-release kubectl config current-context
AGENT_NAME=deployment-release kubectl cluster-info
```

### Phase 2: Secrets Setup
Generate secrets from environment variables.

```bash
AGENT_NAME=deployment-release bash scripts/deployment/setup-k8s-secrets.sh
# Dry-run validation
AGENT_NAME=deployment-release bash scripts/deployment/setup-k8s-secrets.sh --dry-run
```

### Phase 3: Manifest Application
Apply Kustomize overlays via deployment script.

```bash
AGENT_NAME=deployment-release bash scripts/deployment/deploy-local-k8s.sh
```

**Note**: Direct `kubectl apply` is BLOCKED by security policy. Always use the script.

### Phase 4: Rollout Monitoring
Track deployment progress.

```bash
AGENT_NAME=deployment-release kubectl rollout status deployment/<name> -n <namespace>
```

### Phase 5: Health Checks
Verify pod readiness and liveness.

```bash
AGENT_NAME=deployment-release kubectl get pods -n <namespace>
AGENT_NAME=deployment-release kubectl describe pod <pod-name> -n <namespace>
```

### Phase 6: Observability Verification
Confirm observability stack is operational.

```bash
AGENT_NAME=deployment-release kubectl get pods -n gauntlet-agents -l app=otel-collector
AGENT_NAME=deployment-release kubectl get pods -n gauntlet-agents -l app=prometheus
```

### Phase 7: Validation Testing
Run deployment validation scripts.

```bash
AGENT_NAME=deployment-release bash scripts/deployment/deploy-local-k8s.sh --validate-only
```

---

## Script Orchestration

### Deployment Scripts Location
All scripts are in `scripts/deployment/`:

| Script | Purpose |
|--------|---------|
| `deploy-local-k8s.sh` | Main deployment pipeline |
| `setup-k8s-secrets.sh` | Secrets generation from .env |
| `validate-k8s-manifests.sh` | Manifest validation |

### Standard Deployment Flow

```bash
# 1. Setup secrets (if missing)
AGENT_NAME=deployment-release bash scripts/deployment/setup-k8s-secrets.sh

# 2. Deploy with validation
AGENT_NAME=deployment-release bash scripts/deployment/deploy-local-k8s.sh

# 3. Verify deployment
AGENT_NAME=deployment-release kubectl get pods -n gauntlet-agents
AGENT_NAME=deployment-release kubectl rollout status deployment/<name> -n gauntlet-agents
```

### Configuration Update Flow

```bash
# 1. Edit manifest (use Desktop Commander: mcp__desktop-commander__edit_block)

# 2. Validate change
AGENT_NAME=deployment-release bash scripts/deployment/validate-k8s-manifests.sh --mode=standard

# 3. Apply change
AGENT_NAME=deployment-release bash scripts/deployment/deploy-local-k8s.sh

# 4. Restart pods (if ConfigMap/Secret changed)
AGENT_NAME=deployment-release kubectl rollout restart deployment/<name> -n gauntlet-agents
```

### Validation Modes

| Mode | Duration | Use Case |
|------|----------|----------|
| `--mode=quick` | 2-3s | Quick syntax check |
| `--mode=standard` | 5-7s | Pre-deployment (default) |
| `--mode=full` | 7-10s | CI/CD pipeline |

---

## Event-Driven Diagnosis

**Core Principle**: Events first, Logs second, Describe third (minimize kubectl overhead)

### Diagnosis Workflow

```bash
# Step 1: Get Events (ALWAYS first)
AGENT_NAME=deployment-release kubectl get events --sort-by=.lastTimestamp -n <namespace>

# Step 2: Get Logs (if needed)
AGENT_NAME=deployment-release kubectl logs <pod-name> -n <namespace>
AGENT_NAME=deployment-release kubectl logs <pod-name> --previous -n <namespace>  # For crashed pods

# Step 3: Describe (if still unclear)
AGENT_NAME=deployment-release kubectl describe pod <pod-name> -n <namespace>
```

### Exit Code Reference

| Exit Code | Meaning | Common Causes | Remediation |
|-----------|---------|---------------|-------------|
| 0 | Success | Normal termination | No action needed |
| 1 | General error | App error, dependency unavailable | Check logs, delegate to debugger |
| 137 | OOMKilled | Exceeded memory limits | Increase memory limits |
| 143 | SIGTERM | Graceful shutdown | Normal during rollouts |
| 255 | Docker error | Image pull failed, entrypoint error | Check image, verify entrypoint |

### Common Failure Patterns

#### CrashLoopBackOff

**Detection**: Events show "BackOff" reason

**Investigation**:
```bash
AGENT_NAME=deployment-release kubectl get events --sort-by=.lastTimestamp | grep <pod-name>
AGENT_NAME=deployment-release kubectl logs <pod-name> --previous
```

**Root Causes**:
- Exit code 1: Application error (check logs)
- Exit code 137: OOMKilled (increase memory limits)
- Missing env vars: ConfigMap/Secret issue

#### ImagePullBackOff

**Detection**: Events show "Failed to pull image"

**Investigation**:
- Verify image tag in `image-versions.yaml`
- Check imagePullSecrets configuration
- Verify registry connectivity

#### Pending State

**Detection**: Pod status "Pending" for >30 seconds

**Investigation**:
```bash
AGENT_NAME=deployment-release kubectl describe pod <pod-name>
```

**Root Causes**:
- "Insufficient cpu/memory": Scale down or add resources
- "No nodes available": Check affinity rules
- "PVC not bound": Check StorageClass

### Error Classification

**Classify errors BEFORE retrying**:

| Category | Examples | Retry Strategy |
|----------|----------|----------------|
| PERMANENT | "field is immutable", "validation failed", "forbidden" | No retry, fix root cause |
| TRANSIENT | "connection refused", "timeout", HTTP 5xx | Exponential backoff (5s, 10s, 20s), max 3 |
| AMBIGUOUS | Generic errors, unexplained timeouts | Investigate first, then classify |

**Circuit Breaker**: 3 consecutive failures on same operation triggers circuit breaker. Stop retrying and escalate.

---

## Service Discovery

Default NodePorts for local development stack. Verify with `kubectl get svc -n gauntlet-agents`.

| Service | NodePort | URL |
|---------|----------|-----|
| Prometheus | 30090 | `http://localhost:30090` |
| Grafana | 30030 | `http://localhost:30030` |
| Jaeger UI | 31686 | `http://localhost:31686` |
| Loki HTTP | 30100 | `http://localhost:30100` |
| OTel Collector gRPC | 30317 | `http://localhost:30317` |
| OTel Collector HTTP | 30318 | `http://localhost:30318` |

**CRITICAL**: Always use NodePort URLs. NEVER use `kubectl port-forward`.

---

## Anti-Patterns

### NEVER DO

| Anti-Pattern | Why | Correct Approach |
|--------------|-----|------------------|
| Raw `kubectl apply` | Blocked by security policy | Use `bash scripts/deployment/deploy-local-k8s.sh` |
| Raw `kubectl delete` | Blocked by security policy | Use `bash scripts/deployment/deploy-local-k8s.sh --cleanup` |
| `kubectl port-forward` | Ephemeral, no audit trail | Configure NodePort in manifests |
| `kubectl exec` | Security risk | Use `kubectl logs` for debugging |
| `kubectl edit` | Not Git-tracked | Edit manifest file, then apply via script |
| Retry without classifying error | Wastes resources, loops | Classify as PERMANENT/TRANSIENT/AMBIGUOUS first |
| Skip validation before apply | Risk of bad deployments | Always run `validate-k8s-manifests.sh` first |
| Use `latest` image tag | Breaks reproducibility | Use explicit tags (v1.2.3, commit SHA) |

### ALWAYS DO

- Prefix all bash commands with `AGENT_NAME=deployment-release`
- Use Desktop Commander (`mcp__desktop-commander__edit_block`) for manifest edits
- Classify errors before retry attempts
- Document service endpoints with NodePort URLs
- Run validation before deployment

---

## Reference Documentation

Detailed guides for specific topics:

| Topic | Reference File |
|-------|----------------|
| Domain expertise | [reference/domain-expertise.md](reference/domain-expertise.md) |
| Thinking frameworks | [reference/frameworks.md](reference/frameworks.md) |
| Kustomize workflows | [reference/kustomize-integration.md](reference/kustomize-integration.md) |
| Failure patterns | [reference/failure-patterns.md](reference/failure-patterns.md) |
| kubectl commands | [reference/kubectl-operations.md](reference/kubectl-operations.md) |
| Troubleshooting | [reference/troubleshooting-workflows.md](reference/troubleshooting-workflows.md) |
| Manifest editing | [reference/manifest-editing-protocol.md](reference/manifest-editing-protocol.md) |
| Observability stack | [reference/observability-stack-validation.md](reference/observability-stack-validation.md) |

### Kustomize Structure

```
k8s/
├── base/           # Environment-agnostic resources
├── local/          # Local development overlay
├── staging/        # Staging overlay
└── production/     # Production overlay
```

**Workflow**: Base -> Overlays -> Patches -> Transformers

### Resource Ordering (Critical)

Apply resources in dependency order:
1. Namespace (first)
2. ConfigMap, Secret
3. PersistentVolumeClaim
4. Service
5. Deployment, StatefulSet
6. NetworkPolicy (last)

### Rollback Strategy

**Fix-forward preferred** (maintains Git history):
1. Identify root cause
2. Fix manifest
3. Validate change
4. Apply corrected manifest
5. Git commit with fix

**Emergency rollback**:
```bash
# View rollout history
AGENT_NAME=deployment-release kubectl rollout history deployment/<name> -n <namespace>

# Rollback to previous
AGENT_NAME=deployment-release kubectl rollout undo deployment/<name> -n <namespace>

# Rollback to specific revision
AGENT_NAME=deployment-release kubectl rollout undo deployment/<name> --to-revision=<N> -n <namespace>
```

---

## Thinking Frameworks

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

| Framework | When to Use |
|-----------|-------------|
| OODA | All K8s operations (Observe->Orient->Decide->Act) |
| ReACT | Debugging deployment failures |
| Pre-Mortem | Risk assessment before production deploys |

**Context Quality Gate**: CQ >= 0.85 required before proceeding. If CQ < 0.85, research via local docs or Context7 first.
