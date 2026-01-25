# K8s Deployment Frameworks

**Purpose**: Methodologies and reasoning frameworks applied by k8s-deployment agent

---

## OODA Loop K8s Adaptations

### OBSERVE Phase (K8s Operations)

- Parse deployment request → Extract operation type (deploy/troubleshoot/validate/rollback)
- Check cluster connectivity: `kubectl config current-context`
- Review manifest validity: `bash scripts/deployment/validate-k8s-manifests.sh --mode=quick`
- Identify constraints (namespace, environment, validation requirements)

### ORIENT Phase (K8s Context Scoring)

**Context_Quality Formula**: (Domain × 0.4) + (Pattern × 0.3) + (Dependency × 0.2) + (Risk × 0.1)

**Dimension Scoring Examples** (0.0-1.0):
- **Domain**: 0.8-1.0 = k8s/** files, 0.3-0.5 = new resource types
- **Pattern**: 1.0 = CrashLoopBackOff, 0.4 = novel failure
- **Dependency**: 1.0 = all secrets/ConfigMaps present, 0.0 = missing critical
- **Risk**: 0.9 = dry-run validated, 0.3 = untested manifest

**CRITICAL GATE**: IF Context_Quality < 0.85 → RESEARCH FIRST → RETRY ORIENT (max 3)

### Automatic Research Triggers

Execute BEFORE attempting fixes:
1. **Context_Quality < 0.85** → Research via local guides OR Context7/Perplexity
2. **Tool call count >= 10** → STOP, research alternative approach
3. **Same error 3+ times** → Research error pattern (don't retry blindly)
4. **Unknown failure pattern** → Research immediately


### Research Priority

1. **Local guides first**: failure-patterns.md, kubectl-operations.md
2. **Context7** (free, authoritative K8s docs)
3. **Perplexity** (paid, community knowledge) - use sparingly
4. **Escalate** if still BLOCKED after 3 research iterations

### DECIDE Phase

**Operation Path Selection**:
| Path | Workflow | Confidence Threshold |
|------|----------|---------------------|
| Deploy | 7-phase pipeline | 0.8-1.0 execute now |
| Troubleshoot | Event-driven diagnosis | 0.5-0.79 monitor |
| Validate | Mode selection | <0.5 escalate |
| Update | Edit→dry-run→apply | |
| Rollback | History review | |

**Trade-offs**: Scripts > manual kubectl | Fix-forward > rollback | Restart > recreate

### ACT Phase

- Track with TodoWrite (pipeline phases)
- Track tool call count (stop at 10)
- Execute with AGENT_NAME prefix
- Monitor with kubectl (status, events, logs)
- Validate with scripts
- Iterate if confidence <0.85 → return to ORIENT

---

## Navigation Rules

### Information Hierarchy

**1. Essential** (always load):
- K8s manifests, deployment scripts, cluster state
- Location: `k8s/**`, `scripts/deployment/**`, kubectl output

**2. Progressive** (load on-demand):
- K8s failure patterns, kubectl reference, troubleshooting workflows
- Location: `docs/failure-patterns.md`, `docs/kubectl-operations.md`



**3. External** (research when unclear):
- Kubernetes documentation, kubectl best practices
- Location: WebFetch to kubernetes.io, kustomize.io

**4. Escalation** (user decision required):
- User approval, production deployment requests

### Decision Protocol

**Main Path** (standard deployment):
1. Parse request → Identify operation type
2. Assess cluster state → Check prerequisites
3. Execute script workflow → Monitor progress
4. Validate success → Report results

**Follow-up Path** (troubleshooting):
1. Identify failure pattern
2. Gather evidence (events → logs → describe)
3. Classify error (PERMANENT/TRANSIENT/AMBIGUOUS)
4. Apply remediation → Verify fix

---

## Escalation Protocol

**Attempt Definition**: One attempt = kubectl operation + evidence gathering + analysis (1-2 min)

**3-Step Escalation**:

1. **First attempt**: Execute deployment script, gather kubectl output
   - Success: Deployment succeeded OR clear error pattern identified

2. **Second attempt**: Apply systematic troubleshooting (consult failure-patterns.md)
   - Success: Root cause identified OR classified as application issue

3. **Final escalation**: Report to orchestrator with diagnostic findings
   - Required: Failure details, root cause (if known), recommended agent
   - Delegate: App issues → debugger | Dashboard → grafana-dashboard-builder

**Escalation Triggers**:
- Deployment failure after 2 attempts → Escalate with diagnostics
- Application code error (exit 1 with traceback) → Recommend debugger
- Production deployment request → REQUIRE explicit user approval
