# researcher-external Delegation Example

**Purpose**: Template for delegating SRE best practices research to researcher-external agent

## Delegation Pattern

```python
Task(agent="researcher-external", prompt="""
RESEARCH SRE monitoring best practices for <domain> (e.g., Redis, Kafka, API services).

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

## Common Research Domains

- **Redis**: Memory usage, eviction rate, hit ratio, connection pool
- **Kafka**: Consumer lag, partition replication, broker throughput
- **API Services**: Latency percentiles, error rates, request throughput
- **Databases**: Connection pool, query latency, transaction rate
- **Kubernetes**: Pod restarts, resource limits, node capacity
