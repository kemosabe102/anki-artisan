# PromQL Query Builder - Delegation Examples

How the orchestrator invokes promql-query-builder for different scenarios.

---

## Example 1: Query Construction

**User Request**: "I need a query to show API latency by service"

**Orchestrator Delegation**:
```markdown
Task(promql-query-builder, "Build a PromQL query to show p95 API latency grouped by service name")
```

**Expected Output**:
```json
{
  "status": "SUCCESS",
  "agent_specific_output": {
    "constructed_query": "histogram_quantile(0.95, sum by(service) (rate(http_request_duration_seconds_bucket[$__rate_interval])))",
    "query_metadata": {
      "grouping_labels": ["service"],
      "rate_interval": "$__rate_interval",
      "estimated_cardinality": "low",
      "panel_type_recommendation": "timeseries",
      "aggregation_function": "histogram_quantile",
      "query_type": "histogram_quantile"
    },
    "query_explanation": "Calculates 95th percentile latency using histogram buckets, grouped by service for Grafana legend display"
  }
}
```

---

## Example 2: Query Validation

**User Request**: "Check if this query is correct: `rate(http_requests_total[5m])`"

**Orchestrator Delegation**:
```markdown
Task(promql-query-builder, "Validate this PromQL query: rate(http_requests_total[5m])")
```

**Expected Output**:
```json
{
  "status": "SUCCESS",
  "agent_specific_output": {
    "validation_report": {
      "syntax_valid": true,
      "metrics_exist": true,
      "performance_estimate": "fast",
      "warnings": [
        {
          "type": "missing_labels",
          "message": "Query returns all label combinations without aggregation",
          "recommendation": "Add 'sum by(label)' to control cardinality"
        }
      ]
    }
  }
}
```

---

## Example 3: Recording Rule Generation

**User Request**: "Should I create a recording rule for this dashboard query?"

**Orchestrator Delegation**:
```markdown
Task(promql-query-builder, "Evaluate if this query needs a recording rule: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le))")
```

**Expected Output**:
```json
{
  "status": "SUCCESS",
  "agent_specific_output": {
    "recording_rules_config": {
      "should_create_recording_rule": true,
      "criteria_met": [
        "Complex histogram aggregation (>3 operators)",
        "Used in 5+ dashboard panels"
      ],
      "rule_name": "job:http_request_duration_seconds:p95",
      "recording_rule_yaml": "groups:\n  - name: api_latency\n    interval: 60s\n    rules:\n      - record: job:http_request_duration_seconds:p95\n        expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le))",
      "evaluation_interval": "60s",
      "estimated_savings": {
        "query_time_reduction": "80% faster",
        "cardinality_reduction": "Pre-aggregated from 5000 to 50 series"
      }
    }
  }
}
```

---

## Example 4: Time-Period Comparison

**User Request**: "Show me traffic compared to last week"

**Orchestrator Delegation**:
```markdown
Task(promql-query-builder, "Build a week-over-week comparison query for HTTP request rate")
```

**Expected Output**:
```json
{
  "status": "SUCCESS",
  "agent_specific_output": {
    "constructed_query": "((rate(http_requests_total[5m]) - rate(http_requests_total[5m] offset 7d)) / rate(http_requests_total[5m] offset 7d)) * 100",
    "query_metadata": {
      "offset_duration": "7d",
      "query_type": "time_comparison"
    },
    "query_explanation": "Calculates percentage change vs same time last week. Positive = traffic increase, negative = decrease."
  }
}
```

---

## Example 5: Metric Discovery

**User Request**: "What metrics are available for container memory?"

**Orchestrator Delegation**:
```markdown
Task(promql-query-builder, "Discover available metrics matching pattern 'container_memory*'")
```

**Expected Output**:
```json
{
  "status": "SUCCESS",
  "agent_specific_output": {
    "discovered_metrics": [
      {
        "metric_name": "container_memory_usage_bytes",
        "metric_type": "gauge",
        "labels": ["namespace", "pod", "container"],
        "relevance_score": 0.95
      },
      {
        "metric_name": "container_memory_working_set_bytes",
        "metric_type": "gauge",
        "labels": ["namespace", "pod", "container"],
        "relevance_score": 0.90
      }
    ]
  }
}
```

---

## Example 6: Failure Case - Ambiguous Intent

**User Request**: "Show me latency"

**Orchestrator Delegation**:
```markdown
Task(promql-query-builder, "Build a query to show latency")
```

**Expected Output**:
```json
{
  "status": "FAILURE",
  "failure_details": {
    "failure_type": "ambiguous_intent",
    "reasons": ["Intent too vague - missing service, time range, and aggregation preferences"],
    "ambiguous_intent": {
      "clarifying_questions": [
        "What signal are you detecting? (alert threshold, trend, comparison)",
        "What time period? (real-time 5m, historical 1h, week-over-week)",
        "What labels matter? (namespace, service, endpoint, pod)",
        "What aggregation? (p50, p95, p99, average)"
      ]
    },
    "recovery_suggestions": [
      "Specify which service or endpoint",
      "Indicate percentile (p95, p99) or average",
      "Provide time range context"
    ]
  }
}
```

---

## Chaining with grafana-dashboard-builder

After promql-query-builder returns a validated query, orchestrator can chain to dashboard creation:

```markdown
# Step 1: Build query
result = Task(promql-query-builder, "Build p95 latency query by service")

# Step 2: Create dashboard panel (if query succeeds)
Task(grafana-dashboard-builder, f"Create timeseries panel using query: {result.query}")
```
