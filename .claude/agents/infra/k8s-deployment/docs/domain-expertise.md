# K8s Deployment Domain Expertise

**Purpose**: Core responsibilities, workflow operations, and integration points for k8s-deployment agent

---

## Primary Responsibilities

### Deployment Orchestration

**7-Phase Deployment Pipeline**:

1. **Pre-flight Validation** - Cluster connectivity, manifest syntax, secret existence
2. **Secret Setup** - Execute `bash scripts/deployment/setup-k8s-secrets.sh` if secrets missing
3. **Manifest Application** - `bash scripts/deployment/deploy-local-k8s.sh` (uses kubectl apply -k internally)
4. **Rollout Monitoring** - Track deployment/statefulset rollout status with timeout
5. **Health Checks** - Verify pod readiness, liveness probes, replica counts
6. **Observability Verification** - Run verify_observability.py for Grafana/Jaeger/Prometheus
7. **Validation Testing** - Execute validate_deployment.py for synthetic API tests

### Configuration Management

**ConfigMap Updates**:
1. Read current: `kubectl get configmap <name> -o yaml`
2. Edit manifest file in `k8s/local/configmap.yaml`
3. Validate: `bash scripts/deployment/validate-k8s-manifests.sh --mode=standard`
4. Apply: `bash scripts/deployment/deploy-local-k8s.sh`
5. Restart: `kubectl rollout restart deployment/<name>` (ConfigMaps aren't hot-reloaded)

**Secret Rotation** (Immutability Enforcement):
1. Regenerate: `bash scripts/deployment/setup-k8s-secrets.sh --rotate-db-password`
2. Update manifest to reference new secret version
3. Validate and apply
4. Cleanup old secrets


---

## Workflow Operations

### 1. Deploy Operation (`deploy`)

**Input**: Deployment target, manifest path (k8s/local/), namespace, validation flags

**Workflow**:
1. **Analysis**: Parse deployment request, validate cluster connectivity
2. **Research**: Check existing deployment state, review recent events
3. **Todo Creation**: Generate deployment checklist
4. **Implementation**: Execute scripts (setup-k8s-secrets.sh → deploy-local-k8s.sh)
5. **Validation**: Check rollout status, health checks, service endpoints
6. **Reflection**: Document deployment duration, success rate

**Output**: SUCCESS with deployment evidence OR FAILURE with recovery guidance

### 2. Troubleshoot Operation (`troubleshoot`)

**Input**: Troubleshooting context (pod name, failure mode, event timeframe)

**Workflow**:
1. **Analysis**: Identify failure pattern (CrashLoopBackOff/ImagePullBackOff/Pending)
2. **Research**: Retrieve events, logs, describe output
3. **Implementation**: Event correlation, log analysis, resource inspection
4. **Validation**: Verify diagnosis accuracy, test remediation in dry-run

**Output**: SUCCESS with troubleshooting findings OR FAILURE with partial diagnostics

### 3. Validate Operation (`validate`)

**Input**: Validation options (mode, verbose, show diff, namespace)

**Modes**:
| Mode | Duration | Use Case |
|------|----------|----------|
| `--mode=quick` | 2-3s | Quick syntax check |
| `--mode=standard` | 5-7s | Pre-deployment validation |
| `--mode=full` | 7-10s | CI/CD pipeline validation |



### 4. Update Manifest Operation (`update_manifest`)

**Input**: Configuration update (config type, config name, data)

**Workflow**:
1. Read manifest: `Read(k8s/local/<resource>.yaml)`
2. Edit manifest (Desktop Commander: `mcp__desktop-commander__edit_block`)
3. Validate: `bash scripts/deployment/validate-k8s-manifests.sh --mode=standard`
4. Apply: `bash scripts/deployment/deploy-local-k8s.sh`
5. Restart pods if ConfigMap: `kubectl rollout restart deployment/<name>`

### 5. Rollback Operation (`rollback`)

**Input**: Rollback target (deployment name, revision)

**Workflow**:
1. Check history: `kubectl rollout history deployment/<name>`
2. Execute rollback: `kubectl rollout undo deployment/<name> --to-revision=<N>`
3. Monitor rollout: `kubectl rollout status deployment/<name>`
4. Verify health

---

## Integration Points

### Orchestrator Coordination

**Delegation Pattern**: Orchestrator delegates for all K8s operations in local development

**Input Format**: Operation type, deployment target, context-specific parameters

**Failure Handling**: Returns recovery suggestions; orchestrator decides retry/rollback/escalate

### Multi-Agent Workflows

**Upstream Dependencies**:
- `python-code-implementer` - Generates Docker image, updates image version
- `test-executor` - Runs pre-deployment unit tests
- `debugger` - Investigates application-level issues

**Downstream Integration**:
- Deployment success → `validate_deployment.py` → orchestrator reports success
- Deployment failure → troubleshooting → `debugger` for app-level diagnosis
- Dashboard creation → delegate to `grafana-dashboard-builder`



---

## Pre-Flight Checklist

Before any deployment operation:

- [ ] Cluster connectivity: `kubectl config current-context`
- [ ] Manifest validity: kustomization.yaml and all resources exist
- [ ] Validation script exists and executable
- [ ] Required secrets exist (Grafana, PostgreSQL, Redis if applicable)
- [ ] Resource quotas sufficient in namespace
- [ ] Container images pullable
- [ ] Script permissions correct

---

## Validation Checklist

After any operation:

- [ ] Operations within k8s/** and scripts/deployment/** boundaries only
- [ ] Deployment scripts used for ALL kubectl apply/delete operations
- [ ] kubectl commands restricted to approved operations
- [ ] NO direct `kubectl apply` or `kubectl delete`
- [ ] NO `kubectl port-forward` (use NodePort)
- [ ] Manifest edits followed protocol (read → edit → dry-run → deploy)
- [ ] ALL Bash commands used AGENT_NAME prefix
- [ ] Service endpoints documented with NodePort URLs
- [ ] No secrets leaked in outputs

---

## Context7 MCP Integration

**When to Use Context7**:
- Validating Kubernetes manifest schemas
- Researching kubectl command reference
- Version-specific K8s API documentation

**Usage Pattern**:
```markdown
# 1. Resolve Kubernetes API documentation
library_info = resolve_library_id("Kubernetes")

# 2. Get API reference for resource type
docs = get_library_docs(library_info["library_id"], topic="StatefulSet API spec", tokens=5000)

# 3. Validate manifest against official schema
```

**Integration with ORIENT Phase**:
1. Identify knowledge gap
2. Try Context7 first (free, authoritative)
3. Fallback to Perplexity if insufficient
4. Update Context_Quality, proceed to DECIDE if >=0.85
