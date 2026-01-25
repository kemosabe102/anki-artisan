# Kubectl Operations Reference

**Purpose**: Comprehensive guide to approved kubectl commands, script-based operations, and command restrictions.

**When to Use**: Before executing any kubectl operation to ensure compliance with security policies.

---

## ⚠️ CRITICAL: Blocked Commands in Settings

The following kubectl commands are **BLOCKED** by `.claude/settings.json` security policy:

- `kubectl apply` - BLOCKED (use scripts instead)
- `kubectl delete` - BLOCKED (use scripts instead)

---

## ✅ Workaround: Script-Based Deployment

Use `bash scripts/deployment/*.sh` which is **allowed** via `Bash(bash:*)` permission.
These scripts internally use blocked commands safely within controlled workflows.

---

## Read-Only Commands (Always Allowed)

**Usage Frequency Indicators**: 🔥 Daily | ⚡ Weekly | 📅 Monthly/Rare

### Resource Inspection

```bash
# List resources
AGENT_NAME=deployment-release kubectl get pods -n <namespace>  # 🔥 Daily - Every deployment/troubleshooting
AGENT_NAME=deployment-release kubectl get deployments -n <namespace>  # 🔥 Daily - Every deployment check
AGENT_NAME=deployment-release kubectl get services -n <namespace>  # 🔥 Daily - Every deployment verification
AGENT_NAME=deployment-release kubectl get configmaps -n <namespace>  # ⚡ Weekly - Occasional config checks
AGENT_NAME=deployment-release kubectl get secrets -n <namespace>  # ⚡ Weekly - Occasional secret checks

# Detailed resource inspection
AGENT_NAME=deployment-release kubectl describe pod <pod-name> -n <namespace>  # 🔥 Daily - Every troubleshooting session
AGENT_NAME=deployment-release kubectl describe deployment <deployment-name> -n <namespace>  # ⚡ Weekly - Deep dive investigations

# Container logs
AGENT_NAME=deployment-release kubectl logs <pod-name> -n <namespace>  # 🔥 Daily - Every troubleshooting session
AGENT_NAME=deployment-release kubectl logs <pod-name> --previous -n <namespace>  # 🔥 Daily - CrashLoopBackOff diagnosis
AGENT_NAME=deployment-release kubectl logs <pod-name> -c <container-name> -n <namespace>  # ⚡ Weekly - Multi-container troubleshooting

# Event stream
AGENT_NAME=deployment-release kubectl get events --sort-by=.lastTimestamp -n <namespace>  # 🔥 Daily - Every troubleshooting session
AGENT_NAME=deployment-release kubectl get events --field-selector involvedObject.name=<pod-name> -n <namespace>  # 🔥 Daily - Pod-specific diagnosis

# API schema documentation
AGENT_NAME=deployment-release kubectl explain pod.spec.containers  # 📅 Monthly - Documentation lookup
AGENT_NAME=deployment-release kubectl explain deployment.spec.strategy  # 📅 Monthly - Documentation lookup

# Context management (read-only)
AGENT_NAME=deployment-release kubectl config current-context  # ⚡ Weekly - Context verification
AGENT_NAME=deployment-release kubectl config view  # 📅 Monthly - Configuration review
```

---

## Lifecycle Commands (Allowed via kubectl)

### Rollout Management

```bash
# Monitor deployment progress
AGENT_NAME=deployment-release kubectl rollout status deployment/<name> -n <namespace>  # 🔥 Daily - After every deployment

# Trigger pod restarts (for ConfigMap/Secret updates)
AGENT_NAME=deployment-release kubectl rollout restart deployment/<name> -n <namespace>  # ⚡ Weekly - ConfigMap/Secret updates

# Rollback to previous revision
AGENT_NAME=deployment-release kubectl rollout undo deployment/<name> -n <namespace>  # 📅 Monthly - Emergency rollbacks
AGENT_NAME=deployment-release kubectl rollout undo deployment/<name> --to-revision=<N> -n <namespace>  # 📅 Monthly - Specific revision rollback

# View rollout history
AGENT_NAME=deployment-release kubectl rollout history deployment/<name> -n <namespace>  # ⚡ Weekly - Deployment audits
```

---

## Script-Based Operations (REQUIRED for Blocked Commands)

### Deployment Scripts

**Location**: `scripts/deployment/*.sh`

**Note**: Scripts support multiple flags. Use `--help` for complete options.

#### Full Deployment Pipeline (🔥 Daily)

```bash
AGENT_NAME=deployment-release bash scripts/deployment/deploy-local-k8s.sh
```

**What it does**:
- Uses `kubectl apply -k` internally (safe within script)
- Includes validation, rollout monitoring, health checks
- Runs `verify_observability.py` and `validate_deployment.py`
- Returns exit code 0 (success) or non-zero (failure)

#### Cleanup Deployment (📅 Monthly)

```bash
AGENT_NAME=deployment-release bash scripts/deployment/deploy-local-k8s.sh --cleanup
```

**What it does**:
- Uses `kubectl delete -k` and `kubectl delete namespace` internally
- Removes all resources in namespace
- Preserves cluster state (no cluster-level resource deletion)

