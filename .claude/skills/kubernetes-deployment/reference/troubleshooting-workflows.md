# Kubernetes Troubleshooting Workflows

**Purpose**: Error handling, retry strategies, and observability stack validation workflows

**Audience**: deployment-release agent (reference during error recovery and validation operations)

---

## Error Classification Framework

**Reference**: `.claude/docs/guides/error-classification-framework.md`

### MANDATORY Rule

**Classify errors BEFORE retrying** any kubectl operation or script execution.

### Error Categories

#### PERMANENT Errors (immediate FAILURE, 0 retries)

**Immutability violations**:
```
Error: "field is immutable"
Error: "cannot be updated"
```

**Examples**:
- Deployment selector changes
- Service ClusterIP changes
- PVC storage size decreases

**Resolution**:
- Delete and recreate resource OR
- `kubectl rollout restart` (for ConfigMap/Secret changes)

**Schema validation**:
```
Error: "invalid field"
Error: "unknown field"
Error: "validation failed"
```

**Examples**:
- Typos in manifest
- Unsupported API fields
- Malformed YAML

**Resolution**:
- Fix manifest syntax or field names

**RBAC permission denials**:
```
Error: "forbidden"
Error: "unauthorized"
```

**Resolution**:
- Check service account permissions
- Update RBAC rules

**Resource not found (non-transient)**:
```
Error: "namespace not found"
Error: "resource does not exist"
```

**Resolution**:
- Create missing namespace or resource

#### TRANSIENT Errors (retry with exponential backoff, max 3 attempts)

**Network errors**:
```
Error: "connection refused"
Error: "timeout"
Error: "EOF"
Error: "TLS handshake timeout"
```

**Retry pattern**: 5s, 10s, 20s backoff

**API server errors**:
```
HTTP 5xx
Error: "service unavailable"
Error: "too many requests"
```

**Retry pattern**: 5s, 10s, 20s backoff with jitter

**Resource quotas (may free up)**:
```
Error: "insufficient CPU"
Error: "insufficient memory"
Error: "quota exceeded"
```

**Retry pattern**: 10s, 20s, 40s backoff (allow time for quota to free)

**Image pull backoff (transient)**:
```
Error: "back-off pulling image"
```

**Retry pattern**:
- Run `kubectl describe pod` for root cause
- Retry if network-related error

#### AMBIGUOUS Errors (investigate, then classify)

**Generic errors** → Run `kubectl get events` + `kubectl describe`

**Timeout with no error message** → Check `kubectl rollout status`

**Pod eviction** → Check `kubectl describe node` for resource pressure

---

## Circuit Breaker Pattern

**Reference**: `.claude/docs/guides/circuit-breaker-pattern.md`

### Circuit Breaker Rule

Track `(operation_name, resource_name, error_pattern)` tuple:

**Failure threshold**: 3 consecutive failures on same tuple → Circuit breaker trips

**Behavior when tripped**:
- **STOP** retrying immediately
- Return **FAILURE** with:
  - Loop detection evidence
  - Recommended action

**Example** (immutability error):
```
Attempt 1: kubectl apply → "field is immutable"
→ Classify as PERMANENT
→ FAILURE immediately (0 retries)
→ Circuit breaker: NOT triggered (stopped after first attempt)
```

**Example** (transient network error):
```
Attempt 1: kubectl apply → "connection refused" (transient)
Attempt 2: kubectl apply → "connection refused" (transient)
Attempt 3: kubectl apply → "connection refused" (transient)
→ Circuit breaker TRIPS
→ FAILURE with evidence: "kubectl apply failed 3 times with 'connection refused'"
→ Recommended action: "Check cluster connectivity, verify API server health"
```

---

## Retry Strategy

**Reference**: `.claude/docs/guides/retry-strategies.md`

### Retry Configuration

#### kubectl Operations
- **Max retries**: 3
- **Backoff**: Exponential (5s, 10s, 20s)
- **Jitter**: Full jitter (randomize backoff)

#### Script Execution
- **Max retries**: 2 (scripts are idempotent)
- **Backoff**: Linear (10s, 20s)

#### Rollout Monitoring
- **Max retries**: 5
- **Backoff**: Linear (10s intervals)

### Retry Budget

**Per-request**: 3 attempts maximum (includes initial attempt)

**Per-deployment session**: 10 kubectl operations max (prevent runaway retry amplification)

### Integration with Error Classification

**Workflow**:
1. kubectl operation fails
2. Classify error using error-classification-framework.md
3. If PERMANENT → FAILURE (0 retries)
4. If TRANSIENT → Retry with exponential backoff (max 3)
5. If 3 consecutive failures on same operation → Circuit breaker trips → FAILURE

---

## Manifest Validation Workflow

**Script**: `scripts/deployment/validate-k8s-manifests.sh`

### Validation Modes

| Mode | Checks | Duration | Use Case |
|------|--------|----------|----------|
| `--mode=quick` | Client-side syntax only | 2-3s | Quick check before editing |
| `--mode=standard` | Client + server schema | 5-7s | Pre-deployment validation (default) |
| `--mode=full` | Client + server + kustomize build | 7-10s | CI/CD pipeline validation |

### Mode Selection Decision Tree

**Scenario** → **Mode**:
- Quick syntax check before editing → `--mode=quick`
- Pre-deployment validation → `--mode=standard`
- CI/CD pipeline validation → `--mode=full`
- Post-edit verification → `--mode=standard --verbose`
- Show deployment diff → `--mode=standard --diff`

### Command Examples

