# Delegation Examples for k8s-deployment

**Purpose**: Show orchestrator and other agents how to delegate tasks to this agent

---

## When to Delegate to This Agent

### Trigger Conditions

Delegate to `k8s-deployment` when:
- Deploying to local Kubernetes cluster
- Troubleshooting K8s pod failures (CrashLoopBackOff, ImagePullBackOff, Pending)
- Validating Kubernetes manifests
- Updating ConfigMaps or Secrets
- Rolling back deployments
- Managing Kustomize overlays

### NOT This Agent

Do NOT delegate when:
- Application code issues (exit 1 with traceback) → Use `debugger` or `python-code-implementer`
- Grafana dashboard creation → Use `grafana-dashboard-builder`
- Database operations → Use `postgres-timescale-specialist`
- Production deployments → Require explicit user approval first

---

## Basic Delegation Pattern

### Deploy Operation

**Orchestrator says**:
```
Task(k8s-deployment, "Deploy the full observability stack to local k8s cluster")
```

**Agent returns**:
```json
{
  "status": "SUCCESS",
  "agent": "k8s-deployment",
  "confidence": 0.95,

  "agent_specific_output": {
    "operation": "deploy",
    "deployments_updated": ["prometheus", "grafana", "jaeger", "otel-collector", "loki"],
    "rollout_status": "all deployments ready",
    "service_endpoints": {
      "prometheus": "http://localhost:30090",
      "grafana": "http://localhost:30030",
      "jaeger": "http://localhost:31686"
    },
    "validation_passed": true
  }
}
```

---

## Troubleshoot Operation

**Orchestrator says**:
```
Task(k8s-deployment, "Pod jaeger-0 is in CrashLoopBackOff. Diagnose root cause and provide remediation.")
```

**Agent returns** (success):
```json
{
  "status": "SUCCESS",
  "agent": "k8s-deployment",
  "confidence": 0.88,
  "agent_specific_output": {
    "operation": "troubleshoot",
    "failure_pattern": "CrashLoopBackOff",
    "root_cause": "OOMKilled - container exceeded 512Mi memory limit",
    "evidence": {
      "exit_code": 137,
      "events": "Back-off restarting failed container",
      "logs": "memory allocation failed"
    },
    "remediation": [
      "Increase memory limit to 1Gi in k8s/local/jaeger.yaml",
      "Run: kubectl rollout restart statefulset/jaeger"
    ]
  }
}
```



**Agent returns** (failure - application issue):
```json
{
  "status": "FAILURE",
  "agent": "k8s-deployment",
  "confidence": 0.75,
  "failure_details": {
    "failure_type": "application_code_error",
    "reasons": ["Python traceback in logs indicates application bug"],
    "recovery_suggestions": [
      "Delegate to debugger for application code investigation",
      "Check application logs for full traceback"
    ],
    "partial_results": {
      "events_gathered": true,
      "logs_retrieved": true,
      "infrastructure_healthy": true
    }
  }
}
```

---

## Validate Operation

**Orchestrator says**:
```
Task(k8s-deployment, "Validate k8s/local manifests with full mode before CI deployment")
```

**Agent returns**:
```json
{
  "status": "SUCCESS",
  "agent": "k8s-deployment",
  "confidence": 0.92,
  "agent_specific_output": {
    "operation": "validate",
    "mode": "full",
    "validation_passed": true,
    "checks": {
      "client_side": "passed",
      "server_side": "passed",
      "kustomize_build": "passed"
    }
  }
}
```



---

## Multi-Agent Coordination

### Upstream Agents (provide input to this agent)

| Agent | Provides | Example |
|-------|----------|---------|
| `python-code-implementer` | Docker image, updated image version | After code changes, updates `image-versions.yaml` |
| `test-executor` | Pre-deployment test results | Confirms tests pass before deploy |

### Downstream Agents (consume this agent's output)

| Agent | Uses | For |
|-------|------|-----|
| `debugger` | Failure diagnostics | Application-level issue investigation |
| `grafana-dashboard-builder` | Service endpoints | Dashboard data source configuration |

### Parallel Execution Pattern

```
Launch in parallel (after deploy success):
- Task(grafana-dashboard-builder, "Create dashboard for new service")
- Task(test-executor, "Run integration tests against deployed stack")
```

---

## Error Handling

### Retry Conditions

Retry delegation when:
- `confidence < 0.5` with refined context
- `failure_type: "transient_network_error"`

### Escalation Conditions

Escalate to user when:
- 2+ retries failed
- `failure_type: "production_deployment_requested"`
- Agent explicitly requests approval
