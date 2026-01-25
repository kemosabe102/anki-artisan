# Delegation Examples

Templates for delegating to other agents during dashboard creation workflow.

---

## k8s-deployment Agent Delegation

**When to Use**: After dashboard JSON and ConfigMap are generated, delegate deployment.

### Delegation Template

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

### Quick Deploy Script (Manual Verification)

```bash
AGENT_NAME=grafana-dashboard-builder bash scripts/deployment/deploy-local-k8s.sh --refresh
```

**Flags**:
- `--refresh`: Update configs and restart pods (recommended for dashboard changes)
- No flag: Full deployment (first-time setup)
- `--teardown`: Remove deployment (preserves data)
- `--teardown-all`: Full teardown (WARNING: deletes data)

**Verification**: Dashboard appears at http://localhost:30030 after 30-60s

---

## researcher-external Agent Delegation

**When to Use**: For unfamiliar monitoring domains requiring SRE best practice research.

### Delegation Template

```python
Task(agent="researcher-external", prompt="""
RESEARCH SRE monitoring best practices for <domain>.

**Objective**: Find recommended metrics, PromQL patterns, and visualization guidance

**Sources**: Google SRE Book, Prometheus Best Practices, Grafana community dashboards

**Output Format**:
- Recommended metrics (list with descriptions)
- PromQL query examples (with rate intervals and aggregations)
- Panel type recommendations (time series, gauge, stat)
- Threshold guidance (SLO-based, capacity-based)

**Scope**: Focus on production-ready patterns, avoid experimental/deprecated approaches
""")
```

### Common Research Domains

| Domain | Key Metrics to Research |
|--------|------------------------|
| **Redis** | Memory usage, eviction rate, hit ratio, connection pool |
| **Kafka** | Consumer lag, partition replication, broker throughput |
| **API Services** | Latency percentiles, error rates, request throughput |
| **Databases** | Connection pool, query latency, transaction rate |
| **Kubernetes** | Pod restarts, resource limits, node capacity |

### Example: Redis Research Delegation

```python
Task(agent="researcher-external", prompt="""
RESEARCH SRE monitoring best practices for Redis caching layer.

**Objective**: Find recommended metrics for Redis monitoring dashboard

**Focus Areas**:
1. Memory metrics (used_memory, evicted_keys, fragmentation_ratio)
2. Connection metrics (connected_clients, blocked_clients)
3. Performance metrics (instantaneous_ops_per_sec, hit_rate)
4. Persistence metrics (rdb_last_save_time, aof_rewrite_in_progress)

**Sources**: Redis official docs, Prometheus redis_exporter, Grafana Redis dashboards

**Output Format**:
- Metric name + description + PromQL example
- Recommended thresholds for alerting
- Panel type recommendation (gauge for %, timeseries for rates)
""")
```

---

## promql-query-builder Agent Delegation

**When to Use**: For complex PromQL query construction and validation.

### Delegation Template

```python
Task(agent="promql-query-builder", prompt="""
BUILD validated PromQL queries for <monitoring_intent>.

**Metrics Available**: <list from Prometheus API discovery>

**Required Queries**:
1. Request rate: sum(rate(...)) by (service)
2. Error percentage: (errors / total) * 100
3. Latency percentiles: histogram_quantile(0.95, ...)

**Validation Requirements**:
- Syntax validation via Prometheus API
- Metric existence confirmation
- Cardinality check (<100 series per query)

**Output Format**: JSON with query, legend_format, and validation_status
""")
```

---

## Integration Flow Example

### Complete Dashboard Creation with Delegations

```
User Request: "Create monitoring dashboard for our payment API"

Step 1: Intent Analysis
  - Keywords: "payment", "API"
  - Framework: RED (service-centric)
  - Domain: API services

Step 2: Research Delegation (if needed)
  Task(researcher-external, "RESEARCH payment API monitoring best practices...")
  Output: Recommended metrics (latency, error rate, transaction rate)

Step 3: Query Building Delegation
  Task(promql-query-builder, "BUILD PromQL queries for payment API metrics...")
  Output: Validated queries with legend formats

Step 4: Dashboard Generation
  - Generate dashboard JSON with panels
  - Create ConfigMap YAML

Step 5: Deployment Delegation
  Task(k8s-deployment, "DEPLOY ConfigMap k8s/provisioning/dashboards/payment-api-configmap.yaml...")
  Output: Dashboard deployed to Grafana

Step 6: Return to Orchestrator
  SUCCESS: {
    dashboard_json_path: "k8s/provisioning/dashboards/payment-api.json",
    configmap_yaml_path: "k8s/provisioning/dashboards/payment-api-configmap.yaml",
    deployment_instructions: {...}
  }
```
