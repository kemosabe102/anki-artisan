# k8s-deployment Examples

**Purpose**: Concrete usage patterns showing how this agent is called and what it produces

---

## Contents

| File | Purpose | Audience |
|------|---------|----------|
| `delegation-examples.md` | How orchestrator delegates to this agent | Orchestrator, other agents |

---

## Quick Examples

### Deploy Local Stack
```
Task(k8s-deployment, "Deploy the observability stack to local k8s cluster")
```

### Troubleshoot Failing Pod
```
Task(k8s-deployment, "Pod jaeger-0 is in CrashLoopBackOff. Diagnose and fix.")
```

### Validate Before Deploy
```
Task(k8s-deployment, "Validate k8s/local manifests before deployment")
```

### Update ConfigMap
```
Task(k8s-deployment, "Update LOG_LEVEL to DEBUG in the api-config ConfigMap")
```

### Rollback Deployment
```
Task(k8s-deployment, "Rollback otel-collector deployment to previous version")
```

---

## See Also

- **Main agent**: `../k8s-deployment.md`
- **Docs**: `../docs/`
- **Schema**: `../schemas/k8s-deployment.schema.json`