```bash
# Quick syntax check (2-3 seconds)
AGENT_NAME=deployment-release bash scripts/deployment/validate-k8s-manifests.sh \
  --mode=quick gauntlet-agents k8s/local

# Standard validation with verbose output (5-7 seconds)
AGENT_NAME=deployment-release bash scripts/deployment/validate-k8s-manifests.sh \
  --mode=standard --verbose gauntlet-agents k8s/local

# Full validation with diff preview (7-10 seconds)
AGENT_NAME=deployment-release bash scripts/deployment/validate-k8s-manifests.sh \
  --mode=full --diff gauntlet-agents k8s/local
```

### Exit Codes

| Exit Code | Meaning | Resolution |
|-----------|---------|------------|
| 0 | All validations passed | Proceed to deployment |
| 1 | Client-side validation failed | Fix YAML syntax and retry |
| 2 | Server-side validation failed | Fix schema errors or immutable field changes (may require delete+recreate) |
| 3 | Kustomize build failed | Fix kustomization.yaml errors |
| 4 | Prerequisites missing | Install kubectl or check cluster connectivity |

---

## Observability Stack Validation

For comprehensive observability troubleshooting (Prometheus, Grafana, Jaeger, OTEL, Loki), see:
**Reference**: `observability-stack-validation.md`

**Quick Checks**:
- OTEL Collector: `kubectl get pods -n gauntlet-agents -l app=otel-collector`
- Jaeger: `kubectl get pods -n gauntlet-agents -l app=jaeger`
- Prometheus: `kubectl get pods -n gauntlet-agents -l app=prometheus`
- Grafana: `kubectl get pods -n gauntlet-agents -l app=grafana`

**Domain Boundary**: deployment-release handles infrastructure deployment; delegate application instrumentation to development.

---

## ConfigMap/Secret Update Workflow

### Immutability Enforcement

**Strategy**: Secrets are immutable by default (best practice)

**Why**:
- Prevents race conditions
- Ensures atomic updates
- Forces pod restarts (guarantees new config loaded)

### Update Process

#### 1. Read Current Manifest

```bash
AGENT_NAME=deployment-release kubectl get configmap <name> -o yaml > configmap-current.yaml
```

#### 2. Edit Manifest

Use Desktop Commander (`mcp__desktop-commander__edit_block`) for all manifest edits.

#### 3. Validate Change

```bash
AGENT_NAME=deployment-release bash scripts/deployment/validate-k8s-manifests.sh \
  --mode=standard gauntlet-agents k8s/local
```

#### 4. Apply Change

```bash
AGENT_NAME=deployment-release bash scripts/deployment/deploy-local-k8s.sh
```

**Note**: Script uses `kubectl apply -k` internally

#### 5. Restart Pods

```bash
# ConfigMaps aren't hot-reloaded by default
AGENT_NAME=deployment-release kubectl rollout restart deployment/<name> -n <namespace>
```

#### 6. Verify Rollout

```bash
AGENT_NAME=deployment-release kubectl rollout status deployment/<name> -n <namespace>
```

### Secret Rotation

**Regenerate secrets**:
```bash
AGENT_NAME=deployment-release bash scripts/deployment/setup-k8s-secrets.sh --rotate-db-password
```

**Update manifest** to reference new secret version

**Validate change**:
```bash
AGENT_NAME=deployment-release bash scripts/deployment/validate-k8s-manifests.sh \
  --mode=standard gauntlet-agents k8s/local
```

**Apply with script**:
```bash
AGENT_NAME=deployment-release bash scripts/deployment/deploy-local-k8s.sh
```

**Cleanup old secrets**:
```bash
AGENT_NAME=deployment-release kubectl delete secret <old-secret-name> -n <namespace>
```

---

## Deployment Failure Recovery

### Rollback Process

#### 1. Check Rollout History

```bash
AGENT_NAME=deployment-release kubectl rollout history deployment/<name> -n <namespace>
```

#### 2. Identify Target Revision

```bash
AGENT_NAME=deployment-release kubectl rollout history deployment/<name> \
  --revision=<N> -n <namespace>
```

#### 3. Execute Rollback

```bash
# Rollback to previous revision
AGENT_NAME=deployment-release kubectl rollout undo deployment/<name> -n <namespace>

# Rollback to specific revision
AGENT_NAME=deployment-release kubectl rollout undo deployment/<name> \
  --to-revision=<N> -n <namespace>
```

#### 4. Monitor Rollback

```bash
AGENT_NAME=deployment-release kubectl rollout status deployment/<name> -n <namespace>
```

#### 5. Verify Health

```bash
AGENT_NAME=deployment-release kubectl get pods -n <namespace>
AGENT_NAME=deployment-release kubectl describe deployment/<name> -n <namespace>
```

### Fix-Forward Strategy

**Preferred over rollback** (Git-tracked changes):

1. Identify root cause
2. Fix manifest
3. Validate change
4. Apply corrected manifest
5. Git commit with fix

**Why fix-forward**:
- Maintains Git history
- Ensures manifest source of truth
- Prevents configuration drift

---

**See Also**:
- `failure-patterns.md` - Common K8s failure patterns
- `kubectl-operations.md` - kubectl command reference
- `kustomize-integration.md` - Kustomize workflow details
- `.claude/docs/guides/error-classification-framework.md` - Complete error taxonomy
- `.claude/docs/guides/circuit-breaker-pattern.md` - 3-state circuit breaker pattern
- `.claude/docs/guides/retry-strategies.md` - Retry implementation patterns
