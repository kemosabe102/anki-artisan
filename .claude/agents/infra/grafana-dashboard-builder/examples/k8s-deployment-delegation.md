# k8s-deployment Agent Delegation Example

**Purpose**: Template for delegating dashboard deployment to k8s-deployment agent

## Delegation Pattern

```python
Task(agent="k8s-deployment", prompt="""
DEPLOY Grafana dashboard ConfigMap to Kubernetes.

**Objective**: Apply ConfigMap to observability namespace for Grafana sidecar provisioning

**ConfigMap Path**: k8s/provisioning/dashboards/<name>-configmap.yaml

**Deployment Instructions**:
1. Validate ConfigMap has label 'grafana_dashboard: "1"'
2. Apply to namespace 'observability': kubectl apply -f <path> -n observability
3. Verify Grafana sidecar detects dashboard (check sidecar logs)
4. Confirm dashboard appears in Grafana UI (folder: 'Provisioned Dashboards')

**Validation Criteria**:
- ConfigMap created in observability namespace
- Grafana sidecar logs show dashboard import
- Dashboard accessible via Grafana UI

**Rollback Plan**: kubectl delete configmap <name> -n observability if deployment fails
""")
```

## Quick Deploy Script

**Note**: The grafana-dashboard-builder agent creates dashboards and ConfigMaps, but does NOT deploy them directly.

For manual deployment verification, use:

```bash
AGENT_NAME=grafana-dashboard-builder bash scripts/deployment/deploy-local-k8s.sh --refresh
```

**Flags**:
- `--refresh`: Update configs and restart pods (recommended for dashboard changes)
- No flag: Full deployment (first-time setup)
- `--teardown`: Remove deployment (preserves data)
- `--teardown-all`: Full teardown (WARNING: deletes data)

**Verification**: Dashboard appears at http://localhost:30030 after 30-60s