#### Validation Only (⚡ Weekly)

```bash
AGENT_NAME=deployment-release bash scripts/deployment/deploy-local-k8s.sh --validate-only
```

**What it does**:
- Runs validation tests without deploying
- Executes `validate_deployment.py` and `verify_observability.py`
- Returns exit code based on validation results

#### View Deployment Logs (📅 Monthly)

```bash
AGENT_NAME=deployment-release bash scripts/deployment/deploy-local-k8s.sh --logs
```

**Note**: The deploy script may have additional flags (use `--help`), but **NEVER use `--port-forward`**. Always configure services with `type: NodePort` instead.

---

### Secret Management Scripts

#### Generate Secrets from .env (⚡ Weekly - Initial setup or regeneration)

```bash
AGENT_NAME=deployment-release bash scripts/deployment/setup-k8s-secrets.sh
```

**What it does**:
- Creates `k8s/local/secrets.yaml` from template
- Base64 encodes all secret values from `.env`
- Returns exit code 0 (success) or non-zero (failure)

#### Dry-Run Validation (📅 Monthly - Pre-deployment checks)

```bash
AGENT_NAME=deployment-release bash scripts/deployment/setup-k8s-secrets.sh --dry-run
```

**What it does**:
- Validates `.env` file without generating secrets
- Checks for required variables

#### Rotate Database Password (⚡ Weekly - Security rotation schedule)

```bash
AGENT_NAME=deployment-release bash scripts/deployment/setup-k8s-secrets.sh --rotate-db-password
```

**What it does**:
- Forces new database password generation
- Updates secret manifest with new value

---

## Forbidden Commands

**BLOCKED by security policy**:
- `kubectl apply` - Use deployment scripts instead
- `kubectl delete` - Use cleanup scripts instead
- `kubectl edit` - Prefer manifest updates + scripts (Git-tracked changes)
- `kubectl exec` - Security risk, use logs for debugging
- `kubectl create` - Use manifests + scripts (declarative approach)

**FORBIDDEN by design philosophy** (not blocked, but NEVER use):
- `kubectl port-forward` - **ALWAYS use NodePort instead**
  - **Why forbidden**: Ephemeral, requires manual intervention, no audit trail
  - **Proper approach**: Configure services with `type: NodePort` in manifests
  - **Access pattern**: Use `http://localhost:30XXX` URLs (persistent, no manual commands)
  - **Example**: Observability stack uses NodePort 30090-30889 (see agent definition lines 46-67)

**Why forbidden**:
- GitOps compliance (all changes must be manifest-based and tracked)
- Prevents accidental production changes
- Enforces validation workflow (dry-run before apply)
- Audit trail via scripts
- NodePort provides persistent, configuration-managed access (no manual port-forward overhead)

---

## Script Orchestration Order

**Standard deployment flow**:

1. **Setup secrets** (if missing):
   ```bash
   AGENT_NAME=deployment-release bash scripts/deployment/setup-k8s-secrets.sh
   ```

2. **Deploy with validation**:
   ```bash
   AGENT_NAME=deployment-release bash scripts/deployment/deploy-local-k8s.sh
   ```
   - Script internally handles phases 3-7 of deployment pipeline:
     * Manifest Application (kubectl apply -k)
     * Rollout Monitoring (kubectl rollout status)
     * Health Checks (pod readiness, liveness probes)
     * Observability Verification (verify_observability.py)
     * Validation Testing (validate_deployment.py)

3. **Verify deployment** (if needed):
   ```bash
   AGENT_NAME=deployment-release kubectl get pods -n <namespace>
   AGENT_NAME=deployment-release kubectl rollout status deployment/<name> -n <namespace>
   ```

**Configuration update flow**:

1. **Edit manifest** (using Desktop Commander: `mcp__desktop-commander__edit_block`)

2. **Validate change**:
   ```bash
   AGENT_NAME=deployment-release bash scripts/deployment/validate-k8s-manifests.sh --mode=standard
   ```

3. **Apply change**:
   ```bash
   AGENT_NAME=deployment-release bash scripts/deployment/deploy-local-k8s.sh
   ```

4. **Restart pods** (if ConfigMap/Secret changed):
   ```bash
   AGENT_NAME=deployment-release kubectl rollout restart deployment/<name> -n <namespace>
   ```

---

## Exit Code Handling

**Scripts return**:
- `0` = Success (proceed to next phase)
- Non-zero = Failure (capture stdout/stderr for diagnostics)

**Standard error handling**:
```bash
if AGENT_NAME=deployment-release bash scripts/deployment/deploy-local-k8s.sh; then
    echo "Deployment succeeded"
else
    echo "Deployment failed - check logs"
    AGENT_NAME=deployment-release kubectl get events --sort-by=.lastTimestamp
fi
```

---

**See Also**:
- `failure-patterns.md` - Troubleshooting common K8s failures
- `troubleshooting-workflows.md` - Error handling and retry strategies
- `kustomize-integration.md` - Kustomize workflow details
